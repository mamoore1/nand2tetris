import argparse
from io import TextIOWrapper
import os

import enums
import tokenizer as tk
import compilation_engine as ce

def main(path: str) -> None:

    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".jack"):
                input_path = f"{path}/{file}"
                tokenizer = tk.Tokenizer(input_path)
                output_path = input_path.replace(".jack", ".xml")

                compilation_input = tokens_to_list(tokenizer)

                engine = ce.ComplilationEngine(
                    input_strings=compilation_input,
                    output_path = output_path
                )
                engine.compile_class(0)
                engine.close

    elif os.path.isfile(path):
        tokenizer = tk.Tokenizer(path)
        output_path = path.replace(".jack", ".xml")

        compilation_input = tokens_to_list(tokenizer)
        engine = ce.ComplilationEngine(
            input_strings=compilation_input,
            output_path = output_path
        )
        engine.compile_class(0)
        engine.close

    else: 
        raise TypeError("Provided path is neither a file or a folder")

                
def print_tokens(tokenizer: tk.Tokenizer, f: TextIOWrapper) -> None:
    f.write("<tokens>\n")
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        token_type = tokenizer.token_type()

        type_to_token = {
            enums.TokenTypeEnum.KEYWORD: tokenizer.keyword,
            enums.TokenTypeEnum.SYMBOL: tokenizer.symbol,
            enums.TokenTypeEnum.IDENTIFIER: tokenizer.identifier,
            enums.TokenTypeEnum.STRING_CONST: tokenizer.string_val,
            enums.TokenTypeEnum.INT_CONST: tokenizer.int_val,
        }
        f.write(
            f"<{token_type.value}> {type_to_token[token_type]()}"
            f" </{token_type.value}>\n"
        )
    # Final token
    token_type = tokenizer.token_type()
    f.write(
            f"<{token_type.value}> {type_to_token[token_type]()}"
            f" </{token_type.value}>\n"
        )

    f.write("</tokens>\n")


def tokens_to_list(tokenizer: tk.Tokenizer) -> list[str]:
    tokens = []
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        token_type = tokenizer.token_type()

        type_to_token = {
            enums.TokenTypeEnum.KEYWORD: tokenizer.keyword,
            enums.TokenTypeEnum.SYMBOL: tokenizer.symbol,
            enums.TokenTypeEnum.IDENTIFIER: tokenizer.identifier,
            enums.TokenTypeEnum.STRING_CONST: tokenizer.string_val,
            enums.TokenTypeEnum.INT_CONST: tokenizer.int_val,
        }
        tokens.append(
            f"<{token_type.value}> {type_to_token[token_type]()}"
            f" </{token_type.value}>\n"
        )
    # Final token
    token_type = tokenizer.token_type()
    tokens.append(
            f"<{token_type.value}> {type_to_token[token_type]()}"
            f" </{token_type.value}>\n"
        )

    return tokens


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="v1: Convert *.jack files into a *T.xml file taggging all"
        " the tokens correctly"
    )
    argparser.add_argument("path", type=str)
    args = argparser.parse_args()
    main(args.path)
