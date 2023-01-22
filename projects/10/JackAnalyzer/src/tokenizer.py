import typing

# from . import enums as enums
import enums

VALID_SYMBOLS = "{}()[].,;+-*/&|<>=~"



class Tokenizer:
    
    def __init__(self, path: str) -> None:
        self.input_lines = self._parse_input_lines(path)
        self.current_line: typing.Optional[list[str]] = None
        self.current_index = 0
        self.loaded_line = False  # Check we've actually tried to load a line

    def has_more_tokens(self) -> bool:
        """If there are lines remaining, then there are tokens remaining.
        except if we are in the final line and there are no more tokens"""
        if not self.input_lines:
            return False
            
        if len(self.input_lines) == 1 and self.loaded_line:
            return self._check_tokens_remaining()
        return True


    def advance(self) -> None:
        if not self.has_more_tokens():
            raise ValueError("No input lines remaining")

        # If the current line is empty
        if self.current_line is None and not self.loaded_line:
            line = self.input_lines.pop(0)
            self.loaded_line = True
        else:
            line = "".join(self.current_line)

        # Remove whitespace
        line = line.lstrip()
        # If the line is empty or the rest is a comment, load the next line
        if (
            line == ""
            or line.startswith(("//", "/*"))
        ):
            line = self.input_lines.pop(0)

        self.current_line = list(line)
        self.current_token = self._get_next_token()

    def token_type(self) -> enums.TokenTypeEnum:
        
        if enums.KeywordEnum.__members__.get(self.current_token.upper()):
            return enums.TokenTypeEnum.KEYWORD
        elif self.current_token in VALID_SYMBOLS:
            return enums.TokenTypeEnum.SYMBOL
        elif self.current_token[0].isalpha() or self.current_token[0] == "_":
            return enums.TokenTypeEnum.IDENTIFIER
        elif self.current_token[0] == "\"":
            return enums.TokenTypeEnum.STRING_CONST
        elif self.current_token[0].isnumeric():
            return enums.TokenTypeEnum.INT_CONST
        else:
            raise ValueError(f"Unhandled token {self.current_token}")        

    def keyword(self) -> enums.KeywordEnum:
        if self.token_type() != enums.TokenTypeEnum.KEYWORD:
            raise ValueError("Should only be called for KEYWORDS")
        return self.current_token

    def symbol(self) -> str:
        if self.token_type() != enums.TokenTypeEnum.SYMBOL:
            raise ValueError("Should only be called for SYMBOLS")

        if self.current_token == "<":
            return "&lt;"
        elif self.current_token == ">":
            return "&gt;"
        elif self.current_token == "\"":
            return "&quot;"
        elif self.current_token == "&":
            return "&amp;"
        else:
            return self.current_token

    def identifier(self) -> str:
        if self.token_type() != enums.TokenTypeEnum.IDENTIFIER:
            raise ValueError("Should only be called for IDENTIFIER")
        return self.current_token

    def int_val(self) -> int:
        if self.token_type() != enums.TokenTypeEnum.INT_CONST:
            raise ValueError("Should only be called for INT_CONSTS")
        return self.current_token

    def string_val(self) -> str:
        if self.token_type() != enums.TokenTypeEnum.STRING_CONST:
            raise ValueError("Should only be called for STRING_VALS")
        return self.current_token.replace("\"", "")
        
    def _parse_input_lines(self, path) -> list[str]:
        with open(path, "r") as f:
            lines = f.readlines()

        parsed_lines = []
        for line in lines:
            line = line.strip()
            # "* x" is an invalid expression, and multiline comments use "*"
            if (not line or line.startswith(("/", "*"))):
                continue
            parsed_lines.append(line)

        return parsed_lines

    def _check_tokens_remaining(self) -> bool:
        index = self.current_index

        if not self.current_line:
            return False

        while index < len(self.current_line):
            char = self.current_line[index]
            
            # We strip all lines, so this cannot be at the end of a line
            if char.isspace():
                index += 1
            elif char.isalnum():
                return True
            # If it's a comment, then there are no more tokens in the current
            # line
            elif char == "/" and self.current_line[index + 1] in ("/", "*"):
                return False
            else:
                return True
    
    def _get_next_token(self) -> str:
        """Find and return the next token in the current line"""
        token: list[str] = []
        string_opened = False

        if not self.current_line:
            raise ValueError("_get_next_token called with no current line")

        while self.current_index < len(self.current_line):
            current_char = self.current_line.pop(0)
            if current_char in VALID_SYMBOLS:
                return current_char
            elif current_char == '"':
                token.append("\"")
                if string_opened:
                    return "".join(token)
                else:
                    string_opened = True
            elif current_char.isprintable():
                token.append(current_char)
                if self._is_identifier_complete(string_opened):
                    return "".join(token)
            else:
                raise ValueError(f"Unhandled char {current_char}")

    def _is_identifier_complete(self, string_opened: bool):
        return not (
            string_opened 
            or (
                self.current_line 
                and (
                    self.current_line[0].isalnum()
                    or self.current_line[0] == "_"
                )
            )
        ) 
