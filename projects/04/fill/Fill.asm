// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// This is gonna be a pain in the fucking ass because we have to operate with the keyboard and the screen. The keyboard starts at RAM adddress 24756 (0x6000). This is conveniently shortcutted to KBD; i.e., // when a keyboard key is pressed the 16 bit character code appears at RAM[KBD]; when no key is pressed, the code is 0. Luckily, we don't care what the key is; we just need to know that one is being
// pressed. So, when checking, we're just going to do @KBD,D=M, or whatever

// The second part is updating the screen. Because of the way our assembly works, we don't really have a convenient way to darken the screen at once; we're basically going to have to go through each screen 
// position and set it to a non-zero value. Part of the problem is going to be that we need to be able to change the squares back; e.g., we could be part way through darkening the screen when the key is 
// released; this would mean that we have to revert squares back. This suggests that we shouldn't do something sneaky like subtract one from 0 to get 1111111111111111, as this'll be a pain to revert back 
// (alternatively, we could write a loop that adds or subtracts 1 til we hit the state we want, but this seems annoying). This means it'll be simpler to just set the values explicitly; 
// i.e., m=00000000000000000 rather than D=1111111111111, D+1. I might be overcomplicating this: it just says that we need to make sure the screen is darkened or cleared if you hold the button long enough;
// This means that we can just complete the entire process before checking the button again

// The screen is 256 x 512; an 8K block of 16-bit words starting at 16384 (0x4000) trakcs their state; the beginning of this block can be accessed using the symbol SCREEN. Every row is 32 consecutive 
// 16-bit words. My suggestion, then, is that we basically just iterate through each row and update them accordingly. Annoyingly this will take a while, as there's 32 words per row and 256 rows; i.e., 8,192
// memory accesses, but i'm sure we'll survive

// Rough design:
// START
// Check whether a key is being pressed
// load KBD into data register
// if D is zero, jump to CLEAR
// if D is nonzero, jump to DARKEN

// CLEAR
//         load SCREEN into current_address
//     CLOOP
//         if current address is greater than 8192: jump to START
//         set memory at current_address = 0
//         add 16 to current_address
//         jump to CLOOP

// DARKEN
//         load SCREEN into current_address
//     DLOOP
//         if current_address is greater than 8192: jump to START
//         set memory at current_address = 1111111111111111
//         add 16 to current_address
//         jump to DLOOP

(START)
  @KBD
  D=M
  @CLEAR
  D;JEQ
  @DARKEN
  D;JNE

(CLEAR)
  @SCREEN
  D=A
  @current_address
  M=D
  (CLOOP)
    // Check still in screen address
    @current_address
    D=M
    @24576
    D=D-A
    @START
    D;JGE
    // Set memory to 0
    @0
    D=A
    @current_address
    A=M
    M=D
    // Update current address
    @1
    D=A
    @current_address
    M=M+D
    @CLOOP
    0;JMP

(DARKEN)
  @SCREEN
  D=A
  @current_address
  M=D
  (DLOOP)
    // Check still in screen address
    @current_address
    D=M
    @24576
    D=D-A
    @START
    D;JGE
    // Set memory to -1
    D=-1
    @current_address
    A=M
    M=D
    // Update current address
    @1
    D=A
    @current_address
    M=M+D
    @DLOOP
    0;JMP

    




