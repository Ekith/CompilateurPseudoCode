from src.analex import LexicalAnalyser
from src.symboltable import SymbolTable

import logging
import copy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SyntaxError(Exception):
	"""Exception raised for syntax errors in the input."""
	def __init__(self, message):
		super().__init__(message)
		self.message = message

	def __str__(self):
		return self.message

class SyntaxAnalyser:
	def __init__(self, lexical_analyser : LexicalAnalyser, symbol_table : SymbolTable):
		self.lexical_analyser : LexicalAnalyser = lexical_analyser
		self.symbol_table : SymbolTable = symbol_table

 
	def programme(self):
		"""Parse a program."""
		logger.debug("programme()")
		self.lexical_analyser.acceptKeyword("Programme")
		self.specif_prog_princ()
		self.corps_prog_princ()
  
	def specif_prog_princ(self):
		"""Parse the main program specifications."""
		logger.debug("specif_prog_princ()")
		self.lexical_analyser.acceptKeyword("Programme")
		self.identifiant()
		  
	def corps_prog_princ(self):
		"""Parse the main program body."""
		logger.debug("corps_prog_princ()")
		self.partie_decla()
		self.lexical_analyser.acceptKeyword("Debut")
		self.lexical_analyser.acceptKeyword("Programme")
		self.suite_instr()
		self.lexical_analyser.acceptKeyword("Fin")
  
	def partie_decla(self):
		"""Parse the declaration part of the program."""
		logger.debug("partie_decla()")
		if self.lexical_analyser.isKeyword("Prototypes"):
			logger.debug("Parsing procedures or functions")
			self.symbol_table.mode_prototype = True
			self.lexical_analyser.acceptKeyword("Prototypes")
			self.lexical_analyser.acceptSymbol(":")
			self.liste_prototype()
			self.symbol_table.mode_prototype = False
			self.lexical_analyser.acceptKeyword("Definitions")
			self.lexical_analyser.acceptSymbol(":")
			self.liste_decla_op()
		if self.lexical_analyser.isKeyword("Variables"):
			logger.debug("Parsing variable declarations")
			self.lexical_analyser.acceptKeyword("Variables")
			self.lexical_analyser.acceptSymbol(":")
			self.liste_decla_var()
   
		"""
		if not self.lexical_analyser.isKeyword("Procedure") and \
      		not self.lexical_analyser.isKeyword("Fonction") and \
        	not self.lexical_analyser.isKeyword("Variables"):
			raise SyntaxError(message="Expected 'Procedure', 'Fonction', or 'Variables' at the beginning of the declaration part")
  		"""

	def liste_prototype(self):
		"""Parse a list of prototypes."""
		logger.debug("liste_prototype()")
		self.prototype()
		if not self.lexical_analyser.isKeyword("Definitions"):
			self.liste_prototype()

	def prototype(self):
		"""Parse a function or procedure prototype."""
		logger.debug("prototype()")
		if self.lexical_analyser.isKeyword("Fonction"):
			self.prototype_fonction()
		elif self.lexical_analyser.isKeyword("Procedure"):
			self.prototype_procedure()
   
	def prototype_fonction(self):
		"""Parse a function prototype."""
		logger.debug("prototype_fonction()")
		self.lexical_analyser.acceptKeyword("Fonction")
		ident = self.identifiant()
		param = self.partie_formelle()
		self.lexical_analyser.acceptSymbol("->")
		type = self.type()
		self.symbol_table.add_entry(ident, type, "function", param)
		logger.debug(f"Function prototype: {ident}, return type: {type}, parameters: {param}")

	def prototype_procedure(self):
		logger.debug("prototype_procedure()")
		self.lexical_analyser.acceptKeyword("Procedure")
		ident = self.identifiant()
		param = self.partie_formelle()
		self.symbol_table.add_entry(ident, None, "procedure", param)
		logger.debug(f"Procedure prototype: {ident}, parameters: {param}")

	def liste_decla_op(self):
		"""Parse a list of operator declarations."""
		logger.debug("liste_decla_op()")
		self.decla_op()
		if self.lexical_analyser.isKeyword("Procedure") or self.lexical_analyser.isKeyword("Fonction"):
			self.liste_decla_op()

	def decla_op(self):
		"""Parse operator declarations."""
		logger.debug("decla_op()")
		if self.lexical_analyser.isKeyword("Procedure"):
			self.procedure()
		elif self.lexical_analyser.isKeyword("Fonction"):
			self.fonction()
    
	def procedure(self):
		"""Parse a procedure declaration."""
		logger.debug("procedure()")
		self.lexical_analyser.acceptKeyword("Procedure")
		ident = self.identifiant()

		self.symbol_table.enter_scope(ident)
		logger.debug(f"Entering scope: {ident}")
  
		param = self.partie_formelle()
		self.lexical_analyser.acceptSymbol(":")

		logger.debug(f"Procedure declaration: {ident}, parameters: {param}")
  
		self.corps_proc()
		self.symbol_table.leave_scope()

	def fonction(self):
		"""Parse a function declaration."""
		logger.debug("fonction()")
		self.lexical_analyser.acceptKeyword("Fonction")
		ident = self.identifiant()

		self.symbol_table.enter_scope(ident)
		logger.debug(f"Entering scope: {ident}")

		param = self.partie_formelle()
		self.lexical_analyser.acceptSymbol("->")
		type = self.type()
		logger.debug(f"Function type: {type}")
		self.lexical_analyser.acceptSymbol(":")
  
		logger.debug(f"Function type: {type}")

		self.corps_fonction()
		logger.debug(f"Function declaration: {ident}, return type: {type}, parameters: {param}")
		self.symbol_table.leave_scope()
  
	def corps_proc(self):
		"""Parse the body of a procedure."""
		logger.debug("corps_proc()")
		if not self.lexical_analyser.isKeyword("Debut"):
			self.lexical_analyser.acceptKeyword("Variables")
			self.lexical_analyser.acceptSymbol(":")
			self.partie_decla_proc()
		self.lexical_analyser.acceptKeyword("Debut")
		self.suite_instr()
		self.lexical_analyser.acceptKeyword("Fin")
  
	def corps_fonction(self):
		"""Parse the body of a function."""
		logger.debug("corps_fonction()")
		if not self.lexical_analyser.isKeyword("Debut"):
			self.lexical_analyser.acceptKeyword("Variables")
			self.lexical_analyser.acceptSymbol(":")
			self.partie_decla_fonction()
		self.lexical_analyser.acceptKeyword("Debut")
		self.suite_instr()
		self.lexical_analyser.acceptKeyword("Fin")
  
	def partie_formelle(self) -> list:
		"""Parse the formal part of a procedure or function."""
		logger.debug("partie_formelle()")
		self.lexical_analyser.acceptSymbol("(")
		t = [] # List to store formal specifications
		if not self.lexical_analyser.isSymbol(")"):
			t = self.liste_specif_formelles()
		self.lexical_analyser.acceptSymbol(")")
		return t

	def liste_specif_formelles(self) -> list:
		"""Parse a list of formal specifications."""
		logger.debug("liste_specif_formelles()")
		t = self.specif()
		q = [] # List to store formal specifications
		if self.lexical_analyser.isSymbol(","):
			self.lexical_analyser.acceptSymbol(",")
			q = self.liste_specif_formelles()
		return t+q
   
	def specif(self):
		"""Parse a formal specification."""
		logger.debug("specif()")
		names = self.liste_identifiants() # List of identifiers
		self.lexical_analyser.acceptSymbol(":")
		if self.lexical_analyser.isKeyword("entree"):
			mode = self.mode()
		type = self.type()
		logger.debug(f"Formal specification: {names}, type: {type}, mode: {mode if 'mode' in locals() else 'None'}")
		res = []
		if not self.symbol_table.mode_prototype:
			for name in names:
				self.symbol_table.add_entry(name, type, "variable", None, mode)
				res.append(self.symbol_table.lookup(name))
		return res

	def mode(self):
		"""Parse the mode of a formal specification."""
		logger.debug("mode()")
		if self.lexical_analyser.isKeyword("entree"):
			self.lexical_analyser.acceptKeyword("entree")
			if self.lexical_analyser.isKeyword("sortie"):
				self.lexical_analyser.acceptKeyword("sortie")
				return "entreeSortie"
			return "entree"

    
	def type(self):
		"""Parse the type of a formal specification."""
		logger.debug("type()")
		type = ""
		if self.lexical_analyser.isKeyword("entier"):
			self.lexical_analyser.acceptKeyword("entier")
			type = "entier"
		elif self.lexical_analyser.isKeyword("booleen"):
			self.lexical_analyser.acceptKeyword("booleen")
			type = "booleen"
		elif self.lexical_analyser.isKeyword("chaine"):
			self.lexical_analyser.acceptKeyword("chaine")
			type = "chaine"
		elif self.lexical_analyser.isKeyword("flottant"):
			self.lexical_analyser.acceptKeyword("flottant")
			type = "flottant"
		else:
			raise SyntaxError("Expected a type keyword (entier, booleen, chaine, flottant)")
		logger.debug(f"Type: {type}")
		return type

	def partie_decla_proc(self):
		"""Parse the declaration part of a procedure."""
		logger.debug("partie_decla_proc()")
		self.liste_decla_var()
  
	def partie_decla_fonction(self):
		"""Parse the declaration part of a function."""
		logger.debug("partie_decla_fonction()")
		self.liste_decla_var()
  
	def liste_decla_var(self):
		"""Parse a list of variable declarations."""
		logger.debug("liste_decla_var()")
		self.decla_var()
		if not self.lexical_analyser.isKeyword("Debut"):
			self.liste_decla_var()

	def decla_var(self):
		"""Parse a variable declaration."""
		logger.debug("decla_var()")
		names = self.liste_identifiants()
		self.lexical_analyser.acceptSymbol(":")
		type = self.type()
		for name in names:
			self.symbol_table.add_entry(name, type, "variable", None)
		logger.debug(f"Variable declaration: {names}, type: {type}")

	def liste_identifiants(self):
		"""Parse a list of identifiers."""
		logger.debug("liste_identifiants()")
		names = []
		ident = self.identifiant()
		names.append(ident)
		if self.lexical_analyser.isSymbol(","):
			self.lexical_analyser.acceptSymbol(",")
			names.extend(self.liste_identifiants())
		return names

	def suite_instr_non_vide(self):
		"""Parse a non-empty instruction sequence."""
		logger.debug("suite_instr_non_vide()")
		self.instr()
		if not self.lexical_analyser.isKeyword("Fin"):
			self.suite_instr_non_vide()
   
	def suite_instr(self):
		"""Parse an instruction sequence."""
		logger.debug("suite_instr()")
		if not self.lexical_analyser.isKeyword("Fin"):
			self.suite_instr_non_vide()
  
	def instr(self):
		"""Parse an instruction."""
		logger.debug("instr()")
		lexical_analyser_copy : LexicalAnalyser = copy.deepcopy(self.lexical_analyser)
		if self.lexical_analyser.isKeyword("Tant"):
			self.boucle()
		elif self.lexical_analyser.isKeyword("Si"):
			self.condition()
		elif self.lexical_analyser.isKeyword("afficher") or self.lexical_analyser.isKeyword("lire"):
			value_type = self.ent_sort()
		elif self.lexical_analyser.isKeyword("Renvoyer"):
			self.retour()
		elif lexical_analyser_copy.isIdentifier():
			lexical_analyser_copy.acceptIdentifier()
			if lexical_analyser_copy.isSymbol("("): # Check if it's a procedure
				self.appel_proc()
			elif lexical_analyser_copy.isSymbol("="): # Check if it's an assignment
				self.affectation()
		else:
			raise SyntaxError("Expected an instruction (loop, condition, input/output, return, procedure call, or assignment)")

	def appel_proc(self):
		"""Parse a procedure call."""
		logger.debug("appel_proc()")
		self.identifiant()
		self.lexical_analyser.acceptSymbol("(")
		if not self.lexical_analyser.isSymbol(")"):
			self.liste_param()
		self.lexical_analyser.acceptSymbol(")")

	def liste_param(self):
		"""Parse a list of parameters."""
		logger.debug("liste_param()")
		self.expression()
		if self.lexical_analyser.isSymbol(","):
			self.lexical_analyser.acceptSymbol(",")
			self.liste_param()

	def affectation(self):
		"""Parse an assignment."""
		logger.debug("affectation()")
		self.identifiant()
		self.lexical_analyser.acceptSymbol("=")
		self.expression()

	def expression(self) -> str:
		"""Parse an expression."""
		logger.debug("expression()")
		value_type = self.exp_ou()
		# logger.debug(f"Expression type: {value_type}")
		return value_type

	def exp_ou(self) -> str:
		"""Parse the or level of expressions."""
		logger.debug("exp_ou()")
		value_type = self.exp_et()
		if self.lexical_analyser.isKeyword("ou"):
			value_type_A = value_type
			self.lexical_analyser.acceptKeyword("ou")
			logger.debug("Found 'ou' keyword")
			value_type_B = self.exp_ou()
			if value_type_A != "booleen" or value_type_B != "booleen":
				logger.debug(f"exp_ou() found incompatible types")
				raise TypeError(f"Incompatible types: {value_type_A} and {value_type_B}")
			value_type = "booleen"
		# logger.debug(f"exp_ou() returns type: {value_type}")
		return value_type

	def exp_et(self) -> str:
		"""Parse the and level of expressions."""
		logger.debug("exp_et()")
		value_type = self.exp_comp()
		if self.lexical_analyser.isKeyword("et"):
			value_type_A = value_type
			self.lexical_analyser.acceptKeyword("et")
			logger.debug("Found 'et' keyword")
			value_type_B = self.exp_et()
			if value_type_A != "booleen" or value_type_B != "booleen":
				logger.debug(f"exp_et() found incompatible types")
				raise TypeError(f"Incompatible types: {value_type_A} and {value_type_B}")
			value_type = "booleen"
		# logger.debug(f"exp_et() returns type: {value_type}")
		return value_type

	def exp_comp(self) -> str:
		"""Parse the comparison level of expressions."""
		logger.debug("exp_comp()")
		value_type = self.exp_ad()
		if self.lexical_analyser.isKeyword("egal") or self.lexical_analyser.isKeyword("diff"):
			value_type_A = value_type
			self.op_comp()
			value_type_B = self.exp_comp()
			if not self.type_compatible(value_type_A, value_type_B):
				logger.debug(f"exp_comp() found incompatible types")
				raise TypeError(f"Incompatible types: {value_type_A} and {value_type_B}")
			value_type = "booleen"
   
		elif self.lexical_analyser.isKeyword("inf") or self.lexical_analyser.isKeyword("infegal") or \
      		 self.lexical_analyser.isKeyword("sup") or self.lexical_analyser.isKeyword("supegal"):
			value_type_A = value_type
			self.op_comp()
			value_type_B = self.exp_comp()
			if not self.type_compatible(value_type_A, value_type_B):
				logger.debug(f"exp_comp() found incompatible types")
				raise TypeError(f"Incompatible types: {value_type_A} and {value_type_B}")
			value_type = "booleen"
		# logger.debug(f"exp_comp() returns type: {value_type}")
		return value_type

	def op_comp(self):
		"""Parse a comparison operator."""
		logger.debug("op_comp()")
		if self.lexical_analyser.isKeyword("egal"):
			self.lexical_analyser.acceptKeyword("egal")
			logger.debug("Found 'egal' keyword")
		elif self.lexical_analyser.isKeyword("diff"):
			self.lexical_analyser.acceptKeyword("diff")
			logger.debug("Found 'diff' keyword")
		elif self.lexical_analyser.isKeyword("inf"):
			self.lexical_analyser.acceptKeyword("inf")
			logger.debug("Found 'inf' keyword")
		elif self.lexical_analyser.isKeyword("infegal"):
			self.lexical_analyser.acceptKeyword("infegal")
			logger.debug("Found 'infegal' keyword")
		elif self.lexical_analyser.isKeyword("sup"):
			self.lexical_analyser.acceptKeyword("sup")
			logger.debug("Found 'sup' keyword")
		elif self.lexical_analyser.isKeyword("supegal"):
			self.lexical_analyser.acceptKeyword("supegal")
			logger.debug("Found 'supegal' keyword")
		else:
			raise SyntaxError("Expected a relational operator")

	def exp_ad(self) -> str:
		"""Parse the addition level of expressions."""
		logger.debug("exp_ad()")
		value_type = self.exp_mult()
		if self.lexical_analyser.isSymbol("+") or self.lexical_analyser.isSymbol("-"):
			value_type_A = value_type
			self.op_ad()
			value_type_B = self.exp_ad()
			if not self.verify_types(value_type_A, value_type_B, ["number"]):
				logger.debug(f"exp_ad() found incompatible types")
				raise TypeError(f"Incompatible types: {value_type_A} and {value_type_B}")
			if value_type_A == "flottant" or value_type_B == "flottant":
				value_type = "flottant"
			else:
				value_type = "entier"
		# logger.debug(f"exp_ad() returns type: {value_type}")
		return value_type

	def op_ad(self):
		"""Parse an additive operator."""
		logger.debug("op_ad()")
		if self.lexical_analyser.isSymbol("+"):
			self.lexical_analyser.acceptSymbol("+")
			logger.debug("Found '+' symbol")
		elif self.lexical_analyser.isSymbol("-"):
			self.lexical_analyser.acceptSymbol("-")
			logger.debug("Found '-' symbol")
		else:
			raise SyntaxError("Expected an additive operator")

	def exp_mult(self) -> str:
		"""Parse the multiplication level of expressions."""
		logger.debug("exp_mult()")
		value_type = self.prim()
		if self.lexical_analyser.isSymbol("*") or self.lexical_analyser.isSymbol("/") or self.lexical_analyser.isSymbol("//") or self.lexical_analyser.isKeyword("modulo"):
			value_type_A = value_type
			self.op_mult()
			value_type_B = self.exp_mult()
			if self.verify_types(value_type_A, value_type_B, ["number"]):
				logger.debug(f"exp_mult() found incompatible types")
				raise TypeError(f"Incompatible types: {value_type_A} and {value_type_B}")
			if value_type_A == "flottant" or value_type_B == "flottant":
				value_type = "flottant"
			else:
				value_type = "entier"
		# logger.debug(f"exp_mult() returns type: {value_type}")
		return value_type

	def op_mult(self):
		"""Parse a multiplicative operator."""
		logger.debug("op_mult()")
		if self.lexical_analyser.isSymbol("*"):
			self.lexical_analyser.acceptSymbol("*")
			logger.debug("Found '*' symbol")
		elif self.lexical_analyser.isSymbol("/"):
			self.lexical_analyser.acceptSymbol("/")
			logger.debug("Found '/' symbol")
		elif self.lexical_analyser.isSymbol("//"):
			self.lexical_analyser.acceptSymbol("//")
			logger.debug("Found '//' symbol")
		elif self.lexical_analyser.isKeyword("modulo"):
			self.lexical_analyser.acceptKeyword("modulo")
			logger.debug("Found 'modulo' keyword")
		else:
			raise SyntaxError("Expected a multiplicative operator")

	def prim(self):
		"""Parse a primary expression."""
		logger.debug("prim()")
		if self.lexical_analyser.isSymbol("+") or self.lexical_analyser.isSymbol("-") or self.lexical_analyser.isKeyword("non"):
			self.op_unaire()
		value_type = self.elem_prim()
		# logger.debug(f"Primary expression type: {value_type}")
		return value_type
  
	def op_unaire(self):
		"""Parse a unary operator."""
		logger.debug("op_unaire()")
		if self.lexical_analyser.isSymbol("+"):
			self.lexical_analyser.acceptSymbol("+")
			logger.debug("Found '+' symbol")
		elif self.lexical_analyser.isSymbol("-"):
			self.lexical_analyser.acceptSymbol("-")
			logger.debug("Found '-' symbol")
		elif self.lexical_analyser.isKeyword("non"):
			self.lexical_analyser.acceptKeyword("non")
			logger.debug("Found 'non' keyword")
		else:
			raise SyntaxError("Expected a unary operator")

	def elem_prim(self) -> str:
		"""Parse an elementary primary expression."""
		logger.debug("elem_prim()")
		lexical_analyser_copy : LexicalAnalyser = copy.deepcopy(self.lexical_analyser)
		if self.lexical_analyser.isInteger() or \
      		self.lexical_analyser.isBoolean() or \
            self.lexical_analyser.isFloat2() or \
            self.lexical_analyser.isString():
			value_type = self.valeur()
		elif self.lexical_analyser.isSymbol("("):
			self.lexical_analyser.acceptSymbol("(")
			value_type = self.expression()
			self.lexical_analyser.acceptSymbol(")")
		elif lexical_analyser_copy.isIdentifier():
			lexical_analyser_copy.acceptIdentifier()
			if lexical_analyser_copy.isSymbol("("):
				value_type = self.appel_fonct()
				logger.debug(f"Function call type: {value_type}")
			else:
				name = self.identifiant()
				entry = self.symbol_table.lookup(name)
				logger.debug(f"Identifier lookup: {name}, found: {entry}")
				if entry is None:
					raise SyntaxError(f"Identifier '{name}' is not declared")
				value_type = entry.type
		else:
			raise SyntaxError("Expected a primary expression (value, identifier, or function call)")
		logger.debug(f"Elementary primary expression type: {value_type}")
		return value_type

	def appel_fonct(self) -> str:
		"""Parse a function call."""
		logger.debug("appel_fonct()")
		name = self.identifiant()
		self.lexical_analyser.acceptSymbol("(")
		if not self.lexical_analyser.isSymbol(")"):
			self.liste_param()
		self.lexical_analyser.acceptSymbol(")")
		entry = self.symbol_table.lookup(name)
		logger.debug(f"Function call: {name}, found: {entry}, scope: {self.symbol_table.current_scope}")
		if entry is None or entry.role != "function":
			raise SyntaxError(f"Function '{name}' is not declared or is not a function")
		else:
			return entry.type
  
	def valeur(self) -> str:
		"""Parse a value."""
		logger.debug("valeur()")
		if self.lexical_analyser.isFloat2():
			self.flottant()
			logger.debug("Value: float")
			return "flottant"
		elif self.lexical_analyser.isInteger():
			self.entier()
			logger.debug("Value: integer")
			return "entier"
		elif self.lexical_analyser.isKeyword("Vrai") or self.lexical_analyser.isKeyword("Faux"):
			self.val_bool()
			logger.debug("Value: boolean")
			return "booleen"
		elif self.lexical_analyser.isString():
			self.chaine()
			logger.debug("Value: string")
			return "chaine"
		else:
			raise SyntaxError("Expected a value (entier or booleen)")

	def val_bool(self):
		"""Parse a boolean value."""
		logger.debug("val_bool()")
		if self.lexical_analyser.isKeyword("Vrai"):
			self.lexical_analyser.acceptKeyword("Vrai")
			logger.debug("Boolean value: Vrai")
		elif self.lexical_analyser.isKeyword("Faux"):
			self.lexical_analyser.acceptKeyword("Faux")
			logger.debug("Boolean value: Faux")
		else:
			raise SyntaxError("Expected a boolean value (Vrai or Faux)")

	def ent_sort(self) -> str:
		"""Parse an entry or exit."""
		logger.debug("ent_sort()")
		if self.lexical_analyser.isKeyword("afficher"):
			self.lexical_analyser.acceptKeyword("afficher")
			self.lexical_analyser.acceptSymbol("(")
			value_type = self.expression()
			self.lexical_analyser.acceptSymbol(")")
		elif self.lexical_analyser.isKeyword("lire"):
			self.lexical_analyser.acceptKeyword("lire")
			self.lexical_analyser.acceptSymbol("(")
			name = self.identifiant()
			entry = self.symbol_table.lookup(name)
			if entry is None or entry.role != "variable":
				raise SyntaxError(f"Identifier '{name}' is not declared or is not a variable")
			value_type = entry.type
			self.lexical_analyser.acceptSymbol(")")
		else:
			raise SyntaxError("Expected an entry or exit (afficher or lire)")
		return value_type

	def boucle(self):
		"""Parse a loop."""
		logger.debug("boucle()")
		self.lexical_analyser.acceptKeyword("Tant")
		self.lexical_analyser.acceptKeyword("que")
		self.expression()
		self.lexical_analyser.acceptKeyword("Faire")
		self.suite_instr()
		self.lexical_analyser.acceptKeyword("Fin")
		self.lexical_analyser.acceptKeyword("Tant")
		self.lexical_analyser.acceptKeyword("que")
  
	def condition(self):
		"""Parse a condition."""
		logger.debug("condition()")
		self.lexical_analyser.acceptKeyword("Si")
		self.expression()
		self.lexical_analyser.acceptKeyword("Alors")
		self.suite_instr()
		self.lexical_analyser.acceptKeyword("Fin")
		self.lexical_analyser.acceptKeyword("Si")
		if self.lexical_analyser.isKeyword("Sinon"):
			self.lexical_analyser.acceptKeyword("Sinon")
			self.suite_instr()
		self.lexical_analyser.acceptKeyword("Fin")
		self.lexical_analyser.acceptKeyword("Sinon")
    
	def retour(self):
		"""Parse a return statement."""
		logger.debug("retour()")
		self.lexical_analyser.acceptKeyword("Renvoyer")
		value_type = self.expression()
		function_name = self.symbol_table.current_scope
		entry = self.symbol_table.lookup(function_name, "global")
		type_function = entry.type
		if type_function is None:
			raise SyntaxError(f"Function '{function_name}' is not declared or has no return type")
		elif type_function != value_type:
			raise TypeError(f"Return type '{value_type}' does not match function return type '{type_function}'")
		logger.debug(f"Return statement in function '{function_name}': {value_type}")


	def identifiant(self) -> str:
		"""Parse an identifier."""
		logger.debug("identifiant()")
		ident = self.lexical_analyser.acceptIdentifier()
		if not ident:
			lexical_unit = self.lexical_analyser.get_current_unit()
   
			raise SyntaxError(f"Expected an identifier <{self.lexical_analyser.get_value()}> ", lexical_unit.get_line_index(), lexical_unit.get_col_index())
		logger.debug(f"Identifier: {ident}")
		return ident
  
	def entier(self):
		"""Parse an integer."""
		logger.debug("entier()")
		value = self.lexical_analyser.acceptInteger()
		logger.debug(f"Integer value: {value}")
		if not value and value != 0:
			logger.debug("No integer value found")
			raise SyntaxError("Expected an integer")

	def flottant(self) -> float:
		"""Parse a float."""
		logger.debug("flottant()")
		integer_part = self.lexical_analyser.acceptInteger()
		if not integer_part:
			logger.debug("No integer part found")
			raise SyntaxError("Expected an integer part")
		logger.debug(f"Integer part: {integer_part}")

		if self.lexical_analyser.isSymbol("."):
			self.lexical_analyser.acceptSymbol(".")
			fractional_part = self.lexical_analyser.acceptInteger()
			if not fractional_part:
				logger.debug("No fractional part found")
				raise SyntaxError("Expected a fractional part")
			logger.debug(f"Fractional part: {fractional_part}")
			return float(f"{integer_part}.{fractional_part}")
		return float(integer_part)

	def chaine(self) -> str:
		"""Parse a string."""
		logger.debug("chaine()")
		value = self.lexical_analyser.acceptString()
		logger.debug(f"String value: {value}")
		if not value:
			logger.debug("No string value found")
			raise SyntaxError("Expected a string")
		return value

	def analyse(self):
		"""Start the syntax analysis."""
		try:
			self.programme()
			logger.debug("Syntax analysis completed successfully.")
		except SyntaxError as e:
			logger.error(f"Syntax error: {e}")
			raise e
		except Exception as e:
			logger.error(f"Unexpected error during syntax analysis: {e}")
			raise e

	def type_compatible(self, type_A: str, type_B: str) -> bool:
		"""Check if two types are compatible."""
		logger.debug(f"type_compatible(): {type_A} vs {type_B}")
		if type_A == type_B:
			return True
		if type_A == "entier" and type_B == "flottant":
			return True
		if type_A == "flottant" and type_B == "entier":
			return True
		return False

	def verify_types(self, type_A: str, type_B: str, wanted_type: list) -> bool:
		"""Verify if two types are compatible. booleen, nombre->(entier, flottant), chaine"""
		if type_A == "entier" or type_A == "flottant":
			v_type_A = "number"
		else:
			v_type_A = type_A

		if type_B == "entier" or type_B == "flottant":
			v_type_B = "number"
		else:
			v_type_B = type_B

		if v_type_A == v_type_B and v_type_A in wanted_type:
			return True
		return False
