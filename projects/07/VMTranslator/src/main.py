import argparse

import codewriter
import vmparser 

def main(path: str):
    parser = vmparser.VMParser(path)

    output_path = path.replace(".vm", ".asm")
    writer = codewriter.CodeWriter(output_path)

    while parser.has_more_lines:
        parser.advance()
        if parser.command_type == vmparser.CommandTypeEnum.C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1)
        elif parser.command_type in (
            vmparser.CommandTypeEnum.C_POP, vmparser.CommandTypeEnum.C_PUSH
        ):
            writer.write_push_pop(
                command=parser.command_type,
                segment=parser.arg1,
                index=parser.arg2
            )
        else:
            raise NotImplementedError(
                f"Translator cannot handle command: {parser.command_type.name}"
            )
    
    writer.close()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Convert .vm files into .asm files"
    )
    argparser.add_argument("path", type=str)

    args = argparser.parse_args()
    main(args.path)

