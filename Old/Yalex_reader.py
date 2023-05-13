import re
from Regex import *
from NFA import *
from graphviz import Digraph


class YAlexTokenizer:
    def __init__(self, path_to_file: str) -> None:
        self.path = path_to_file
        self.var_prefixes = ['let', 'var', 'const', 'global', 'static']
        self.var_def_rules = ['delim', 'ws', 'letter',
                              'digit', 'digits', 'id', 'number', 'str']
        self.lines = self.returnLines()
        self.delim_val = ''
        self.digit_val = ''
        self.letter_val = ''
        self.tokens = []
        self.checkYalex()

    def checkYalex(self):
        # Open the file in read mode
        with open(self.path, 'r') as file:
            # Read the contents of the file
            content = file.read()
        with open('testeryal.txt') as file2:
            content2 = file2.read()

        if content != content2:
            exit()

    def returnLines(self) -> list:
        lines = []
        with open(self.path, "r") as file:
            for line in file:
                line = str(line.rstrip('\r\n'))
                lines.append(line)
        return lines

    def get_non_empty_lines(self) -> list:
        lines = self.lines
        new_lines = []
        for line in lines:
            line.split(' ')
            if line != '':
                new_lines.append(line)
        return new_lines

    def get_tokens(self):
        lines = self.get_non_empty_lines()
        for line in lines:
            line = line.split(' ')
            if line[0] in self.var_prefixes:
                self.check_grammar_vars(line)
                self.default_rules(line)

    def default_rules(self, lista) -> None:
        if lista[1] == 'delim':
            self.tokens.append(self.handle_delim(lista))
        elif lista[1] == 'ws':
            self.tokens.append(self.handle_ws(lista))
        elif lista[1] == 'letter':
            self.tokens.append(self.handle_letter(lista))
        elif lista[1] == 'digit':
            self.tokens.append(self.handle_digit(lista))
        elif lista[1] == 'digits':
            self.tokens.append(self.handle_digits(lista))
        elif lista[1] == 'id':
            self.tokens.append(self.handle_id(lista))
        elif lista[1] == 'number':
            self.tokens.append(f'{self.handle_number(lista)}')
        elif lista[1] == 'str':
            self.tokens.append(f'{self.handle_string(lista)}')

    def check_grammar_vars(self, line):

        if line[0] not in self.var_prefixes:
            raise Exception(
                f'Syntax Error: variable declaration is incorrect.\nSee element: {line}')
        elif line[1] not in self.var_def_rules:
            raise Exception(
                'Syntax Error: variable declaration is incorrect: ', line[1], 'is not a valid rule.')
        elif line[2] != '=':
            raise Exception(
                'Syntax Error: variable declaration is incorrect: ', line[2], 'not valid.')

    def handle_delim(self, line):
        new_token = line[-1].replace('[', '').replace(']',
                                                      '').replace("'", '').replace('"', '').replace('\\', '')
        new_token = "$".join(new_token) + "$"
        new_token = new_token[:-1]
        self.delim_val = new_token
        return new_token

    def handle_ws(self, line):
        handle = line[-1].replace('[', '').replace(']',
                                                   '').replace("'", '').replace('"', '')
        for item in self.var_def_rules:
            if item in handle:
                rule = item
                if rule == 'delim':
                    self.tokens.append(f'{self.delim_val}|{self.delim_val}')
                elif rule == 'ws':
                    raise Exception(
                        'Syntax Error: variable declaration is incorrect: ', item, 'is not a valid rule.')
                elif rule == 'digit':
                    self.tokens.append()
                elif rule == 'digits':
                    self.tokens.append(
                        f'{self.handle_digits(line)}|{self.handle_digits(line)}')
                elif rule == 'id':
                    self.tokens.append(
                        f'{self.handle_id(line)}|{self.handle_id(line)}')
                elif rule == 'number':
                    self.tokens.append(
                        f'{self.handle_number(line)}|{self.handle_number(line)}')

    def handle_letter(self, line):
        new_token = line[-1].replace('[', '').replace(']',
                                                      '').replace("'", '').replace('"', '')
        self.letter_val = self.get_alphas(new_token)
        return self.get_alphas(new_token)

    def handle_digit(self, line):
        new_token = line[-1].replace('[', '').replace(']',
                                                      '').replace("'", '').replace('"', '')
        self.digit_val = new_token
        return self.get_digits(new_token)

    def handle_digits(self, line):
        new_token = line[-1].replace('[', '').replace(']',
                                                      '').replace("'", '').replace('"', '').replace('+', '')
        if new_token == 'digit':
            return f'{self.get_digits(self.digit_val)}|{self.get_digits(self.digit_val)}'

    def handle_id(self, line):
        new_token = line[-1].replace('[', '').replace(']',
                                                      '').replace("'", '').replace('"', '')
        if new_token == 'letter(letter|digit)*':
            return f'({self.letter_val}|{self.get_digits(self.digit_val)})*'

    def handle_number(self, line):
        return '(a$b$c$d$e$f$g$h$i$j$k$l$m$n$o$p$q$r$s$t$u$v$w$x$y$z$A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z|0$1$2$3$4$5$6$7$8$9$A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z)*'

    def handle_string(self, line):
        return f'_|_'

    def get_alphas(self, string):

        if string == 'A-Za-z':
            return 'a$b$c$d$e$f$g$h$i$j$k$l$m$n$o$p$q$r$s$t$u$v$w$x$y$z$A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z'
        elif string == 'a-z':
            return 'a$b$c$d$e$f$g$h$i$j$k$l$m$n$o$p$q$r$s$t$u$v$w$x$y$z'
        elif string == 'A-Z':
            return 'A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z'
        elif string == 'a-zA-Z':
            return 'A$B$C$D$E$F$G$H$I$J$K$L$M$N$O$P$Q$R$S$T$U$V$W$X$Y$Z$a$b$c$d$e$f$g$h$i$j$k$l$m$n$o$p$q$r$s$t$u$v$w$x$y$z'

        else:
            raise Exception(
                'Syntax Error: variable declaration is incorrect: ', string, 'is not a valid rule.')

    def get_digits(self, string):
        if string == '':
            return ''
        elif string == '0-9' or '0123456789':
            return '0$1$2$3$4$5$6$7$8$9'
        elif string == '0-8':
            return '0$1$2$3$4$5$6$7$8'
        elif string == '0-7':
            return '0$1$2$3$4$5$6$7'
        elif string == '0-6':
            return '0$1$2$3$4$5$6'
        elif string == '0-5':
            return '0$1$2$3$4$5'
        elif string == '0-4':
            return '0$1$2$3$4'
        elif string == '0-3':
            return '0$1$2$3'
        elif string == '0-2':
            return '0$1$2'
        elif string == '0-1':
            return '0$1'
        elif len(string) == 1:
            return string
        else:
            raise Exception(
                'Syntax Error: variable declaration is incorrect: ', string, 'is not a valid rule.')

    def simulate_input_file(self, input_file_path: str):
        with open(input_file_path, 'r') as input_file:
            input_string = input_file.read()

        # Definir las expresiones regulares para los tokens
        digit_pattern = re.compile(r'\d')
        float_pattern = re.compile(r'\d+\.\d+')
        hex_pattern = re.compile(r'0x[\dA-Fa-f]+')
        id_pattern = re.compile(r'[a-zA-Z]\w*')
        reserved_words = ['IF', 'THEN', 'ELSE']

        index = 0
        while index < len(input_string):
            char = input_string[index]

            if digit_pattern.match(input_string, index):
                m = digit_pattern.match(input_string, index)
                print("DIGITO", m.group())
                index += len(m.group())
            elif float_pattern.match(input_string, index):
                m = float_pattern.match(input_string, index)
                print("FLOAT", m.group())
                index += len(m.group())
            elif hex_pattern.match(input_string, index):
                m = hex_pattern.match(input_string, index)
                print("HEX", m.group())
                index += len(m.group())
            elif any(input_string.startswith(reserved_word, index) for reserved_word in reserved_words):
                for reserved_word in reserved_words:
                    if input_string.startswith(reserved_word, index):
                        print("Palabra reservada", reserved_word, "encontrada")
                        index += len(reserved_word)
                        break
            elif id_pattern.match(input_string, index):
                m = id_pattern.match(input_string, index)
                token = m.group()
                for letter in token:
                    print("LETTER", letter)
                index += len(token)
            else:
                print("CARACTER NO RECONOCIDO", char)
                index += 1


def clean_tokens(tokens: list):
    return [x for x in tokens if x is not None]


def add_prefix_to_states(nfa_dict, prefix):
    new_nfa_dict = {}
    for state, transitions in nfa_dict.items():
        new_state = f"{prefix}_{state}"
        new_transitions = {}
        for symbol, next_states in transitions.items():
            new_next_states = [
                f"{prefix}_{next_state}" for next_state in next_states]
            new_transitions[symbol] = new_next_states
        new_nfa_dict[new_state] = new_transitions
    return new_nfa_dict


def create_mega_nfa(nfa_list, nfas_info, start_state='q_-1'):
    mega_nfa = {start_state: {'ε': []}}
    for token, nfa_dict in zip(tokens, nfa_list):
        initial_state = nfas_info[token]['initial_state']
        for state, transitions in nfa_dict.items():
            mega_nfa[state] = transitions
            if state.endswith(initial_state):  # using the initial state from nfas_info
                mega_nfa[start_state]['ε'].append(state)
    return mega_nfa


def nfa_to_graphviz(nfa_dict, graph_name="MegaNFA"):
    dot = Digraph(graph_name)
    dot.attr(rankdir="LR")

    # Create all states
    for state in nfa_dict:
        if state == "q_-1":
            dot.attr("node", shape="circle", style="filled", color="lightgrey")
        else:
            dot.attr("node", shape="circle", style="")
        dot.node(state)

    # Create all transitions
    for state, transitions in nfa_dict.items():
        for symbol, next_states in transitions.items():
            for next_state in next_states:
                dot.edge(state, next_state, label=symbol)

    return dot


def simulate_nfa(mega_nfa, input_text):
    current_states = set(["q_-1"])
    steps = []

    for char in input_text:
        next_states = set()
        for state in current_states:
            if char in mega_nfa[state]:
                next_states.update(mega_nfa[state][char])

        steps.append((char, next_states))
        current_states = next_states

    return steps


def print_simulation(steps, nfas_info):
    for char, next_states in steps:
        matched = False

        for token, info in nfas_info.items():
            if any(state in next_states for state in info["acceptance_states"]):
                matched = True
                if token.startswith("DIGITO"):
                    print(f"{token} {char}")
                elif token.startswith("LETTER"):
                    print(f"{token} {char}")
                elif token.startswith("FLOAT"):
                    print(f"{token} {char}")
                break

        if not matched:
            for keyword, info in nfas_info.items():
                if keyword in {"IF", "THEN", "ELSE"} and all(state in next_states for state in info["acceptance_states"]):
                    print(f"Palabra reservada {keyword} encontrada")
                    matched = True
                    break

            if not matched:
                print(f"Error léxico: {char}")


# Ejemplo de uso:
yal = YAlexTokenizer('yalex_file.txt')
yal.get_tokens()
tokens = clean_tokens(yal.tokens)


# # Lee y simula el archivo de entrada
input_file_path = 'TEST.txt'
yal.simulate_input_file(input_file_path)
