import argparse, os, logging


from analex import LexicalAnalyser
from anasyn import SyntaxAnalyser
from symboltable import SymbolTable

def main(input_file, symbol_table_file=None, lexical_analysis_file=None, output_file=None):
    
    input_filename = os.path.abspath(input_file)
    if symbol_table_file:
        symbol_table_filename = os.path.abspath(symbol_table_file)
    if lexical_analysis_file:
        lexical_analysis_filename = os.path.abspath(lexical_analysis_file)
    if output_file:
        output_filename = os.path.abspath(output_file)

    try:
        f = open(input_filename, 'r')
    except FileNotFoundError:
        logging.error(f"Error: can't open input file '{input_filename}'!")
        return
    
    lexical_analyser = LexicalAnalyser()

    try:
        lineIndex = 0
        for line in f:
            line = line.rstrip('\r\n')
            lexical_analyser.analyse_line(lineIndex, line)
            lineIndex = lineIndex + 1
        f.close()
    except Exception as e:
        f.close()
        logging.error(f"Error: {e}")
        return

    logging.info(f"Lexical analysis completed. {lineIndex} lines processed.")

    if lexical_analysis_file:
        lexical_analyser.save_to_file(lexical_analysis_filename)
        
    symbol_table = SymbolTable()
    syntax_analyser = SyntaxAnalyser(lexical_analyser=lexical_analyser, symbol_table=symbol_table)

    try:
        syntax_analyser.analyse()
        logging.info("Syntax analysis completed.")
        
        if symbol_table_file:
            with open(symbol_table_filename, 'w') as output_file:
                output_file.write(str(symbol_table))

    except Exception as e:
        logging.error(f"Error: {e}")
        return
    


parser = argparse.ArgumentParser(description="Pseudo-code compiler")
parser.add_argument("input_file", help="Input file containing pseudo code")

# -st to choose the output file for the symbol table
parser.add_argument("-st", "--symbol_table", help="Output file for the symbol table")

# -al to choose the output file for the lexical analyser
parser.add_argument("-al", "--lexical_analysis", help="Output file for the lexical analyser")

# -o to choose output file
parser.add_argument("-o", "--output_file", help="Output file for the compiled code")

# -v for verbose output
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output", default=False)

args = parser.parse_args()

if __name__ == "__main__":

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    main(
        input_file=args.input_file,
        symbol_table_file=args.symbol_table,
        lexical_analysis_file=args.lexical_analysis,
        output_file=args.output_file
    )