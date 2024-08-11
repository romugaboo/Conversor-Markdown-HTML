import ply.lex as lex
import ply.yacc as yacc
import re
import sys
from bs4 import BeautifulSoup as bs

# Definições do Lexer
tokens = ('CABECALHO', 'ITEM_LISTA', 'NEGRITO_ITALICO', 'NEGRITO', 'ITALICO',
          'LINK', 'PARAGRAFO')


def t_CABECALHO(t):
    r'\#{1,6}\s.*'
    t.value = ('CABECALHO', t.value)
    return t


def t_ITEM_LISTA(t):
    r'\-\s.*'
    t.value = ('ITEM_LISTA', t.value)
    return t


def t_NEGRITO_ITALICO(t):
    r'\*\*\*.*?\*\*\*'
    t.value = ('NEGRITO_ITALICO', t.value.strip('*'))
    return t


def t_NEGRITO(t):
    r'\*\*.*?\*\*'
    t.value = ('NEGRITO', t.value.strip('*'))
    return t


def t_ITALICO(t):
    r'\*.*?\*'
    t.value = ('ITALICO', t.value.strip('*'))
    return t


def t_LINK(t):
    r'\[.*?\]\(.*?\)'
    t.value = ('LINK', t.value)
    return t


def t_PARAGRAFO(t):
    r'[^#\-\*\[\]\n>].+'
    t.value = ('PARAGRAFO', t.value.strip())
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = '\t\n'


def t_error(t):
    print("Caractere ilegal: ", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()  # constrói o lexer


# Definições do Parser
def p_documento(p):
    'documento : corpo'
    p[0] = '<html><body>' + p[1] + '</body></html>'


def p_corpo(p):
    '''corpo : elementos'''
    p[0] = ''.join(p[1])


def p_elementos(p):
    '''elementos : elementos elemento
                 | elemento'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_elemento(p):
    '''elemento : T
                | L'''
    p[0] = p[1]


def p_T(p):
    '''T : cabecalho
         | negrito_italico
         | negrito
         | italico
         | link
         | paragrafo'''
    p[0] = p[1]


def p_cabecalho(p):
    'cabecalho : CABECALHO'
    nivel = p[1][1].count('#')
    texto = p[1][1][nivel:].strip()
    elementos = parse_elementos_inline(texto)
    p[0] = f'<h{nivel}>{"".join(elementos)}</h{nivel}>'


def p_negrito_italico(p):
    'negrito_italico : NEGRITO_ITALICO'
    p[0] = f'<strong><em>{p[1][1]}</em></strong>'


def p_negrito(p):
    'negrito : NEGRITO'
    p[0] = f'<strong>{p[1][1]}</strong>'


def p_italico(p):
    'italico : ITALICO'
    p[0] = f'<em>{p[1][1]}</em>'


def p_link(p):
    'link : LINK'
    match = re.match(r'\[(.*?)\]\((.*?)\)', p[1][1])
    texto = match.group(1)
    url = match.group(2)
    p[0] = f'<a href="{url}">{texto}</a>'


def p_paragrafo(p):
    'paragrafo : PARAGRAFO'
    elementos = parse_elementos_inline(p[1][1])
    p[0] = f'<p>{"".join(elementos)}</p>'


def p_L(p):
    '''L : lista'''
    p[0] = p[1]


def p_lista(p):
    '''lista : itens_lista'''
    p[0] = '<ul>' + ''.join(p[1]) + '</ul>'


def p_itens_lista(p):
    '''itens_lista : itens_lista item_lista
                   | item_lista'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_item_lista(p):
    'item_lista : ITEM_LISTA'
    texto = p[1][1][2:].strip()
    elementos = parse_elementos_inline(texto)
    p[0] = f'<li>{"".join(elementos)}</li>'


def parse_elementos_inline(texto):
    elementos = []
    padrao = r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*|\[.*?\]\(.*?\)|[^*[\]]+)'
    correspondencias = re.findall(padrao, texto)
    for correspondencia in correspondencias:
        if correspondencia.startswith('***'):
            elementos.append(
                f'<strong><em>{correspondencia.strip("*")}</em></strong>')
        elif correspondencia.startswith('**'):
            elementos.append(f'<strong>{correspondencia.strip("*")}</strong>')
        elif correspondencia.startswith('*'):
            elementos.append(f'<em>{correspondencia.strip("*")}</em>')
        elif correspondencia.startswith('['):
            correspondencia_link = re.match(r'\[(.*?)\]\((.*?)\)',
                                            correspondencia)
            elementos.append(
                f'<a href="{correspondencia_link.group(2)}">{correspondencia_link.group(1)}</a>'
            )
        else:
            elementos.append(correspondencia)
    return elementos


def p_error(p):
    print("Erro de sintaxe na entrada: ", p)


parser = yacc.yacc()  # constrói o parser

print(
    "Olá! Eu traduzo textos em markdown para HTML!\nInsira o texto em markdown a ser traduzido (pressione Ctrl+D ao terminar):\n"
)
texto_markdown = sys.stdin.read()

resultado = parser.parse(texto_markdown)  # executa o parser
resultado = bs(resultado, 'html.parser').prettify()

with open('output.html', 'w', encoding='utf-8') as arquivo:
    arquivo.write(resultado)
    print(
        '\n\nTradução para HTML realizada com sucesso.\nO resultado foi salvo em output.html\n'
    )
