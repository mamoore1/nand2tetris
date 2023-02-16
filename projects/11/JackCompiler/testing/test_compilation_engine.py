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

    with mock.patch.object(ce.ComplilationEngine, "__init__", mock_init):
        compilation_engine = ce.ComplilationEngine()
        yield compilation_engine
        compilation_engine.destination.close()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> class </keyword>\n",
                f"<identifier> {CLASS_NAME} </identifier>\n",
                "<symbol> { </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<class>\n",
                "  <keyword> class </keyword>\n",
                f"  name: {CLASS_NAME}, category: class, index: None, usage: declared\n",
                "  <symbol> { </symbol>\n",
                "  <symbol> } </symbol>\n",
                "</class>\n",
            ],
            []
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
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<class>\n",
                "  <keyword> class </keyword>\n",
                f"  name: {CLASS_NAME}, category: class, index: None, usage: declared\n",
                "  <symbol> { </symbol>\n",
                "  <subroutineDec>\n",
                "    <keyword> function </keyword>\n",
                "    <keyword> void </void>\n",
                "    name: draw, category: subroutine, index: None, usage: declared\n",
                "    <symbol> ( </symbol>\n",
                "    <parameterList>\n",
                "      <keyword> int </keyword>\n",
                "      name: input, category: arg, index: 0, usage: declared\n",
                "      <symbol> , </symbol>\n",
                "      <keyword> int </keyword>\n",
                "      name: output, category: arg, index: 1, usage: declared\n",
                "    </parameterList>\n",
                "    <symbol> ) </symbol>\n",
                "    <subroutineBody>\n",
                "      <symbol> { </symbol>\n",
                "      <statements>\n",
                "        <letStatement>\n",
                "          <keyword> let </keyword>\n",
                "          name: x, category: var, index: 0, usage: used\n",
                "          <symbol> = </symbol>\n",
                "          <expression>\n",
                "            <term>\n",
                "              <integerConstant> 3 </integerConstant>\n",
                "            </term>\n",
                "          </expression>\n",
                "          <symbol> ; </symbol>\n",
                "        </letStatement>\n",
                "      </statements>\n",   
                "      <symbol> } </symbol>\n",
                "    </subroutineBody>\n",
                "  </subroutineDec>\n",
                "  <symbol> } </symbol>\n",
                "</class>\n",
            ],
            [
                {
                    "name": "x", 
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                }
            ],
        ),
        (
            [
                "<keyword> class </keyword>\n",
                f"<identifier> {CLASS_NAME} </identifier>\n",
                "<symbol> { </symbol>\n",
                "<keyword> static </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> abc </identifier>\n",
                "<symbol> , </symbol>\n",
                "<identifier> xyz </identifier>\n",
                "<symbol> ; </symbol>\n",
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
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<class>\n",
                "  <keyword> class </keyword>\n",
                f"  name: {CLASS_NAME}, category: class, index: None, usage: declared\n",
                "  <symbol> { </symbol>\n",
                "  <classVarDec>\n",
                "    <keyword> static </keyword>\n",
                "    <keyword> int </keyword>\n",
                "    name: abc, category: static, index: 0, usage: declared\n",
                "    <symbol> , </symbol>\n",
                "    name: xyz, category: static, index: 1, usage: declared\n",
                "    <symbol> ; </symbol>\n",
                "  </classVarDec>\n",
                "  <subroutineDec>\n",
                "    <keyword> function </keyword>\n",
                "    <keyword> void </void>\n",
                "    name: draw, category: subroutine, index: None, usage: declared\n",
                "    <symbol> ( </symbol>\n",
                "    <parameterList>\n",
                "      <keyword> int </keyword>\n",
                "      name: input, category: arg, index: 0, usage: declared\n",
                "      <symbol> , </symbol>\n",
                "      <keyword> int </keyword>\n",
                "      name: output, category: arg, index: 1, usage: declared\n",
                "    </parameterList>\n",
                "    <symbol> ) </symbol>\n",
                "    <subroutineBody>\n",
                "      <symbol> { </symbol>\n",
                "      <statements>\n",
                "        <letStatement>\n",
                "          <keyword> let </keyword>\n",
                "          name: x, category: var, index: 0, usage: used\n",
                "          <symbol> = </symbol>\n",
                "          <expression>\n",
                "            <term>\n",
                "              <integerConstant> 3 </integerConstant>\n",
                "            </term>\n",
                "          </expression>\n",
                "          <symbol> ; </symbol>\n",
                "        </letStatement>\n",
                "      </statements>\n",   
                "      <symbol> } </symbol>\n",
                "    </subroutineBody>\n",
                "  </subroutineDec>\n",
                "  <symbol> } </symbol>\n",
                "</class>\n",
            ],
            [
                {
                    "name": "x", 
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                }
            ],
        ),
    ]
)
def test_compile_class(
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict[str, str]], 
    engine: ce.ComplilationEngine
):

    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )

    engine.input_lines = input_lines
    engine.compile_class(0)

    assert "".join(expected) ==  engine.destination.getvalue()
    

@pytest.mark.parametrize(
    "input_lines,expected,", [
        (
            [
                "<keyword> static </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> xyz </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<classVarDec>\n",
                "  <keyword> static </keyword>\n",
                "  <keyword> int </keyword>\n",
                "  name: xyz, category: static, index: 0, usage: declared\n",
                "  <symbol> ; </symbol>\n",
                "</classVarDec>\n",
            ],
        ),
        (
            [
                "<keyword> static </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> abc </identifier>\n",
                "<symbol> , </symbol>\n",
                "<identifier> xyz </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<classVarDec>\n",
                "  <keyword> static </keyword>\n",
                "  <keyword> int </keyword>\n",
                "  name: abc, category: static, index: 0, usage: declared\n",
                "  <symbol> , </symbol>\n",
                "  name: xyz, category: static, index: 1, usage: declared\n",
                "  <symbol> ; </symbol>\n",
                "</classVarDec>\n",
            ]
        ),
        (
            [
                "<keyword> static </keyword>\n",
                "<identifier> Square </identifier>\n",
                "<identifier> square </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<classVarDec>\n",
                "  <keyword> static </keyword>\n",
                "  name: Square, category: class, index: None, usage: used\n",
                "  name: square, category: static, index: 0, usage: declared\n",
                "  <symbol> ; </symbol>\n",
                "</classVarDec>\n",
            ]
        )
    ]
)
def test_compile_class_var_dec(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine,
):
    engine.input_lines = input_lines
    engine.compile_class_var_dec(0)

    assert "".join(expected) == engine.destination.getvalue()


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
                "<symbol> } </symbol>\n",
            ],
            [
                "<subroutineDec>\n",
                "  <keyword> function </keyword>\n",
                "  <keyword> void </void>\n",
                "  name: draw, category: subroutine, index: None, usage: declared\n",
                "  <symbol> ( </symbol>\n",
                "  <parameterList>\n",
                "  </parameterList>\n",
                "  <symbol> ) </symbol>\n",
                "  <subroutineBody>\n",
                "    <symbol> { </symbol>\n",
                "    <statements>\n",
                "    </statements>\n",
                "    <symbol> } </symbol>\n",
                "  </subroutineBody>\n",
                "</subroutineDec>\n",
            ],
            [],
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
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<subroutineDec>\n",
                "  <keyword> function </keyword>\n",
                "  <keyword> void </void>\n",
                "  name: draw, category: subroutine, index: None, usage: declared\n",
                "  <symbol> ( </symbol>\n",
                "  <parameterList>\n",
                "    <keyword> int </keyword>\n",
                "    name: input, category: arg, index: 0, usage: declared\n",
                "    <symbol> , </symbol>\n",
                "    <keyword> int </keyword>\n",
                "    name: output, category: arg, index: 1, usage: declared\n",
                "  </parameterList>\n",
                "  <symbol> ) </symbol>\n",
                "  <subroutineBody>\n",
                "    <symbol> { </symbol>\n",
                "    <statements>\n",
                "      <letStatement>\n",
                "        <keyword> let </keyword>\n",
                "        name: x, category: var, index: 0, usage: used\n",
                "        <symbol> = </symbol>\n",
                "        <expression>\n",
                "          <term>\n",
                "            <integerConstant> 3 </integerConstant>\n",
                "          </term>\n",
                "        </expression>\n",
                "        <symbol> ; </symbol>\n",
                "      </letStatement>\n",
                "    </statements>\n",   
                "    <symbol> } </symbol>\n",
                "  </subroutineBody>\n",
                "</subroutineDec>\n",
            ],
            [
                {
                    "name": "x", 
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                }
            ],
        )
    ]
)
def test_compile_subroutine(
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict[str, str]], 
    engine: ce.ComplilationEngine,
):
    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )

    engine.input_lines = input_lines
    engine.compile_subroutine(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
        (
            [],
            ["<parameterList>\n", "</parameterList>\n"],
        ),
        (
            [
                "<keyword> int </keyword>\n",
                "<identifier> input </identifier>\n",
            ],
            [
                "<parameterList>\n",
                "  <keyword> int </keyword>\n",
                "  name: input, category: arg, index: 0, usage: declared\n",
                "</parameterList>\n",
            ]
        ),
        (
            [
                "<keyword> int </keyword>\n",
                "<identifier> input </identifier>\n",
                "<symbol> , </symbol>\n",
                "<keyword> int </keyword>\n",
                "<identifier> output </identifier>\n",
            ],
            [
                "<parameterList>\n",
                "  <keyword> int </keyword>\n",
                "  name: input, category: arg, index: 0, usage: declared\n",
                "  <symbol> , </symbol>\n",
                "  <keyword> int </keyword>\n",
                "  name: output, category: arg, index: 1, usage: declared\n",
                "</parameterList>\n",
            ]
        )
    ]
)
def test_compile_parameter_list(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine,
):
    engine.input_lines = input_lines
    engine.compile_parameter_list(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols",
    [
        (
            [
                "<symbol> { </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<subroutineBody>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "  </statements>\n",
                "  <symbol> } </symbol>\n",
                "</subroutineBody>\n",
            ],
            []
        ),
        (
            [
                "<symbol> { </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<subroutineBody>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "      <symbol> = </symbol>\n",
                "      <expression>\n",
                "        <term>\n",
                "          <integerConstant> 3 </integerConstant>\n",
                "        </term>\n",
                "      </expression>\n",
                "      <symbol> ; </symbol>\n",
                "    </letStatement>\n",
                "  </statements>\n",   
                "  <symbol> } </symbol>\n",
                "</subroutineBody>\n",
            ],
            [
                {
                    "name": "x", 
                    "category": enums.SymbolCategoryEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                }
            ]
        ),
        (
            [
                "<symbol> { </symbol>\n",
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> xyz </identifier>\n",
                "<symbol> ; </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> xyz </identifier>\n",
                "<symbol> = </symbol>\n",
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<subroutineBody>\n",
                "  <symbol> { </symbol>\n",
                "  <varDec>\n",
                "    <keyword> var </keyword>\n",
                "    <keyword> int </keyword>\n",
                "    name: xyz, category: var, index: 0, usage: declared\n",
                "    <symbol> ; </symbol>\n",
                "  </varDec>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      name: xyz, category: var, index: 0, usage: used\n",
                "      <symbol> = </symbol>\n",
                "      <expression>\n",
                "        <term>\n",
                "          <integerConstant> 3 </integerConstant>\n",
                "        </term>\n",
                "      </expression>\n",
                "      <symbol> ; </symbol>\n",
                "    </letStatement>\n",
                "  </statements>\n",   
                "  <symbol> } </symbol>\n",
                "</subroutineBody>\n",
            ],
            []
        )
    ]
)
def test_compile_subroutine_body(
    engine: ce.ComplilationEngine, 
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict[str, str]]
):
    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["category"]
        )

    engine.input_lines = input_lines
    engine.compile_subroutine_body(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
        (
            [
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<varDec>\n",
                "  <keyword> var </keyword>\n",
                "  <keyword> int </keyword>\n",
                "  name: x, category: var, index: 0, usage: declared\n",
                "  <symbol> ; </symbol>\n",
                "</varDec>\n"
            ]
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
            [
                "<varDec>\n",
                "  <keyword> var </keyword>\n",
                "  <keyword> int </keyword>\n",
                "  name: x, category: var, index: 0, usage: declared\n",
                "  <symbol> , </symbol>\n",
                "  name: y, category: var, index: 1, usage: declared\n",
                "  <symbol> ; </symbol>\n",
                "</varDec>\n"
            ]
        ),
        (
            [
                "<keyword> var </keyword>\n",
                "<identifier> Square </identifier>\n",
                "<identifier> square </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<varDec>\n",
                "  <keyword> var </keyword>\n",
                "  name: Square, category: class, index: None, usage: used\n",
                "  name: square, category: var, index: 0, usage: declared\n",
                "  <symbol> ; </symbol>\n",
                "</varDec>\n",
            ]
        )
    ]
)
def test_compile_var_dec(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    engine.compile_var_dec(0)

    assert "".join(expected) == engine.destination.getvalue()

@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<statements>\n",
                "  <letStatement>\n",
                "    <keyword> let </keyword>\n",
                "    name: x, category: var, index: 0, usage: used\n",
                "    <symbol> = </symbol>\n",
                "    <expression>\n",
                "      <term>\n",
                "        <integerConstant> 3 </integerConstant>\n",
                "      </term>\n",
                "    </expression>\n",
                "    <symbol> ; </symbol>\n",
                "  </letStatement>\n",
                "</statements>\n",    
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
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
                "<keyword> return </keyword\n",
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<statements>\n",
                "  <whileStatement>\n",
                "    <keyword> while </keyword>\n",
                "    <symbol> ( </symbol>\n",
                "    <expression>\n",
                "      <term>\n",
                "        name: x, category: var, index: 0, usage: used\n",
                "      </term>\n",
                "    </expression>\n",
                "    <symbol> ) </symbol>\n",
                "    <symbol> { </symbol>\n",
                "    <statements>\n",
                "      <letStatement>\n",
                "        <keyword> let </keyword>\n",
                "        name: x, category: var, index: 0, usage: used\n",
                "        <symbol> = </symbol>\n",
                "        <expression>\n",
                "          <term>\n",
                "            <integerConstant> 3 </integerConstant>\n",
                "          </term>\n",
                "        </expression>\n",
                "        <symbol> ; </symbol>\n",
                "      </letStatement>\n",
                "    </statements>\n",
                "    <symbol> } </symbol>\n",
                "  </whileStatement>\n",
                "  <returnStatement>\n",
                "    <keyword> return </keyword\n",
                "    <expression>\n",
                "      <term>\n",
                "        <integerConstant> 3 </integerConstant>\n",
                "      </term>\n",
                "    </expression>\n",
                "    <symbol> ; </symbol>\n",
                "  </returnStatement>\n",
                "</statements>\n",
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
    engine.compile_statements(0)
    
    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<letStatement>\n",
                "  <keyword> let </keyword>\n",
                "  name: x, category: var, index: 0, usage: used\n",
                "  <symbol> = </symbol>\n",
                "  <expression>\n",
                "    <term>\n",
                "      <integerConstant> 3 </integerConstant>\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ; </symbol>\n",
                "</letStatement>\n",    
            ],
            [
                {
                    "name": "x", 
                    "kind": enums.SymbolKindEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT
                }
            ]
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
    engine.compile_let(0)

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
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<ifStatement>\n",
                "  <keyword> if </keyword>\n",
                "  <symbol> ( </symbol>\n",
                "  <expression>\n",
                "    <term>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "      <symbol> = </symbol>\n",
                "      <expression>\n",
                "        <term>\n",
                "          <integerConstant> 3 </integerConstant>\n",
                "        </term>\n",
                "      </expression>\n",
                "      <symbol> ; </symbol>\n",
                "    </letStatement>\n",
                "  </statements>\n",
                "  <symbol> } </symbol>\n",
                "</ifStatement>\n",
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
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
                "<keyword> else </keyword>\n",
                "<symbol> { </symbol>\n",
                "<keyword> let </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> = </symbol>\n",
                "<integerConstant> 5 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",

            ],
            [
                "<ifStatement>\n",
                "  <keyword> if </keyword>\n",
                "  <symbol> ( </symbol>\n",
                "  <expression>\n",
                "    <term>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "      <symbol> = </symbol>\n",
                "      <expression>\n",
                "        <term>\n",
                "          <integerConstant> 3 </integerConstant>\n",
                "        </term>\n",
                "      </expression>\n",
                "      <symbol> ; </symbol>\n",
                "    </letStatement>\n",
                "  </statements>\n",
                "  <symbol> } </symbol>\n",
                "  <keyword> else </keyword>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "      <symbol> = </symbol>\n",
                "      <expression>\n",
                "        <term>\n",
                "          <integerConstant> 5 </integerConstant>\n",
                "        </term>\n",
                "      </expression>\n",
                "      <symbol> ; </symbol>\n",
                "    </letStatement>\n",
                "  </statements>\n",
                "  <symbol> } </symbol>\n",
                "</ifStatement>\n",
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
    engine.compile_if(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
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
                "<integerConstant> 3 </integerConstant>\n",
                "<symbol> ; </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<whileStatement>\n",
                "  <keyword> while </keyword>\n",
                "  <symbol> ( </symbol>\n",
                "  <expression>\n",
                "    <term>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "      <symbol> = </symbol>\n",
                "      <expression>\n",
                "        <term>\n",
                "          <integerConstant> 3 </integerConstant>\n",
                "        </term>\n",
                "      </expression>\n",
                "      <symbol> ; </symbol>\n",
                "    </letStatement>\n",
                "  </statements>\n",
                "  <symbol> } </symbol>\n",
                "</whileStatement>\n",
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
    engine.compile_while(0)

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
                "<doStatement>\n",
                "  <keyword> do </keyword>\n",
                "  name: Square, category: class, index: None, usage: used\n",
                "  <symbol> . </symbol>",
                "  name: drawRectangle, category: subroutine, index: None,"
                " usage: used\n",
                "  <symbol> ( </symbol>\n",
                "  <expressionList>\n",
                "  </expressionList>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> ; </symbol>\n", 
                "</doStatement>\n",
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
                "<doStatement>\n",
                "  <keyword> do </keyword>\n",
                "  name: drawRectangle, category: subroutine, index: None, usage: used\n",
                "  <symbol> ( </symbol>\n",
                "  <expressionList>\n",
                "    <expression>\n",
                "      <term>\n",
                "        name: x, category: var, index: 0, usage: used\n",
                "      </term>\n",
                "    </expression>\n",
                "  </expressionList>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> ; </symbol>\n", 
                "</doStatement>\n",
            ],
            [
                {
                    "name": "x", 
                    "type_": enums.VarTypeEnum.INT, 
                    "kind": enums.SymbolKindEnum.VAR
                }
            ],

        )
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
    engine.compile_do(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<keyword> return </keyword>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<returnStatement>\n",
                "  <keyword> return </keyword>\n",
                "  <symbol> ; </symbol>\n",
                "</returnStatement>\n",
            ],
            [],
        ),
        (
            [
                "<keyword> return </keyword>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ; </symbol>\n",
            ],
            [
                "<returnStatement>\n",
                "  <keyword> return </keyword>\n",
                "  <expression>\n",
                "    <term>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ; </symbol>\n",
                "</returnStatement>\n",
            ],
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
    engine.compile_return(0)

    assert "".join(expected) == engine.destination.getvalue()



@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            [
                "<identifier> x </identifier>\n",
            ], 
            [
                "<expression>\n",
                "  <term>\n",
                "    name: x, category: var, index: 0, usage: used\n",
                "  </term>\n",
                "</expression>\n",
            ],
            [
                {
                    "name": "x", 
                    "kind": enums.SymbolKindEnum.VAR, 
                    "type_": enums.VarTypeEnum
                }
            ]
        ),
        (
            [
                "<identifier> x </identifier>\n",
                "<symbol> + </symbol>\n",
                "<identifier> y </identifier>\n"
            ],
            [
                "<expression>\n",
                "  <term>\n",
                "    name: x, category: var, index: 0, usage: used\n",
                "  </term>\n",
                "  <symbol> + </symbol>\n",
                "  <term>\n",
                "    name: y, category: var, index: 1, usage: used\n",
                "  </term>\n",
                "</expression>\n",
            ],
            [
                {
                    "name": "x", 
                    "kind": enums.SymbolKindEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT,
                },
                {
                    "name": "y", 
                    "kind": enums.SymbolKindEnum.VAR, 
                    "type_": enums.VarTypeEnum.INT,
                }
            ]
        )
    ]
)
def test_compile_expression(    
    input_lines: list[str], 
    expected: list[str],
    symbols: list[dict], 
    engine: ce.ComplilationEngine,
):
    for symbol in symbols:
        engine.function_table.define(
            symbol["name"], symbol["type_"], symbol["kind"]
        )
    # This test is ignoring most of the possible forms of expressions
    engine.input_lines = input_lines
    engine.compile_expression(0) 

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            ["<identifier> x </identifier>\n",],
            [
                "<term>\n",
                "  name: x, category: var, index: 0, usage: used\n",
                "</term>\n",
            ],
            {
                "name": "x",
                "category": enums.SymbolKindEnum.VAR,
                "type": "int"
            },
        ),
        (
            ["<integerConstant> 3 </integerConstant>\n",],
            [
                "<term>\n",
                "  <integerConstant> 3 </integerConstant>\n",
                "</term>\n",
            ],
            {
                "name": "x",
                "category": enums.SymbolKindEnum.VAR,
                "type": "int"
            },
        ),
        (
            [   
                "<symbol> - </symbol>\n",
                "<identifier> x </identifier>\n",
            ],
            [
                "<term>\n",
                "  <symbol> - </symbol>\n",
                "  <term>\n",
                "    name: x, category: var, index: 0, usage: used\n",
                "  </term>\n"
                "</term>\n",
            ],
            {
                "name": "x",
                "category": enums.SymbolKindEnum.VAR,
                "type": "int"
            },
        ),
        (
            [
                "<symbol> ( </symbol>\n",
                "<identifier> x </identifier>\n",
                "<symbol> ) </symbol>\n",
            ],
            [
                "<term>\n",
                "  <symbol> ( </symbol>\n",
                "  <expression>\n",
                "    <term>\n",
                "      name: x, category: var, index: 0, usage: used\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ) </symbol>\n",
                "</term>\n",
            ],
            {
                "name": "x",
                "category": enums.SymbolKindEnum.VAR,
                "type": "int"
            },
        )
    ]
)
def test_compile_term(
    input_lines: list[str], 
    expected: list[str], 
    symbols: dict[str, str], 
    engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    engine.function_table.define(
        symbols["name"], symbols["type"], symbols["category"]
    )
    engine.compile_term(0) 

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected,symbols", [
        (
            ["<identifier> x </identifier>\n"],
            [
                "<expressionList>\n",
                "  <expression>\n",
                "    <term>\n",
                "      name: x, category: arg, index: 0, usage: used\n",
                "    </term>\n",
                "  </expression>\n",
                "</expressionList>\n",
            ],
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
            [
                "<expressionList>\n",
                "  <expression>\n",
                "    <term>\n",
                "      name: x, category: arg, index: 0, usage: used\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> , </symbol>\n",
                "  <expression>\n",
                "    <term>\n",
                "      name: y, category: arg, index: 1, usage: used\n",
                "    </term>\n",
                "  </expression>\n",
                "</expressionList>\n",
            ],
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
    engine.compile_expression_list(0) 

    assert "".join(expected) == engine.destination.getvalue()

@pytest.mark.parametrize(
    "input_lines,expected", [
        (
            [
                "<identifier> square </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
            ],
            [
                "name: square, category: subroutine, index: None, usage: used\n",
                "<symbol> ( </symbol>\n",
                "<expressionList>\n",
                "</expressionList>\n",
                "<symbol> ) </symbol>\n",
            ]
        ),
        (
            [
                f"<identifier> {CLASS_NAME} </identifier>\n",
                "<symbol> . </symbol>\n",
                "<identifier> draw </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
            ],
            [
                f"name: {CLASS_NAME}, category: class, index: None, usage: used\n",
                "<symbol> . </symbol>\n",
                "name: draw, category: subroutine, index: None, usage: used\n",
                "<symbol> ( </symbol>\n",
                "<expressionList>\n",
                "</expressionList>\n",
                "<symbol> ) </symbol>\n",
            ]
        )
    ]
)
def test_compile_subroutine_call(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    engine.compile_subroutine_call(0)

    assert "".join(expected) == engine.destination.getvalue()