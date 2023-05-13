from collections import deque
from NFA import *
from Regex import *
from graphviz import *



class NFAToDFA:
    def __init__(self, nfa_dict, start_state, final_state, accept_states):
        self.nfa_dict = nfa_dict
        self.start_state = start_state
        self.final_state = final_state
        self.accept_states = accept_states
        self.alphabet = self.get_alphabet()
        self.dfa_dict = self.construct_dfa()

    def get_alphabet(self):
        alphabet = set()
        for state_transitions in self.nfa_dict.values():
            for symbol in state_transitions.keys():
                if symbol != 'ε':
                    alphabet.add(symbol)
        return alphabet

    def epsilon_closure(self, states):
        closure = set(states)
        for state in states:
            if 'ε' in self.nfa_dict[state]:
                closure |= self.epsilon_closure(self.nfa_dict[state]['ε'])
        return closure

    def move(self, states, symbol):
        next_states = set()
        for state in states:
            if symbol in self.nfa_dict[state]:
                next_states |= set(self.nfa_dict[state][symbol])
        return next_states

    def construct_dfa(self):
        dfa_dict = {}
        start_closure = self.epsilon_closure([self.start_state])
        unmarked = deque([start_closure])
        marked = set()

        while unmarked:
            current = unmarked.popleft()
            marked.add(frozenset(current))

            for symbol in self.alphabet:
                next_closure = self.epsilon_closure(self.move(current, symbol))
                if not next_closure:
                    continue

                if frozenset(next_closure) not in marked:
                    unmarked.append(next_closure)

                current_label = ','.join(sorted(current))
                next_label = ','.join(sorted(next_closure))

                if current_label not in dfa_dict:
                    dfa_dict[current_label] = {}

                dfa_dict[current_label][symbol] = next_label

        return dfa_dict

    def get_dfa(self):
        return self.dfa_dict

    def draw_dfa(self):
        dot = Digraph()
        dot.graph_attr['rankdir'] = 'LR'
        dot.node_attr.update(shape='circle')

        for from_state, transitions in self.dfa_dict.items():
            for symbol, to_state in transitions.items():
                dot.edge(from_state, to_state, label=symbol)

        dot.node('qi', shape='point', label='', width='0')
        dot.edge('qi', ','.join(sorted(self.epsilon_closure([self.start_state]))))

        for state_label in self.dfa_dict:
            state_set = set(state_label.split(','))
            if state_set.intersection(self.accept_states):
                dot.node(state_label, shape='doublecircle')

        return dot
    
    def simulacion_dfa(self, input_string):
        current_state = ','.join(sorted(self.epsilon_closure([self.start_state])))
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if symbol in self.dfa_dict[current_state]:
                current_state = self.dfa_dict[current_state][symbol]
            else:
                return False

        state_set = set(current_state.split(','))
        return bool(state_set.intersection(self.accept_states))

    def simulacion_nfa(self, nfa_dict, start_state, final_state, accept_states, input_string):
        def dfs(state, index):
            if index == len(input_string):
                return state in accept_states

            if (state, index) in memo:
                return memo[(state, index)]

            if 'ε' in nfa_dict[state]:
                for next_state in nfa_dict[state]['ε']:
                    if dfs(next_state, index):
                        memo[(state, index)] = True
                        return True

            if input_string[index] in nfa_dict[state]:
                for next_state in nfa_dict[state][input_string[index]]:
                    if dfs(next_state, index + 1):
                        memo[(state, index)] = True
                        return True

            memo[(state, index)] = False
            return False

        memo = {}
        return dfs(start_state, 0)

    def minimize_dfa(self):
        def get_merged_states(partition):
            merged = set()
            for group in partition:
                merged |= group
            return frozenset(merged)

        def split(group, symbol, partition):
            target_sets = [g for g in partition if any(self.dfa_dict[state].get(symbol) == next_state for state in g for next_state in self.dfa_dict[state].values())]
            if not target_sets:
                return None
            return group.intersection(get_merged_states(target_sets))




        partitions = [set(self.dfa_dict.keys())]
        new_partitions = []

        while partitions != new_partitions:
            if new_partitions:
                partitions = new_partitions.copy()

            new_partitions = []
            for group in partitions:
                if len(group) == 1:
                    new_partitions.append(group)
                    continue

                split_group = set()
                for symbol in self.alphabet:
                    subgroup = split(group, symbol, partitions)
                    if subgroup:
                        split_group = subgroup
                        break

                if split_group:
                    new_partitions.append(split_group)
                    new_partitions.append(group.difference(split_group))
                else:
                    new_partitions.append(group)

        state_mapping = {}
        for group in new_partitions:
            new_state = ','.join(sorted(group))
            for state in group:
                state_mapping[state] = new_state

        minimized_dfa = {}
        for state, transitions in self.dfa_dict.items():
            new_state = state_mapping[state]
            if new_state not in minimized_dfa:
                minimized_dfa[new_state] = {}

            for symbol, next_state in transitions.items():
                minimized_dfa[new_state][symbol] = state_mapping[next_state]

        self.dfa_dict = minimized_dfa


if __name__ == "__main__":
    # Regex to Postfix
    print("-------------------------Regex to Postfix-------------------------")
    regex = "(a*|b*)$c"
    r2p = RegexToPostfix(regex)
    postfix = r2p.to_postfix()
    print("Postfix expression:", postfix)
    
    print("--------------------------Postfix to NFA--------------------------")
    p2n = PostfixToNFA(postfix)
    nfa = p2n.thompsons_algorithm()
    p2n.print_states(nfa)
    p2n.print_transition_table(nfa)
    # p2n.draw_nfa(nfa)
    print("NFA Dictionary:")
    print(p2n.nfa_to_dict(nfa))
    print("Start State:", p2n.get_start_state(nfa))
    print("Final State:", p2n.get_final_state(nfa))
    print("Accept States:", p2n.get_accept_states(nfa))
    
    print("--------------------------NFA to DFA--------------------------")
    nfa_to_dfa = NFAToDFA(p2n.nfa_to_dict(nfa), p2n.get_start_state(nfa), p2n.get_final_state(nfa), p2n.get_accept_states(nfa))
    dfa_dict = nfa_to_dfa.get_dfa()
    print("DFA Dictionary:")
    print(dfa_dict)
    dfa_graph = nfa_to_dfa.draw_dfa()
    dfa_graph.render('dfa', format='png', cleanup=True)
    
    print("--------------------------Simulaciones--------------------------")
    input_string = "bab"
    is_accepted_nfa = nfa_to_dfa.simulacion_nfa(p2n.nfa_to_dict(nfa), p2n.get_start_state(nfa), p2n.get_final_state(nfa), p2n.get_accept_states(nfa), input_string)
    print(f"Cadena '{input_string}' aceptada por el NFA: {is_accepted_nfa}")
    is_accepted = nfa_to_dfa.simulacion_dfa(input_string)
    print(f"Cadena '{input_string}' aceptada por el DFA: {is_accepted}")
    
    print("----------------------------Direct DFA---------------------------")
    r2afd = RegexToAFD(regex)
    r2afd.finishedFunction()

    
