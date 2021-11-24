#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * YES if word is recognized
 * NO if word is rejected
Determinises the automaton if it's non deterministic
"""

from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn
import sys
import pdb # for debugging

##################

def is_deterministic(a:Automaton)->bool:
  transitions = a.transitions
  length = len(transitions)
  n = 0
  test = 0
  while n > length - 1:
    currentTransition = transitions[n]
    nextTransition = transitions[n + 1]
    currentSymbole = currentTransition[1]
    nextSymbole = nextTransition[1]
    currentState = currentTransition[0]
    nextState = nextTransition[0]
    if currentState == nextState & currentSymbole == nextSymbole:  # si pour le meme etat de depart on a 2 fois le meme symbole il est non deterministe
      test = test + 1
    if currentSymbole == "%" | nextSymbole == "%":  # si un symbole de transition est epsilon il est non deterministe
      test = test + 1
    n = n + 1
  if test != 0:
    return False
  
##################
  
def recognizes(a:Automaton, word:str)->bool:
  wordLettres = list(word)
  wordLength = len(wordLettres)
  alphabet = a.alphabet
  finalstates = a.acceptstates
  states = a.states
  lengthAlphabet = len(wordLettres)
  while lengthAlphabet > 0:
    if not alphabet.__contains__(wordLettres[lengthAlphabet]):
      return False
      break
    lengthAlphabet = lengthAlphabet - 1
  transitions = a.transitions
  n = 0
  pointer = 0
  while pointer < wordLength:
    currentLetter = wordLettres[pointer]
    if transitions[n].__contains__(currentLetter):
      currentTransitions = transitions[n]
      n = currentTransitions[2]
      test = n
      while test > len(transitions):
        currentTransitions2 = transitions[test]
        if currentTransitions2[1].__contains__(n):
          n = n + test
        else:
          test = test + 1

    pointer = pointer + 1
    if finalstates.__contains__(n):
      return True
    else:
      n = n + 1
    if n > len(transitions):
      return False
  
##################

def determinise(a:Automaton):
  finalstates = a.acceptstates
  transitions = a.transitions
  numberOfTransitions = len(transitions)
  states = a.states
  alphabet = a.alphabet
  test = 0
  while test > numberOfTransitions:
    currentTransitions = transitions[test]
    state = currentTransitions[2]
    if currentTransitions.__contains__('%'):
        if  finalstates.__contains__(state):
            a.make_accept(currentTransitions[0])
        test2 = 0
        nextTransition = 0
        while test2 < nextTransition:
          currentTransitions2 = transitions[test2]
          if currentTransitions2[1] == state:
            nextTransition = currentTransitions2
          else:
            test2 = test2+1
        a.add_transition(currentTransitions[0],nextTransition[1],nextTransition[2])
        a.remove_transition(currentTransitions[0],currentTransitions[1],currentTransitions[2])
        a.remove_unreachable()
    test = test + 1
  if not is_deterministic(a):
    test = 0
    initialstates = list()
    initialstates.append(a.initial)
    while test > len(states):
      results =set()
      transitionsState = list()
      currentState = state[test]
      for i in transitions:
        if i[1] == currentState :
          transitionsState.append(i)
      test2 = 0
      while test2 > len(alphabet) :
        for i in transitionsState:
          if i[1] == alphabet[test2] :
            results.add(i[3])
        initialstates.append(results)
        test2 = test2 +1
      test = test +1







  else :
    pass

##################

if __name__ == "__main__" :
  if len(sys.argv) != 3:
    usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
    error(usagestring.format(sys.argv[0]))

  automatonfile = sys.argv[1]  
  word = sys.argv[2]

  a = Automaton("dummy")
  a.from_txtfile(automatonfile)
  if not is_deterministic(a) :
    determinise(a)
  if recognizes(a, word):
    print("YES")
  else:
    print("NO")
