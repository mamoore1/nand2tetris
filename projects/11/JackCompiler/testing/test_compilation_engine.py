from io import StringIO
from unittest import mock

import pytest

import JackCompiler.src.compilation_engine as ce

@pytest.fixture
def engine():
    
    def mock_init(self):
        self.input_lines = []
        self.destination = StringIO()

    with mock.patch.object(ce.ComplilationEngine, "__init__", mock_init):
        compilation_engine = ce.ComplilationEngine()
        yield compilation_engine
        compilation_engine.destination.close()


@pytest.mark.parametrize(
    "input_lines,expected", [
        (
            [
                "<keyword> class </keyword>\n",
                "<identifier> Test </identifier>\n",
                "<symbol> { </symbol>\n",
                "<symbol> } </symbol>\n",
            ],
            [
                "<class>\n",
                "  <keyword> class </keyword>\n",
                "  <identifier> Test </identifier>\n",
                "  <symbol> { </symbol>\n",
                "  <symbol> } </symbol>\n",
                "</class>\n",
            ]
        ),
        (
            [
                "<keyword> class </keyword>\n",
                "<identifier> Test </identifier>\n",
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
                "  <identifier> Test </identifier>\n",
                "  <symbol> { </symbol>\n",
                "  <subroutineDec>\n",
                "    <keyword> function </keyword>\n",
                "    <keyword> void </void>\n",
                "    <identifier> draw </identifier>\n",
                "    <symbol> ( </symbol>\n",
                "    <parameterList>\n",
                "      <keyword> int </keyword>\n",
                "      <identifier> input </identifier>\n",
                "      <symbol> , </symbol>\n",
                "      <keyword> int </keyword>\n",
                "      <identifier> output </identifier>\n",
                "    </parameterList>\n",
                "    <symbol> ) </symbol>\n",
                "    <subroutineBody>\n",
                "      <symbol> { </symbol>\n",
                "      <statements>\n",
                "        <letStatement>\n",
                "          <keyword> let </keyword>\n",
                "          <identifier> x </identifier>\n",
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
        ),
        (
            [
                "<keyword> class </keyword>\n",
                "<identifier> Test </identifier>\n",
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
                "  <identifier> Test </identifier>\n",
                "  <symbol> { </symbol>\n",
                "  <classVarDec>\n",
                "    <keyword> static </keyword>\n",
                "    <keyword> int </keyword>\n",
                "    <identifier> abc </identifier>\n",
                "    <symbol> , </symbol>\n",
                "    <identifier> xyz </identifier>\n",
                "    <symbol> ; </symbol>\n",
                "  </classVarDec>\n",
                "  <subroutineDec>\n",
                "    <keyword> function </keyword>\n",
                "    <keyword> void </void>\n",
                "    <identifier> draw </identifier>\n",
                "    <symbol> ( </symbol>\n",
                "    <parameterList>\n",
                "      <keyword> int </keyword>\n",
                "      <identifier> input </identifier>\n",
                "      <symbol> , </symbol>\n",
                "      <keyword> int </keyword>\n",
                "      <identifier> output </identifier>\n",
                "    </parameterList>\n",
                "    <symbol> ) </symbol>\n",
                "    <subroutineBody>\n",
                "      <symbol> { </symbol>\n",
                "      <statements>\n",
                "        <letStatement>\n",
                "          <keyword> let </keyword>\n",
                "          <identifier> x </identifier>\n",
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
        ),
    ]
)
def test_compile_class(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    engine.compile_class(0)

    assert "".join(expected) ==  engine.destination.getvalue()
    

@pytest.mark.parametrize(
    "input_lines,expected", [
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
                "  <identifier> xyz </identifier>\n",
                "  <symbol> ; </symbol>\n",
                "</classVarDec>\n",
            ]
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
                "  <identifier> abc </identifier>\n",
                "  <symbol> , </symbol>\n",
                "  <identifier> xyz </identifier>\n",
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
    "input_lines,expected", [
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
                "  <identifier> draw </identifier>\n",
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
            ]
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
                "  <identifier> draw </identifier>\n",
                "  <symbol> ( </symbol>\n",
                "  <parameterList>\n",
                "    <keyword> int </keyword>\n",
                "    <identifier> input </identifier>\n",
                "    <symbol> , </symbol>\n",
                "    <keyword> int </keyword>\n",
                "    <identifier> output </identifier>\n",
                "  </parameterList>\n",
                "  <symbol> ) </symbol>\n",
                "  <subroutineBody>\n",
                "    <symbol> { </symbol>\n",
                "    <statements>\n",
                "      <letStatement>\n",
                "        <keyword> let </keyword>\n",
                "        <identifier> x </identifier>\n",
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
            ]
        )
    ]
)
def test_compile_subroutine(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine,
):
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
                "  <identifier> input </identifier>\n",
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
                "  <identifier> input </identifier>\n",
                "  <symbol> , </symbol>\n",
                "  <keyword> int </keyword>\n",
                "  <identifier> output </identifier>\n",
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
    "input_lines,expected",
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
            ]
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
                "      <identifier> x </identifier>\n",
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
        ),
        (
            [
                "<symbol> { </symbol>\n",
                "<keyword> var </keyword>\n",
                "<keyword> int </keyword>\n",
                "<identifier> xyz </identifier>\n",
                "<symbol> ; </symbol>\n",
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
                "  <varDec>\n",
                "    <keyword> var </keyword>\n",
                "    <keyword> int </keyword>\n",
                "    <identifier> xyz </identifier>\n",
                "    <symbol> ; </symbol>\n",
                "  </varDec>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      <identifier> x </identifier>\n",
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
        )
    ]
)
def test_compile_subroutine_body(
    engine: ce.ComplilationEngine, input_lines: list[str], expected: list[str]
):
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
                "  <identifier> x </identifier>\n",
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
                "  <identifier> x </identifier>\n",
                "  <symbol> , </symbol>\n",
                "  <identifier> y </identifier>\n",    
                "  <symbol> ; </symbol>\n",
                "</varDec>\n"
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
    "input_lines,expected", [
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
                "    <identifier> x </identifier>\n",
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
                "        <identifier> x </identifier>\n",
                "      </term>\n",
                "    </expression>\n",
                "    <symbol> ) </symbol>\n",
                "    <symbol> { </symbol>\n",
                "    <statements>\n",
                "      <letStatement>\n",
                "        <keyword> let </keyword>\n",
                "        <identifier> x </identifier>\n",
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
            ]
        )
    ]
)
def test_compile_statements(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    engine.compile_statements(0)
    
    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
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
                "  <identifier> x </identifier>\n",
                "  <symbol> = </symbol>\n",
                "  <expression>\n",
                "    <term>\n",
                "      <integerConstant> 3 </integerConstant>\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ; </symbol>\n",
                "</letStatement>\n",    
            ]
        )
    ]
)
def test_compile_let(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    engine.compile_let(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
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
                "      <identifier> x </identifier>\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      <identifier> x </identifier>\n",
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
            ]
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
                "      <identifier> x </identifier>\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      <identifier> x </identifier>\n",
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
                "      <identifier> x </identifier>\n",
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
            ]
        )
    ]
)
def test_compile_if(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):

    engine.input_lines = input_lines
    engine.compile_if(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
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
                "      <identifier> x </identifier>\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> { </symbol>\n",
                "  <statements>\n",
                "    <letStatement>\n",
                "      <keyword> let </keyword>\n",
                "      <identifier> x </identifier>\n",
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
            ]
        )
    ]
)
def test_compile_while(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):

    engine.input_lines = input_lines
    engine.compile_while(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
        (
            [
                "<keyword> do </keyword>\n",
                "<identifier> Screen </identifier>\n",
                "<symbol> . </symbol>",
                "<identifier> drawRectangle </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<symbol> ) </symbol>\n",
                "<symbol> ; </symbol>\n", 
            ],
            [
                "<doStatement>\n",
                "  <keyword> do </keyword>\n",
                "  <identifier> Screen </identifier>\n",
                "  <symbol> . </symbol>",
                "  <identifier> drawRectangle </identifier>\n",
                "  <symbol> ( </symbol>\n",
                "  <expressionList>\n",
                "  </expressionList>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> ; </symbol>\n", 
                "</doStatement>\n",
            ],
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
                "  <identifier> drawRectangle </identifier>\n",
                "  <symbol> ( </symbol>\n",
                "  <expressionList>\n",
                "    <expression>\n",
                "      <term>\n",
                "        <identifier> x </identifier>\n",
                "      </term>\n",
                "    </expression>\n",
                "  </expressionList>\n",
                "  <symbol> ) </symbol>\n",
                "  <symbol> ; </symbol>\n", 
                "</doStatement>\n",
            ],
        )
    ]
)
def test_compile_do(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    # This test is basically gibberish currently, as we don't resolve 
    # expressions or subroutine calls

    engine.input_lines = input_lines
    engine.compile_do(0)

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
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
            ]
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
                "      <identifier> x </identifier>\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ; </symbol>\n",
                "</returnStatement>\n",
            ]
        )
    ]
)
def test_compile_return(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):

    engine.input_lines = input_lines
    engine.compile_return(0)

    assert "".join(expected) == engine.destination.getvalue()



@pytest.mark.parametrize(
    "input_lines,expected", [
        (
            [
                "<identifier> x </identifier>\n",
            ], 
            [
                "<expression>\n",
                "  <term>\n",
                "    <identifier> x </identifier>\n",
                "  </term>\n",
                "</expression>\n",
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
                "    <identifier> x </identifier>\n",
                "  </term>\n",
                "  <symbol> + </symbol>\n",
                "  <term>\n",
                "    <identifier> y </identifier>\n",
                "  </term>\n",
                "</expression>\n",
            ]
        )
    ]
)
def test_compile_expression(    
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    # This test is ignoring most of the possible forms of expressions
    engine.input_lines = input_lines
    engine.compile_expression(0) 

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
        (
            ["<identifier> x </identifier>\n",],
            [
                "<term>\n",
                "  <identifier> x </identifier>\n",
                "</term>\n",
            ],
        ),
        (
            ["<integerConstant> 3 </integerConstant>\n",],
            [
                "<term>\n",
                "  <integerConstant> 3 </integerConstant>\n",
                "</term>\n",
            ],
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
                "    <identifier> x </identifier>\n",
                "  </term>\n"
                "</term>\n",
            ],
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
                "      <identifier> x </identifier>\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> ) </symbol>\n",
                "</term>\n",
            ],
        )
    ]
)
def test_compile_term(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    engine.compile_term(0) 

    assert "".join(expected) == engine.destination.getvalue()


@pytest.mark.parametrize(
    "input_lines,expected", [
        (
            ["<identifier> x </identifier>\n"],
            [
                "<expressionList>\n",
                "  <expression>\n",
                "    <term>\n",
                "      <identifier> x </identifier>\n",
                "    </term>\n",
                "  </expression>\n",
                "</expressionList>\n",
            ],
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
                "      <identifier> x </identifier>\n",
                "    </term>\n",
                "  </expression>\n",
                "  <symbol> , </symbol>\n",
                "  <expression>\n",
                "    <term>\n",
                "      <identifier> y </identifier>\n",
                "    </term>\n",
                "  </expression>\n",
                "</expressionList>\n",
            ],
        ),
    ]
)
def test_compile_expression_list(    
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    # This test is ignoring most of the possible forms of expressions
    engine.input_lines = input_lines
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
                "<identifier> square </identifier>\n",
                "<symbol> ( </symbol>\n",
                "<expressionList>\n",
                "</expressionList>\n",
                "<symbol> ) </symbol>\n",
            ]
        )
    ]
)
def test_compile_subroutine(
    input_lines: list[str], expected: list[str], engine: ce.ComplilationEngine
):
    engine.input_lines = input_lines
    engine.compile_subroutine_call(0)

    assert "".join(expected) == engine.destination.getvalue()