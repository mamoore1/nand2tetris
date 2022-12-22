from . import main

def test_first_pass():
    assembly = [
        "// Load 0\n",
        "@0\n",
        "D=A\n",
        "(LOOP)\n",
        "@1\n",
        "D=D+A\n"
        "@LOOP\n",
        "0;JMP\n",
        "(END)\n",
        "@END\n",
        "0;JMP\n",
    ]

    with open("test.asm", mode="w") as f:
        f.writelines(assembly)

    symbol_table = main.first_pass("test.asm", {})
    assert symbol_table == {
        "END": "6",
        "LOOP": "2",
    }
