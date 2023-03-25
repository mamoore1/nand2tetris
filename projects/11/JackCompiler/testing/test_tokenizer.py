from unittest import mock
import pytest

import JackCompiler.src.enums as enums
import JackCompiler.src.tokenizer as tk

@pytest.fixture
def tokenizer():

    def mock_init(self):
        self.input_lines = []
        self.current_line = None
        self.current_index = -1
        self.loaded_line = False

    with mock.patch.object(tk.Tokenizer, "__init__", mock_init):
        return tk.Tokenizer()


@pytest.mark.parametrize(
    "text,has_more_tokens", [
        ([""], False), 
        (["let x = 1"], True), 
        (["do foo()"], True),
        (["let x = x + 1  // Why are we doing this?"], True),
        (["", "let x = 1;"], True)
    ]
)
def test_has_more_tokens(
    tokenizer: tk.Tokenizer, text: str, has_more_tokens: bool
):
    tokenizer.input_lines = text
    tokenizer.current_line = text[0]
    tokenizer.loaded_line = True
    assert tokenizer.has_more_tokens() == has_more_tokens


@pytest.mark.parametrize(
    "text,tokens", [
        (["    } "], ["}"],),
        (["{ // Hello world"], ["{"]),
        (['"hello"'], ['"hello"']),
        (["let x = x + 1"], ["let", "x", "=", "x", "+" , "1"]),
        (["\"hello world\""], ["\"hello world\""]),
        (
            [
                "class Square {", 
                "field int x, y;  // comment", 
                "field int size;"
            ],
            [
                "class", "Square", "{", 
                "field", "int", "x", "," , "y", ";",
                "field", "int", "size", ";"
            ],
        ),
    ]
)
def test_advance(tokenizer: tk.Tokenizer, text: list[str], tokens: list[str]):
    tokenizer.input_lines = text

    while tokenizer.has_more_tokens():
        token = tokens.pop(0)
        tokenizer.advance()
        assert tokenizer.current_token == token, (
            tokenizer.current_token, token
        )

@pytest.mark.parametrize(
    "token,expected_token_type", [
        ('let', "keyword"),
        ('+', "symbol"),
        ('foo', "identifier"),
        ('"foo"', "string_const"),
        ('3', "int_const"),
    ]
)
def test_token_type(
    tokenizer: tk.Tokenizer, token: str, expected_token_type: str
):
    tokenizer.input_lines = [token]
    tokenizer.advance()
    assert expected_token_type == tokenizer.token_type()


def test_keyword(tokenizer: tk.Tokenizer):
    tokenizer.input_lines = ["let"]
    tokenizer.advance()
    assert "let" == tokenizer.keyword()


def test_symbol(tokenizer: tk.Tokenizer):
    tokenizer.input_lines = [";"]
    tokenizer.advance()
    assert ";" == tokenizer.symbol()


def test_identifier(tokenizer: tk.Tokenizer):
    tokenizer.input_lines = ["foo"]
    tokenizer.advance()
    assert "foo" == tokenizer.identifier()


def test_int_val(tokenizer: tk.Tokenizer):
    tokenizer.input_lines = ["23"]
    tokenizer.advance()
    assert "23" == tokenizer.int_val()


def test_string_val(tokenizer: tk.Tokenizer):
    tokenizer.input_lines = ["\"hello world\""]
    tokenizer.advance()
    assert "hello world" == tokenizer.string_val()


def test_string_val_2(tokenizer: tk.Tokenizer):
    tokenizer.input_lines = [
        "\"Test 1: expected result: 5; actual result: \""
    ]
    tokenizer.advance()
    assert "Test 1: expected result: 5; actual result: " == tokenizer.string_val()

