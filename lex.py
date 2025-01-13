import enum
import sys


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Lexer:
    def __init__(self, source):
        self.source = source + "\n"
        self.currChar = ""
        self.currPos = -1
        self.nextChar()

    def nextChar(self):
        self.currPos += 1
        if self.currPos >= len(self.source):
            self.currChar = "\0"
        else:
            self.currChar = self.source[self.currPos]

    def peek(self):
        if self.currPos + 1 >= len(self.source):
            return "\0"
        return self.source[self.currPos + 1]

    def abort(self, message):
        sys.exit("Lexing error. " + message)

    def skipWhitespace(self):
        pass

    def skipComment(self):
        if self.currChar == "#":
            while self.currChar != "\n":
                self.nextChar()

    def getToken(self):
        self.skipWhitespace()
        self.skipComment()

        token = None
        match self.currChar:
            case "+":
                token = Token(self.currChar, TokenType.PLUS)
            case "-":
                token = Token(self.currChar, TokenType.MINUS)
            case "*":
                token = Token(self.currChar, TokenType.ASTERISK)
            case "/":
                token = Token(self.currChar, TokenType.SLASH)
            case "\n":
                token = Token(self.currChar, TokenType.NEWLINE)
            case "\0":
                token = Token("", TokenType.EOF)
            case "=":
                if self.peek() == "=":
                    lastChar = self.currChar
                    self.nextChar()
                    token = Token(lastChar + self.currChar, TokenType.EQEQ)
                else:
                    token = Token(self.currChar, TokenType.EQ)
            case ">":
                if self.peek() == "=":
                    lastChar = self.currChar
                    self.nextChar()
                    token = Token(lastChar + self.currChar, TokenType.GTEQ)
                else:
                    token = Token(self.currChar, TokenType.GT)
            case '"':
                self.nextChar()
                startpos = self.currPos

                while self.currPos != '"':
                    if (
                        self.currChar == "\r"
                        or self.currChar == "\n"
                        or self.currChar == "\t"
                        or self.currChar == "\\"
                        or self.currChar == "%"
                    ):
                        self.abort("Illegal character in string.")
                    self.nextChar()
                tokentxt = self.source[startpos : self.currPos]
                token = Token(tokentxt, TokenType.STRING)
            case _ if self.currChar.isdigit():
                startpos = self.currPos
                while self.peek().isdigit():
                    self.nextChar()
                if self.peek() == ".":
                    self.nextChar()

                    if not self.peek().isdigit():
                        self.abort("Illegal character is numer")
                    while self.peek().isdigit():
                        self.nextChar()
                toktext = self.source[startpos : self.currPos + 1]
                token = Token(toktext, TokenType.NUMBER)

            case _:
                self.abort("Unknown token: " + self.currChar)

        self.nextChar()
        return token


class Token:
    def __init__(self, tokenText, tokenKind) -> None:
        self.text = tokenText
        self.kind = tokenKind
