import enum
import typing

class AutoStringEnum(str, enum.Enum):
    
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[typing.Any]
    ) -> str:
        return name


class TokenTypeEnum(AutoStringEnum):
    KEYWORD = enum.auto()
    SYMBOL = enum.auto()
    IDENTIFIER = enum.auto()
    INT_CONST = enum.auto()
    STRING_CONST = enum.auto()


class KeywordEnum(AutoStringEnum):
    CLASS = enum.auto()
    CONSTRUCTOR = enum.auto()
    FUNCTION = enum.auto()
    METHOD = enum.auto()
    FIELD = enum.auto()
    STATIC = enum.auto()
    VAR = enum.auto()
    INT = enum.auto()
    CHAR = enum.auto()
    BOOLEAN = enum.auto()
    VOID = enum.auto()
    TRUE = enum.auto()
    FALSE = enum.auto()
    NULL = enum.auto()
    THIS = enum.auto()
    LET = enum.auto()
    DO = enum.auto()
    IF = enum.auto()
    ELSE = enum.auto()
    WHILE = enum.auto()
    RETURN = enum.auto()


class SymbolKindEnum(AutoStringEnum):
    STATIC = enum.auto()
    FIELD = enum.auto()
    ARG = enum.auto()
    VAR = enum.auto()


class SymbolCategoryEnum(AutoStringEnum):
    STATIC = enum.auto()
    FIELD = enum.auto()
    ARG = enum.auto()
    VAR = enum.auto()
    CLASS = enum.auto()
    SUBROUTINE = enum.auto()


class VarTypeEnum(AutoStringEnum):
    INT = enum.auto()
    STR = enum.auto()
    BOOLEAN = enum.auto()


class SegmentEnum(AutoStringEnum):
    CONSTANT = enum.auto()
    ARGUMENT = enum.auto()
    LOCAL = enum.auto()
    STATIC = enum.auto()
    THIS = enum.auto()
    THAT = enum.auto()
    POINTER = enum.auto()
    TEMP = enum.auto()


class ArithmentCommandEnum(AutoStringEnum):
    ADD = enum.auto()
    SUB = enum.auto()
    NEG = enum.auto()
    EQ = enum.auto()
    GT = enum.auto()
    LT = enum.auto()
    AND = enum.auto()
    OR = enum.auto()
    NOT = enum.auto()
