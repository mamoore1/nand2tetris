from io import StringIO
from unittest import mock

import pytest

from JackCompiler.src import enums
from JackCompiler.src import vm_writer as vmw

@pytest.fixture
def vm_writer():
    """
    VMWriter for test cases; mocks the __init__ function so that it doesn't
    need to open an actual file and instead just uses a StringIO instance.
    """

    def mock_init(self):
        self.destination = StringIO()

    with mock.patch.object(vmw.VMWriter, "__init__", mock_init):
        writer = vmw.VMWriter()
        yield writer
        writer.destination.close()


@pytest.mark.parametrize(
    "segment,index,expected", [
        (enums.SegmentEnum.CONSTANT, 2, "push constant 2\n"),
        (enums.SegmentEnum.THAT, 1, "push that 1\n"),
    ]
)
def test_write_push(
    vm_writer: vmw.VMWriter, segment: str, index: int, expected: str
):
    """Check that we can correctly push from different segments"""

    vm_writer.write_push(segment, index)
    assert expected == vm_writer.destination.getvalue()


@pytest.mark.parametrize(
    "segment,index,expected", [
        (enums.SegmentEnum.CONSTANT, 2, "pop constant 2\n"),
        (enums.SegmentEnum.THAT, 1, "pop that 1\n"),
    ]
)
def test_write_pop(
    vm_writer: vmw.VMWriter, segment: str, index: int, expected: str
):
    """Check that we can correctly push from different segments"""

    vm_writer.write_pop(segment, index)
    assert expected == vm_writer.destination.getvalue()


@pytest.mark.parametrize(
    "command, expected", [
        (enums.ArithmentCommandEnum.ADD, "add\n"),
        (enums.ArithmentCommandEnum.NOT, "not\n"),
    ]
)
def test_write_arithmetic(
    vm_writer: vmw.VMWriter, command: str, expected: str
):
    vm_writer.write_arithmetic(command)
    assert expected == vm_writer.destination.getvalue()


def test_write_label(vm_writer: vmw.VMWriter):
    label = "Foo$bar.baz0"
    vm_writer.write_label(label)
    assert f"label {label}\n" == vm_writer.destination.getvalue()


def test_write_goto(vm_writer: vmw.VMWriter):
    goto = "Foobar"
    vm_writer.write_goto(goto)
    assert f"goto {goto}\n" == vm_writer.destination.getvalue()


def test_write_if(vm_writer: vmw.VMWriter):
    if_label = "L1"
    vm_writer.write_if(if_label)
    assert f"if-goto {if_label}\n" == vm_writer.destination.getvalue()


@pytest.mark.parametrize(
    "name,n_args", [("test", 3), ("foo", 1), ("bar", 0)]
)
def test_write_call(vm_writer: vmw.VMWriter, name: str, n_args: int):

    vm_writer.write_call(name, n_args)
    assert f"call {name} {n_args}\n" == vm_writer.destination.getvalue()


@pytest.mark.parametrize(
    "name,n_vars", [("test", 3), ("foo", 1), ("bar", 0)]
)
def test_write_function(vm_writer: vmw.VMWriter, name: str, n_vars: int):

    vm_writer.write_function(name, n_vars)
    assert f"function {name} {n_vars}\n" == vm_writer.destination.getvalue()


def test_write_return(vm_writer: vmw.VMWriter):
    vm_writer.write_return()
    assert "return\n" == vm_writer.destination.getvalue()
