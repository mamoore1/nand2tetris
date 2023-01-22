import enum
import typing

class AutoStringEnum(str, enum.Enum):
    
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[typing.Any]
    ) -> str:
        return name


class TokenTypeEnum(str, enum.Enum):
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"


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