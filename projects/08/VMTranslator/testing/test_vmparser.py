
from typing import Optional

import pytest

from VMTranslator.src.vmparser import CommandTypeEnum, VMParser

@pytest.mark.parametrize(
    "command,command_type,arg1,arg2", [
        ("push argument 1",CommandTypeEnum.C_PUSH,"argument",1),
        ("pop static 2",CommandTypeEnum.C_POP,"static",2),
        ("add",CommandTypeEnum.C_ARITHMETIC,"add",None),
        ("not",CommandTypeEnum.C_ARITHMETIC,"not",None),
        ("label foo", CommandTypeEnum.C_LABEL, "foo", None),
        ("goto foo", CommandTypeEnum.C_GOTO, "foo", None),
        ("if-goto foo", CommandTypeEnum.C_IF, "foo", None)
    ]
)
def test_vmparser_minimal(
    command: str, 
    command_type: CommandTypeEnum,
    arg1: str,
    arg2: Optional[str]
):
    """Check that the VMParser correctly reads these commands"""

    def mock_init(self):
        self.lines = [f"{command}\n"]
        self.current_line = -1
        self.command_type = None
        self.arg1 = None
        self.arg2 = None

    VMParser.__init__ = mock_init
    parser = VMParser()

    parser.advance()
    assert parser.command_type == command_type
    assert parser.arg1 == arg1
    assert parser.arg2 == arg2
