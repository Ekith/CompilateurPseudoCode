from src.analex import LexicalAnalyser

import os

class CodeGenerator:
    
    def __init__(self, output_file):
        self.output_file = os.path.abspath(output_file)

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
            
            "infegal" : "<=",
            "inf" : "<",
            "sup" : ">",
            "supegal" : ">=",
            "egal" : "==",
            "diff" : "!=",
            "et" : "&&",
            "ou" : "||",
            "non" : "!",
            "modulo" : "%",
            
            "entree" : "",
            "entree sortie": "*",

            "print_entier" : "%d",
            "print_booleen" : "%d",
            "print_chaine" : "%s",
            "print_flottant" : "%f"
        }

        if value in keywords:
            return keywords[value]
        return value
    
    def delete_file(self):
        os.remove(self.output_file)

    def set_output_file(self, output_file):
        self.output_file = os.path.abspath(output_file)
        with open(self.output_file, 'w') as f:
            f.write("")

    def compile_file(self):
        os.system(f"gcc {self.output_file} -o {self.output_file}.out -Wall")
        os.remove(self.output_file)
    
    def execute_file(self):
        os.system(f"{self.output_file}.out")
        os.remove(f"{self.output_file}.out")