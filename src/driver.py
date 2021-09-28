import ply.lex as lex
import ply.yacc as yacc

toks = []
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

testString = "(p<=>~p)^(q=>r)"
#testString = "~(p=>q)"
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

def p_expression_or(p):
    'expression : expression OR term'
    p[0] = p[1] or p[3]

def p_expression_and(p):
    'expression : expression AND term'
    p[0] = p[1] and p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_expression_not(p):
    'expression : NOT term'
    p[0] = not p[2]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

#DEFAULT VALUE FOR LITERAL (this function should NOT be used)
def p_factor_propvar(p):
    'factor : PROPVAR'
    p[0] = 1

def p_factor_propval(p):
    'factor : PROPVAL'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Error de sintaxis en la entrada.")

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