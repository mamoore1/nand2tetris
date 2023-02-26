
from typing import Optional

# import enums as enums
from JackCompiler.src import enums
# import symbol_table as st
from JackCompiler.src import symbol_table as st

CLASS_VAR_DECS = ["field", "static",]
OPS = ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "=",]
SUBROUTINE_DECS = ["constructor", "function", "method",]
STATEMENT_DECS = ["let", "if", "while", "do", "return",]
UNARY_OPS = ["-", "~",]


class ComplilationEngine:
    
    def __init__(self, input_strings: list[str], output_path: str) -> None:

        self.input_lines = input_strings
        self.destination = open(output_path, "w")
        self.class_table = st.SymbolTable()
        self.function_table = st.SymbolTable()
        self.class_name = None
        
    def compile_class(self) -> None:
        """
        'class' className '{' classVarDec* subroutineDec* '}'
        """
        self._write_line("<class>\n")
        self._write_keyword_line() # class    

        class_name = self._pop_value_from_next_line()
        self.class_name = class_name
        self._write_variable_info(
            class_name, 
            "declared", 
            category=enums.SymbolCategoryEnum.CLASS
        )        

        self._write_symbol_line()  # "{"
        
        while self._get_value(self.input_lines[0]) in CLASS_VAR_DECS:
            self.compile_class_var_dec()

        while self._get_value(self.input_lines[0]) in SUBROUTINE_DECS:
            self.compile_subroutine()

        self._write_symbol_line()  # "}"
        self._write_line("</class>\n")

    def compile_class_var_dec(self) -> None:
        """
        ('static'|'field') type varName (',' varName)* ';'
        """
        self._write_line("<classVarDec>\n")
        var_category = enums.SymbolKindEnum[
            self._get_value(self.input_lines[0]).upper()
        ]
        self._write_keyword_line()  # field or static
        var_type = self._compile_type()
        self._write_variable_info(
             
            self._pop_value_from_next_line(), 
            "declared",
            var_category,
            var_type
        )

        while "," in self.input_lines[0]:
            self._write_symbol_line()  # ","
            self._write_variable_info(
                 
                self._pop_value_from_next_line(), 
                "declared", 
                var_category, 
                var_type
            )

        self._write_symbol_line()  # ";"
        self._write_line("</classVarDec>\n")


    def compile_subroutine(self) -> None:
        """
        ('constructor'|'function'|'method') ('void'|type) subroutineName '('
        parameterList ')' subroutineBody
        """
        self._write_line("<subroutineDec>\n")

        self._compile_type()  # (constructor|function|method)
        self._compile_type()  # ("void"|type)
        subroutine_name = self._pop_value_from_next_line()
        self._write_subroutine_info( subroutine_name, "declared")
        
        self._write_symbol_line()  # "("
        self.compile_parameter_list()
        self._write_symbol_line()  # ")"
        
        self.compile_subroutine_body()
        
        self._write_line("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """
        ((type varName) (',' type varName)*)?
        """
        self._write_line("<parameterList>\n")
        
        if self.input_lines and "keyword" in self.input_lines[0]:
            arg_type = self._get_value(self.input_lines[0])
            self._compile_type()  # param type
            arg_name = self._pop_value_from_next_line()
            self._write_variable_info(
                 
                arg_name, 
                "declared", 
                enums.SymbolCategoryEnum.ARG, 
                type_=enums.VarTypeEnum[arg_type.upper()]
            )

        while self.input_lines and "," in self.input_lines[0]:
            self._write_symbol_line()  # ","
            arg_type = self._get_value(self.input_lines[0])
            self._compile_type()  # param type
            arg_name = self._pop_value_from_next_line()
            self._write_variable_info(
                 
                arg_name, 
                "declared", 
                enums.SymbolCategoryEnum.ARG, 
                type_=enums.VarTypeEnum[arg_type.upper()]
            )

        self._write_line("</parameterList>\n")

    def compile_subroutine_body(self) -> None:
        """
        '{' varDec* statements '}'
        """
        self._write_line("<subroutineBody>\n")
        self._write_symbol_line()  # "{"

        while self.input_lines and "var" in self.input_lines[0]:
            self.compile_var_dec()
            
        self.compile_statements()
        self._write_symbol_line()  # "}"
        self._write_line("</subroutineBody>\n")

    def compile_var_dec(self) -> None:
        """
        'var' type varName (',' varName)* ';'
        """
        self._write_line("<varDec>\n")
        self._write_keyword_line() # var

        var_type = self._compile_type()
        var_name = self._pop_value_from_next_line()
        self._write_variable_info(
             
            var_name,
            "declared", 
            enums.SymbolCategoryEnum.VAR, 
            type_=var_type
        )

        while self.input_lines and "," in self.input_lines[0]:
            self._write_next_input_line()  # ","
            var_name = self._pop_value_from_next_line()
            self._write_variable_info(
                 
                var_name,
                "declared", 
                enums.SymbolCategoryEnum.VAR, 
                type_=enums.VarTypeEnum[var_type.upper()]
            )

        self._write_next_input_line()  # ";"
        self._write_line("</varDec>\n")

    def compile_statements(self) -> None:
        """
        statement*
        """
        self._write_line("<statements>\n")

        while (
            self.input_lines and self._get_value(self.input_lines[0]) in STATEMENT_DECS
        ):
            token = self.input_lines[0].split()[1]
            match token:
                case "let":
                    self.compile_let()
                case "if":
                    self.compile_if()
                case "while":
                    self.compile_while()
                case "do":
                    self.compile_do()
                case "return":
                    self.compile_return()
                case _:
                    raise ValueError(
                        f"Expected valid statement declaration, received {token}"
                    )

        self._write_line("</statements>\n")

    def compile_let(self) -> None:
        """
        'let' varName ('[' expression ']')? '=' expression ';'
        """
        self._write_line("<letStatement>\n")
        self._write_keyword_line()  # let

        self._write_variable_info(
             self._pop_value_from_next_line(), usage="used"
        )
        # self._write_next_input_line()  # varName

        if self._get_value(self.input_lines[0]) == "[":
            self._write_symbol_line()  # "["
            self.compile_expression()
            self._write_symbol_line()  # "]"
            
        self._write_symbol_line()  # "="
        self.compile_expression()
        self._write_symbol_line()  # ";"
        self._write_line("</letStatement>\n")

    def compile_if(self) -> None:
        """
        'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self._write_line("<ifStatement>\n")
        self._write_keyword_line()  # if
        self._write_symbol_line()  # "("
        self.compile_expression()
        self._write_symbol_line()  # ")"
        self._write_symbol_line()  # "{"
        self.compile_statements()
        self._write_symbol_line()  # "}"

        if self.input_lines and "else" in self.input_lines[0]:
            self._write_keyword_line()  # else
            self._write_symbol_line()  # "{"
            self.compile_statements()
            self._write_symbol_line()  # "}"

        self._write_line("</ifStatement>\n")

    def compile_while(self) -> None:
        """
        'while' '(' expression ')' '{' statements '}'
        """
        self._write_line("<whileStatement>\n")
        self._write_keyword_line()  # if
        self._write_symbol_line()  # "("
        self.compile_expression()
        self._write_symbol_line()  # ")"
        self._write_symbol_line()  # "{"
        self.compile_statements()
        self._write_symbol_line()  # "}"
        self._write_line("</whileStatement>\n")

    def compile_do(self) -> None:
        """
        'do' subroutineCall ';'
        """
        self._write_line("<doStatement>\n")
        self._write_keyword_line()  # do
        self.compile_subroutine_call()
        self._write_symbol_line()  # ";"
        self._write_line("</doStatement>\n")

    def compile_return(self) -> None:
        """
        'do' expression? ';'
        """
        self._write_line("<returnStatement>\n")
        self._write_keyword_line()  # return
        if "symbol" not in self.input_lines[0]:
            self.compile_expression()
        self._write_symbol_line()  # ";" 
        self._write_line("</returnStatement>\n")

    def compile_expression(self) -> None:
        """
        term (op term)
        """
        self._write_line("<expression>\n")
        self.compile_term()

        if self.input_lines and self.input_lines[0].split(" ")[1] in OPS:
            self._write_next_input_line()  # OP
            self.compile_term()

        self._write_line("</expression>\n")

    def compile_term(self) -> None:
        """
        term: 
        integerConstant | stringConstant | keywordConstant | varName |
        varName'['expression']'|'(' expression ')' | (unaryOp term) | subroutineCall
        """
        # Currently this assumes all terms will be single identifiers/keywords 
        # etc, and does not handle cases like arrays
        self._write_line("<term>\n")
        
        if (
            len(self.input_lines) > 1 
            and self._get_value(self.input_lines[0]).isalpha()
            and self._get_value(self.input_lines[1]) in ["(", "."]
        ):
            self.compile_subroutine_call()
        elif (
            len(self.input_lines) > 1
            and self._get_value(self.input_lines[0]).isalpha()
            and self._get_value(self.input_lines[1]) == "["
        ):
            self._write_next_input_line()  # varName
            self._write_symbol_line()  # "["
            self.compile_expression()
            self._write_symbol_line()  # "]"
        elif (
            self._get_value(self.input_lines[0]) == "("
        ):
            self._write_symbol_line()  # "("
            self.compile_expression()
            self._write_symbol_line()  # ")"
        elif self._get_value(self.input_lines[0]) in UNARY_OPS:
            self._write_next_input_line()  # UNARY OP
            self.compile_term()
        else:
            if "identifier" in self.input_lines[0]:
                term = self._pop_value_from_next_line()
                self._write_variable_info( term, "used")
            else:
                self._write_next_input_line()  # term
        self._write_line("</term>\n")

    def compile_expression_list(self) -> int:
        """
        (expression (',' expression)*)?
        """
        self._write_line("<expressionList>\n")

        while (
            self.input_lines 
            and ")" not in self.input_lines[0]
        ):
            if "," in self.input_lines[0]:            
                self._write_symbol_line()  # ","
            self.compile_expression()
        self._write_line("</expressionList>\n")

    def compile_subroutine_call(self) -> int:
        """
        The book claims you don't need this and should just handle this as part
        of "compile_term", but this is wrong; doSubroutine is handled without
        "expression" and "term" tags so this would fail the tests.

        subroutineCall:
        subroutineName'('expressionList')' | 
        (className|varName)'.'subroutineName'('expressionList')'
        """
        if  "." not in self.input_lines[1]:
            self._write_subroutine_info(
                self._pop_value_from_next_line(), "used"
            )  # subroutineName 
        else:
            # (className | varName)
            self._write_variable_info(
                
                self._pop_value_from_next_line(), 
                "used", 
                category=enums.SymbolCategoryEnum.CLASS
            )

        if "." in self.input_lines[0]:
            self._write_symbol_line()  # "."
            self._write_subroutine_info(
                self._pop_value_from_next_line(), "used"
            )  # subroutineName
        
        self._write_symbol_line()  # "("
        self.compile_expression_list()
        self._write_symbol_line()  # ")"

    def close(self):
        self.destination.close()

    def _compile_type(self) -> str:
        """Check whether the type is a Jack type or a custom type, write it to
        the output and return the type"""

        type_value = self._get_value(self.input_lines[0])

        if type_value in ("function", "void"):
            self._write_next_input_line()
            return type_value

        try: 
            type_value = enums.VarTypeEnum[type_value.upper()]
        except KeyError:
            # It's a class
            self._pop_next_input_line()
            self._write_variable_info(type_value, usage="used")
        else:
            self._write_next_input_line()

        return type_value

    def _write_keyword_line(self) -> None:
        if "keyword" not in (next_line := self.input_lines[0]):
            raise ValueError(f"Expected keyword, got {next_line}")
        self._write_next_input_line()

    def _write_symbol_line(self) -> None:
        if "symbol" not in (next_line := self.input_lines[0]):
            raise ValueError(f"Expected symbol, got {next_line}")
        
        self._write_next_input_line()

    def _write_next_input_line(self):
        line = self._pop_next_input_line()
        self._write_line(line)

    def _write_line(self, line: str):
        self.destination.write(line)

    def _pop_next_input_line(self):
        return self.input_lines.pop(0)

    def _pop_value_from_next_line(self) -> str:
        return self._get_value(self._pop_next_input_line())

    def _get_value(self, line: str) -> str:
        return line.split(" ")[1]

    def _write_subroutine_info(
        self, name: str, usage: str
    ) -> None:
        line = (
            f"name: {name}, category: subroutine, index: None, usage: {usage}\n"
        )
        self._write_line(line)
        
    def _write_variable_info(
        self, 
        name: str, 
        usage: str, 
        category: Optional[enums.SymbolCategoryEnum] = None,
        type_: Optional[enums.VarTypeEnum] = None
    ) -> None:
        if usage == "declared":
            if category == enums.SymbolCategoryEnum.CLASS:
                index = None
            elif category == enums.SymbolCategoryEnum.SUBROUTINE:
                index = None
            elif category in (
                enums.SymbolCategoryEnum.FIELD, enums.SymbolCategoryEnum.STATIC
            ):
                if not (category and type_):
                    raise ValueError(
                        "Defining a SymbolTable entry requires a category and a"
                        " type."
                    )
                self.class_table.define(
                    name, 
                    type_=type_, 
                    kind=enums.SymbolKindEnum[category]
                )
                index = self.class_table.index_of(name)
            elif category in (
                enums.SymbolCategoryEnum.ARG, enums.SymbolCategoryEnum.VAR
            ):
                if not (category and type_):
                    raise ValueError(
                        "Defining a SymbolTable entry requires a category and a"
                        " type."
                    )
                self.function_table.define(
                    name, 
                    type_=type_, 
                    kind=enums.SymbolKindEnum[category]
                )
                index = self.function_table.index_of(name)
            else:
                raise ValueError(
                    f"Couldn't figure out what to do with: {name} {usage}"
                    f" {category} {type_}"
                )
        elif usage == "used":
            if category == enums.SymbolCategoryEnum.CLASS:
                index = None
            elif self.function_table.rows.get(name):
                category = self.function_table.kind_of(name)
                index = self.function_table.index_of(name)
            elif self.class_table.rows.get(name):
                category = self.class_table.kind_of(name)
                index = self.class_table.index_of(name)
            else:
                category = "class"
                index = None
        else:
            raise NotImplementedError(
                f"Usage case: {usage} not implemented"
            )

        line = (
            f"name: {name}, category: {category.lower()}, index: {index},"
            f" usage: {usage}\n"
        )
        self._write_line(line)


def code_write(lines: list[str]) -> list[str]:

    output_lines = []

    map_symbol_to_op = {
        "+": "add",
        "-": "sub",
        "*": "Math.multiply",
        "/": "Math.divide",
    }
    map_symbol_to_unary_op = {
        "-": "neg",
        "!": "not",
    }

    if len(lines) >= 2 and get_value(lines[1]) in OPS:
        
        exp_1 = [pop_next_line(lines)]  # Needs to be a list to be passed to code_write
        op = pop_value_from_next_line(lines)
        exp_2 = lines

        output_lines.extend(code_write(exp_1))
        output_lines.extend(code_write(exp_2))

        output_lines.append(f"{map_symbol_to_op[op]}\n")
    elif (
        len(lines) > 2 
        and "identifier" in lines[0] 
        and get_value(lines[1]) == "("
    ):
        func = pop_value_from_next_line(lines)
        pop_next_line(lines)  # "("
        while ")" not in lines[0]:
            lines_to_parse = []
            while get_value(lines[0]) not in "),":
                lines_to_parse.append(pop_next_line(lines))
            output_lines.extend(code_write(lines_to_parse))
            if "," in lines[0]:
                pop_next_line(lines)

        output_lines.extend(f"call {func}\n")
    elif len(lines) >= 2 and get_value(lines[0]) in UNARY_OPS:
        op = pop_value_from_next_line(lines)
        
        output_lines.extend(code_write(pop_next_line(lines)))
        output_lines.extend(f"{map_symbol_to_unary_op[op]}\n")
    elif "identifier" in lines[0]:
        term = pop_value_from_next_line(lines)
        output_lines.append(f"push {term}\n")
    elif "const" in lines[0]:
        output_lines.extend(f"push {pop_value_from_next_line(lines)}\n")

    return output_lines


def pop_next_line(lines: list[str]) -> str:
    return lines.pop(0)


def pop_value_from_next_line(lines: list[str]) -> str:
    return get_value(lines.pop(0))


def get_value(line: str) -> str:
    return line.split(" ")[1]
