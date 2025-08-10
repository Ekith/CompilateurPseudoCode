import sys, argparse, re

from src.lexicalunit import LexicalUnit, Character, Keyword, Symbol, Identifier, Integer, Fel, String, Float

DEBUG = False

LEXICAL_UNIT_CHARACTER			= "char"
LEXICAL_UNIT_KEYWORD			= "keyword"
LEXICAL_UNIT_SYMBOL				= "symbol"
LEXICAL_UNIT_IDENTIFIER			= "ident"
LEXICAL_UNIT_INTEGER			= "integer"
LEXICAL_UNIT_FEL				= "fel"

KEYWORDS  = [ \
    "Programme", "Debut", "Fin", "Procedure", "Fonction", "Variables", "Prototypes", "Definitions",
    "Si", "Sinon", "Alors", "Tant", "que", "Faire",
    "afficher", "lire", "Renvoyer",
    "entree", "entree sortie",
    "entier", "booleen", "flottant", "chaine",
    "Vrai", "Faux",
    "egal", "diff", "inf", "infegal", "sup", "supegal",
    "ou", "et", "non", "modulo"
	]


SYMBOLS = [
    "->", "=", "+", "-", "*", "/", "(", ")", ",", ";", ":", "."
]

class AnaLexException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
	
## Lexical analyser class
#
class LexicalAnalyser(object):	
        ## Attribute to store the different lexical units
	lexical_units = []

        ## Index used to keep track of the lexical unit under treatment
	lexical_unit_index = -1
	
        ## The constructor
	def __init__(self):
		lexical_units = []
	
        ## Analyse a line and extract the lexical units. 
        # The extracted lexical units are then added to the attribute lexical_units.
        # @param lineIndex index of the line in the original text
        # @param line the lien of text to analyse
	def analyse_line(self, lineIndex, line):
		space = re.compile("\s")
		digit = re.compile("[0-9]")
		char = re.compile("[a-zA-Z]")
		beginColIndex = 0
		c = ''
		colIndex = 0
		while colIndex < len(line):
			c = line[colIndex]
			unitValue = None
			if c == '/': # begin of comment or /= ...
				beginColIndex = colIndex
				colIndex = colIndex + 1
				c = line[colIndex]
				if c == '/': # it is a comment => skip rest of line
					return
				else:
					# record as character
					unitValue = Symbol(lineIndex, colIndex-1, 1, "/")
			elif digit.match(c):
				# It is a number 
				beginColIndex = colIndex
				n = 0
				while colIndex<len(line) and (digit.match(c)):
					n = 10*n + int(c)
					colIndex = colIndex + 1
					if colIndex < len(line):
						c = line[colIndex]
				unitValue = Integer(lineIndex, beginColIndex, colIndex-beginColIndex, n)
			elif space.match(c):
				colIndex = colIndex + 1
			elif char.match(c):
				# It is either an identifier or a keyword
				beginColIndex = colIndex
				ident = ''
				while colIndex<len(line) and (char.match(c) or digit.match(c)):
					ident = ident + c
					colIndex = colIndex + 1
					if colIndex < len(line): 
						c = line[colIndex]
					
				if string_is_keyword(ident): # Check if it is a keyword
					unitValue = Keyword(lineIndex, beginColIndex, len(ident), ident)
				else: # It is an identifier
					unitValue = Identifier(lineIndex, beginColIndex, len(ident), ident)
     
			elif c == '"': # String literal
				# It is either an identifier or a keyword
				beginColIndex = colIndex
				string = ''
				is_escaped = False
				while colIndex<len(line) and not is_escaped:
					string = string + c
					colIndex = colIndex + 1
					if colIndex < len(line): 
						c = line[colIndex]
					if c == '"':
						string += c
						is_escaped = not is_escaped
						colIndex = colIndex + 1 # Skip the closing quote

				unitValue = String(lineIndex, beginColIndex, len(string), string)

			elif c == "'": # String literal
				# It is either an identifier or a keyword
				beginColIndex = colIndex
				string = ''
				is_escaped = False
				while colIndex<len(line) and not is_escaped:
					string = string + c
					colIndex = colIndex + 1
					if colIndex < len(line): 
						c = line[colIndex]
					if c == "'":
						string += c
						is_escaped = not is_escaped
						colIndex = colIndex + 1 # Skip the closing quote

				unitValue = String(lineIndex, beginColIndex, len(string), string)

			elif c == '-': # Subtraction
				beginColIndex = colIndex
				colIndex = colIndex + 1
				c = line[colIndex]
				if c == '>': # It is a symbol
					unitValue = Symbol(lineIndex, colIndex-1, 2, "->")
					colIndex = colIndex + 1
				else: # It is a character
					unitValue = Symbol(lineIndex, colIndex-1, 1, "-")

			elif string_is_symbol(c): # It is a symbol
				beginColIndex = colIndex
				colIndex = colIndex + 1
				unitValue = Symbol(lineIndex, beginColIndex, 1, c)

			else:
				colIndex = colIndex + 1
				unitValue = Character(lineIndex, colIndex-1, 1, c)
    
			if unitValue != None:
				self.lexical_units.append(unitValue)
		
        ## Saves the lexical units to a text file.
        # @param filename Name of the output file (if "" then output to stdout)
	def save_to_file(self, filename):
		output_file = None
		if filename != "":
			try:
				output_file = open(filename, 'w')
			except:
				print("Error: can\'t open output file!")
				return
		else:
			output_file = sys.stdout
		
		for lexicalUnit in self.lexical_units:
			output_file.write("%s" % lexicalUnit)
			
		if filename != "":
			output_file.close()
	
        ## Loads lexical units from a text file.
        # @param filename Name of the file to load (if "" then stdin is used)
	def load_from_file(self, filename):
		input_file = None
		if filename != "":
			try:
				input_file = open(filename, 'w')
			except:
				print("Error: can\'t open output file!")
				return
		else:
			input_file = sys.stdint
		
		lines = input_file.read_lines()
			
		if filename != "":
			input_file.close()
		
		for line in lines:
			lexical_unit = LexicalUnit.extract_from_line(line)
			self.lexical_units.append(lexical_unit)

        ## Verifies that the current lexical unit index is not out of bounds
        # return True if lexical_unit_index < len(lexical_units)
	def verify_index(self):
		return self.lexical_unit_index < len(self.lexical_units)
		
        ## Accepts a given keyword if it corresponds to the current lexical unit.
        # @param keyword string containing the keyword
        # @exception AnaLexException When the keyword is not found
	def acceptKeyword(self, keyword):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while keyword "+keyword+" expected!")
		if self.lexical_units[self.lexical_unit_index].is_keyword(keyword):
			self.lexical_unit_index += 1
		else:
			raise 	("Expecting keyword "+keyword+" <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")

        ## Accepts an identifier if it corresponds to the current lexical unit.
        # @return identifier string value
        # @exception AnaLexException When no identifier is found
	def acceptIdentifier(self) -> str:
		if not self.verify_index():
			raise AnaLexException("Found end of entry while identifer expected!")
		if self.lexical_units[self.lexical_unit_index].is_identifier():
			value =  self.lexical_units[self.lexical_unit_index].get_value()
			self.lexical_unit_index += 1
			return value
		else:
			raise AnaLexException("Expecting identifier <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")
	
        ## Accepts an integer if it corresponds to the current lexical unit.
        # @return integer value
        # @exception AnaLexException When no integer is found
	def acceptInteger(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while integer value expected!")
		if self.lexical_units[self.lexical_unit_index].is_integer():
			value = self.lexical_units[self.lexical_unit_index].get_value()
			self.lexical_unit_index += 1
			return value
		else:
			raise AnaLexException("Expecting integer <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")
	

        ## Accepts a Fel instance if it corresponds to the current lexical unit.
        # @exception AnaLexException When no Fel is found
	def acceptFel(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting .!")
		if self.lexical_units[self.lexical_unit_index].is_fel():
			self.lexical_unit_index += 1
		else:
			raise AnaLexException("Expecting end of program <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")

        ## Accepts a given character if it corresponds to the current lexical unit.
        # @param c string containing the character
        # @exception AnaLexException When the character is not found
	def acceptCharacter(self, c):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting character " + c + "!")
		if self.lexical_units[self.lexical_unit_index].is_character(c):
			self.lexical_unit_index += 1
		else:
			raise AnaLexException("Expecting character " + c + " <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")	

        ## Accepts a given symbol if it corresponds to the current lexical unit.
        # @param s string containing the symbol
        # @exception AnaLexException When the symbol is not found
	def acceptSymbol(self, s):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting symbol " + s + "!")
		if self.lexical_units[self.lexical_unit_index].is_symbol(s):
			self.lexical_unit_index += 1
		else:
			raise AnaLexException("Expecting symbol " + s + " <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")	
	
	    ## Accepts a given = if it corresponds to the current lexical unit.
        # @param s string containing the symbol
        # @exception AnaLexException When the symbol is not found
	def acceptString(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting a string !")
		if self.lexical_units[self.lexical_unit_index].is_string():
			value = self.lexical_units[self.lexical_unit_index].get_value()
			self.lexical_unit_index += 1
			return value
		else:
			raise AnaLexException("Expecting string <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")


 
 
        ## Tests if a given keyword corresponds to the current lexical unit.
        # @return True if the keyword is found
        # @exception AnaLexException When the end of entry is found
	def isKeyword(self, keyword):
		if not self.verify_index():
			raise AnaLexException("Unexpected end of entry!")
		if self.lexical_units[self.lexical_unit_index].is_keyword(keyword):
			return True
		return False

        ## Tests the current lexical unit corresponds to an identifier.
        # @return True if an identifier is found
        # @exception AnaLexException When the end of entry is found
	def isIdentifier(self):
		if not self.verify_index():
			raise AnaLexException("Unexpected end of entry!")
		if self.lexical_units[self.lexical_unit_index].is_identifier():
			return True
		return False

	## Tests if a given character corresponds to the current lexical unit.
        # @return True if the character is found
        # @exception AnaLexException When the end of entry is found
	def isCharacter(self, c):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting character " + c + "!")
		if self.lexical_units[self.lexical_unit_index].is_character(c):
			return True
		return False			

        ## Tests the current lexical unit corresponds to an integer.
        # @return True if an integer is found
        # @exception AnaLexException When the end of entry is found
	def isInteger(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting integer value!")
		if self.lexical_units[self.lexical_unit_index].is_integer():
			return True
		return False			

        ## Tests if a given symbol corresponds to the current lexical unit.
        # @return True if the symbol is found
        # @exception AnaLexException When the end of entry is found
	def isSymbol(self, s):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting symbol " + s + "!")
		if self.lexical_units[self.lexical_unit_index].is_symbol(s):
			return True
		return False

        ## Tests if a string corresponds to the current lexical unit.
        # @return True if a string is found
        # @exception AnaLexException When the end of entry is found
	def isString(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting string!")
		if self.lexical_units[self.lexical_unit_index].is_string():
			return True
		return False

	def isFloat2(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting float!")
		if self.lexical_units[self.lexical_unit_index].is_integer():
			if self.lexical_units[self.lexical_unit_index+1].is_symbol("."):
				if self.lexical_units[self.lexical_unit_index+2].is_integer():
					return True
		return False

	def isBoolean(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting boolean!")
		if self.lexical_units[self.lexical_unit_index].is_keyword("Vrai") or self.lexical_units[self.lexical_unit_index].is_keyword("Faux"):
			return True
		return False

        ## Returns the value of the current lexical unit
        # @return value of the current unit
	def get_value(self):
		return self.lexical_units[self.lexical_unit_index].get_value()

		## Returns the current lexical unit
		# @return current lexical unit
	def get_current_unit(self):
		return self.lexical_units[self.lexical_unit_index]

        ## Initializes the lexical analyser
	def init_analyser(self):
		self.lexical_unit_index = 0
	
########################################################################				 		 

## Tests if a keyword is in the table of keywords
# @return True if the keyword is found
def string_is_keyword(s):
	return KEYWORDS.count(s) != 0

def string_is_symbol(s):
	return SYMBOLS.count(s) != 0

		 
########################################################################				 	
def main():
	parser = argparse.ArgumentParser(description='Do the lexical analysis of a NNP program.')
	parser.add_argument('inputfile', type=str, nargs=1, help='name of the input source file')
	parser.add_argument('-o', '--outputfile', dest='outputfile', action='store', default="", help='name of the output file (default: stdout)')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
	
	args = parser.parse_args()

	filename = args.inputfile[0]
	f = None
	try:
		f = open(filename, 'r')
	except:
		print("Error: can\'t open input file!")
		return
		
	outputFilename = args.outputfile
	
	lexical_analyser = LexicalAnalyser()
	
	lineIndex = 0
	for line in f:
		line = line.rstrip('\r\n')
		lexical_analyser.analyse_line(lineIndex, line)
		lineIndex = lineIndex + 1
	f.close()
	
	lexical_analyser.save_to_file(outputFilename)
	
########################################################################				 

if __name__ == "__main__":
    main() 



