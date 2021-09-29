from ply import lex
import ply.yacc as yacc
import matplotlib.pyplot as plt
import networkx as nx

tokens = (
    'VAR',
    'LPAREN',
    'RPAREN',
    'OPERATORS',
    'TRUE',
    'NOT',
    'FALSE',
    
)

t_ignore = ' \t'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_TRUE = r'1'
t_FALSE = r'0'
t_NOT = r'\~'
t_VAR = r'[p,q,r,s,t,u,v,w,x,y,z]+'
t_OPERATORS = r'\^|=>|<=>|o'
tupla = ()

def t_newline( t ):
  r'\n+'
  t.lexer.lineno += len( t.value )

def t_error( t ):
  print("Invalid Token:",t.value[0])
  t.lexer.skip( 1 )

lexer = lex.lex()


precedence = (
    ( 'left', 'OPERATORS'),
    ( 'nonassoc', 'NOT' )
)

def p_parens( p ) :
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error( p ):
    print("Syntax error in input!")

def p_operators(p):
  '''expr : expr OPERATORS expr'''
  p[0] = (p[2] , p[3] , p[1])

def p_expr2negated( p ) :
    ''' expr : NOT expr
    | NOT TRUE
    | NOT FALSE
    '''
    p[0] = (p[1], p[2])

def p_const(p):
    ''' expr : TRUE
        | FALSE
    '''
    p[0] = p[1]

def p_expr2VAR( p ) :
    'expr : VAR'
    p[0] = (p[1])

def plotGraph(g,res):
    res = list(res)
    if len(res) == 3:
        plotGraph(g, [res[0], res[1]])
        plotGraph(g, [res[0], res[2]])
    elif len(res) == 2:
        if (type(res[1]) == list) or (type(res[1]) == tuple):
            g.add_edge(res[0], list(res[1])[0])
            plotGraph(g, res[1])
        else:
            g.add_edge(res[0], res[1])
    if len(res) == 1:
        g.add_node(res[0])

text = input('Ingrese la expresion: ')
parser = yacc.yacc()
res = parser.parse(text)
print('RESULTADO: ', res)
g = nx.DiGraph()
plotGraph(g,res)
nx.draw(g , with_labels=True, arrows=True)
plt.show()