
from enum import auto, Enum


class WritableCommandEnum(str, Enum):
    C_PUSH = auto()
    C_POP = auto()
    
    @staticmethod
    def _generate_next_value(name, start, count, last_values):
        return name


PUSH_D = [
    "@SP\n",
    "A=M\n",
    "M=D\n",
    "@SP\n",
    "M=M+1\n",
]
POP_D = [
    "@SP\n",
    "M=M-1\n",
    "A=M\n",
    "D=M\n",       
]
POP_INTO_ADDRESS = [
    "@R13\n",
    "M=D\n",
    *POP_D,
    "@R13\n",
    "A=M\n",
    "M=D\n",
]
ONE_LINE_DOUBLE_ARG_COMMANDS = {
    "add": "+",
    "sub": "-",
    "and": "&",
    "or": "|",
}
SEGMENT_TO_ADDRESS_MAP = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}
            

class CodeWriter:    

    def __init__(self, path: str):
        self.destination = open(path, "w")
        self.filename = self._determine_filename(path)
        # Keep track of how many boolean checks there have been
        self.bool_count = 0

    def write_arithmetic(self, command: str) -> None:
        """Convert an arithmetic command into a series of instructions."""

        single_argument_commands: dict[str, str] = {"neg": "-", "not": "!"}
        if command in single_argument_commands:
            op = single_argument_commands[command]
            lines = [*POP_D, f"D={op}D\n",*PUSH_D,]
        else:
            lines = [*POP_D, "@SP\n", "M=M-1\n", "A=M\n",]
            op = ONE_LINE_DOUBLE_ARG_COMMANDS.get(command)
            if op:
                lines.extend([f"D=M{op}D\n", *PUSH_D,])
            else:
                lines = self._handle_multiline_commands(command) 
                if not lines:
                    raise NotImplementedError(
                        f"Functionality for command {command} has not been"
                        " implemented."
                    )
        self.destination.writelines(lines)

    def write_push_pop(
        self, command: WritableCommandEnum, segment: str, index: int
    ) -> None:
        """Convert a push or pop command to assembly and write to file."""

        command = WritableCommandEnum[command.name]

        if command == WritableCommandEnum.C_POP:
            lines = self._handle_pop(segment, index)
        elif command == WritableCommandEnum.C_PUSH:
            lines = self._handle_push(segment, index)
        else:
            raise ValueError(
                f"Expected writable command, received: {command.name}"
            )

        self.destination.writelines(lines)

    def _determine_filename(self, path: str):
        return path.split("/")[-1].split(".")[0]

    def _handle_multiline_commands(self, command: str) -> list[str]:

        equality_command_to_false_jump_map = {
            "eq": "JNE",
            "lt": "JLE",  # This looks the wrong way round because of stack
            "gt": "JGE",  # FILO behaviour
        }

        if not (jump := equality_command_to_false_jump_map.get(command, None)):
            raise ValueError(
                f"Received invalid command {command}"
            )
        else:
            lines = [
                *POP_D,
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
                *PUSH_D,
            ]
            self.bool_count += 1
            return lines

    def _handle_pop(self, segment: str, index: int) -> list[str]:
        if segment == "temp":
            lines = [
                "@5\n",
                "D=A\n",
                f"@{index}\n",
                "D=D+A\n",
            ]
        elif segment == "pointer":
            address = "THIS" if index == 0 else "THAT"
            lines = [
                f"@{address}\n",
                "D=A\n",
            ]
        elif segment == "static":
            lines = [
                f"@{self.filename}.{index}\n",
                "D=A\n",
            ]
        else:
            lines = [
                f"@{SEGMENT_TO_ADDRESS_MAP[segment]}\n",
                "D=M\n",
                f"@{index}\n",
                "D=D+A\n",
            ]
        # Store the address in R13, then Pop SP into address in R13
        lines.extend(POP_INTO_ADDRESS)
        return lines

    def _handle_push(self, segment: str, index: int) -> list[str]:
        if segment == "constant":
            lines = [
                f"@{index}\n",
                "D=A\n",
            ]
        elif segment == "temp":
            lines = [
                f"@{index}\n",
                "D=A\n",
                "@5\n",     # "temp" represents r5-12
                "A=D+A\n",
                "D=M\n",
            ]
        elif segment == "pointer":
            address = "THIS" if index == 0 else "THAT"
            lines = [
                f"@{address}\n",
                "D=M\n",
            ]
        elif segment == "static":
            lines = [
                f"@{self.filename}.{index}\n",
                "D=M\n",
            ]
        else:
            # Segment is mapped to a pre-allocated variable
            lines = [
                f"@{index}\n",
                "D=A\n",
                f"@{SEGMENT_TO_ADDRESS_MAP[segment]}\n",
                "A=M+D\n",
                "D=M\n",
            ]
        # Push to stack
        lines.extend(PUSH_D)
        return lines

    def close(self):
        end_loop = [
            "(END)\n",
            "@END\n",
            "0;JMP\n",
        ]
        self.destination.writelines(end_loop)
        self.destination.close()
        
