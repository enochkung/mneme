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

    def autosetBlocks(
            self, blocksDict: Dict[str, DisplayBlock], connectionsDict: Dict[str, DisplayConnection]
    ) -> Dict[str, Tuple[int, float]]:
        return self.runOptimisation(blocksDict, connectionsDict)

    def getLevels(self, scriptsDict: Dict[str, DisplayBlock]) -> Dict[int, List[str]]:
        scriptPathLocLengths = {
            scriptID: len(script.mnemeSelf.pathLocation.split('\\'))
            for scriptID, script in scriptsDict.items()
        }

        minLevel, maxLevel = min(scriptPathLocLengths.values()), max(scriptPathLocLengths.values())
        for scriptID, scriptLevel in scriptPathLocLengths.items():
            self.scriptsByLevel.setdefault(scriptLevel - minLevel, list()).append(scriptID)

        return self.scriptsByLevel

    def runOptimisation(
            self, scriptsDict: Dict[str, DisplayBlock], connectionsDict: Dict[str, DisplayConnection]
    ) -> Dict[str, Tuple[int, float]]:
        """
        This problem is to minimise the distances of the connections that exist and secondarily files of the same folder
        are closer to each other.
        Distances are measured using taxi cab metric, so d((X1, Y1), (X2, Y2)) = abs(X1 - X2) + abs(Y1 - Y2).

        For each script, we know which level it belongs to and how many spaces are there in each level. We associate
        to the script a number in range(number of spaces in level).
        :return:
        """

        def objFunc():
            return sum(
                np.abs(connection.sourceBlock.level - connection.targetBlock.level)
                for connection in connectionsDict.values()
            ) + sum(connection['upper'] + connection['lower'] for connection in connectionVar.values())

        solver = pywraplp.Solver.CreateSolver('SCIP')

        levelCoordinates, lateralCoordinates, spacesByLevel = self.getConstants(scriptsDict, connectionsDict)
        self.numLevels = max(level for level in spacesByLevel) + 1
        scriptVar, connectionVar = self.createVariables(solver, scriptsDict, connectionsDict, spacesByLevel)
        self.setConstraints(solver, spacesByLevel, scriptVar, connectionVar, connectionsDict)
        solver.Minimize(objFunc())

        status = solver.Solve()

        return self.interpretSolution(scriptVar, spacesByLevel)

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

    @staticmethod
    def createVariables(
            solver: pywraplp.Solver,
            scriptsDict: Dict[str, DisplayBlock],
            connectionDict: Dict[str, DisplayConnection],
            spacesByLevel: Dict[int, int]
    ) -> Tuple[Dict[int, Dict[str, Dict[int, pywraplp.Solver.BoolVar]]],
               Dict[str, Dict[str, pywraplp.Solver.NumVar]]]:
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
            for space in range(spacesByLevel[scriptObj.level]):
                scriptVar.setdefault(scriptObj.level, dict()).setdefault(scriptID, dict())[space + 1] = \
                    solver.BoolVar(f'X[{scriptObj.level}, {scriptIndex}, {space+1}]')

        for connectionIndex, (connectionID, connectionObj) in enumerate(connectionDict.items()):
            connectionVar[connectionID] = {
                'upper': solver.NumVar(0, solver.infinity(), f'C[{connectionIndex}, U]'),
                'lower': solver.NumVar(0, solver.infinity(), f'C[{connectionIndex}, L]')
            }

        return scriptVar, connectionVar

    @staticmethod
    def setConstraints(
            solver: pywraplp.Solver,
            spacesByLevel: Dict[int, int],
            scriptVar: Dict[int, Dict[str, Dict[int, pywraplp.Solver.BoolVar]]],
            connectionVar: Dict[str, Dict[str, pywraplp.Solver.NumVar]],
            connectionsDict: Dict[str, DisplayConnection],
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
        for level, scripts in scriptVar.items():
            for scriptID, spaceVars in scripts.items():
                solver.Add(solver.Sum(var for space, var in spaceVars.items()) == 1)
            for space in range(spacesByLevel[level]):
                solver.Add(solver.Sum(script[space + 1] for scriptID, script in scripts.items()) == 1)

        for connectionID, upperAndLowerConnectionVars in connectionVar.items():
            connectionObj = connectionsDict[connectionID]
            sourceScript, targetScript = connectionObj.sourceBlock, connectionObj.targetBlock
            sourceScriptID, targetScriptID = sourceScript.id, targetScript.id
            solver.Add(
                upperAndLowerConnectionVars['upper'] - upperAndLowerConnectionVars['lower'] ==
                solver.Sum(
                    space/(spacesByLevel[sourceScript.level] + 1) * var
                    for space, var in scriptVar[sourceScript.level][sourceScriptID].items()
                ) - solver.Sum(
                    space/(spacesByLevel[targetScript.level] + 1) * var
                    for space, var in scriptVar[targetScript.level][targetScriptID].items()
                )
            )

    @staticmethod
    def interpretSolution(
            scriptVar: Dict[int, Dict[str, Dict[int, pywraplp.Solver.BoolVar]]],
            spacesByLevel: Dict[int, int],
    ):
        coordinateByScript = dict()

        for level, scripts in scriptVar.items():
            for scriptID, spaceVar in scripts.items():
                coordinateByScript[scriptID] =\
                    (level, sum(
                        space * var.solution_value() / (spacesByLevel[level] + 1)
                        for space, var in spaceVar.items()
                    ))

        return coordinateByScript


class Navigator:
    def autosetConnections(self, blocksDict: Dict[str, DisplayBlock],
                           connectionsDict: Dict[str, DisplayConnection]):
        """
        Optimise Connection lines to have minimum overlaps

        Variables are
        :param blocksDict:
        :param connectionsDict:
        :return:
        """

        # solver = pywraplp.Solver.CreateSolver('SCIP')
        return self.naiveSolution(connectionsDict)

    def naiveSolution(self, connectionsDict: Dict[str, DisplayConnection]) -> Dict[str, List[Tuple[float, float]]]:
        connectionPos = dict()
        for connectionID, connection in connectionsDict.items():
            sourcePos = connection.sourceBlock.center
            targetPos = connection.targetBlock.center
            connectionPos[connectionID] = [sourcePos, (targetPos[0], sourcePos[1]), targetPos]

        return connectionPos

    def createVariables(self, solver: pywraplp.Solver,
                        connectionsDict: Dict[str, DisplayConnection]) -> None:
        """
        Variables are
            - for each connection, each connection has N vertices
            - each has an X and Y coordinates per vertex
        :param solver:
        :return:
        """
        connectionvar = dict()
        for connectionIndex, (connectionID, connection) in enumerate(connectionsDict.items()):
            connectionvar.setdefault(connectionID, dict())[connection.sourceBlock.id] = [
                solver.NumVar(connection.sourceBlock.center[1] - connection.sourceBlock.shape[1]/2,
                              connection.sourceBlock.center[1] + connection.sourceBlock.shape[1]/2,
                              f'C[S,{connectionIndex}]'),
                solver.NumVar(connection.targetBlock.center[1] - connection.targetBlock.shape[1]/2,
                              connection.targetBlock.center[1] + connection.targetBlock.shape[1]/2,
                              f'C[T,{connectionIndex}]')
            ]