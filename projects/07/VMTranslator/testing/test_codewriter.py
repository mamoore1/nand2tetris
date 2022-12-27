from io import StringIO

from VMTranslator.src.codewriter import CodeWriter, WritableCommandEnum

import pytest


@pytest.mark.parametrize(
    "path,filename",
    [
        ("/home/mike/Test.vm","Test"),
        ("Foo.asm", "Foo"),
        ("Bar", "Bar"),
        ("hello/World.tst", "World"),
    ]
)
def test__determine_filename(path: str, filename: str):

    def mock_init(self):
        pass

    CodeWriter.__init__ = mock_init

    codewriter = CodeWriter()
    assert codewriter._determine_filename(path) == filename


@pytest.mark.parametrize(
    "vm_command,expected_asm", [
        (
            "add", 
            [
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M+D\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ),
        (
            "not", 
            [
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M\n",
                "D=!D\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ),
        (
            "or", 
            [
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M|D\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ),
        (
            "eq",
            [
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=D-M\n",
                "@FALSE_0\n",
                "D;JNE\n",
                "D=-1\n",
                "@CONTINUE_0\n",
                "0;JMP\n",
                "(FALSE_0)\n",
                "D=0\n",
                "@CONTINUE_0\n",
                "0;JMP\n",
                "(CONTINUE_0)\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        )
    ]
)
def test_write_arithmetic_single_command(
    vm_command: str, expected_asm: list[str]
):
    """Check that the CodeWriter writes the vm commands successfully"""
    
    def mock_init(self):
        self.destination = StringIO()
        self.bool_count = 0
        
    CodeWriter.__init__ = mock_init

    codewriter = CodeWriter()
    codewriter.write_arithmetic(vm_command)
    assert "".join(expected_asm) == codewriter.destination.getvalue()
    codewriter.close()


@pytest.mark.parametrize(
    "command,segment,index,expected_asm", [
        (
            WritableCommandEnum.C_PUSH, "that", 5, [
                "@5\n",
                "D=A\n",
                "@THAT\n",
                "A=M+D\n",
                "D=M\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ), 
        (
            WritableCommandEnum.C_POP, "argument", 1, [
                "@ARG\n",
                "D=M\n",
                "@1\n",
                "D=D+A\n",
                "@R13\n",
                "M=D\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M\n",
                "@R13\n",
                "A=M\n",
                "M=D\n",
            ]
        ),
        (
            WritableCommandEnum.C_PUSH, "local", 2, [
                "@2\n",
                "D=A\n",
                "@LCL\n",
                "A=M+D\n",
                "D=M\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ),
        (
            WritableCommandEnum.C_PUSH, "constant", 18, [
                "@18\n",
                "D=A\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ),
        (
            WritableCommandEnum.C_PUSH, "temp", 3, [
                "@3\n",
                "D=A\n",
                "@5\n",
                "A=D+A\n",
                "D=M\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ), 
        (
            WritableCommandEnum.C_PUSH, "pointer", 0, [
                "@THIS\n",
                "D=M\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ),
        (
            WritableCommandEnum.C_PUSH, "pointer", 1, [
                "@THAT\n",
                "D=M\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ),
        (
            WritableCommandEnum.C_PUSH, "static", 3, [
                "@Foo.3\n",
                "D=M\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
        ),
        (
            WritableCommandEnum.C_POP, "static", 18, [
                "@Foo.18\n",
                "D=A\n",
                "@R13\n",
                "M=D\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M\n",
                "@R13\n",
                "A=M\n",
                "M=D\n",
            ]
        )
    ]
)
def test_write_push_pop(
    command: WritableCommandEnum, 
    segment: str, 
    index: int, 
    expected_asm: list[str]
):
    """Check that the CodeWriter writes the vm command successfully"""
    def mock_init(self):
        self.destination = StringIO()
        self.bool_count = 0
        self.filename = "Foo"

    CodeWriter.__init__ = mock_init

    codewriter = CodeWriter()
    codewriter.write_push_pop(command, segment, index)
    assert "".join(expected_asm) == codewriter.destination.getvalue()
    codewriter.close()

    