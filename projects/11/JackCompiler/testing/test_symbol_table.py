
import pytest

from JackCompiler.src import enums
from JackCompiler.src import symbol_table as st


@pytest.fixture
def symbol_table():
    return st.SymbolTable()


def test___init__():
    """Check that a new symbol table is created with all indices == 0
    and an empty list of rows"""
    symbol_table = st.SymbolTable()

    assert symbol_table.static_index == 0
    assert symbol_table.field_index == 0
    assert symbol_table.arg_index == 0
    assert symbol_table.var_index == 0
    assert symbol_table.rows == {}


def test_reset(symbol_table: st.SymbolTable):
    """Check that the symbol table is emptied and all the indices are set
    to 0"""
    
    symbol_table.define(
        name="argtest0", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )
    symbol_table.define(
        name="vartest0", type_=enums.VarTypeEnum.STR, kind=enums.SymbolKindEnum.VAR
    )
    symbol_table.reset()

    assert symbol_table.static_index == 0
    assert symbol_table.field_index == 0
    assert symbol_table.arg_index == 0
    assert symbol_table.var_index == 0
    assert symbol_table.rows == {}


def test_define(symbol_table: st.SymbolTable):

    symbol_table.define(
        name="argtest0", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )
    symbol_table.define(
        name="vartest0", type_=enums.VarTypeEnum.STR, kind=enums.SymbolKindEnum.VAR
    )
    symbol_table.define(
        name="fieldtest0", 
        type_=enums.VarTypeEnum.BOOLEAN, 
        kind=enums.SymbolKindEnum.FIELD 
    )
    symbol_table.define(
        name="statictest0", 
        type_=enums.VarTypeEnum.INT, 
        kind=enums.SymbolKindEnum.STATIC
    )
    
    assert {
        "argtest0": {
            "type": enums.VarTypeEnum.INT, 
            "kind": enums.SymbolKindEnum.ARG, 
            "index": 0
        },
        "vartest0": {
            "type": enums.VarTypeEnum.STR, 
            "kind": enums.SymbolKindEnum.VAR, 
            "index": 0
        },
        "fieldtest0": {
            "type": enums.VarTypeEnum.BOOLEAN, 
            "kind": enums.SymbolKindEnum.FIELD, 
            "index": 0
        },
        "statictest0": {
            "type": enums.VarTypeEnum.INT, 
            "kind": enums.SymbolKindEnum.STATIC, 
            "index": 0
        },
    } == symbol_table.rows 

    symbol_table.define(
        name="argtest1", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )
    symbol_table.define(
        name="vartest1", type_=enums.VarTypeEnum.STR, kind=enums.SymbolKindEnum.VAR
    )

    assert {
        "argtest1": {
            "type": enums.VarTypeEnum.INT, 
            "kind": enums.SymbolKindEnum.ARG, 
            "index": 1
        },
        "vartest1": {
            "type": enums.VarTypeEnum.STR, 
            "kind": enums.SymbolKindEnum.VAR, 
            "index": 1
        }
    } | symbol_table.rows == symbol_table.rows

    assert 2 == symbol_table.arg_index
    assert 2 == symbol_table.var_index
    assert 1 == symbol_table.field_index
    assert 1 == symbol_table.static_index 


def test_var_count(symbol_table: st.SymbolTable):
    
    symbol_table.define(
        name="argtest0", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )
    symbol_table.define(
        name="argtest1", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )
    symbol_table.define(
        name="argtest2", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )

    symbol_table.define(
        name="vartest0", type_=enums.VarTypeEnum.STR, kind=enums.SymbolKindEnum.VAR
    )
    symbol_table.define(
        name="vartest1", type_=enums.VarTypeEnum.STR, kind=enums.SymbolKindEnum.VAR
    )

    assert 3 == symbol_table.var_count(enums.SymbolKindEnum.ARG)
    assert 2 == symbol_table.var_count(enums.SymbolKindEnum.VAR)
    assert 0 == symbol_table.var_count(enums.SymbolKindEnum.FIELD)


def test_kind_of(symbol_table: st.SymbolTable):

    symbol_table.define(
        name="argtest", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )

    assert enums.SymbolKindEnum.ARG == symbol_table.kind_of("argtest")


def test_type_of(symbol_table: st.SymbolTable):

    symbol_table.define(
        name="argtest", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )

    assert enums.VarTypeEnum.INT == symbol_table.type_of("argtest")


def test_index_of(symbol_table: st.SymbolTable):

    symbol_table.define(
        name="argtest", type_=enums.VarTypeEnum.INT, kind=enums.SymbolKindEnum.ARG
    )

    assert 0 == symbol_table.index_of("argtest")
