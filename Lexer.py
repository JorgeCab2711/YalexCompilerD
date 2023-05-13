import ply.lex as lex
from tabulate import tabulate
class LexerAnalyzer:
    def __init__(self, yalex_file, code_file):
        self.tokens = (
            'WHITESPACE',
            'ID',
            'NUMBER',
            'PLUS',
            'MINUS',
            'TIMES',
            'DIV',
            'LPAREN',
            'RPAREN',
            'LT',      
            'COLON',   
            'EQUAL',   
            'SEMICOLON', 
        )
        self.output_tokens = []
        self.lexer = lex.lex(module=self)
        self.yalex_file = yalex_file
        self.analyze_file(code_file)
  
        
        
    # Definición de tokens
    def t_WHITESPACE(self, t):
        r'\s+'
        pass  # Ignorar los espacios en blanco

    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z0-9]*'
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?([eE][-+]?\d+)?'
        t.value = float(t.value)  # Convertir la cadena a un número
        return t

    def t_PLUS(self, t):
        r'\+'
        return t

    def t_MINUS(self, t):
        r'-'
        return t

    def t_TIMES(self, t):
        r'\*'
        return t

    def t_DIV(self, t):
        r'/'
        return t

    def t_LPAREN(self, t):
        r'\('
        return t

    def t_RPAREN(self, t):
        r'\)'
        return t

    def t_LT(self, t):
        r'<'
        return t

    def t_COLON(self, t):
        r':'
        return t

    def t_EQUAL(self, t):
        r'='
        return t

    def t_SEMICOLON(self, t):
        r';'
        return t

    # Manejo de errores léxicos
    def t_error(self, t):
        print(f"'{t.value[0]}' Caracter No Válido")
        t.lexer.skip(1)

    def analyze_file(self, file_name):
        with open(file_name, "r") as file:
            data = file.read()
        
        # Tokenizar el archivo
        self.lexer.input(data)
        
        for token in self.lexer:
            token = str(token).replace("LexToken(", "")
            if token[-1] == ')':
                token = token[:-1]
            token = token.split(",")
            self.output_tokens.append(token)
                
    def print_output(self):
        print(tabulate(self.output_tokens, headers=["Token", "Lexema", "Linea", "Posicion"]))          
            

if __name__ == "__main__":
    lexer = LexerAnalyzer('./yalex.txt', "file.txt")
    
   
    
    
