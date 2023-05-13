import graphviz
from collections import deque
from Regex import RegexToPostfix


class State:
    def __init__(self, label=None, arrow=None):
        self.label = label
        self.arrow = arrow if arrow else []


class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept


class PostfixToNFA:
    def __init__(self, postfix):
        self.postfix = postfix
        self.states_count = 0

    def new_state(self, label=None, arrow=None):
        self.states_count += 1
        return State("q{}".format(self.states_count), arrow)

    def thompsons_algorithm(self):
        stack = deque()

        for char in self.postfix:
            if char.isalnum() or char == 'ε' or char == '_':
                s1 = self.new_state()
                s2 = self.new_state()
                s1.arrow.append((char, s2))
                nfa = NFA(s1, s2)
                stack.append(nfa)
            elif char == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                s1 = self.new_state(
                    arrow=[('ε', nfa1.start), ('ε', nfa2.start)])
                s2 = self.new_state()
                nfa1.accept.arrow.append(('ε', s2))
                nfa2.accept.arrow.append(('ε', s2))
                nfa = NFA(s1, s2)
                stack.append(nfa)
            elif char == '$':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa1.accept.arrow.append(('ε', nfa2.start))
                nfa = NFA(nfa1.start, nfa2.accept)
                stack.append(nfa)
            elif char == '*':
                nfa1 = stack.pop()
                s1 = self.new_state(arrow=[('ε', nfa1.start)])
                s2 = self.new_state()
                nfa1.accept.arrow.append(('ε', s2))
                s1.arrow.append(('ε', s2))
                nfa = NFA(s1, nfa1.accept)
                stack.append(nfa)
            elif char == '?':
                nfa1 = stack.pop()
                s1 = self.new_state(arrow=[('ε', nfa1.start)])
                s2 = self.new_state()
                nfa1.accept.arrow.append(('ε', s2))
                s1.arrow.append(('ε', s2))
                nfa = NFA(s1, s2)
                stack.append(nfa)

        return stack.pop()

    def draw_nfa(self, nfa):
        graph = graphviz.Digraph(format='png', engine='dot')
        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['splines'] = 'polyline'

        visited = set()

        def visit(state):
            if state in visited:
                return
            visited.add(state)

            for label, next_state in state.arrow:
                graph.edge(state.label, next_state.label, label=label)
                visit(next_state)

        visit(nfa.start)
        graph.node(nfa.accept.label, shape='doublecircle')
        graph.render('./images/nfa', view=True)

    def print_states(self, nfa):
        print("Initial State:", nfa.start.label)
        print("Acceptance State:", nfa.accept.label)

        def visit(state, visited=None):
            if visited is None:
                visited = set()
            if state in visited:
                return
            visited.add(state)

            for label, next_state in state.arrow:
                visit(next_state, visited)

            return visited

        all_states = visit(nfa.start)
        non_accept_states = all_states - {nfa.start, nfa.accept}
        print("Non-Acceptance States:",
              ', '.join(s.label for s in non_accept_states))

    def get_all_states(self, nfa):
        visited = set()

        def visit(state):
            if state in visited:
                return
            visited.add(state)

            for label, next_state in state.arrow:
                visit(next_state)

            return visited

        return visit(nfa.start)

    def print_transition_table(self, nfa):
        all_states = self.get_all_states(nfa)
        symbols = {
            transition[0] for state in all_states for transition in state.arrow if transition[0] != 'ε'}

        print("NFA Transition Table:")
        print("State", end="\t")
        for symbol in sorted(symbols):
            print(symbol, end="\t")
        print("ε")

        for state in sorted(all_states, key=lambda s: int(s.label[1:])):
            print(state.label, end="\t")
            for symbol in sorted(symbols):
                next_states = [
                    arrow[1].label for arrow in state.arrow if arrow[0] == symbol]
                print(",".join(next_states) if next_states else "-", end="\t")
            epsilon_transitions = [
                arrow[1].label for arrow in state.arrow if arrow[0] == 'ε']
            print(",".join(epsilon_transitions)
                  if epsilon_transitions else "-")

    def nfa_to_dict(self, nfa):
        all_states = self.get_all_states(nfa)
        nfa_dict = {}

        for state in all_states:
            transitions = {}
            for symbol, next_state in state.arrow:
                if symbol not in transitions:
                    transitions[symbol] = []
                transitions[symbol].append(next_state.label)
            nfa_dict[state.label] = transitions

        return nfa_dict

    def get_start_state(self, nfa):
        return nfa.start.label

    def get_final_state(self, nfa):
        return nfa.accept.label

    def get_accept_states(self, nfa):
        return [nfa.accept.label]


if __name__ == "__main__":
    regex = "(a*|b*)$c"
    cadena = 'aabc'
    r2p = RegexToPostfix(regex)
    postfix = r2p.to_postfix()
    print("Postfix expression:", postfix)
    p2n = PostfixToNFA(postfix)
    nfa = p2n.thompsons_algorithm()
    p2n.print_states(nfa)
    p2n.print_transition_table(nfa)
    p2n.draw_nfa(nfa)
    print("NFA Dictionary:")
    print(p2n.nfa_to_dict(nfa))
    print("Start State:", p2n.get_start_state(nfa))
    print("Final State:", p2n.get_final_state(nfa))
    print("Accept States:", p2n.get_accept_states(nfa))
