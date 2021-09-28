import ply.lex as lex
import ply.yacc as yacc
import networkx as nx
import matplotlib.pyplot as plt

G = nx.MultiDiGraph()

toks = []
nodes = []
edges = []
tokens = (
    'PROPVAR',
    'PROPVAL',
    'NOT',
    'AND',
    'OR',
    'DOUBLEIMPLIES',
    'IMPLIES',
    'LPAREN',
    'RPAREN',
)

def t_PROPVAR(t):
    r'[p-z]+'
    return t

def t_PROPVAL(t):
    r'0|1+'
    t.value = int(t.value)
    return t

def t_NOT(t):
    r'~'
    return t

def t_AND(t):
    r'\^'
    return t

def t_OR(t):
    r'o'
    return t

def t_DOUBLEIMPLIES(t):
    r'<=>'
    return t

def t_IMPLIES(t):
    r'=>'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

testString = input("Porfavor ingrese una expresion para evaluar: \n")
lexer = lex.lex()
lexer.input(testString)

hasMoreTokens = True

print("Input: ", testString)

while hasMoreTokens:
    tok = lexer.token()
    if not tok:
        hasMoreTokens = False
    else:
        toks.append(tok)
        #print(tok)

for item in toks:
    if item.type == 'PROPVAR':
        if testString.find(item.value) > -1:
            truthVal = input("Ingrese el valor de verdad de "+ item.value + ": ")
            testString = testString.replace(item.value, truthVal)
        #print(testString)

precedence = (
    ('left', 'DOUBLEIMPLIES'),
    ('left', 'IMPLIES'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
)

def p_expression_doubleimp(p):
    'expression : expression DOUBLEIMPLIES expression'
    if (p[1] == 0 or p[1] == False) and (p[3] == 0 or p[3] == False):
        p[0] = 1
    elif (p[1] == 0 or p[1] == False) and (p[3] == 1 or p[3] == True):
        p[0] = 0
    elif (p[1] == 1 or p[1] == True) and (p[3] == 0 or p[3] == False):
        p[0] = 0
    elif (p[1] == 1 or p[1] == True) and (p[3] == 1 or p[3] == True):
        p[0] = 1

    initial = len(G.nodes)
    first = "Expression " + str(len(G.nodes))
    G.add_node(first)
    second = "Expression " + str(len(G.nodes))
    G.add_node(second)
    third = "<=> " + str(len(G.nodes))
    G.add_node(third)
    fourth = "Expression " + str(len(G.nodes))
    G.add_node(fourth)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Expression") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)
    G.add_edge(first, third)
    G.add_edge(first, fourth)

def p_expression_imp(p):
    'expression : expression IMPLIES expression'
    if (p[1] == 0 or p[1] == False) and (p[3] == 0 or p[3] == False):
        p[0] = 1
    elif (p[1] == 0 or p[1] == False) and (p[3] == 1 or p[3] == True):
        p[0] = 1
    elif (p[1] == 1 or p[1] == True) and (p[3] == 0 or p[3] == False):
        p[0] = 0
    elif (p[1] == 1 or p[1] == True) and (p[3] == 1 or p[3] == True):
        p[0] = 1

    initial = len(G.nodes)
    first = "Expression " + str(len(G.nodes))
    G.add_node(first)
    second = "Expression " + str(len(G.nodes))
    G.add_node(second)
    third = "=> " + str(len(G.nodes))
    G.add_node(third)
    fourth = "Expression " + str(len(G.nodes))
    G.add_node(fourth)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Expression") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)
    G.add_edge(first, third)
    G.add_edge(first, fourth)

def p_expression_or(p):
    'expression : expression OR term'
    p[0] = p[1] or p[3]

    initial = len(G.nodes)
    first = "Expression " + str(len(G.nodes))
    G.add_node(first)
    second = "Expression " + str(len(G.nodes))
    G.add_node(second)
    third = "o " + str(len(G.nodes))
    G.add_node(third)
    fourth = "Term " + str(len(G.nodes))
    G.add_node(fourth)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Expression") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)
    G.add_edge(first, third)
    G.add_edge(first, fourth)

def p_expression_and(p):
    'expression : expression AND term'
    p[0] = p[1] and p[3]

    initial = len(G.nodes)
    first = "Expression " + str(len(G.nodes))
    G.add_node(first)
    second = "Expression " + str(len(G.nodes))
    G.add_node(second)
    third = "^ " + str(len(G.nodes))
    G.add_node(third)
    fourth = "Term " + str(len(G.nodes))
    G.add_node(fourth)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Expression") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)
    G.add_edge(first, third)
    G.add_edge(first, fourth)

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

    initial = len(G.nodes)
    first = "Expression " + str(len(G.nodes))
    G.add_node(first)
    second = "Term " + str(len(G.nodes))
    G.add_node(second)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Expression") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)


def p_expression_not(p):
    'expression : NOT term'
    p[0] = not p[2]

    initial = len(G.nodes)
    first = "Expression " + str(len(G.nodes))
    G.add_node(first)
    second = "~ " + str(len(G.nodes))
    G.add_node(second)
    third = "Term " + str(len(G.nodes))
    G.add_node(third)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Expression") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)
    G.add_edge(first, third)

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

    initial = len(G.nodes)
    first = "Term " + str(len(G.nodes))
    G.add_node(first)
    second = "Factor " + str(len(G.nodes))
    G.add_node(second)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Expression") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)

#DEFAULT VALUE FOR LITERAL (this function should NOT be used)
def p_factor_propvar(p):
    'factor : PROPVAR'
    p[0] = 1

    initial = len(G.nodes)
    first = "Factor " + str(len(G.nodes))
    G.add_node(first)
    second = p[1] + str(len(G.nodes))
    G.add_node(second)

    if initial > 0:
        G.add_edge(list(G.nodes)[initial - 1], first)
    G.add_edge(first, second)

def p_factor_propval(p):
    'factor : PROPVAL'
    p[0] = p[1]

    initial = len(G.nodes)
    first = "Factor " + str(len(G.nodes))
    G.add_node(first)
    second = str(p[1]) + " " + str(len(G.nodes))
    G.add_node(second)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Term") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

    initial = len(G.nodes)
    first = "Factor " + str(len(G.nodes))
    G.add_node(first)
    second = "( " + str(len(G.nodes))
    G.add_node(second)
    third = "Expression " + str(len(G.nodes))
    G.add_node(third)
    fourth = ") " + str(len(G.nodes))
    G.add_node(fourth)

    if initial > 0:
        previous = list(G.nodes)
        for nod in previous:
            if nod.find("Term") > -1:
                G.add_edge(nod, first)
                break
    G.add_edge(first, second)
    G.add_edge(first, third)
    G.add_edge(first, fourth)

def p_error(p):
    #print("Error de sintaxis en la entrada.")
    a = 0

parser = yacc.yacc()

hasNotParsed = True

while hasNotParsed:
    try:
        s = testString
    except EOFError:
        hasNotParsed = False
    if not s: continue
    else:
        result = parser.parse(s)
        if result == 1 or result == True:
            print("Valor de verdad resultante: ", 1)
        elif result == 0 or result == False:
            print("Valor de verdad resultante: ", 0)
        hasNotParsed = False

#print(G.edges)

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()