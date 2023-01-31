import uuid
from typing import Dict, List, Tuple

import numpy as np
from ortools.linear_solver import pywraplp

from managers.displayManager.displayObject import DisplayBlock, DisplayConnection


class Cartographer:
    """
    This object will create an optimiser for the displaying of blocks
    """
    scriptsByLevel: Dict[int, List[str]] = dict()
    numLevels: int = None
    numSpacesByLevel: Dict[int, int] = dict()
    scriptCoordinates: List[Tuple[int, int]] = list()

    def autosetBlockAndConnections(
            self, blocksDict: Dict[str, DisplayBlock], connectionsDict: Dict[str, DisplayConnection]
    ) -> None:
        # self.getLevels(blocksDict)
        # self.getScriptCoordinates()
        # self.getConnectionDistances(connectionDict)
        self.runOptimisation(blocksDict, connectionsDict)

    def getLevels(self, scriptsDict: Dict[str, DisplayBlock]) -> Dict[int, List[str]]:
        scriptPathLocLengths = {
            scriptID: len(script.mnemeSelf.pathLocation.split('\\'))
            for scriptID, script in scriptsDict.items()
        }

        minLevel, maxLevel = min(scriptPathLocLengths.values()), max(scriptPathLocLengths.values())
        for scriptID, scriptLevel in scriptPathLocLengths.items():
            self.scriptsByLevel.setdefault(scriptLevel - minLevel, list()).append(scriptID)

        return self.scriptsByLevel

    def getScriptCoordinates(self):
        """
        1. For N levels, divide screen vertically to N+1 sections
        2. For M scripts per level, divide screen horizontally to M+1 sections

        Then each script is given a coordinate for its centre
        :return:
        """
        self.numLevels = len(self.scriptsByLevel)
        self.numSpacesByLevel = {level: len(scriptsOnLevel) for level, scriptsOnLevel in self.scriptsByLevel.items()}
        self.scriptCoordinates = [(level, space) for level, numSpaces in self.numSpacesByLevel.items()
                                  for space in range(numSpaces)]

    def getConnectionDistances(self, connectionDict: Dict[str, DisplayConnection]):
        for connectionID, connection in connectionDict.items():
            sourceBlock, targetBlock = connection.sourceBlock, connection.targetBlock
            sourceLevel, targetLevel = sourceBlock.level, sourceBlock.level

        pass

    def runOptimisation(self, scriptsDict: Dict[str, DisplayBlock], connectionsDict: Dict[str, DisplayConnection]):
        """
        This problem is to minimise the distances of the connections that exist and secondarily files of the same folder
        are closer to each other.
        Distances are measured using taxi cab metric, so d((X1, Y1), (X2, Y2)) = abs(X1 - X2) + abs(Y1 - Y2).

        For each script, we know which level it belongs to and how many spaces are there in each level. We associate
        to the script a number in range(number of spaces in level).
        :return:
        """
        solver = pywraplp.Solver.CreateSolver('SCIP')

        levelCoordinates, lateralCoordinates, spacesByLevel = self.getConstants(scriptsDict, connectionsDict)
        scriptVar, connectionVar = self.createVariables(solver, scriptsDict, connectionsDict, spacesByLevel)
        self.setConstraints(solver, spacesByLevel, scriptVar, connectionVar)
        solver.Minimize()

        status = solver.Solve()

        self.interpretSolution()
        pass

    def getConstants(self, scriptsDict: Dict[str, DisplayBlock], connectionDict: Dict[str, DisplayConnection]) -> \
            Tuple[Dict[Tuple[int, int], int], Dict[Tuple[int, int], np.array], Dict[int, int]]:
        """
        1. Get every pair of levels in connections
        2. Get coordinates of spaces in those levels
        3. Distances are determined by change of level and number of spaces in the two respective levels
        :return:
        """

        levelCoodinates = {
            (connection.sourceBlock.level, connection.targetBlock.level):
                np.abs(connection.sourceBlock.level - connection.targetBlock.level)
            for connection in connectionDict.values()
        }

        scriptsByLevel = self.getLevels(scriptsDict)
        spacesByLevel = {level: len(scripts) for level, scripts in scriptsByLevel.items()}

        lateralCoordinates = {
            (spacesByLevel[connection.sourceBlock.level], spacesByLevel[connection.targetBlock.level]): list()
            for connection in connectionDict.values()
        }
        for numSpacePairs in lateralCoordinates.keys():
            lateralCoordinates[numSpacePairs] = np.array(
                [
                    [np.abs(i / (numSpacePairs[0] + 1) - j / (numSpacePairs[1] + 1)) for j in
                     range(1, numSpacePairs[1] + 1)]
                    for i in range(1, numSpacePairs[0] + 1)
                ]
            )

        return levelCoodinates, lateralCoordinates, spacesByLevel

    def createVariables(
            self, solver: pywraplp.Solver,
            scriptsDict: Dict[str, DisplayBlock],
            connectionDict: Dict[str, DisplayConnection],
            spacesByLevel: Dict[int, int]
    ) -> Tuple[Dict[int, Dict[str, pywraplp.Solver.IntVar]], Dict[str, pywraplp.Solver.NumVar]]:
        """
        Variables are
        X_s
            - for every script s, X_s takes the values of 1 to num of spaces on the level of script s

        C_s1s2u
            - for scripts s1 and s2 upper

        C_s1s2l
            - for scripts s1 and s2 lower

        C_s1s2u and C_s1s2l to be used to make absolute values of distances

        :param connectionDict:
        :param solver:
        :param scriptsDict:
        :param spacesByLevel:
        :return:
        """
        scriptVar = dict()
        connectionVar = dict()

        for scriptIndex, (scriptID, scriptObj) in enumerate(scriptsDict.items()):
            scriptVar.setdefault(scriptObj.level, dict())[scriptID] = solver.IntVar(1, spacesByLevel[scriptObj.level], f'X[{scriptIndex}]')

        for connectionIndex, (connectionID, connectionObj) in enumerate(connectionDict.items()):
            connectionVar[connectionID] = {
                'upper': solver.NumVar(0, solver.infinity(), f'C[{connectionIndex}, U]'),
                'lower': solver.NumVar(0, solver.infinity(), f'C[{connectionIndex}, L]')
            }

        return scriptVar, connectionVar

    def setConstraints(
            self, solver: pywraplp.Solver,
            spacesByLevel: Dict[int, int],
            scriptVar: Dict[int, Dict[str, pywraplp.Solver.IntVar]],
            connectionVar: Dict[str, Dict[str, pywraplp.Solver.NumVar]]
    ):
        """
        Consider level L, which has spaces sigma(L).

        X_Ls = 1, 2, ..., sigma(L).
        For set S of scripts in level L, we have X_Ls <= sigma(L), X_L

        :param solver:
        :param spacesByLevel:
        :param scriptVar:
        :param connectionVar:
        :return:
        """
        for level, spaces in spacesByLevel.items():
            varList = list(scriptVar[level].items())
            levelRange = list(range(1, spaces + 1))
            for varIndex in range(len(varList)):
                firstVars = varList[:(varIndex + 1)]
                if varIndex != len(varList) - 1:
                    solver.Add(
                        sum(levelRange[:(varIndex + 1)]) <= solver.Sum(firstVar[1] for firstVar in firstVars)
                        <= sum(levelRange[(-varIndex - 1):])
                    )
                else:
                    solver.Add(solver.Sum(firstVar[1] for firstVar in firstVars) == sum(levelRange[:]))


        for connectionID, upperAndLowerConnectionVars in connectionVar.items():

            solver.Add(upperAndLowerConnectionVars['upper'] - upperAndLowerConnectionVars['lower'] == )
