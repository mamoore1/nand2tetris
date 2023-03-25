import typing as t
from io import StringIO
from unittest import mock

import pytest

import JackCompiler.src.compilation_engine as ce
import JackCompiler.src.symbol_table as st
from JackCompiler.src import enums


CLASS_NAME = "Test"


@pytest.fixture
def engine():
    
    def mock_init(self):
        self.input_lines = []
        self.destination = StringIO()
        self.class_table = st.SymbolTable()
        self.function_table = st.SymbolTable()
        self.class_name = CLASS_NAME
        self.if_count = 0
        self.while_count = 0

    with mock.patch.object(ce.ComplilationEngine, "__init__", mock_init):
        compilation_engine = ce.ComplilationEngine()
        yield compilation_engine
        compilation_engine.destination.close()


@pytest.mark.parametrize(
    "input_lines,expected,symbols,defined_symbols", [
        (
            [
                "<keyword> class </keyword>\n",
                f"<identifier> {CLASS_NAME} </identifier>\n",
                "<symbol> { </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
            ],
            [],
            {
            },
        ),
        (
            [
                "<keyword> class </keyword>\n",
                f"<identifier> {CLASS_NAME} </identifier>\n",
                "<symbol> { </symbol>\n",
                "<keyword> function </keyword>\n",
                "<keyword> void </void>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> input </identifier>\n",
                "<symbol> , </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> output </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "function Test.draw 1\n",
                "push constant 3\n",
                "pop local 0\n",
            ],
            [],
            {
                "input": {
                    "kind": enums.SymbolKindEnum.ARG,
                    "type_": "int",
                    "index": 0
                },
                "output": {
                    "kind": enums.SymbolKindEnum.ARG,
                    "type_": "int",
                    "index": 1,
                },
                "x": {
                    "kind": enums.SymbolKindEnum.VAR,
                    "type_": "int",
                    "index": 0,
                }
            },
        ),
        # (
        #     [
        #         "<keyword> class </keyword>\n",
        #         f"<identifier> {CLASS_NAME} </identifier>\n",
        #         "<symbol> { </symbol>\n",
        #         "<keyword> static </keyword>\n",
        #         "<keyword> int </keyword>\n",
        #         "<identifier> abc </identifier>\n",
        #         "<symbol> , </symbol>\n",
        #         "<identifier> xyz </identifier>\n",
        #         "<symbol> ; </symbol>\n",
        #         "<keyword> function </keyword>\n",
        #         "<keyword> void </void>\n",
        #         "<identifier> draw </identifier>\n",
        #         "<symbol> ( </symbol>\n",
        #         "<keyword> int </keyword>\n",
        #         "<identifier> input </identifier>\n",
        #         "<symbol> , </symbol>\n",
        #         "<keyword> int </keyword>\n",
        #         "<identifier> output </identifier>\n",
        #         "<symbol> ) </symbol>\n",
        #         "<symbol> { </symbol>\n",
        #         "<keyword> let </keyword>\n",
        #         "<identifier> x </identifier>\n",
        #         "<symbol> = </symbol>\n",
        #         "<int_constant> 3 </int_constant>\n",
        #         "<symbol> ; </symbol>\n",
        #         "<symbol> } </symbol>\n",
        #         "<symbol> } </symbol>\n",
        #     ],
        #     [

        #     ],
        #     [],
        #     {
        #         "this": {
        #             "kind": enums.SymbolKindEnum.FIELD, 
        #             "type_": CLASS_NAME,
        #             "index": 0,
        #         },
        #         "input": {
        #             "kind": enums.SymbolKindEnum.ARG,
        #             "type_": "int",
        #             "index": 0
        #         },
        #         "output": {
        #             "kind": enums.SymbolKindEnum.ARG,
        #             "type_": "int",
        #             "index": 1,
        #         },
        #         "x": {
        #             "kind": enums.SymbolKindEnum.VAR,
        #             "type_": "int",
        #             "index": 0,
        #         }
        #     },
        # ),
    ]
)
def test_compile_class(
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict[str, str]],
    defined_symbols: dict[str, dict[str, t.Any]], 
    engine: ce.ComplilationEngine
):

    # for symbol in symbols:
    #     engine.function_table.define(
    #         symbol["name"], symbol["type_"], symbol["category"]
    #     )

    engine.input_lines = input_lines
    engine.compile_class()

    assert "".join(expected) ==  engine.destination.getvalue()
    
    for symbol, attributes in defined_symbols.items():
        table = engine.function_table
        if attributes["kind"] in (
            enums.SymbolKindEnum.FIELD, enums.SymbolKindEnum.STATIC
        ):
            table = engine.class_table

        assert attributes["kind"] == table.kind_of(symbol)
        assert attributes["type_"] == table.type_of(symbol)
        assert attributes["index"] == table.index_of(symbol)
    

@pytest.mark.parametrize(
    "input_lines,expected,defined_symbols", [
        (
            [
                "<keyword> field </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> xyz </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [],
            {"xyz": {"type_": "int", "kind": enums.SymbolKindEnum.FIELD, "index": 1}},
        ),
        (
            [
                "<keyword> field </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> abc </identifier>\n",
                "<symbol> , </symbol>\n",
                "<identifier> xyz </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [],
            {
                "abc": {"type_": "int", "kind": enums.SymbolKindEnum.FIELD, "index": 1},
                "xyz": {"type_": "int", "kind": enums.SymbolKindEnum.FIELD, "index": 2}
            },
        ),
        (
            [
                "<keyword> field </keyword>\n",
                "<identifier> Square </identifier>\n",
                "<identifier> square </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [],
            {"square": {"type_": "Square", "kind": enums.SymbolKindEnum.FIELD, "index": 1}},

        ),
        # TODO: reinstate static tests
        # (
        #     [
        #         "<keyword> static </keyword>\n",
        #         "<keyword> int </keyword>\n",
        #         "<identifier> xyz </identifier>\n",
        #         "<symbol> ; </symbol>\n",
        #     ],
        #     [
        #         "<classVarDec>\n",
        #         "<keyword> static </keyword>\n",
        #         "<keyword> int </keyword>\n",
        #         "name: xyz, category: static, index: 0, usage: declared\n",
        #         "<symbol> ; </symbol>\n",
        #         "</classVarDec>\n",
        #     ],
        # ),
        # (
        #     [
        #         "<keyword> static </keyword>\n",
        #         "<keyword> int </keyword>\n",
        #         "<identifier> abc </identifier>\n",
        #         "<symbol> , </symbol>\n",
        #         "<identifier> xyz </identifier>\n",
        #         "<symbol> ; </symbol>\n",
        #     ],
        #     [
        #         "<classVarDec>\n",
        #         "<keyword> static </keyword>\n",
        #         "<keyword> int </keyword>\n",
        #         "name: abc, category: static, index: 0, usage: declared\n",
        #         "<symbol> , </symbol>\n",
        #         "name: xyz, category: static, index: 1, usage: declared\n",
        #         "<symbol> ; </symbol>\n",
        #         "</classVarDec>\n",
        #     ]
        # ),
        # (
        #     [
        #         "<keyword> static </keyword>\n",
        #         "<identifier> Square </identifier>\n",
        #         "<identifier> square </identifier>\n",
        #         "<symbol> ; </symbol>\n",
        #     ],
        #     [
        #         "<classVarDec>\n",
        #         "<keyword> static </keyword>\n",
        #         "name: Square, category: class, index: None, usage: used\n",
        #         "name: square, category: static, index: 0, usage: declared\n",
        #         "<symbol> ; </symbol>\n",
        #         "</classVarDec>\n",
        #     ]
        # )
    ]
)
def test_compile_class_var_dec(
    input_lines: list[str], 
    expected: list[str],
    defined_symbols: dict[str, dict[str, t.Any]], 
    engine: ce.ComplilationEngine,
):
    defined_symbols["this"] = {
        "type_": "Test", "kind": enums.SymbolKindEnum.FIELD, "index": 0
    }
    engine.input_lines = input_lines
  
    # NB. a class will always have its own type as this 0 (called "this")
    engine.class_table.define("this", "Test", enums.SymbolKindEnum.FIELD)
    engine.compile_class_var_dec()

    table = engine.class_table

    assert "".join(expected) == engine.destination.getvalue()
    for name, attributes in defined_symbols.items():
        assert attributes["type_"] == table.type_of(name)
        assert attributes["kind"] == table.kind_of(name)
        assert attributes["index"] == table.index_of(name)


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> function </keyword>\n",
                "<keyword> void </void>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> return </keyword>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            # 0 here indicates the number of local args
            ["function Test.draw 0\n", "return\n"],
            [
                {
                    "name": "this", 
                    "type_": "Test", 
                    "category": enums.SymbolKindEnum.FIELD
                }
            ],
        ),
        (
            [
                "<keyword> function </keyword>\n",
                "<keyword> void </void>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> input </identifier>\n",
                "<symbol> , </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> output </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> return </keyword>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "function Test.draw 0\n",
                "return\n",
            ],
            [
                {
                    "name": "this", 
                    "type_": "Test", 
                    "category": enums.SymbolKindEnum.FIELD
                }
            ],
        ),
        (
            [
                "<keyword> function </keyword>\n",
                "<keyword> void </void>\n",
                "<identifier> fillMemory </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> startAddress </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> , </symbol>\n",
                "<identifier> y </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> return </keyword>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "function Test.fillMemory 2\n",
                "return\n",
            ],
            [
                {
                    "name": "this", 
                    "type_": "Test", 
                    "category": enums.SymbolKindEnum.FIELD
                }
            ],
        ),
        (
            [
                "<keyword> function </keyword>\n",
                "<keyword> void </void>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> input </identifier>\n",
                "<symbol> , </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> output </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> var </keyword>\n",
                "<identifier> Square </identifier>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> do </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> . </symbol\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "function Test.draw 1\n",
                "push local 0\n",
                "call Square.draw 1\n",
                "pop temp 0\n",
            ],
            [
                {
                    "name": "this", 
                    "type_": "Test", 
                    "category": enums.SymbolKindEnum.FIELD
                }
            ],
        ),
        (
            [
                "<keyword> function </keyword>\n",
                "<keyword> void </void>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> input </identifier>\n",
                "<symbol> , </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> output </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "function Test.draw 1\n",
                "push constant 3\n",
                "pop local 0\n",
            ],
            [
                {
                    "name": "this", 
                    "type_": "Test", 
                    "category": enums.SymbolKindEnum.FIELD
                }
            ],
        ),
    ]
)
def test_compile_subroutine(
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict[str, str]], 
    engine: ce.ComplilationEngine,
):
    for symbol in symbols:
        if symbol["category"] in (
            enums.SymbolKindEnum.FIELD, enums.SymbolKindEnum.STATIC
        ):
            engine.class_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )
            
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )

    engine.input_lines = input_lines
    engine.compile_subroutine()

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> constructor </keyword>\n",
                f"<identifier> {CLASS_NAME} </identifier>\n",
                "<identifier> new </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> ax </identifier>\n",
                "<symbol> , </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> ay </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> let </keyword>\n",    
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<identifier> ax </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> let </keyword>\n",    
                "<identifier> y </identifier>\n",
                "<symbol> = </symbol>\n",
                "<identifier> ay </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> return </keyword>\n",    
                "<identifier> this </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                f"function {CLASS_NAME}.new 0\n",
                "push constant 2\n",
                "call Memory.alloc 1\n",
                "pop pointer 0\n",
                "push argument 0\n",
                "pop this 0\n",
                "push argument 1\n",
                "pop this 1\n",
                "push pointer 0\n",
                "return\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": "int", 
                    "category": enums.SymbolKindEnum.FIELD
                },
                {
                    "name": "y", 
                    "type_": "int", 
                    "category": enums.SymbolKindEnum.FIELD
                },
            ],
        )
    ]
)
def test_compile_subroutine_constructor(
    input_lines: list[str], 
    expected: list[str], 
    symbols: list[dict[str, str]],
    engine: ce.ComplilationEngine,
):
    """Compile a constructor (separated this out from compile_subroutine for 
    clarity)"""
    for symbol in symbols:
        if symbol["category"] in (
            enums.SymbolKindEnum.FIELD, enums.SymbolKindEnum.STATIC
        ):
            engine.class_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )
            
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )

    engine.input_lines = input_lines
    engine.compile_subroutine()

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> method </keyword>\n",
                "<identifier> int </identifier>\n",
                "<identifier> distance </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<identifier> Point </identifier>\n",
                "<identifier> other </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> var </keyword>\n",    
                "<keyword> int </keyword>\n",    
                "<identifier> dx </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> let </keyword>\n",    
                "<identifier> dx </identifier>\n",
                "<symbol> = </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> - </symbol>\n",
                "<identifier> other </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> getx </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> return </keyword>\n",    
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "function Point.distance 1\n",
                "push argument 0\n",
                "pop pointer 0\n",
                "push this 0\n",
                "push argument 1\n"
                "call Point.getx 1\n",
                "sub\n",
                "pop local 0\n",
                "return\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": "int", 
                    "category": enums.SymbolKindEnum.FIELD
                },
            ],
        )
    ]
)
def test_compile_subroutine_method(
    input_lines: list[str], 
    expected: list[str], 
    symbols: list[dict[str, str]],
    engine: ce.ComplilationEngine,
):
    """Compile a method (separated this out from compile_subroutine for 
    clarity)"""
    for symbol in symbols:
        if symbol["category"] in (
            enums.SymbolKindEnum.FIELD, enums.SymbolKindEnum.STATIC
        ):
            engine.class_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )
            
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )

    engine.input_lines = input_lines
    engine.class_name = "Point"
    engine.compile_subroutine()

    assert "".join(expected) == engine.destination.getvalue()



@pytest.mark.parametrize(
    "input_lines,expected,defined_symbols", [
        (
            [],
            [],
            {}
        ),
        (
            [
                "<keyword> int </keyword>\n",
                "<identifier> input </identifier>\n",
            ],
            [],
            {
                "input": {
                    "kind": enums.SymbolCategoryEnum.ARG, 
                    "type_": "int",
                    "index": 0,
                }
            }
        ),
        (
            [
                "<keyword> int </keyword>\n",
                "<identifier> input </identifier>\n",
                "<symbol> , </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> output </identifier>\n",
            ],
            [],
            {
                "input": {
                    "kind": enums.SymbolCategoryEnum.ARG, 
                    "type_": "int",
                    "index": 0,
                },
                "output": {
                    "kind": enums.SymbolCategoryEnum.ARG, 
                    "type_": "int",
                    "index": 1,
                }
            }
        ),
        (
            [
                "<keyword> Square </keyword>\n",
                "<identifier> input </identifier>\n",
                "<symbol> , </symbol>\n",
                "<keyword> Test </keyword>\n",
                "<identifier> output </identifier>\n",
            ],
            [],
            {
                "input": {
                    "kind": enums.SymbolCategoryEnum.ARG, 
                    "type_": "Square",
                    "index": 0,
                },
                "output": {
                    "kind": enums.SymbolCategoryEnum.ARG, 
                    "type_": "Test",
                    "index": 1,
                }
            }
        )
    ]
)
def test_compile_parameter_list(
    input_lines: list[str], 
    expected: list[str],
    defined_symbols: dict[str, dict[str, t.Any]],
    engine: ce.ComplilationEngine,
):
    engine.input_lines = input_lines
    engine.compile_parameter_list()

    assert "".join(expected) == engine.destination.getvalue()
    for symbol, attributes in defined_symbols.items():
        assert attributes["kind"] == engine.function_table.kind_of(symbol)
        assert attributes["type_"] == engine.function_table.type_of(symbol)
        assert attributes["index"] == engine.function_table.index_of(symbol)


@pytest.mark.parametrize(
    "input_lines,expected,defined_symbols",
    [
        (
            ["<symbol> { </symbol>\n", "<symbol> } </symbol>\n",],
            ["function Test.test 0\n"],
            {}
        ),
        (
            [
                "<symbol> { </symbol>\n",
                "<keyword> return </keyword>\n",
                "<int_constant> 1 </int_constant>\n",
                "<symbol> + </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "function Test.test 0\n",
                "push constant 1\n",
                "push constant 3\n",
                "add\n",
                "return\n",
            ],
            {}
        ),
        (
            [
                "<symbol> { </symbol>\n",
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> , </symbol>\n",
                "<identifier> y </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> y </identifier>\n",
                "<symbol> = </symbol>\n",
                "<identifier> Square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "function Test.test 2\n",
                "push constant 3\n",
                "pop local 0\n",
                "call Square.draw 0\n",
                "pop local 1\n",
            ],
            {
               "x": {"kind": enums.SymbolKindEnum.VAR, "type_": "int", "index": 0,},
               "y": {"kind": enums.SymbolKindEnum.VAR, "type_": "int", "index": 1,},
            }
        )
    ]
)
def test_compile_subroutine_body(
    engine: ce.ComplilationEngine, 
    input_lines: list[str], 
    expected: list[str],
    defined_symbols: dict[str, dict[str, t.Any]]
):
    engine.input_lines = input_lines
    function_info = "function Test.test"

    engine.compile_subroutine_body(function_info, "function")

    assert "".join(expected) == engine.destination.getvalue()

    table = engine.function_table
    for name, attributes in defined_symbols.items():
        assert attributes["kind"] == table.kind_of(name)
        assert attributes["type_"] == table.type_of(name)
        assert attributes["index"] == table.index_of(name)


@pytest.mark.parametrize(
    "input_lines,expected,defined_symbols", [
        (
            [
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [],
            {
                "x": {
                        "kind": enums.SymbolKindEnum.VAR,
                        "type": "int",
                        "index": 0,
                }
            }
        ),
        (
            [
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> , </symbol>\n",
                "<identifier> y </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [],
            {
                "x": {
                        "kind": enums.SymbolKindEnum.VAR,
                        "type": "int",
                        "index": 0,
                },
                "y": {
                        "kind": enums.SymbolKindEnum.VAR,
                        "type": "int",
                        "index": 1,
                }
            }
        ),
        (
            [
                "<keyword> var </keyword>\n",
                "<identifier> Square </identifier>\n",
                "<identifier> square </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [],
            {
                "square": {
                        "kind": enums.SymbolKindEnum.VAR,
                        "type": "Square",
                        "index": 0,
                }
            }
        )
    ]
)
def test_compile_var_dec(
    input_lines: list[str], 
    expected: list[str],
    defined_symbols: dict[str, dict[str, t.Any]],
    engine: ce.ComplilationEngine,
):
    engine.input_lines = input_lines
    engine.compile_var_dec()

    assert "".join(expected) == engine.destination.getvalue()
    
    table = engine.function_table
    for symbol, attributes in defined_symbols.items():
        assert attributes["type"] == table.type_of(symbol)
        assert attributes["kind"] == table.kind_of(symbol)
        assert attributes["index"] == table.index_of(symbol)


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "push constant 3\n",
                "pop local 0\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.INT, 
                    "kind": enums.SymbolKindEnum.VAR
                }
            ]
        ),
        (
            [
                "<keyword> while </keyword>\n",
                "<symbol> ( </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
                "<keyword> return </keyword\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "label WHILE1\n",
                "push local 0\n",
                "not\n",
                "if-goto ENDWHILE1\n",
                "push constant 3\n",
                "pop local 0\n",
                "goto WHILE1\n",
                "label ENDWHILE1\n",
                "push constant 3\n",
                "return\n",

            ],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.INT, 
                    "kind": enums.SymbolKindEnum.VAR
                }
            ]
        )
    ]
)
def test_compile_statements(
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict[str, str]], 
    engine: ce.ComplilationEngine
):

    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["kind"]
        )

    engine.input_lines = input_lines
    engine.compile_statements()
    
    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "push constant 3\n",
                "pop local 0\n",    
            ],
            [
                {
                    "name": "x", 
                    "kind": enums.SymbolKindEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                }
            ]
        ),
        (
            [
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<identifier> Square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>",
                "<symbol> ) </symbol>",
                "<symbol> ; </symbol>\n",
            ],
            [
                "call Square.draw 0\n",
                "pop local 0\n",    
            ],
            [
                {
                    "name": "x", 
                    "kind": enums.SymbolKindEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                }
            ]
        ),
        # TODO: add array example
        (
            [
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<identifier> arr </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<integer_const> 2 <integer_const>\n",
                "<symbol> ] </symbol>\n",                
                "<symbol> ; </symbol>\n",
            ],
            [
                "push local 1\n",
                "push constant 2\n",
                "add\n",
                "pop pointer 1\n",
                "push that 0\n",
                "pop local 0\n",
            ],
            [
                {
                    "name": "x",
                    "kind": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                {   "name": "arr",
                    "kind": enums.SymbolCategoryEnum.VAR, 
                    "type_": "Array"
                },
            ],
        ),
        (
            [
                "<keyword> let </keyword>\n",
                "<identifier> arr_1 </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<integer_const> 3 <integer_const>\n",
                "<symbol> ] </symbol>\n",                
                "<symbol> = </symbol>\n",
                "<identifier> arr_2 </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<integer_const> 2 <integer_const>\n",
                "<symbol> ] </symbol>\n",                
                "<symbol> ; </symbol>\n",
            ],
            [
                "push local 0\n",
                "push constant 3\n",
                "add\n",
                "push local 1\n",
                "push constant 2\n",
                "add\n",
                "pop pointer 1\n",
                "push that 0\n",
                "pop temp 0\n",
                "pop pointer 1\n",
                "push temp 0\n",
                "pop that 0\n",
            ],
            [
                {   "name": "arr_1",
                    "kind": enums.SymbolCategoryEnum.VAR, 
                    "type_": "Array"
                },
                {   
                    "name": "arr_2",
                    "kind": enums.SymbolCategoryEnum.VAR, 
                    "type_": "Array"
                },
            ],
        ),
        (
            [
                "<keyword> let </keyword>\n",
                "<identifier> arr_1 </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<identifier> arr_2 </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> + </symbol>\n",
                "<integer_const> 3 <integer_const>\n",
                "<symbol> ] </symbol>\n",                
                "<symbol> ] </symbol>\n",                
                "<symbol> = </symbol>\n",
                "<integer_const> 2 <integer_const>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "push local 0\n",
                "push local 1\n",
                "push local 2\n",
                "push constant 3\n",
                "add\n",
                "add\n",
                "pop pointer 1\n",
                "push that 0\n",
                "add\n",
                "push constant 2\n",
                "pop temp 0\n",
                "pop pointer 1\n",
                "push temp 0\n",
                "pop that 0\n",
            ],
            [
                {   "name": "arr_1",
                    "kind": enums.SymbolCategoryEnum.VAR, 
                    "type_": "Array"
                },
                {   
                    "name": "arr_2",
                    "kind": enums.SymbolCategoryEnum.VAR, 
                    "type_": "Array"
                },
                {   
                    "name": "x",
                    "kind": enums.SymbolCategoryEnum.VAR, 
                    "type_": "int"
                },
            ],
        )
    ]
)
def test_compile_let(
    input_lines: list[str], 
    expected: list[str], 
    symbols: list[dict[str, str]], 
    engine: ce.ComplilationEngine
):

    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["kind"]
        )

    engine.input_lines = input_lines
    engine.compile_let()

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> if </keyword>\n",
                "<symbol> ( </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "push local 0\n",
                "not\n",
                "if-goto ELSE1\n",
                "push constant 3\n",
                "pop local 0\n",
                "goto ENDIF1\n",
                "label ELSE1\n",
                "label ENDIF1\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.INT, 
                    "kind": enums.SymbolKindEnum.VAR
                }
            ],
        ),
        (
            [
                "<keyword> if </keyword>\n",
                "<symbol> ( </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
                "<keyword> else </keyword>\n",
                "<symbol> { </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<int_constant> 5 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "push local 0\n",
                "not\n",
                "if-goto ELSE1\n",
                "push constant 3\n",
                "pop local 0\n",
                "goto ENDIF1\n",
                "label ELSE1\n",
                "push constant 5\n",
                "pop local 0\n",
                "label ENDIF1\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.INT, 
                    "kind": enums.SymbolKindEnum.VAR
                }
            ]
        )
    ]
)
def test_compile_if(
    input_lines: list[str], 
    expected: list[str], 
    symbols: list[dict[str, str]],
    engine: ce.ComplilationEngine,
):

    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["kind"]
        )

    engine.input_lines = input_lines
    engine.compile_if()

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> while </keyword>\n",
                "<symbol> ( </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> &lt; </symbol>\n",
                "<int_constant> 10 </int_constant>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> { </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> + </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "label WHILE1\n",
                "push local 0\n",
                "push constant 10\n",
                "lt\n",
                "not\n",
                "if-goto ENDWHILE1\n",
                "push local 0\n",
                "push constant 3\n",
                "add\n",
                "pop local 0\n",
                "goto WHILE1\n",
                "label ENDWHILE1\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.INT, 
                    "kind": enums.SymbolKindEnum.VAR
                }
            ]
        )
    ]
)
def test_compile_while(
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict[str, str]],
    engine: ce.ComplilationEngine
):

    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["kind"]
        )

    engine.input_lines = input_lines
    engine.compile_while()

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> do </keyword>\n",
                "<identifier> Square </identifier>\n",
                "<symbol> . </symbol>",
                "<identifier> drawRectangle </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> ; </symbol>\n", 
            ],
            [
                "call Square.drawRectangle 0\n",
                "pop temp 0\n",
            ],
            [],
        ), 
        (
            [
                "<keyword> do </keyword>\n",
                "<identifier> drawRectangle </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> ; </symbol>\n", 
            ],
            [
                "push pointer 0\n",
                "push local 0\n", 
                f"call {CLASS_NAME}.drawRectangle 2\n", 
                "pop temp 0\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.INT, 
                    "kind": enums.SymbolKindEnum.VAR
                },
            ],
        ),
        (
            [
                "<keyword> do </keyword>\n",
                "<identifier> square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> drawRectangle </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> ; </symbol>\n", 
            ],
            [
                "push local 1\n",
                "push local 0\n", 
                "call Square.drawRectangle 2\n", 
                "pop temp 0\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.INT, 
                    "kind": enums.SymbolKindEnum.VAR
                },
                {
                    "name": "square",
                    "type_": "Square",
                    "kind": enums.SymbolKindEnum.VAR
                }
            ],
        ),
    ]
)
def test_compile_do(
    input_lines: list[str], 
    expected: list[str], 
    symbols: list[dict[str, str]],
    engine: ce.ComplilationEngine
):
    
    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["kind"]
        )


    engine.input_lines = input_lines
    engine.compile_do()

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> return </keyword>\n",
                "<symbol> ; </symbol>\n",
            ],
            ["return\n"],
            [],
        ),
        (
            [
                "<keyword> return </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            ["push local 0\n", "return\n"],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.STR, 
                    "kind": enums.SymbolKindEnum.VAR
                }
            ]
        )
    ]
)
def test_compile_return(
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict[str, str]],
    engine: ce.ComplilationEngine
):

    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["kind"]
        )

    engine.input_lines = input_lines
    engine.compile_return()

    assert "".join(expected) == engine.destination.getvalue()



@pytest.mark.parametrize(
    "input_lines,symbols,expected", [
        (  # 0
            ["<string_const> Ello </string_const>"],
            {},
            [
                "push constant 4\n",
                "call String.new 1\n",
                "push constant 69\n",
                "call String.appendChar 2\n",
                "push constant 108\n",
                "call String.appendChar 2\n",
                "push constant 108\n",
                "call String.appendChar 2\n",
                "push constant 111\n",
                "call String.appendChar 2\n",
            ],
        ),
        (  # 1
            ["<keyword> true </keyword>\n"],
            {},
            ["push constant 1\n", "neg\n"],
        ),
        (  # 2
            ["<keyword> false </keyword>\n"],
            {},
            ["push constant 0\n"],
        ),
        (  # 3
            ["<keyword> null </keyword>\n"],
            {},
            ["push constant 0\n"],
        ),
        (  # 4
            ["<keyword> this </keyword>\n"],
            {},
            ["push pointer 0\n"],
        ),
        (  # 5
            [
                "<int_constant> 3 </int_constant>\n",
                "<symbol> + </symbol>\n",
                "<int_constant> 2 </int_constant>\n"
            ],
            {},
            ["push constant 3\n", "push constant 2\n", "add\n"],
        ),
        (  # 6
            [
                "<int_constant> 3 </int_constant>\n",
                "<symbol> * </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
            ],
            {},
            [
                "push constant 3\n", "push constant 2\n", "call Math.multiply 2\n",
            ],
        ),
        (  # 7
            [
                "<symbol> - </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
            ],
            {},
            [
                "push constant 2\n", 
                "neg\n",
            ],
        ),
        (  # 3
            [
                "<int_constant> 3 <int_constant>\n",
                "<symbol> + </symbol>\n",
                "<identifier> Square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> g </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<int_constant> 7 </int_constant>\n",
                "<symbol> - </symbol>\n",
                "<int_constant> 5 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<symbol> - </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> ) </symbol>\n",
            ],
            {},
            [
                "push constant 3\n",
                "push constant 2\n", 
                "push constant 7\n", 
                "push constant 5\n", 
                "sub\n", 
                "push constant 2\n", 
                "neg\n",
                "call Square.g 3\n",
                "add\n",
            ],
        ),
        (
            ["<identifier> x </identifier>\n",],
            {
                "x": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            ["push local 0\n"],
        ),
        (
            [
                "<identifier> x </identifier>\n",
                "<symbol> + </symbol>\n",
                "<identifier> y </identifier>\n"
            ],
            {
                "x": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "y": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            ["push local 0\n", "push local 1\n", "add\n"],
        ),
        (
            [
                "<identifier> z </identifier>\n",
                "<symbol> * </symbol>\n",
                "<identifier> a </identifier>\n",
            ],
            {
                "z": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "a": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            [
                "push local 0\n", "push local 1\n", "call Math.multiply 2\n",
            ]
        ),
        (
            [
                "<symbol> - </symbol>\n",
                "<identifier> z </identifier>\n",
            ],
            {
                "z": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            [
                "push local 0\n", 
                "neg\n",
            ],
        ),
        (
            [
                "<identifier> x </identifier>\n",
                "<symbol> + </symbol>\n",
                "<identifier> g </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<identifier> z </identifier>\n",
                "<symbol> - </symbol>\n",
                "<int_constant> 5 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<symbol> - </symbol>\n",
                "<identifier> y </identifier>\n",
                "<symbol> ) </symbol>\n",
            ],
            {
                "x": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "y": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "z": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            [
                "push local 0\n", 
                "push pointer 0\n",
                "push constant 2\n", 
                "push local 2\n", 
                "push constant 5\n", 
                "sub\n", 
                "push local 1\n", 
                "neg\n",
                f"call {CLASS_NAME}.g 4\n",
                "add\n",  
            ],
        ),
        (
            [
                "<identifier> Square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> g </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<identifier> y </identifier>\n",
                "<symbol> - </symbol>\n",
                "<int_constant> 5 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<symbol> - </symbol>\n",
                "<identifier> z </identifier>\n",
                "<symbol> ) </symbol>\n",
            ],
            {
                "y": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "z": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            [
                "push constant 2\n", 
                "push local 0\n", 
                "push constant 5\n", 
                "sub\n", 
                "push local 1\n", 
                "neg\n",
                "call Square.g 3\n",
            ],
        ),
    ]
)
def test_compile_expression(    
    input_lines: list[str], 
    symbols: dict[str, dict[str, t.Any]], 
    expected: list[str],
    engine: ce.ComplilationEngine,
):
    for symbol in symbols.keys():
        engine.function_table.define(
            symbol, symbols[symbol]["type_"], symbols[symbol]["category"]
        )
    # This test is ignoring most of the possible forms of expressions
    engine.input_lines = input_lines
    engine.compile_expression() 

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            ["<identifier> x </identifier>\n",],
            ["push local 0\n"],
            {
                "name": "x",
                "category": enums.SymbolKindEnum.VAR,
                "type": "int"
            },
        ),
        (
            ["<int_const> 3 </int_const>\n",],
            ["push constant 3\n"],
            {},
        ),
        (
            [   
                "<symbol> - </symbol>\n",
                "<identifier> x </identifier>\n",
            ],
            ["push local 0\n", "neg\n"],
            {
                "name": "x",
                "category": enums.SymbolKindEnum.VAR,
                "type": "int"
            },
        ),
    ]
)
def test_compile_term(
    input_lines: list[str], 
    expected: list[str], 
    symbols: dict[str, str], 
    engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    if symbols:
        engine.function_table.define(
            symbols["name"], symbols["type"], symbols["category"]
        )
    engine.compile_term() 

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            ["<identifier> x </identifier>\n"],
            ["push argument 0\n",],
            [
                {
                    "name": "x",
                    "kind": enums.SymbolKindEnum.ARG,
                    "type": int
                }
            ]
        ),
        (
            [
                "<identifier> x </identifier>\n",
                "<symbol> , </symbol>\n",
                "<identifier> y </identifier>\n",
            ],
            ["push argument 0\n","push argument 1\n"],
            [
                {
                    "name": "x",
                    "kind": enums.SymbolKindEnum.ARG,
                    "type": int
                },
                {
                    "name": "y",
                    "kind": enums.SymbolKindEnum.ARG,
                    "type": str
                },
            ]

        ),
    ]
)
def test_compile_expression_list(    
    input_lines: list[str], 
    expected: list[str], 
    symbols: list[dict[str, str]], 
    engine: ce.ComplilationEngine,
):
    # This test is ignoring most of the possible forms of expressions
    engine.input_lines = input_lines
    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type"], symbol["kind"]
        )
    engine.compile_expression_list() 

    assert "".join(expected) == engine.destination.getvalue()

@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        # Function / Constructor calls
        (
            [
                "<identifier> Square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
            ],
            ["call Square.draw 0\n"],
            {},    
        ),
        (
            [
                "<identifier> Point </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> new </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ) </symbol>\n",
            ],
            [
                "push constant 2\n",
                "push constant 3\n",
                "call Point.new 2\n",
            ],
            {},
        ),
        # Method calls
        (
            [
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
            ],
            [
                "push pointer 0\n",
                f"call {CLASS_NAME}.draw 1\n",
            ],
            {},
        ),
        (
            [
                "<identifier> square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
            ],
            [
                "push local 0\n",
                "call Square.draw 1\n",
            ],
            {"square": {"kind": enums.SymbolKindEnum.VAR, "type_": "Square"}},
        ),
        (
            [
                "<identifier> square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<int_constant> 3 </int_constant>\n",
                "<symbol> ) </symbol>\n",
            ],
            [
                "push local 0\n",
                "push constant 2\n",
                "push constant 3\n",
                "call Square.draw 3\n"
            ],
            {"square": {"kind": enums.SymbolKindEnum.VAR, "type_": "Square"}},
        ),
    ]
)
def test_compile_subroutine_call(
    input_lines: list[str], 
    expected: list[str],
    symbols: dict[str, dict[str, t.Any]], 
    engine: ce.ComplilationEngine
):

    symbols["this"] = {"type_": CLASS_NAME, "kind": enums.SymbolKindEnum.FIELD}

    for name, attributes in symbols.items():
        if attributes["kind"] in (
            enums.SymbolKindEnum.FIELD, enums.SymbolKindEnum.STATIC
        ):
            table = engine.class_table
        else:
            table = engine.function_table
        table.define(name, attributes["type_"], attributes["kind"])

    assert expected == engine._compile_subroutine_call(input_lines)


@pytest.mark.parametrize(
    "input_lines,expected", [
        (  # 0
            ["<string_const> Ello </string_const>"],
            [
                "push constant 4\n",
                "call String.new 1\n",
                "push constant 69\n",
                "call String.appendChar 2\n",
                "push constant 108\n",
                "call String.appendChar 2\n",
                "push constant 108\n",
                "call String.appendChar 2\n",
                "push constant 111\n",
                "call String.appendChar 2\n",
            ],
        ),
        (  # 1
            ["<keyword> true </keyword>\n"],
            ["push constant 1\n", "neg\n"]
        ),
        (  # 2
            ["<keyword> false </keyword>\n"],
            ["push constant 0\n"]
        ),
        (  # 3
            ["<keyword> null </keyword>\n"],
            ["push constant 0\n"]
        ),
        (  # 4
            ["<keyword> this </keyword>\n"],
            ["push pointer 0\n"]
        ),
        (  # 5
            [
                "<int_constant> 3 </int_constant>\n",
                "<symbol> + </symbol>\n",
                "<int_constant> 2 </int_constant>\n"
            ],
            ["push constant 3\n", "push constant 2\n", "add\n"],
        ),
        (  # 6
            [
                "<int_constant> 3 </int_constant>\n",
                "<symbol> * </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
            ],
            [
                "push constant 3\n", "push constant 2\n", "call Math.multiply 2\n",
            ]
        ),
        (  # 7
            [
                "<symbol> - </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
            ],
            [
                "push constant 2\n", 
                "neg\n",
            ],
        ),
        (  # 8
            [
                "<int_constant> 3 <int_constant>\n",
                "<symbol> + </symbol>\n",
                "<identifier> Square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> g </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<int_constant> 7 </int_constant>\n",
                "<symbol> - </symbol>\n",
                "<int_constant> 5 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<symbol> - </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> ) </symbol>\n",
            ],
            [
                "push constant 3\n",
                "push constant 2\n", 
                "push constant 7\n", 
                "push constant 5\n", 
                "sub\n", 
                "push constant 2\n", 
                "neg\n",
                "call Square.g 3\n",
                "add\n",
            ],
        ),
        (
            [
                "<int_constant> 1 <int_constant>\n",
                "<symbol> + </symbol>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 <int_constant>\n",
                "<symbol> * </symbol>\n",
                "<int_constant> 3 <int_constant>\n",
                "<symbol> ) </symbol>\n",                   
            ],
            [
                "push constant 1\n",
                "push constant 2\n",
                "push constant 3\n",
                "call Math.multiply 2\n",
                "add\n",
            ]
        ),
        (
            [
                "<int_constant> 1 <int_constant>\n",
                "<symbol> + </symbol>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 <int_constant>\n",
                "<symbol> * </symbol>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 3 <int_constant>\n",
                "<symbol> / </symbol>\n",
                "<int_constant> 4 <int_constant>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> ) </symbol>\n"                   
            ],
            [
                "push constant 1\n",
                "push constant 2\n",
                "push constant 3\n",
                "push constant 4\n",
                "call Math.divide 2\n",
                "call Math.multiply 2\n",
                "add\n",
            ]
        ),
    ]
)
def test_code_write_no_identifiers(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    output = engine.code_write(input_lines)
    assert "".join(expected) == "".join(output)


@pytest.mark.parametrize(
    "input_lines,declared_vars,expected", [
        (
            ["<identifier> x </identifier>\n",],
            {
                "x": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            ["push local 0\n"],
        ),
        (
            [
                "<identifier> x </identifier>\n",
                "<symbol> + </symbol>\n",
                "<identifier> y </identifier>\n"
            ],
            {
                "x": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "y": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            ["push local 0\n", "push local 1\n", "add\n"],
        ),
        (
            [
                "<identifier> z </identifier>\n",
                "<symbol> * </symbol>\n",
                "<identifier> a </identifier>\n",
            ],
            {
                "z": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "a": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            [
                "push local 0\n", "push local 1\n", "call Math.multiply 2\n",
            ]
        ),
        (
            [
                "<symbol> - </symbol>\n",
                "<identifier> z </identifier>\n",
            ],
            {
                "z": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            [
                "push local 0\n", 
                "neg\n",
            ],
        ),
        (
            [
                "<identifier> x </identifier>\n",
                "<symbol> + </symbol>\n",
                "<identifier> g </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<identifier> z </identifier>\n",
                "<symbol> - </symbol>\n",
                "<int_constant> 5 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<symbol> - </symbol>\n",
                "<identifier> y </identifier>\n",
                "<symbol> ) </symbol>\n",
            ],
            {
                "x": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "y": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "z": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            [
                "push local 0\n", 
                "push pointer 0\n",
                "push constant 2\n", 
                "push local 2\n", 
                "push constant 5\n", 
                "sub\n", 
                "push local 1\n", 
                "neg\n",
                f"call {CLASS_NAME}.g 4\n",
                "add\n",  
            ],
        ),
        (
            [
                "<identifier> Square </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> g </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<int_constant> 2 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<identifier> y </identifier>\n",
                "<symbol> - </symbol>\n",
                "<int_constant> 5 </int_constant>\n",
                "<symbol> , </symbol>\n",
                "<symbol> - </symbol>\n",
                "<identifier> z </identifier>\n",
                "<symbol> ) </symbol>\n",
            ],
            {
                "y": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
                "z": {
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                },
            },
            [
                "push constant 2\n", 
                "push local 0\n", 
                "push constant 5\n", 
                "sub\n", 
                "push local 1\n", 
                "neg\n",
                "call Square.g 3\n",
            ],
        ),
        (
            [
                "<identifier> arr </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<integer_constant> 2 </integer_constant>\n",
                "<symbol> ] </symbol>\n",
            ],
            {
                "arr" :{
                    "category": enums.SymbolCategoryEnum.VAR,
                    "type_": "Array",
                }
            },
            [
                "push local 0\n", 
                "push constant 2\n", 
                "add\n", 
                "pop pointer 1\n",
                "push that 0\n",
            ],
        ),
        (
            [
                "<identifier> arr </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> + </symbol>\n",
                "<integer_constant> 1 </integer_constant>\n",
                "<symbol> ] </symbol>\n",
            ],
            {
                "arr" :{
                    "category": enums.SymbolCategoryEnum.VAR,
                    "type_": "Array",
                },
                "x" :{
                    "category": enums.SymbolCategoryEnum.VAR,
                    "type_": "int",
                }
            },
            [
                "push local 0\n", 
                "push local 1\n",
                "push constant 1\n",
                "add\n",
                "add\n", 
                "pop pointer 1\n",
                "push that 0\n",
            ],
        ),
        (
            [
                "<identifier> arr1 </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<identifier> arr2 </identifier>\n",
                "<symbol> [ </symbol>\n",
                "<integer_constant> 2 </integer_constant>\n",
                "<symbol> ] </symbol>\n",
                "<symbol> + </symbol>\n",
                "<integer_constant> 1 </integer_constant>\n",
                "<symbol> ] </symbol>\n",
            ],
            {
                "arr1" :{
                    "category": enums.SymbolCategoryEnum.VAR,
                    "type_": "Array",
                },
                "arr2" :{
                    "category": enums.SymbolCategoryEnum.VAR,
                    "type_": "Array",
                },
            },
            [
                "push local 0\n", 
                "push local 1\n"
                "push constant 2\n",
                "add\n",
                "pop pointer 1\n",
                "push that 0\n", 
                "push constant 1\n",
                "add\n",
                "add\n",
                "pop pointer 1\n",
                "push that 0\n",
            ],
        ),
    ]
)
def test_code_write_identifier(
    input_lines: list[str], 
    declared_vars: dict[str, t.Any],
    expected: list[str], 
    engine: ce.ComplilationEngine
):
    
    for var, attributes in declared_vars.items():
        if attributes["category"] in (
            enums.SymbolCategoryEnum.ARG,
            enums.SymbolCategoryEnum.VAR,
        ):
            engine.function_table.define(
                var, attributes["type_"], attributes["category"]
            )
        else:
            engine.class_table.define(
                var, attributes["type_"], attributes["category"]
            )

    output = engine.code_write(input_lines)
    assert "".join(expected) == "".join(output)

