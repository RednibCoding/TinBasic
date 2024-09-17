##############################################################################
# CONSTANTS
##############################################################################
DIGITS = "0123456789"

##############################################################################
# ERRORS
##############################################################################
class Error:
    def __init__(self, name, pos_start, pos_end, desc):
        self.name = name
        self.desc = desc
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        result = f"ERROR: {self.pos_start.filename}:{self.pos_start.ln}:{self.pos_start.col}: {self.name}: {self.desc}"
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, desc):
        super().__init__("Illegal Character", pos_start, pos_end, desc)

##############################################################################
# Position
##############################################################################
class SrcPos:
    def __init__(self, idx, ln, col, filename, filetext):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.filename = filename
        self.filetext = filetext
    
    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0
        
        return self

    def copy(self):
        return SrcPos(self.idx, self.ln, self.col, self.filename, self.filetext)

##############################################################################
# TOKEN
##############################################################################

TYPE_INT = "INT"
TYPE_FLOAT = "FLOAT"
TYPE_PLUS = "PLUS"
TYPE_MINUS = "MINUS"
TYPE_MUL = "MUL"
TYPE_DIV = "DIV"
TYPE_LPAREN = "LPAREN"
TYPE_RPAREN = "RPAREN"

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        if self.value: return f"{self.type}:{self.value}"
        return f"{self.type}"
    
##############################################################################
# LEXER
##############################################################################

class Lexer:
    def __init__(self, filename, text):
        self.text = text
        self.filename = filename
        self.pos = SrcPos(-1, 1, 0, filename, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.current_char = None
        self.pos.advance(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
    
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Token(TYPE_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TYPE_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TYPE_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TYPE_DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TYPE_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TYPE_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")

        return tokens, None
    
    def make_number(self):
        num_str = ""
        has_dot = False

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if has_dot: break
                has_dot = True
                num_str += "."
            else:
                num_str += self.current_char
            
            self.advance()
        
        if has_dot:
            return Token(TYPE_FLOAT, float(num_str))

        return Token(TYPE_INT, int(num_str))


##############################################################################
# RUN
##############################################################################

def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, err = lexer.make_tokens()

    return tokens, err