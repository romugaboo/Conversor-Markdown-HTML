# Conversor de Markdown para HTML

Este projeto é um conversor de Markdown para HTML desenvolvido em Python, utilizando as bibliotecas PLY (Python Lex-Yacc) e BeautifulSoup. O conversor processa um texto em Markdown e o transforma em HTML, salvando o resultado em um arquivo chamado `output.html`.

## Requisitos

- Bibliotecas necessárias: `ply`, `beautifulsoup4`

Você pode instalar as dependências necessárias utilizando o seguinte comando:

```bash
pip install ply beautifulsoup4
```

## Como usar

1. Clone o repositório ou faça o download dos arquivos.
2. Navegue até o diretório do projeto.
3. Execute o script:

```bash
python main.py
```

4. Insira o texto em Markdown quando solicitado. Pressione `Ctrl+D` (ou `Ctrl+Z` no Windows) ao terminar.
5. O arquivo `output.html` será gerado com o resultado da conversão.

## Exemplo de Uso

Entrada Markdown:

```markdown
# Meu Título

- Item 1
- Item 2

Este é um texto com **negrito**, *itálico*, e ***negrito e itálico***.

Veja mais em [Python](https://www.python.org).
```

Saída HTML:

```html
<html>
  <body>
    <h1>Meu Título</h1>
    <ul>
      <li>Item 1</li>
      <li>Item 2</li>
    </ul>
    <p>
      Este é um texto com <strong>negrito</strong>,
      <em>itálico</em>, e
      <strong><em>negrito e itálico</em></strong>.
    </p>
    <p>Veja mais em <a href="https://www.python.org">Python</a>.</p>
  </body>
</html>
```
## Referências
Este projeto foi inspirado no repositório [Exemplo-Analisadore-Lexico-Python](https://github.com/MichaelTheFear/Exemplo-Analisadore-Lexico-Python) de [MichaelTheFear](https://github.com/MichaelTheFear).

## Autores

Este projeto foi desenvolvido por:

- **Larissa** - [GitHub: romugaboo](https://github.com/romugaboo)
- **Rafael** - [GitHub: Guaricaya](https://github.com/Guaricaya)