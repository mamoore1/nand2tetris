
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
                "A=M\n",
                f"M={op}M\n",
            ]

            self.destination.writelines(lines)
        elif command in double_argument_commands:
            # We need to pop one value
            
            op = double_argument_commands[command]

            # Problem: some commands are super simple (e.g., "add" = "+"), 
            # while others are more complicated (e.g., however we figure out what
            # eq is? Presumably with an eq jump? )

            lines = [
                "@SP\n",
                "A=M\n",
                "D=M\n",
                "@SP\n",
                "M=M-1\n",
                "A=M\n",
                f"M=D{op}M\n"
            ]

            self.destination.writelines(lines)

    def write_push_pop(
        self, command: WritableCommandEnum, segment: str, index: int
    ) -> None:
        
        try:
            WritableCommandEnum[command]
        except KeyError:
            raise KeyError(f"Command {command.name} is not writable.")

    def close(self):
        self.destination.close()
        
