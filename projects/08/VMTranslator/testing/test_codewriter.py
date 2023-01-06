from io import StringIO

from VMTranslator.src.codewriter import CodeWriter, WritableCommandEnum

import pytest

@pytest.fixture
def codewriter():
    def mock_init(self):
        self.destination = StringIO()
        self.bool_count = 0
        self.filename = "Foo"

    CodeWriter.__init__ = mock_init

    codewriter = CodeWriter()
    yield codewriter

    codewriter.close()
    


@pytest.mark.parametrize(
    "path,filename",
    [
        ("/home/mike/Test.vm","Test"),
        ("Foo.asm", "Foo"),
        ("Bar", "Bar"),
        ("hello/World.tst", "World"),
    ]
)
def test__determine_filename(path: str, filename: str, codewriter: CodeWriter):
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
    vm_command: str, expected_asm: list[str], codewriter: CodeWriter,
):
    """Check that the CodeWriter writes the vm commands successfully"""
    codewriter.write_arithmetic(vm_command)
    assert "".join(expected_asm) == codewriter.destination.getvalue()


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
    expected_asm: list[str],
    codewriter: CodeWriter,
):
    """Check that the CodeWriter writes the vm command successfully"""
    codewriter.write_push_pop(command, segment, index)
    assert "".join(expected_asm) == codewriter.destination.getvalue()

    
def test_write_label(codewriter: CodeWriter):
    """Check that the CodeWriter writes a label command successfully"""
    codewriter.write_label("foo")
    assert "(foo)\n" == codewriter.destination.getvalue()


def test_goto(codewriter: CodeWriter):
    """Check that the CodeWriter writes an unconditional goto correctly"""
    codewriter.write_goto("foo")
    assert "@foo\n0;JMP\n" == codewriter.destination.getvalue()


def test_if(codewriter: CodeWriter):
    """Check that the CodeWriter writes conditional gotos"""
    expected_asm = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@foo",
        "D;JNE\n",
    ]
    
    codewriter.write_if("foo")
    assert "\n".join(expected_asm) == codewriter.destination.getvalue()


def test_set_file_name(codewriter: CodeWriter):
    codewriter.set_file_name("foo")
    assert codewriter.filename == "foo"


def test_write_function(codewriter: CodeWriter):    
    
    push_zero = ["@SP", "A=M", "M=0", "@SP", "M=M+1",]
    expected_asm = ["(Foo.bar)",]

    num_args = 3
    for _ in range(num_args):
        expected_asm.extend(push_zero)
    
    codewriter.set_file_name("Foo")
    codewriter.write_function("bar", 3)
    assert "\n".join(expected_asm) + "\n" == codewriter.destination.getvalue()


@pytest.mark.skip(reason="Not implemented")
def test_write_call(codewriter: CodeWriter):

    num_args = 2

    expected_asm = [
        "@Foo.bar$ret.0",  # Get address of return address and push to stack
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@LCL",  # Push address of local to stack
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@ARG",  # Push address of arg to stack
        "D=M", 
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@THIS",  # Push address of THIS to stack
        "D=M", 
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@THAT",  # Push address of THAT to stack
        "D=M", 
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@SP",  # Set new address of ARG to be SP - 5 - numArgs
        "D=M",
        "@5",
        "D=D-A"
        f"@{num_args}",
        "D=D-A",
        "@ARG",
        "M=D",
        "@SP",  # Set LCL to equal the current stack pointer
        "D=M",
        "@LCL",
        "M=D",
        "@Foo.bar",  # Call function
        "0;JMP",
        "(Foo.bar$ret.0)\n",  # Define return label
    ]

    codewriter.set_file_name("Foo")
    codewriter.write_call("bar", num_args)
    assert "\n".join(expected_asm) == codewriter.destination.getvalue()


def test_write_return(codewriter: CodeWriter):

    expected_asm = [
        "@LCL",
        "D=A",
        "@5",  # push temp 0
        "M=D",
        "@5",
        "A=D-A",
        "D=M",
        "@6",  # push temp 1
        "M=D",
        "@ARG", # pop arg 0; I think the version of this in my notes is wrong,
        # so redo it
    ]


    codewriter.set_file_name("Foo")
    codewriter.write_return()
    assert "\n".join(expected_asm) == codewriter.destination.getvalue()
