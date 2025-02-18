
## WITH 1 LEVEL OF RECURSION
g1 = """
S -> A{1} B{2} // B{2} A{1}
A -> A{1} B{2} // B{2} A{1}
B -> b // d
A -> a // c
"""

## WITH 2 LEVELS OF RECURSION
g2 = """
S -> A{1} B{2} // B{2} A{1}

A -> A{1} B{2} // A{1} B{2}
A -> B{1} B{2} // B{1} B{2}

B -> A{1} A{2} // A{2} A{1}
B -> B{1} A{2} // B{1} A{2}

A -> a // e
A -> b // f
A -> a // g

B -> b // f
B -> a // e
"""

## WITH 3 LEVELS OF RECURSION
g3 = """
S -> A{1} B{2} // B{2} A{1}

A -> A{1} B{2} // A{1} B{2}
A -> C{1} C{2} // C{1} C{2}

B -> B{1} B{2} // B{2} B{1}
B -> B{1} A{2} // B{1} A{2}

C -> C{1} A{2} // A{2} C{1}
C -> A{1} B{2} // B{2} A{1}

A -> a // e
A -> b // f
A -> a // g

B -> b // f
B -> a // e

C -> c // g
C -> d // h
"""

## WITH 4 LEVELS OF RECURSION
g4 = """
S -> A{1} B{2} // B{2} A{1}

A -> A{1} B{2} // A{1} B{2}
A -> C{1} C{2} // C{1} C{2}

B -> B{1} D{2} // D{2} B{1}
B -> D{1} A{2} // D{1} A{2}

C -> C{1} D{2} // D{2} C{1}
C -> A{1} B{2} // B{2} A{1}

D -> C{1} A{2} // C{1} A{2}
D -> D{1} C{2} // D{1} C{2}

A -> a // e
A -> b // f
A -> a // g

B -> b // f
B -> a // e

C -> c // g
C -> d // h

D -> d // h
D -> c // g
"""

## WITH 5 LEVELS OF RECURSION
g5 = """
S -> A{1} B{2} // B{2} A{1}

A -> A{1} B{2} // A{1} B{2}
A -> C{1} F{2} // C{1} F{2}

B -> B{1} F{2} // F{2} B{1}
B -> D{1} A{2} // D{1} A{2}

C -> C{1} D{2} // D{2} C{1}
C -> F{1} B{2} // B{2} F{1}

D -> F{1} A{2} // F{1} A{2}
D -> D{1} C{2} // D{1} C{2}

F -> D{1} B{2} // B{2} D{1}
F -> F{1} C{2} // C{2} F{1}

A -> a // e
A -> b // f
A -> a // g

B -> b // f
B -> a // e

C -> c // g
C -> d // h

D -> d // h
D -> c // g

F -> c // g
F -> a // e
"""

