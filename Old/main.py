"""
Universidad del Valle de Guatemala
Jorge Caballeros Pérez
Laboratorio B 
"""
from Regex import *
from DirectDFA import *
from NFA import *
from Old.DFA import *

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
p2n.draw_nfa(nfa)
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
dfa_graph.render('./images/dfa', format='png', cleanup=True)

print("--------------------------Simulaciones--------------------------")
input_string = "bab"
is_accepted_nfa = nfa_to_dfa.simulacion_nfa(p2n.nfa_to_dict(nfa), p2n.get_start_state(nfa), p2n.get_final_state(nfa), p2n.get_accept_states(nfa), input_string)
print(f"Cadena '{input_string}' aceptada por el NFA: {is_accepted_nfa}")
is_accepted = nfa_to_dfa.simulacion_dfa(input_string)
print(f"Cadena '{input_string}' aceptada por el DFA: {is_accepted}")

print("----------------------------Direct DFA---------------------------")
r2afd = RegexToAFD(regex)
r2afd.finishedFunction()