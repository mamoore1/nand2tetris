
CLASS_VAR_DECS = ["field", "static",]
OPS = ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "=",]
SUBROUTINE_DECS = ["constructor", "function", "method",]
STATEMENT_DECS = ["let", "if", "while", "do", "return",]
UNARY_OPS = ["-", "~",]

class ComplilationEngine:
    
    def __init__(self, input_strings: list[str], output_path: str) -> None:

        self.input_lines = input_strings
        self.destination = open(output_path, "w")
        
    def compile_class(self, indent: int) -> None:
        """
        'class' className '{' classVarDec* subroutineDec* '}'
        """
        self._write_line(indent, "<class>\n")    
        self._write_next_input_line(indent + 1)  # class        
        self._write_next_input_line(indent + 1)  # class name
        self._write_next_input_line(indent + 1)  # "{"
        
        while self._get_value(self.input_lines[0]) in CLASS_VAR_DECS:
            self.compile_class_var_dec(indent + 1)

        while self._get_value(self.input_lines[0]) in SUBROUTINE_DECS:
            self.compile_subroutine(indent + 1)

        self._write_next_input_line(indent + 1)  # "}"
        self._write_line(indent, "</class>\n")

    def compile_class_var_dec(self, indent: int) -> None:
        """
        ('static'|'field') type varName (',' varName)* ';'
        """
        self._write_line(indent, "<classVarDec>\n")
        self._write_next_input_line(indent + 1)  # field or static
        self._write_next_input_line(indent + 1)  # var type
        self._write_next_input_line(indent + 1)  # var name

        while "," in self.input_lines[0]:
            self._write_next_input_line(indent + 1)  # symbol ","
            self._write_next_input_line(indent + 1)  # var name

        self._write_next_input_line(indent + 1)  # symbol ";"
        self._write_line(indent, "</classVarDec>\n")

    def compile_subroutine(self, indent: int) -> None:
        """
        ('constructor'|'function'|'method') ('void'|type) subroutineName '('
        parameterList ')' subroutineBody
        """
        self._write_line(indent, "<subroutineDec>\n")
        self._write_next_input_line(indent + 1)  # subroutine type
        self._write_next_input_line(indent + 1)  # return type
        self._write_next_input_line(indent + 1)  # subroutine name
        self._write_next_input_line(indent + 1)  # "("
        self.compile_parameter_list(indent + 1)
        self._write_next_input_line(indent + 1)  # ")"
        self.compile_subroutine_body(indent + 1)
        self._write_line(indent, "</subroutineDec>\n")

    def compile_parameter_list(self, indent: int) -> None:
        """
        ((type varName) (',' type varName)*)?
        """
        self._write_line(indent, "<parameterList>\n")
        
        if self.input_lines and "keyword" in self.input_lines[0]:
            self._write_next_input_line(indent + 1)  # param type
            self._write_next_input_line(indent + 1)  # param name

        while self.input_lines and "," in self.input_lines[0]:
            self._write_next_input_line(indent + 1)  # ","
            self._write_next_input_line(indent + 1)  # param type
            self._write_next_input_line(indent + 1)  # param name

        self._write_line(indent, "</parameterList>\n")

    def compile_subroutine_body(self, indent: int) -> None:
        """
        '{' varDec* statements '}'
        """
        self._write_line(indent, "<subroutineBody>\n")
        self._write_next_input_line(indent + 1)  # "{"

        while self.input_lines and "var" in self.input_lines[0]:
            self.compile_var_dec(indent + 1)
            
        self.compile_statements(indent + 1)
        self._write_next_input_line(indent + 1)  # "}"
        self._write_line(indent, "</subroutineBody>\n")

    def compile_var_dec(self, indent: int) -> None:
        """
        'var' type varName (',' varName)* ';'
        """
        self._write_line(indent, "<varDec>\n")
        self._write_next_input_line(indent + 1)  # var
        self._write_next_input_line(indent + 1)  # type
        self._write_next_input_line(indent + 1)  # identifier

        while self.input_lines and "," in self.input_lines[0]:
            self._write_next_input_line(indent + 1)  # ","
            self._write_next_input_line(indent + 1)  # identifier

        self._write_next_input_line(indent + 1)  # ";"
        self._write_line(indent, "</varDec>\n")

    def compile_statements(self, indent: int) -> None:
        """
        statement*
        """
        self._write_line(indent, "<statements>\n")


        while (
            self.input_lines and self._get_value(self.input_lines[0]) in STATEMENT_DECS
        ):
            token = self.input_lines[0].split()[1]
            match token:
                case "let":
                    self.compile_let(indent + 1)
                case "if":
                    self.compile_if(indent + 1)
                case "while":
                    self.compile_while(indent + 1)
                case "do":
                    self.compile_do(indent + 1)
                case "return":
                    self.compile_return(indent + 1)
                case _:
                    raise ValueError(
                        f"Expected valid statement declaration, received {token}"
                    )

        self._write_line(indent, "</statements>\n")

    def compile_let(self, indent: int) -> None:
        """
        'let' varName ('[' expression ']')? '=' expression ';'
        """
        self._write_line(indent, "<letStatement>\n")
        self._write_next_input_line(indent + 1)  # let
        self._write_next_input_line(indent + 1)  # varName

        if self._get_value(self.input_lines[0]) == "[":
            self._write_next_input_line(indent + 1)  # "["
            self.compile_expression(indent + 1)
            self._write_next_input_line(indent + 1)  # "]"
            
        self._write_next_input_line(indent + 1)  # "="
        self.compile_expression(indent + 1)
        self._write_next_input_line(indent + 1)  # ";"
        self._write_line(indent, "</letStatement>\n")

    def compile_if(self, indent: int) -> None:
        """
        'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self._write_line(indent, "<ifStatement>\n")
        self._write_next_input_line(indent + 1)  # if
        self._write_next_input_line(indent + 1)  # "("
        self.compile_expression(indent + 1)
        self._write_next_input_line(indent + 1)  # ")"
        self._write_next_input_line(indent + 1)  # "{"
        self.compile_statements(indent + 1)
        self._write_next_input_line(indent + 1)  # "}"

        if self.input_lines and "else" in self.input_lines[0]:
            self._write_next_input_line(indent + 1)  # else
            self._write_next_input_line(indent + 1)  # "{"
            self.compile_statements(indent + 1)
            self._write_next_input_line(indent + 1)  # "}"

        self._write_line(indent, "</ifStatement>\n")

    def compile_while(self, indent: int) -> None:
        """
        'while' '(' expression ')' '{' statements '}'
        """
        self._write_line(indent, "<whileStatement>\n")
        self._write_next_input_line(indent + 1)  # if
        self._write_next_input_line(indent + 1)  # "("
        self.compile_expression(indent + 1)
        self._write_next_input_line(indent + 1)  # ")"
        self._write_next_input_line(indent + 1)  # "{"
        self.compile_statements(indent + 1)
        self._write_next_input_line(indent + 1)  # "}"
        self._write_line(indent, "</whileStatement>\n")

    def compile_do(self, indent: int) -> None:
        """
        'do' subroutineCall ';'
        """
        self._write_line(indent, "<doStatement>\n")
        self._write_next_input_line(indent + 1)  # do
        self.compile_subroutine_call(indent + 1)
        self._write_next_input_line(indent + 1) # ";"
        self._write_line(indent, "</doStatement>\n")

    def compile_return(self, indent: int) -> None:
        """
        'do' expression? ';'
        """
        self._write_line(indent, "<returnStatement>\n")
        self._write_next_input_line(indent + 1)  # return
        if "symbol" not in self.input_lines[0]:
            self.compile_expression(indent + 1) 
        self._write_next_input_line(indent + 1)  # ;
        self._write_line(indent, "</returnStatement>\n")

    def compile_expression(self, indent: int) -> None:
        """
        term (op term)
        """
        self._write_line(indent, "<expression>\n")
        self.compile_term(indent + 1)

        if self.input_lines and self.input_lines[0].split(" ")[1] in OPS:
            self._write_next_input_line(indent + 1)  # OP
            self.compile_term(indent + 1)

        self._write_line(indent, "</expression>\n")

    def compile_term(self, indent: int) -> None:
        """
        term: 
        integerConstant | stringConstant | keywordConstant | varName |
        varName'['expression']'|'(' expression ')' | (unaryOp term) | subroutineCall
        """
        # Currently this assumes all terms will be single identifiers/keywords 
        # etc, and does not handle cases like arrays
        self._write_line(indent, "<term>\n")
        
        if (
            len(self.input_lines) > 1 
            and self._get_value(self.input_lines[0]).isalpha()
            and self._get_value(self.input_lines[1]) in ["(", "."]
        ):
            self.compile_subroutine_call(indent + 1)
        elif (
            len(self.input_lines) > 1
            and self._get_value(self.input_lines[0]).isalpha()
            and self._get_value(self.input_lines[1]) == "["
        ):
            self._write_next_input_line(indent + 1)  # varName
            self._write_next_input_line(indent + 1)  # "["
            self.compile_expression(indent + 1)
            self._write_next_input_line(indent + 1)  # "]"
        elif (
            self._get_value(self.input_lines[0]) == "("
        ):
            self._write_next_input_line(indent + 1)  # "("
            self.compile_expression(indent + 1)
            self._write_next_input_line(indent + 1)  # ")" 
        elif self._get_value(self.input_lines[0]) in UNARY_OPS:
            self._write_next_input_line(indent + 1)  # UNARY OP
            self.compile_term(indent + 1)
        else:
            self._write_next_input_line(indent + 1)  # term
        self._write_line(indent, "</term>\n")

    def compile_expression_list(self, indent: int) -> int:
        """
        (expression (',' expression)*)?
        """
        self._write_line(indent, "<expressionList>\n")

        while (
            self.input_lines 
            and ")" not in self.input_lines[0]
        ):
            if "," in self.input_lines[0]:
                self._write_next_input_line(indent + 1)
            self.compile_expression(indent + 1)
        self._write_line(indent, "</expressionList>\n")

    def compile_subroutine_call(self, indent: int) -> int:
        """
        The book claims you don't need this and should just handle this as part
        of "compile_term", but this is wrong; doSubroutine is handled without
        "expression" and "term" tags so this would fail the tests.

        subroutineCall:
        subroutineName'('expressionList')' | 
        (className|varName)'.'subroutineName'('expressionList')'
        """
        self._write_next_input_line(indent)  # subroutineName
        

        if "." in self.input_lines[0]:
            self._write_next_input_line(indent)  # "."
            self._write_next_input_line(indent)  # className | varName
        
        self._write_next_input_line(indent)  # (
        self.compile_expression_list(indent)
        self._write_next_input_line(indent)  # )

    def close(self):
        self.destination.close()

    def _write_line(self, indent: int, line: str):
        spaces = ["  " for _ in range(indent)]
        self.destination.write("".join(spaces) + line)

    def _pop_next_input_line(self):
        return self.input_lines.pop(0)

    def _write_next_input_line(self, indent: int):
        line = self._pop_next_input_line()
        self._write_line(indent, line)


    def _get_value(self, line: str) -> str:
        return line.split(" ")[1]
