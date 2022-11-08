class Coeus:
    def __init__(self):
        self.classes = dict()
        self.functions = dict()
        self.others = dict()

    def generate(self, code):
        print(code)

    def get_num_lines(self, text):
        return text.count('\n')

    def split_code(self, text):
        return text.split('\n')

    def organise_code(self, split_text):
        current_obj = None
        for line in split_text:
            if line == '':
                continue
            split_text_list = split_text.split(' ')
            if split_text_list[0] == 'class':
                class_name = split_text_list[1]
                self.classes[class_name] = {'methods': list(), 'attributes': list()}
                current_obj = 'class'
                continue
            if split_text_list[0] == 'def':
                func_name = split_text_list[1]
                self.functions[func_name] = list()
                current_obj = 'func'
                continue
            if current_obj is not None:
                if '\t' not in line:
                    current_obj = None
                else:
                    actual_line = line.split('\t')[-1]
