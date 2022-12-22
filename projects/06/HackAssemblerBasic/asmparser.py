
from enum import Enum


class InstructionTypeEnum(str, Enum):
    A_INSTRUCTION = "A_INSTRUCTION"
    C_INSTRUCTION = "C_INSTRUCTION"


class Parser:
    def __init__(self, path: str):
        with open(path) as f:
            self.lines: list[str] = f.readlines()
        
        self.num_lines = len(self.lines)
        self.current_line = 0

    def advance(self):
        
        if not self.has_more_lines:
            raise ValueError("No more lines to parse")

        self.current_line += 1
        loaded_line = self.lines[self.current_line]

        if not self._is_valid_line(loaded_line):
            if not self.has_more_lines:
                return
            else:
                self.advance()
        else:
            loaded_line = loaded_line.strip().replace(" ", "")
            if loaded_line.startswith("@"):
                self.instruction_type = InstructionTypeEnum.A_INSTRUCTION
                self.symbol = loaded_line[1:]
                self.dest = None
                self.comp = None
                self.jump = None
            else:
                self.instruction_type = InstructionTypeEnum.C_INSTRUCTION
                self.symbol = None
                
                dest = None
                jump = None
                if "=" in loaded_line:
                    dest = loaded_line.split("=")[0]
                if ";" in loaded_line:
                    jump = loaded_line.split(";")[-1]
                
                self.dest = dest
                self.comp = loaded_line.split("=")[-1].split(";")[0]
                self.jump = jump
                

    def _is_valid_line(self, line: str) -> bool:
        line = line.strip()
        if (
            not line
            or line.startswith("//")
        ):
            return False

        return True


    @property
    def has_more_lines(self):
        return len(self.lines) > self.current_line + 1


