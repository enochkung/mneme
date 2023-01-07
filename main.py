from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
from tkinter.scrolledtext import ScrolledText

# from crius import Crius
from mainV2 import main


class CodeViz:
    def __init__(self):
        self.compiler = Tk()
        self.compiler.title('CodeViz19')
        self.compiler.geometry('1800x900+10+10')
        self.canvas = CodeVizCanvas(self.compiler)
        self.editor = CodeVizEditor(self.compiler)
        self.output = CodeVizOutput(self.compiler)
        self.menu = CodeVizMenu(self.compiler, self.editor, self.output, self.canvas)

        self.compiler.mainloop()


class CodeVizMenu:
    def __init__(self, compiler, editor, output, canvas):
        self.menu_bar = Menu(compiler, tearoff=False)
        self.editor = editor
        self.output = output
        self.file_menu = FileMenu(self.menu_bar, self.editor)
        self.run_menu = RunMenu(self.menu_bar, self.editor, self.output, self.file_menu)
        self.diagram_menu = DiagramMenu(self.menu_bar, self.editor, canvas, self.output)
        compiler.config(menu=self.menu_bar)


class DiagramMenu:
    def __init__(self, menu_bar, editor, canvas, output):
        self.menu_bar = menu_bar
        self.editor = editor
        self.canvas = canvas
        self.output = output
        self.menu = Menu(self.menu_bar, tearoff=False)
        self.menu.add_command(label='Generate', command=self.generate_diagram)
        self.menu_bar.add_cascade(label='Diagram', menu=self.menu)

    def generate_diagram(self):
        self.canvas.generate_diagram(self.editor)


class RunMenu:
    def __init__(self, menu_bar, editor, output, file_menu):
        self.menu_bar = menu_bar
        self.file_menu = file_menu
        self.editor = editor
        self.output = output
        self.menu = Menu(self.menu_bar, tearoff=False)
        self.menu.add_command(label='Run', command=self.run_script)
        self.menu_bar.add_cascade(label='Run', menu=self.menu)
        self.process = None

    def run_script(self):
        if self.editor.file_path == '':
            self.file_menu.save()
        command = f'python {self.editor.file_path}'
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = self.process.communicate()
        self.output.code_output.delete('1.0', END)
        self.output.code_output.insert('1.0', output)
        self.output.code_output.insert('2.0', error)


class FileMenu:
    def __init__(self, menu_bar, editor):
        self.menu_bar = menu_bar
        self.editor = editor
        self.menu = Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='File', menu=self.menu)
        self.menu.add_command(label='New', command=self.new_file)
        self.menu.add_command(label='Open', command=self.open_file)
        self.menu.add_command(label='Save', command=self.save)
        self.menu.add_command(label='Save As', command=self.save_as)
        self.menu.add_command(label='Exit', command=exit)

    def new_file(self):
        self.save()
        self.editor.file_path = ''
        self.editor.editor.delete('1.0', END)

    def open_file(self):
        path = askopenfilename(filetypes=[('Python Files', '*.py')])
        with open(path, 'r') as file:
            code = file.read()
            self.editor.editor.delete('1.0', END)
            self.editor.editor.insert('1.0', code)
            self.set_file_path(path)

    def save(self):
        if self.editor.file_path == '':
            self.save_as()
            return
        self.save_as(self.editor.file_path)

    def save_as(self, path=None):
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')]) if path is None else path
        with open(path, 'w') as file:
            code = self.editor.editor.get('1.0', END)
            file.write(code)
            self.set_file_path(path)

    def set_file_path(self, path):
        self.editor.file_path = path


class CodeVizCanvas:
    def __init__(self, compiler):
        self.compiler = compiler
        self.crius = Crius()
        diagram_canvas = Canvas(self.compiler, bg='white', height=10, width=120, highlightthickness=3,
                                highlightbackground='black')
        diagram_canvas.create_line(1, 1, 500, 500)
        diagram_canvas.pack(fill=BOTH, expand=True, side='right')

    def generate_diagram(self, editor):
        code = editor.editor.get('1.0', END)
        self.crius.generate(code)


class CodeVizEditor:
    def __init__(self, compiler):
        self.file_path = ''
        self.editor = ScrolledText(compiler, width=120, height=45)
        self.editor.pack(padx=10, pady=10, anchor="w")


class CodeVizOutput:
    def __init__(self, compiler):
        self.code_output = ScrolledText(compiler, width=120, height=20)
        self.code_output.pack(padx=10, pady=10, anchor="w")


if __name__ == '__main__':
    # CodeViz()
    main()