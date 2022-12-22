from io import StringIO

from mimesis import Code
from VMTranslator.src.codewriter import CodeWriter

import pytest

@pytest.mark.parametrize(
    "vm_command,expected_asm", [
        (
            "add", 
            [
                "@SP\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "M=D+M\n"
            ]
        ),
        (
            "not", 
            [
                "@SP\n",
                "A=M\n",
                "M=!M\n",
            ]
        ),
        (
            "or", 
            [
                "@SP\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "M=D|M\n",
            ]
        ),
        (
            "lt", 
            [
                "@SP\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "M=D|M\n",
            ]
        )
    ]
)
def test_write_arithmetic(vm_command: str, expected_asm: list[str]):
    """Check that the CodeWriter writes the vm commands successfully"""
    
    def mock_init(self):
        self.destination = StringIO()

    CodeWriter.__init__ = mock_init

    codewriter = CodeWriter()
    codewriter.write_arithmetic(vm_command)
    assert codewriter.destination.getvalue() == "".join(expected_asm)
    codewriter.close()

@pytest.mark.parametrize(
    "vm_command,expected_asm", [
        ("push this 3", ""),
        ("pop argument 1", ""),
        ("push static 2", ""),
    ]
)
def test_write_push_pop(vm_command: str, expected_asm: str):
    """Check that the CodeWriter writes the vm command successfully"""
    pass