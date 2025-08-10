from analex import LexicalAnalyser
from anasyn import SyntaxAnalyser
from symboltable import SymbolTable

import logging

def main():
    filename = "example/input.pcode"
    f = None
    try:
        f = open(filename, 'r')
    except:
        print("Error: can\'t open input file!")
        return

    outputFilename = "example/output.txt"
    symbolTableFilename = "example/symbol_table.txt"

    lexical_analyser = LexicalAnalyser()
	
    lineIndex = 0
    for line in f:
        line = line.rstrip('\r\n')
        lexical_analyser.analyse_line(lineIndex, line)
        lineIndex = lineIndex + 1
    f.close()

    lexical_analyser.save_to_file(outputFilename)
    
    symbol_table = SymbolTable()
    syntaxys_analyser = SyntaxAnalyser(lexical_analyser=lexical_analyser, symbol_table=symbol_table)
    try:
        syntaxys_analyser.analyse()

        with open(symbolTableFilename, 'w') as output_file:
            output_file.write(str(symbol_table))

    except Exception as e:
        print(f"Error: {e}")
        return
    
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().setLevel(logging.DEBUG)
    logger = logging.getLogger(__name__)

    main()
