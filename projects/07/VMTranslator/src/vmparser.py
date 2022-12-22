from typing import Optional

from enum import auto, Enum

class CommandTypeEnum(str, Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()

    @staticmethod
    def _generate_next_value(name, start, count, last_values):
        return name


class VMParser:
    
    def __init__(self, path: str):
        with open(path) as f:
            self.lines: list[str] = f.readlines

        self.current_line: int = -1
        self.command_type: Optional[str] = None
        self.arg1: Optional[str] = None
        self.arg2: Optional[int] = None

    def advance(self) -> None:
        """Load the next valid line into the parser and set command_type, arg1
        and arg2 accordingly"""
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
            loaded_line = loaded_line.strip()
            if "//" in loaded_line:
                loaded_line = loaded_line.split("//")[0]
            
            line_parts = loaded_line.split(" ")
            if len(line_parts) == 1:
                self._handle_1_part_instruction(line_parts)
            elif len(line_parts) == 3:
                self._handle_3_part_instructions(line_parts)
            else:
                raise NotImplementedError(
                    f"Parser cannot handle argument {loaded_line} with"
                    f" {len(line_parts)} parts"
                )

    @property
    def has_more_lines(self) -> bool:
        return len(self.lines) > self.current_line
    
    def _is_valid_line(self, line: str) -> bool:
        """Ignore lines if they are either blank or only contain a comment"""
        line = line.strip()

        if (
            not line
            or line.startswith("//")
        ):
            return False

        return True

    def _handle_1_part_instruction(self, line_parts: list[str]) -> None:
        self.command_type = CommandTypeEnum.C_ARITHMETIC
        self.arg1 = line_parts[0]
        self.arg2 = None

    def _handle_3_part_instructions(self, line_parts: list[str]) -> None:
        self.arg1 = line_parts[1]
        self.arg2 = int(line_parts[2])
        if line_parts[0] == "push":
            self.command_type = CommandTypeEnum.C_PUSH
        elif line_parts[0] == "pop":
            self.command_type = CommandTypeEnum.C_POP
        else:
            raise NotImplementedError(
                f"Parser cannot handle instruction {line_parts[0]}"
            )

