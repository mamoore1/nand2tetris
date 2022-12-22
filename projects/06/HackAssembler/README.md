### Overview

This package contains the basic version of the HackAssembler, HackAssemblerBasic.
Unlike the full version, this version cannot handle symbol definitions (.e.g.,
(LOOP), x=1, etc.). Instead, this version does one pass over of the provided
.asm file, and then converts the included assembly into a binary .hack file.

### Converting instructions
The Hack system supports two types of instructions: A instructions, with the 
format @xxx, where xxx is a decimal value, and C instructions, which are symbolic
interpretations the binary instructions with the format dest=comp;jump.

A instructions convert into "0" followed by a 15-digit binary representation of
the code. C instructions convert into the format:
111accccccdddjjj, where a is the A register bit, cs indicate the op code of the computation,
ds indicate memory storage and js indicate jump rules.

As this suggests, the way to implement this is as follows:
    open the .asm file
    iterate through the lines
        for each line
            strip the whitespace and newline
            if the instruction begins with @, 
                convert it into "0" followed by the binary representation of xxx
            else:
                get the binary representation of the c instruction by calling
                dest(), comp() and jump()
            print this line into the destination file

The books suggests splitting these operation into a parser module and a code 
module; the former cleans the lines and breaks the instruction into its underlying
components, while the latter translates Hack mnemonics into their binary codes. 
For the basic assembler, the parser does not need to be able to handle 
symbolic references; for the full assembler it will.
