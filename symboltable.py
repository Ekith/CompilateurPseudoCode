import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SymbolTableError(Exception):
    """Custom exception for symbol table errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class SymbolTableEntry:
    def __init__(self, name, type, role, scope, args, mode=None):
        self.name = name            # nom du symbole
        self.type = type            # type pour une variable, type de retour pour une fonction, None pour une procédure
        self.role = role            # 'variable', 'function', 'procedure', etc.
        self.scope = scope          # soit 'global' soit le nom de la fonction où la variable est déclarée
        self.mode = mode            # mode ('None', 'entree', 'entreeSortie')
        self.args = args            # None pour une variable, liste des arguments pour une procédure ou fonction

    def __str__(self):
        if self.args == None:
            return f"{self.name} : {self.role} ({self.type}) in scope '{self.scope}' in mode {self.mode}"
        else:
            arg_str = ""
            for arg in self.args:
                arg_str += arg.name + ", "
            return f"{self.name} : {self.role} (returns {self.type}) (arguments : {arg_str}) in scope '{self.scope}'"


class SymbolTable:
    def __init__(self):
        self.entries = []       # Stocke les entrées de la table des symboles
        self.current_scope = "global"   # Scope où se trouve actuellement la table
        


    def enter_scope(self, scope_name):
        self.current_scope = scope_name
    
    
    def leave_scope(self):
        self.current_scope = "global"
    
    def add_entry(self, name, symbol_type, role, args, mode=None):
        if self.lookup(name, self.current_scope):
            logger.error(f"Duplicate declaration of '{name}' in scope '{self.current_scope}'")
            raise SymbolTableError(f"Duplicate declaration of '{name}' in scope '{self.current_scope}'")
        if role == "variable":
            try:
                entry = SymbolTableEntry(name, symbol_type, role, self.current_scope, args, mode)
            except Exception as e:
                raise SymbolTableError(f"Error adding variable '{name}': {e}")
        else:
            try:
                entry = SymbolTableEntry(name, symbol_type, role, self.current_scope, args)
            except Exception as e:
                raise SymbolTableError(f"Error adding function '{name}': {e}")
        self.entries.append(entry)
        
    def lookup(self, name, scope=None):
        if scope is None:
            scope = self.current_scope
        for entry in self.entries:
            if entry.name == name and entry.scope == scope:
                return entry
        return None

    def verify_ident(self, ident, type):
        if self.lookup(ident):
            if self.lookup(ident).type == type:
                print(f"'{ident}' is declared in scope '{self.current_scope}' with type '{type}'")
                return True
            else:
                raise Exception(f"Type mismatch for '{ident}' in scope '{self.current_scope}' expected '{self.lookup(ident).type}' found '{type}'")
        else:
            raise Exception(f"'{ident}' is not declared in scope '{self.current_scope}'")

    def __str__(self):
        result = "===============Symbol Table:===============\n"
        for entry in self.entries:
            result += str(entry) + "\n"
        result += "===========================================\n"
        return result