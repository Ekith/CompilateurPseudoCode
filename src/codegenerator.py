from src.analex import LexicalAnalyser


class CodeGenerator:
    
    def __init__(self, output_file):
        self.output_file = output_file

        self.number_of_tabs = 0

        with open(self.output_file, 'w') as f:
            f.write("")

    def write(self, text):
        
        if text == "":
            text = " "
        
        if text[-1] == ";":
            text += "\n"

        elif text[-1] == "}":
            self.number_of_tabs -= 1
            text = text + "\n"

        elif text[-1] == "{":
            self.number_of_tabs += 1
            text = text + "\n"

        if self.is_new_line():
            text = "\t" * self.number_of_tabs + text

        with open(self.output_file, 'a') as f:
            f.write(text)


    def is_new_line(self):
        last_car = self.get_last_car()
        return last_car == "\n"

    def get_last_car(self):
        with open(self.output_file, 'r') as f:
            lines = f.readlines()
            if lines:
                return lines[-1][-1]
        return ""
    
    def association_keyword(self, value):
        
        keywords = {
            "entier": "int",
            "booleen": "bool",
            "chaine": "char*",
            "flottant": "float",
            "vide" : "void",
            "infeg" : "<=",
            "inf" : "<",
            "sup" : ">",
            "supeg" : ">=",
            "egal" : "==",
            "diff" : "!=",
            "et" : "&&",
            "ou" : "||",
            "non" : "!",
            "modulo" : "%",

            "print_entier" : "%d",
            "print_booleen" : "%d",
            "print_chaine" : "%s",
            "print_flottant" : "%f"
        }

        if value in keywords:
            return keywords[value]
        return value