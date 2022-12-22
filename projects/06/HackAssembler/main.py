"""Main file of the basic hack assembler; this is called by the user
and uses the parser and code modules to generate the correct .hack output file
"""

import argparse

import code
import asmparser


def main(path: str):

    symbol_table = {
        "R0": "0",
        "R1": "1",
        "R2": "2",
        "R3": "3",
        "R4": "4",
        "R5": "5",
        "R6": "6",
        "R7": "7",
        "R8": "8",
        "R9": "9",
        "R10": "10",
        "R11": "11",
        "R12": "12",
        "R13": "13",
        "R14": "14",
        "R15": "15",
        "SP": "0",
        "LCL": "1",
        "ARG": "2",
        "THIS": "3",
        "THAT": "4",
        "SCREEN": "16384",
        "KBD": "24576",
    }

    # This is bad design; we should really just load the file once
    symbol_table: dict[str, str] = first_pass(path, symbol_table)

    # Generate the code using the symbol table
    second_pass(path, symbol_table)


def first_pass(path: str, symbol_table: dict[str, str]) -> dict[str, str]:

    parser = asmparser.Parser(path)
    line_count = -1
    while parser.has_more_lines:
        parser.advance()
        
        if parser.instruction_type in (
            asmparser.InstructionTypeEnum.A_INSTRUCTION,
            asmparser.InstructionTypeEnum.C_INSTRUCTION
        ):
            line_count += 1
        else:
            symbol_table[parser.symbol] = str(line_count + 1)

    return symbol_table


def second_pass(path: str, symbol_table: dict[str, str]):
    parser = asmparser.Parser(path)

    symbol_ram_address = 16

    output_lines = []
    while parser.has_more_lines:
        parser.advance()
        if parser.instruction_type == asmparser.InstructionTypeEnum.A_INSTRUCTION:
            symbol = parser.symbol
            
            if not symbol.isnumeric():
                symbol_location = symbol_table.get(symbol, None)
                
                if not symbol_location:
                    symbol_table[symbol] = str(symbol_ram_address)
                    symbol = symbol_ram_address
                    
                    symbol_ram_address += 1
                else:
                    symbol = symbol_location

            binary_symbol = bin(int(symbol)).removeprefix("0b").zfill(16)
            output_lines.append(f"{binary_symbol}\n")
                
        elif parser.instruction_type == asmparser.InstructionTypeEnum.L_INSTRUCTION:
            continue 
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
