
import pytest

from HackAssemblerBasic.code import comp
from HackAssemblerBasic.code import dest
from HackAssemblerBasic.code import jump

@pytest.mark.parametrize(
    "mnemonic,binary_code", [
        ("0", "0101010"),
        ("1", "0111111"),
        ("-1", "0111010"),
        ("D", "0001100"),
        ("A", "0110000"),
        ("!D", "0001101"),
        ("!A", "0110001"),
        ("-D", "0001111"),
        ("-A", "0110011"),
        ("D+1", "0011111"),
        ("A+1", "0110111"),
        ("D-1", "0001110"),
        ("A-1", "0110010"),
        ("D+A", "0000010"),
        ("D-A", "0010011"),
        ("A-D", "0000111"),
        ("D&A", "0000000"),
        ("D|A", "0010101"),
        ("M", "1110000"),
        ("!M", "1110001"),
        ("M+1", "1110111"),
        ("M-1", "1110010"),
        ("D+M", "1000010"),
        ("D-M", "1010011"),
        ("M-D", "1000111"),
        ("D&M", "1000000"),
        ("D|M", "1010101"),
    ]
)
def test_comp(mnemonic: str, binary_code: str):
    """Check that comp correctly returns the binary values of the comp 
    instructions"""
    if len(binary_code) != 7:
        raise ValueError(
            f"Binary code should have 7 characters, had {len(binary_code)}"
        )

    assert binary_code == comp(mnemonic)


@pytest.mark.parametrize(
    "mnemonic,binary_code",
    [
        (None, "000"),
        ("M", "001"),
        ("D", "010"),
        ("DM", "011"),
        ("A", "100"),
        ("AM", "101"),
        ("AD", "110"),
        ("ADM", "111"),
    ]
)
def test_dest(mnemonic: str, binary_code: str):
    assert binary_code == dest(mnemonic)
    

@pytest.mark.parametrize(
    "mnemonic,binary_code",
    [
        (None,"000"),
        ("JGT","001"),
        ("JEQ","010"),
        ("JGE","011"),
        ("JLT","100"),
        ("JNE","101"),
        ("JLE","110"),
        ("JMP","111")
    ]
)
def test_jump(mnemonic: str, binary_code: str):
    assert binary_code == jump(mnemonic)
