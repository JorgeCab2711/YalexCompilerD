from Lexer import *

class ParserGenerator:
    def __init__(self, tokens, grammar_file):
        self.tokens = tokens
        self.grammar = self._load_grammar(grammar_file)

    def _load_grammar(self, file_name):
        grammar = {}
        tokens = [token[0] for token in self.tokens]
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()

            for line in lines:
                line = line.strip()
                if not line or line.startswith("/*") or line.startswith("%") or line == "IGNORE WHITESPACE":
                    continue

                if line == ";":  # Final de una definición de producción
                    if grammar[non_terminal][-1] == []:
                        grammar[non_terminal] = grammar[non_terminal][:-1]
                    continue

                if ":" in line:  # Solo procesar las líneas con reglas de producción
                    non_terminal, productions = line.split(":")
                    non_terminal = non_terminal.strip()
                    productions = [prod.strip().split() for prod in productions.split("|")]
                    valid_productions = []
                    for prod in productions:
                        if all(token in tokens for token in prod):
                            valid_productions.append(prod)
                    grammar[non_terminal] = valid_productions
                else:  # Continuación de una definición de producción
                    production = line.split()
                    if non_terminal in grammar:
                        grammar[non_terminal][-1] += production
                    else:
                        grammar[non_terminal] = [production]

            return grammar
        except IOError:
            print(f"Error al abrir el archivo {file_name}")
            return None

    def generate_parser(self):
        print("Tokens:")
        for token in self.tokens:
            print(token)

        print("\nGramática:")
        for non_terminal, productions in self.grammar.items():
            print(f"{non_terminal} -> {productions}")

def normilize_input_tokens( tokens : list):
        for token in tokens:
            token.pop()
            token.pop()
            new_token = token.pop(1).replace("'", "")
            token.append(new_token)
        return tokens

if __name__ == '__main__':
    # Lexer parte del laboratorio C y D 
    lexer = LexerAnalyzer('./yalex.txt', "file.txt")
    tokens_lexer = normilize_input_tokens(lexer.output_tokens)
    

    # Parser parte del laboratorio E
    parser = ParserGenerator(tokens_lexer, 'yapar_file.txt')
    parser.generate_parser()
