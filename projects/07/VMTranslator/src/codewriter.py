
from enum import auto, Enum


class WritableCommandEnum(str, Enum):
    C_PUSH = auto()
    C_POP = auto()
    
    @staticmethod
    def _generate_next_value(name, start, count, last_values):
        return name


class CodeWriter:
    def __init__(self, path: str):
        self.destination = open(path, "w")
        self.filename = self._determine_filename(path)
        # Keep track of how many boolean checks there have been
        self.bool_count = 0

    def _determine_filename(self, path: str):
        return path.split("/")[-1].split(".")[0]

    def write_arithmetic(self, command: str) -> None:
        """Convert an arithmetic command into a series of instructions. Note
         that, although technically we need to pop instructions off the stack,
         we can in fact modify them in-place. E.g., for an add instruction, 
         instead of popping both values off the stack, we can pop the first and
         then do M=D op M. (I assume this will later come back to bite me, but 
         oh well)."""

        single_argument_commands: dict[str, str] = {"neg": "-", "not": "!"}
        double_argument_commands: dict[str, str] = {
            "add": "+", 
            "sub": "-", 
            "eq": "=", 
            "gt": "", 
            "lt": "", 
            "and": "&", 
            "or": "|",
        }

        if command in single_argument_commands:
            # We can operate inplace on the stack
            # pop the command

            op = single_argument_commands[command]

            lines = [
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                f"M={op}M\n",
                "@SP\n",
                "M=M+1\n",
            ]

            self.destination.writelines(lines)
        elif command in double_argument_commands:
            # We need to pop one value
            
            lines = [
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
            ]
            
            simple_commands = {
                "add": "+",
                "sub": "-",
                "and": "&",
                "or": "|",
            }

            op = simple_commands.get(command)
            if op:
                next_line = f"M=M{op}D\n"
                lines.append(next_line)
                lines.extend(
                    ["@SP\n", "M=M+1\n",]
                )
            else:
                lines = self._handle_multiline_commands(command) 
                if not lines:
                    raise NotImplementedError(
                        f"Functionality for command {command} has not been"
                        " implemented."
                    )


            self.destination.writelines(lines)


    def _handle_multiline_commands(self, command: str) -> list[str]:

        equality_command_to_false_jump_map = {
            "eq": "JNE",
            "lt": "JLE",  # This seem the wrong way round because of stack
            "gt": "JGE",  # FILO behaviour
        }

        if (jump := equality_command_to_false_jump_map.get(command, None)):
            lines = [
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                "D=D-M\n",
                f"@FALSE_{self.bool_count}\n",
                f"D;{jump}\n",
                "D=-1\n",
                f"@CONTINUE_{self.bool_count}\n",
                "0;JMP\n",
                f"(FALSE_{self.bool_count})\n",
                "D=0\n",
                f"@CONTINUE_{self.bool_count}\n",
                "0;JMP\n",
                f"(CONTINUE_{self.bool_count})\n",
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ]
            self.bool_count += 1
            return lines
        else:
            raise NotImplementedError(
                f"Command {command} has not been implemented"
            )


    def write_push_pop(
        self, command: WritableCommandEnum, segment: str, index: int
    ) -> None:
        
        try:
            command = WritableCommandEnum[command.name]
        except KeyError:
            raise KeyError(f"Command {command.name} is not writable.")

        segment_to_address_map = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }

        if command == WritableCommandEnum.C_POP:
            if segment == "temp":
                lines = [
                    "@5\n",
                    "D=A\n",
                    f"@{index}\n",
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
            elif segment == "pointer":
                address = "THIS" if index == 0 else "THAT"
                lines = [
                    f"@{address}\n",
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
            elif segment == "static":
                lines = [
                    f"@{self.filename}.{index}\n",
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
            else:
                lines = [
                    f"@{segment_to_address_map[segment]}\n",
                    "D=M\n",
                    f"@{index}\n",
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
        elif command == WritableCommandEnum.C_PUSH:

            if segment == "constant":
                lines = [
                    f"@{index}\n",
                    "D=A\n",
                    "@SP\n",
                    "A=M\n",
                    "M=D\n",
                    "@SP\n",
                    "M=M+1\n",
                ]
            elif segment == "temp":
                lines = [
                    f"@{index}\n",
                    "D=A\n",
                    "@5\n",     # "temp" represents r5-12
                    "A=D+A\n",
                    "D=M\n",
                    "@SP\n",
                    "A=M\n",
                    "M=D\n",
                    "@SP\n",
                    "M=M+1\n",
                ]
            elif segment == "pointer":
                address = "THIS" if index == 0 else "THAT"
                lines = [
                    f"@{address}\n",
                    "D=M\n",
                    "@SP\n",
                    "A=M\n",
                    "M=D\n",
                    "@SP\n",
                    "M=M+1\n",
                ]
            elif segment == "static":
                lines = [
                    f"@{self.filename}.{index}\n",
                    "D=M\n",
                    "@SP\n",
                    "A=M\n",
                    "M=D\n",
                    "@SP\n",
                    "M=M+1\n",
                ]
            
            else:
                lines = [
                    f"@{index}\n",
                    "D=A\n",
                    f"@{segment_to_address_map[segment]}\n",
                    "A=M+D\n",
                    "D=M\n",
                    "@SP\n",
                    "A=M\n",
                    "M=D\n",
                    "@SP\n",
                    "M=M+1\n",
                ]
            
        else:
            raise ValueError(
                f"Expected writable command, received: {command.name}"
            )

        self.destination.writelines(lines)

    def close(self):
        end_loop = [
            "(END)\n",
            "@END\n",
            "0;JMP\n",
        ]
        self.destination.writelines(end_loop)
        self.destination.close()
        
