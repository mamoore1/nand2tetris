"""Main file of the basic hack assembler; this is called by the user
and uses the parser and code modules to generate the correct .hack output file
"""

import argparse

import code
import asmparser


def main(path: str):
    parser = asmparser.Parser(path)

    output_lines = []
    while parser.has_more_lines:
        parser.advance()
        if parser.instruction_type == asmparser.InstructionTypeEnum.A_INSTRUCTION:
            symbol = parser.symbol
            binary_symbol = bin(int(symbol)).removeprefix("0b").zfill(16)
            output_lines.append(f"{binary_symbol}\n")
        else:
            output_lines.append(
                f"111{code.comp(parser.comp)}{code.dest(parser.dest)}{code.jump(parser.jump)}\n"
            )

    file_path = path.removesuffix(".asm")
    with open(f"{file_path}.hack", "w") as f:
        f.writelines(output_lines)
    

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Convert .asm files into .hack binary files"
    )
    argparser.add_argument("path", type=str)

    args = argparser.parse_args()
    main(args.path)
