# 计算理论导引

## Finate Automaton
A ***finite automaton*** is a 5-tuple (Q, Σ, δ, q0, F ), where
1. Q is a finite set called the states,
2. Σ is a finite set called the alphabet,
3. δ : Q × Σ−→ Q is the transition function
4. q0 ∈ Q is the start state, and
5. F ⊆ Q is the set of accept states

## Language

If **A** is the set of all strings that machine **M** accepts, we say that **A** is the ***language of machine*** **M** and write ***L(M ) = A***. We say that **M** recognizes **A** or that **M** accepts **A**

## Regular Language
A language is called a ***regular language*** if some finite automaton recognizes it.



## Nondeterministic Finite Automaton
A nondeterministic finite automaton is a 5-tuple (Q,Σ,δ,q0,F),
where
1. Q is a finite set of states,
2. Σ is a finite alphabet,
3. δ : Q × Σε −→ P (Q) is the transition function, 
4. q0 ∈ Q is the start state, and
5. F ⊆ Q is the set of accept states.