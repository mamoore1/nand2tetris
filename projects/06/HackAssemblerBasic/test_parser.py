
from HackAssemblerBasic.asmparser import InstructionTypeEnum, Parser

def test_parser_flow():
    """Use the parser to load the file and go through all the lines"""

    assembly = [
        "// Load 1\n",
        "@1\n",
        "D=A\n",
        "// Load 2\n",
        "@2\n",
        "D=D+A\n",
        "\n",
        "@3\n",
        "M=D\n",
        "@4\n",
        "0;JMP\n",
    ]

    with open("test.asm", mode="w") as f:
        f.writelines(assembly)

    parser = Parser("test.asm")
    assert parser.lines == assembly
    assert parser.num_lines == len(assembly)

    # Parser starts without any instructions loaded
    parser.advance()
    assert parser.has_more_lines
    assert parser.instruction_type == InstructionTypeEnum.A_INSTRUCTION
    assert parser.symbol == "1"
    
    parser.advance()
    assert parser.instruction_type == InstructionTypeEnum.C_INSTRUCTION
    assert parser.dest == "D"
    assert parser.comp == "A"
    assert parser.jump == None

    parser.advance()
    assert parser.has_more_lines
    assert parser.instruction_type == InstructionTypeEnum.A_INSTRUCTION
    assert parser.symbol == "2"
    
    parser.advance()
    assert parser.instruction_type == InstructionTypeEnum.C_INSTRUCTION
    assert parser.dest == "D"
    assert parser.comp == "D+A"
    assert parser.jump == None

    parser.advance()
    assert parser.has_more_lines
    assert parser.instruction_type == InstructionTypeEnum.A_INSTRUCTION
    assert parser.symbol == "3"
    
    parser.advance()
    assert parser.instruction_type == InstructionTypeEnum.C_INSTRUCTION
    assert parser.dest == "M"
    assert parser.comp == "D"
    assert parser.jump == None

    parser.advance()
    assert parser.has_more_lines
    assert parser.instruction_type == InstructionTypeEnum.A_INSTRUCTION
    assert parser.symbol == "4"
    
    parser.advance()
    assert parser.instruction_type == InstructionTypeEnum.C_INSTRUCTION
    assert parser.dest == None
    assert parser.comp == "0"
    assert parser.jump == "JMP"
