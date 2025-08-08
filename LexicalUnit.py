########################################################################				 	
#### LexicalUnit classes					    ####				 	
########################################################################

## Class LexicalUnit
#
# Root class for the hierarchy of Lexical Units
class LexicalUnit(object):
	line_index = -1
	col_index = -1	
	length = 0
	value = None
	
	## The constructor
	def __init__(self, l, c, ln, value):
		self.line_index = l
		self.col_index = c
		self.length = ln
		self.value = value
		
	def get_line_index(self):
		return self.line_index
	
	def get_col_index(self):
		return self.col_index
		
	def get_length(self):
		return self.length
		
	def get_value(self):
		return self.value
	
	def is_keyword(self, keyword):
		return False

	def is_character(self, c):
		return False

	def is_symbol(self, s):
		return False
	
	def is_integer(self):
		return False
	
	def is_identifier(self):
		return False
		
	def is_fel(self):
		return False
	
        ## Static method used to retreive a specific LexicalUnit from 
        # a line of text formatted by __str__
        # @param line the line of text to process
        # @return A lexical unit (instance of a child class)
	@staticmethod
	def extract_from_line(line):
		fields = line.split('\t')
		if fields[0] == Identifier.__class__.__name__:
			return Identifier(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Keyword.__class__.__name__:
			return Keyword(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Character.__class__.__name__:
			return Character(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Symbol.__class__.__name__:
			return Symbol(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Fel.__class__.__name__:
			return Fel(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Integer.__class__.__name__:
			return Integer(fields[1], fields[2], fields[3], fields[4])
	
        ## Returns the object as a formatted string
	def __str__(self):
		unitValue = {'classname':self.__class__.__name__,'lIdx':self.line_index,'cIdx':self.col_index,'length':self.length,'value':self.value}
		return '%(classname)s\t%(lIdx)d\t%(cIdx)d\t%(length)d\t%(value)s\n' % unitValue

## Class to represent Identifiers
#
# This class inherits from LexicalUnit.
class Identifier(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Identifier, self).__init__(l, c, ln, v)

	## Return true since it is an Identifier
	def is_identifier(self):
		return True

## Class to represent Keywords
#
# This class inherits from LexicalUnit.		
class Keyword(LexicalUnit):
	## The constructor
	def __init__(self, l, c, ln, v):
		super(Keyword, self).__init__(l, c, ln, v)
		
        ## Return true since it is a keyword
	def is_keyword(self, keyword):
		return self.get_value() == keyword

## Class to represent Characters
#
# This class inherits from LexicalUnit.			
class Character(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Character, self).__init__(l, c, ln, v)

        ## Return true since it is a character
	def is_character(self, c):
		return self.get_value() == c

## Class to represent Symbols
#
# This class inherits from LexicalUnit.		
class Symbol(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Symbol, self).__init__(l, c, ln, v)

        ## Return true since it is a symbol
	def is_symbol(self, s):
		return self.get_value() == s

## Class to represent Integers
#
# This class inherits from LexicalUnit.		
class Integer(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Integer, self).__init__(l, c, ln, v)
	
        ## Return true since it is an integer
	def is_integer(self):
		return True

## Class to represent Fel (End of entry)
#
# This class inherits from LexicalUnit.			
class Fel(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Fel, self).__init__(l, c, ln, v)

        ## Return true since it is a Fel instance
	def is_fel(self):
		return True
	