
from re import M
from typing import Optional

from JackCompiler.src import enums
from JackCompiler.src import symbol_table as st

CLASS_VAR_DECS = ["field", "static",]
OPS = ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "=",]
SUBROUTINE_DECS = ["constructor", "function", "method",]
STATEMENT_DECS = ["let", "if", "while", "do", "return",]
UNARY_OPS = ["-", "~",]
KEYWORD_CONSTANTS = ["true", "false", "null", "this"]

MAP_SYMBOL_TO_OP = {
    "+": "add",
    "-": "sub",
    "*": "call Math.multiply 2",
    "/": "call Math.divide 2",
    "&lt;": "lt",
    "&gt;": "gt",
    "=": "eq",
    "&amp;": "and",
    "|": "or",
}
MAP_SYMBOL_TO_UNARY_OP = {
    "-": "neg",
    "~": "not",
}
MAP_KEYWORD_CONSTANT_TO_LINES = {
    "true": ["push constant 1\n", "neg\n"],
    "false": ["push constant 0\n"],
    "null": ["push constant 0\n"],
    "this": ["push pointer 0\n"],
}
MAP_KIND_TO_SEGMENT = {
    enums.SymbolKindEnum.STATIC: "static",
    enums.SymbolKindEnum.FIELD: "this",
    enums.SymbolKindEnum.VAR: "local",
    enums.SymbolKindEnum.ARG: "argument",
}

class ComplilationEngine:
    
    def __init__(self, input_strings: list[str], output_path: str) -> None:

        self.input_lines = input_strings
        self.destination = open(output_path, "w")
        self.class_table = st.SymbolTable()
        self.function_table = st.SymbolTable()
        self.class_name = None
        self.if_count = 0
        self.while_count = 0
        
    def compile_class(self) -> None:
        """
        'class' className '{' classVarDec* subroutineDec* '}'
        """
        # self._write_line("<class>\n")
        self._pop_next_input_line()
        # self._write_keyword_line() # class    

        class_name = self._pop_value_from_next_line()
        self.class_name = class_name
        # self._write_variable_info(
        #     class_name, 
        #     "declared", 
        #     category=enums.SymbolCategoryEnum.CLASS
        # )        
        # self._declare_variable("this", enums.SymbolKindEnum.FIELD, class_name)

        self._pop_next_input_line()  # "{"
        # self._write_symbol_line()  # "{"
        
        while self._get_value(self.input_lines[0]) in CLASS_VAR_DECS:
            self.compile_class_var_dec()

        while self._get_value(self.input_lines[0]) in SUBROUTINE_DECS:
            self.compile_subroutine()

        self._pop_next_input_line() # "}"
        # self._write_symbol_line()  # "}"
        # self._write_line("</class>\n")

    def compile_class_var_dec(self) -> None:
        """
        ('static'|'field') type varName (',' varName)* ';'
        """
        var_kind = enums.SymbolKindEnum[
            self._pop_value_from_next_line().upper()
        ]  # field or static
        var_type = self._pop_value_from_next_line()
        
        var_name = self._pop_value_from_next_line()

        self.class_table.define(var_name, var_type, var_kind)

        while "," in self.input_lines[0]:
            self._pop_next_input_line()  # ","
            var_name = self._pop_value_from_next_line()
            self.class_table.define(var_name, var_type, var_kind)

        self._pop_next_input_line()  # ";"

    def compile_subroutine(self) -> None:
        """
        ('constructor'|'function'|'method') ('void'|type) subroutineName '('
        parameterList ')' subroutineBody
        """
        self.function_table.reset()
        subroutine_kind = self._pop_value_from_next_line()
        if subroutine_kind == "method":
            self.function_table.define(
                "this", self.class_name, enums.SymbolKindEnum.ARG
            )

        self._pop_value_from_next_line()  # ('void'|type)
        
        if subroutine_kind == "method":
            _, _, class_name = self._determine_variable_attributes("this")
        else:
            class_name = self.class_name
    
        subroutine_name = self._pop_value_from_next_line()
        
        self._pop_next_input_line()  # "("
        self.compile_parameter_list()
        self._pop_next_input_line()  # ")"
        
        subroutine_definition = (
            f"function {class_name}.{subroutine_name}"
        )

        self.compile_subroutine_body(subroutine_definition, subroutine_kind)

    def compile_parameter_list(self) -> None:
        """
        ((type varName) (',' type varName)*)?
        """
        if self.input_lines and ")" not in self.input_lines[0]:
            arg_type = self._pop_value_from_next_line()
            arg_name = self._pop_value_from_next_line()
            self._declare_variable(arg_name, enums.SymbolKindEnum.ARG, arg_type)

        while self.input_lines and "," in self.input_lines[0]:
            self._pop_next_input_line()
            arg_type = self._pop_value_from_next_line()
            arg_name = self._pop_value_from_next_line()
            self._declare_variable(arg_name, enums.SymbolKindEnum.ARG, arg_type)

    def compile_subroutine_body(
        self, subroutine_definition: str, subroutine_kind: str
    ) -> None:
        """
        '{' varDec* statements '}'
        """
        self._pop_next_input_line()  # "{"

        var_count = 0
        while self.input_lines and "var" in self.input_lines[0]:
            var_count += self.compile_var_dec()
        
        self._write_line(f"{subroutine_definition} {var_count}\n")

        if subroutine_kind == "constructor":
            num_fields = 0
            for _ in range(len(self.class_table.rows)):
                num_fields += 1
            self._write_line(f"push constant {num_fields}\n")
            self._write_line("call Memory.alloc 1\n")
            self._write_line("pop pointer 0\n")
        elif subroutine_kind == "method":
            self._write_line("push argument 0\n")
            self._write_line("pop pointer 0\n")

        self.compile_statements()
        
        self._pop_next_input_line()  # "}"

    def compile_var_dec(self) -> None:
        """
        'var' type varName (',' varName)* ';'
        """
        self._pop_next_input_line()  # var
        
        var_count = 1
        type_ = self._pop_value_from_next_line()
        var_name = self._pop_value_from_next_line()

        self._declare_variable(var_name, enums.SymbolKindEnum.VAR, type_)

        while self.input_lines and "," in self.input_lines[0]:
            var_count += 1
            self._pop_next_input_line()  # ","
            var_name = self._pop_value_from_next_line()
            self._declare_variable(var_name, enums.SymbolKindEnum.VAR, type_)

        self._pop_next_input_line()  # ";"
        return var_count

    def compile_statements(self) -> None:
        """
        statement*
        """
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

    def compile_let(self) -> None:
        """
        'let' varName ('[' expression ']')? '=' expression ';'
        """
        self._pop_next_input_line()  # let

        var_name = self._pop_value_from_next_line()
        kind, index, _ = self._determine_variable_attributes(var_name)

        array = False
        if self._get_value(self.input_lines[0]) == "[":
            array = True
            self._write_line(f"push {MAP_KIND_TO_SEGMENT[kind]} {index}\n")
            self._pop_next_input_line()  # "["
            self.compile_expression()
            self._pop_next_input_line()  # "]"
            self._write_line("add\n")

        self._pop_value_from_next_line()  # "="            
        self.compile_expression()

        if array:
            self._write_line("pop temp 0\n")
            self._write_line("pop pointer 1\n")
            self._write_line("push temp 0\n")
            self._write_line("pop that 0\n")
        else:
            self._write_line(f"pop {MAP_KIND_TO_SEGMENT[kind]} {index}\n")
        self._pop_next_input_line()  # ";"

    def compile_if(self) -> None:
        """
        'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self._pop_next_input_line()  # if
        self._pop_next_input_line()  # "("
        self.compile_expression()
        self._pop_next_input_line() # ")"
        
        self.if_count += 1
        end_label = f"ENDIF{self.if_count}"
        else_label = f"ELSE{self.if_count}"

        self._write_line("not\n")
        self._write_line(f"if-goto {else_label}\n")
        self._pop_next_input_line() # "{"
        self.compile_statements()
        self._pop_next_input_line() # "}"
        self._write_line(f"goto {end_label}\n")

        self._write_line(f"label {else_label}\n"),
        
        if self.input_lines and "else" in self.input_lines[0]:
            self._pop_next_input_line() # else
            self._pop_next_input_line() # "{"
            self.compile_statements()
            self._pop_next_input_line() # "}"
        self._write_line(f"label {end_label}\n")

    def compile_while(self) -> None:
        """
        'while' '(' expression ')' '{' statements '}'
        """
        self.while_count += 1
        while_label = f"WHILE{self.while_count}"
        endwhile_label = f"ENDWHILE{self.while_count}"

        self._write_line(f"label {while_label}\n")

        self._pop_next_input_line()  # while
        self._pop_next_input_line()  # "("
        self.compile_expression()
        self._pop_next_input_line() # ")"

        self._write_line("not\n")
        self._write_line(f"if-goto {endwhile_label}\n")

        self._pop_next_input_line()  # "{"
        self.compile_statements()
        self._pop_next_input_line()  # "}"
        self._write_line(f"goto {while_label}\n")
        self._write_line(f"label {endwhile_label}\n")

    def compile_do(self) -> None:
        """
        'do' subroutineCall ';'
        """
        self._pop_next_input_line()  # "do"
        self.compile_expression()
        self._pop_next_input_line()  # ";"
        self.destination.write("pop temp 0\n")

    def compile_return(self) -> None:
        """
        'do' expression? ';'
        """
        pop_value_from_next_line(self.input_lines)  # "do"
        
        if self.input_lines and get_value(self.input_lines[0]) != ";":
            self.compile_expression()

        self._write_line("return\n")
        self._pop_value_from_next_line()  # ";"


    def compile_expression(self) -> None:
        """
        term (op term)
        """
        lines = self.code_write(self.input_lines)
        self.destination.writelines(lines)
        
    def compile_term(self) -> None:
        """
        term: 
        integerConstant | stringConstant | keywordConstant | varName |
        varName'['expression']'|'(' expression ')' | (unaryOp term) | subroutineCall
        """
        lines = self._code_write_term(self.input_lines)
        self.destination.writelines(lines)

    def compile_expression_list(self) -> int:
        """
        (expression (',' expression)*)?
        """
        lines, _ = self._code_write_expression_list(self.input_lines)
        self.destination.writelines(lines)

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
            else:
                category, index, _ = self._declare_variable(
                    name, category, type_
                )
        elif usage == "used":
            if category == enums.SymbolCategoryEnum.CLASS:
                index = None
            else:
                category, index, _ = self._determine_variable_attributes(name)
        else:
            raise NotImplementedError(
                f"Usage case: {usage} not implemented"
            )

        line = (
            f"name: {name}, category: {category.lower()}, index: {index},"
            f" usage: {usage}\n"
        )
        self._write_line(line)

    def _declare_variable(
            self, name: str, kind: enums.SymbolKindEnum, type_: str
        ) -> tuple[str, int, str]:
        """Receives the variable information, defines it in the appropriate
        class/function table and returns the kind, index and type_"""
        if kind in (
            enums.SymbolCategoryEnum.FIELD, enums.SymbolCategoryEnum.STATIC
        ):
            self.class_table.define(name, type_, kind)
            index = self.class_table.index_of(name)
        elif kind in (
            enums.SymbolCategoryEnum.ARG, enums.SymbolCategoryEnum.VAR
        ):
            self.function_table.define(name, type_, kind)
            index = self.function_table.index_of(name)
        else:
            raise ValueError(f"Can't handle kind: {kind}")
        
        return kind, index, type_

    def _determine_variable_attributes(self, name: str) -> tuple[
        Optional[str], Optional[int], Optional[str]
    ]:
        """Takes variable name, return kind/category, index and type"""
        category = index = type_ = None
        if self.function_table.rows.get(name):
            category = self.function_table.kind_of(name)
            index = self.function_table.index_of(name)
            type_ = self.function_table.type_of(name)
        elif self.class_table.rows.get(name):
            category = self.class_table.kind_of(name)
            index = self.class_table.index_of(name)
            type_ = self.class_table.type_of(name)
       
        return category, index, type_

    def code_write(self, lines: list[str]) -> list[str]:
        """
        term (op term)

        Turns an expression into code
        """
        output_lines = []

        output_lines.extend(self._code_write_term(lines))

        if lines and lines[0].split(" ")[1] in OPS:
            op = pop_value_from_next_line(lines)
            output_lines.extend(self._code_write_term(lines))
            output_lines.append(f"{MAP_SYMBOL_TO_OP[op]}\n")

        return output_lines

    def _code_write_term(self, lines: list[str]) -> list[str]:
        """
        Compiles a term
        """
        output_lines = []
        
        if (get_value(lines[0])) == "(":
            pop_next_line(lines)

            open_brackets = 1
            lines_in_expression = []
            
            while open_brackets > 0:
                next_line = pop_next_line(lines)
                if get_value(next_line) == "(":
                    open_brackets += 1
                elif get_value(next_line) == ")":
                    open_brackets -= 1
                lines_in_expression.append(next_line)

            # Pop the final bracket
            lines_in_expression.pop()

            if lines_in_expression:
                output_lines.extend(self.code_write(lines_in_expression))
        elif len(lines) > 1 and (get_value(lines[1])) == "[":
            kind, index, type_ = self._determine_variable_attributes(
                pop_value_from_next_line(lines)
            )
            if type_ != "Array":
                raise ValueError(
                    "Trying to index into something that is not an array"
                    f": type {type_}"
                )
            pop_value_from_next_line(lines)  # "["
            output_lines.append(f"push {MAP_KIND_TO_SEGMENT[kind]} {index}\n")

            open_brackets = 1
            lines_in_expression = []

            while open_brackets > 0:
                next_line = pop_next_line(lines)
                if get_value(next_line) == "[":
                    open_brackets += 1
                elif get_value(next_line) == "]":
                    open_brackets -= 1
                lines_in_expression.append(next_line)

            # pop the final bracket
            lines_in_expression.pop()

            if lines_in_expression:
                output_lines.extend(self.code_write(lines_in_expression))

            output_lines.append("add\n")
            output_lines.append("pop pointer 1\n")
            output_lines.append("push that 0\n")

        elif (
            len(lines) > 1
            and get_value(lines[0]).isalpha()
            and get_value(lines[1]) in ["(", "."]
        ):
            output_lines.extend(self._compile_subroutine_call(lines))
        elif get_value(lines[0]) in UNARY_OPS:
            op = pop_value_from_next_line(lines)
            output_lines.extend(self._code_write_term(lines))
            output_lines.append(f"{MAP_SYMBOL_TO_UNARY_OP[op]}\n")
        else:
            if "identifier" in lines[0]:
                var = pop_value_from_next_line(lines)

                if var == "this":
                    output_lines.append("push pointer 0\n")
                else:
                    kind, index, _ = self._determine_variable_attributes(var)
                    output_lines.append(
                        f"push {MAP_KIND_TO_SEGMENT[kind]} {index}\n"
                    )
            elif "string_const" in lines[0]:
                output_lines.extend(push_string(pop_value_from_next_line(lines)))
            elif "const" in lines[0]:  # NB that this will break if the line value contains "const"
                constant = pop_value_from_next_line(lines)
                output_lines.append(f"push constant {constant}\n")
            elif get_value(lines[0]) in KEYWORD_CONSTANTS:
                output_lines.extend(
                    MAP_KEYWORD_CONSTANT_TO_LINES[pop_value_from_next_line(lines)]
                )
            else:
                raise ValueError({lines[0]})

        return output_lines

    def _compile_subroutine_call(self, lines: list[str]) -> list[str]:
            # Functions are always called with a class name; methods are always
            # called from an initialised object (i.e., a varName); constructors
            # are always called as functions: they differ only in the internals

        output_lines = []
        n_args = 0

        if "." not in lines[1]:
            # method on current object
            method_name = pop_value_from_next_line(lines)
            output_lines.append(f"push pointer 0\n")
            n_args += 1
            subroutine_name = f"{self.class_name}.{method_name}"
        else:
            #  className | varName
            class_name = pop_value_from_next_line(lines)
            kind, index, type_ = self._determine_variable_attributes(class_name)
            
            if type_:  # method
                class_name = type_
                output_lines.append(f"push {MAP_KIND_TO_SEGMENT[kind]} {index}\n")
                n_args += 1
            
        if "." in lines[0]:
            pop_next_line(lines)
            method_name = pop_value_from_next_line(lines)
            subroutine_name = f"{class_name}.{method_name}"

        pop_next_line(lines)  # "("
        expressions, function_args = self._code_write_expression_list(lines)
        output_lines.extend(expressions)
        n_args += function_args
        pop_next_line(lines)  # ")"

        # Add one to nargs to indicate that we push this
        output_lines.append(f"call {subroutine_name} {n_args}\n")
        
        return output_lines

    def _code_write_expression_list(self, lines: list[str]) -> tuple[list[str], int]:
        """
        (expression (',' expression)*)?
        
        returns the compiled expressions and the number of arguments
        """
        output_lines = []

        n_args = 0

        while (lines and ")" not in lines[0]):
            if "," in lines[0]:
                pop_next_line(lines)
            n_args += 1
            output_lines.extend(self.code_write(lines))

        return output_lines, n_args


def push_string(string: str) -> list[str]:
    """Takes a string value as input and returns the list of commands needed
    to push the resulting string to the top of the stack"""
    output_lines = []
    
    output_lines.extend(
        [f"push constant {len(string)}\n", "call String.new 1\n"]
    )

    for char in string:
        output_lines.extend(
            [f"push constant {ord(char)}\n", "call String.appendChar 2\n"]
        )
        
    return output_lines


def pop_next_line(lines: list[str]) -> str:
    return lines.pop(0)


def pop_value_from_next_line(lines: list[str]) -> str:
    return get_value(lines.pop(0))


def get_value(line: str) -> str:
    start_index = line.find(">") + 1
    end_index = line.find("<", start_index)

    return line[start_index:end_index].strip()
