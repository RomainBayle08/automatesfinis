#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * ERROR if non deterministic
 * YES if word is recognized
 * NO if word is rejected
"""

from automaton import Automaton, EPSILON, error, warn
import sys
import pdb


##################

def is_deterministic(a: 'Automaton') -> bool:
    transitions = a.transitions
    length = len(transitions)
    n = 0
    test = 0
    while n > length-1:
        currentTransition = transitions[n]
        nextTransition = transitions[n+1]
        currentSymbole = currentTransition[1]
        nextSymbole = nextTransition[1]
        currentState = currentTransition[0]
        nextState = nextTransition[0]
        if currentState == nextState & currentSymbole == nextSymbole: #si pour le meme etat de depart on a 2 fois le meme symbole il est non deterministe
            test = test + 1
        if currentSymbole == "%" | nextSymbole == "%":#si un symbole de transition est epsilon il est non deterministe
            test = test + 1
        n = n + 1
    if test != 0:
        return False





##################

def recognizes(a: 'Automaton', word: str) -> bool:
    wordLettres = list(word)
    wordLength = len(wordLettres)
    alphabet = a.alphabet
    finalstates = a.acceptstates
    states = a.states
    lengthAlphabet = len(wordLettres)
    while lengthAlphabet> 0:
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
            pointer = pointer + 1
            if finalstates.__contains__(n):
                return True
        else:
            n = n+1
        if n > len(transitions):
            return False



##################

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
        error(usagestring.format(sys.argv[0]))

    automatonfile = sys.argv[1]
    word = sys.argv[2]

    a = Automaton("dummy")
    a.from_txtfile(automatonfile)

    if not is_deterministic(a):
        print("ERROR")
    elif recognizes(a, word):
        print("YES")
    else:
        print("NO")
