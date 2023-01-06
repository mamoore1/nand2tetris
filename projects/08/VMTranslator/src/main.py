import argparse
import os

import codewriter
import vmparser 

def main(path: str):

    if os.path.isdir(path):
        filename = path.split("/")[-1]
        output_path = f"{path}/{filename}.asm"
        writer = codewriter.CodeWriter(output_path)

        for file in os.listdir(path):
            if file.endswith(".vm"):
                parser = vmparser.VMParser(f"{path}/{file}")
                writer.set_file_name(file.removesuffix(".vm"))
                write_lines(parser, writer)

    elif os.path.isfile(path):
        parser = vmparser.VMParser(path)
        output_path = path.replace(".vm", ".asm")
        writer = codewriter.CodeWriter(output_path)
        write_lines(parser, writer)
    else:
        raise TypeError("Provided path is neither a file or a folder")

    writer.close()


def write_lines(parser, writer) -> None:
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
        elif parser.command_type == vmparser.CommandTypeEnum.C_LABEL:
            writer.write_label(parser.arg1)
        elif parser.command_type == vmparser.CommandTypeEnum.C_GOTO:
            writer.write_goto(parser.arg1)
        elif parser.command_type == vmparser.CommandTypeEnum.C_IF:
            writer.write_if(parser.arg1)
        else:
            raise NotImplementedError(
                f"Translator cannot handle command: {parser.command_type.name}"
            )


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Convert .vm files into .asm files"
    )
    argparser.add_argument("path", type=str)

    args = argparser.parse_args()
    main(args.path)

