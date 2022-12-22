// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// We can do multiplication by instead using a loop to sum numbers. E.g., a * b can be
// interpreted as a + a + a +... b times

// Load R0 into
  @R0
  D=M
  @input
  M=D

// Load 0 into product
  @0
  D=A
  @product
  M=D

// Load R1 into count
  @R1
  D=M
  @count
  M=D

(LOOP)
  // If count <= 0, goto end
  @count
  D=M
  @STORE
  D;JLE

  // Otherwise add product to itself
  @input
  D=M
  @product
  M=M+D

  // Subtract 1 from count
  @count
  M=M-1

  @LOOP
  0;JMP

(STORE)
  @product
  D=M
  @R2
  M=D
  @END
  0;JMP

(END)
  @END
  0;JMP
