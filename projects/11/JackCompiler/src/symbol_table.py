from multiprocessing.sharedctypes import Value
import typing as t

from JackCompiler.src import enums

class SymbolTable:
    
    symbol_kind_to_index_name = {
        enums.SymbolKindEnum.ARG: "arg_index",
        enums.SymbolKindEnum.VAR: "var_index",
        enums.SymbolKindEnum.FIELD: "field_index",
        enums.SymbolKindEnum.STATIC: "static_index"
    }

    def __init__(self):
        """
        Create a SymbolTable with no rows and all indices initialised to zero
        """
        self.reset()

    def reset(self):
        """
        Clear a SymbolTable, removing all rows and resetting all indices 
        to zero
        """
        self.rows: dict[
            t.Optional[
                dict[
                    str, t.Union[enums.VarTypeEnum, enums.SymbolKindEnum, int]
                ]
            ]
        ] = {}

        self.static_index = 0
        self.field_index = 0
        self.arg_index = 0
        self.var_index = 0

    def define(
        self, name: str, type_: enums.VarTypeEnum, kind: enums.SymbolKindEnum
    ):
        """
        Add a new row to the symbol table; we use the row name as the key to a
        dictionary for easier access
        """
        index_name = self.symbol_kind_to_index_name[kind]
        index_value = getattr(self, index_name)

        self.rows[name] = {
            "type": type_,
            "kind": kind,
            "index": index_value
        }
        
        self.__setattr__(index_name, index_value + 1)

    def var_count(self, kind: enums.SymbolKindEnum) -> int:
        """
        Return the number of rows with the supplied kind in the SymbolTable;
        this will be equivalent to the index number
        """
        return getattr(
            self, self.symbol_kind_to_index_name[kind]
        )

    def kind_of(self, name: str) -> enums.SymbolKindEnum:
        """
        Return the kind of the table entry with the given name"""
        return self._get_key_from_rows_with_name(name, "kind")
        
    def type_of(self, name: str) -> str:
        return self._get_key_from_rows_with_name(name, "type")                
    
    def index_of(self, name: str) -> int:
        return self._get_key_from_rows_with_name(name, "index")

    def _get_key_from_rows_with_name(self, name: str, key: str) -> t.Any:
        if row := self.rows.get(name):
            return row[key]
        raise ValueError(f"No entry with name {name}")     

