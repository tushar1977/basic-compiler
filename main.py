from lex import Lexer, TokenType


def main():
    source = '+-1239.8654*"This is comment"83848'
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()


main()
