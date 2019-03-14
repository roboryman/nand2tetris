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

// @SCREEN
//  + @SCREEN is an I/O pointer to ==> RAM[16384] or RAM[0x4000]
//  + 256 rows of 512 pixels per row
//  + Each row represented in RAM by 32 consecutive 16-bit words
//  + This implies that there are a grand total of 8192 16-bit words to represent
//      the screen, starting at @SCREEN
//  + white = 0, black = 1
// @KBD:
//  + @KBD is an I/O pointer to ==> RAM[24576] or RAM[0x6000]
//  + When a key is pressed, the 16-bit ASCII appears in this address location
//  + When no key is detected as pressed, 0 appears in this address location

(LOOP)
        // Setup i counter variable for SETSCREEN loop.
        @8191   // 8192 total words address the screen; we already address 0x4000.
        D=A
        @i
        M=D

        // Set default color to all black (key down).
        @color
        M=-1    // -1 represented as 1111111111111111 in Hack.

        // Pressed key? Jump to SETSCREEN.
        @KBD
        D=M
        @SETSCREEN
        D;JNE

        // No pressed key? Set color to white, then jump to SETSCREEN.
        @color
        M=0     // RAM[@color] = white
        @SETSCREEN
        0;JMP

(SETSCREEN)
        // If i < 0, send back to parent loop.
        @i
        D=M
        @LOOP
        D;JLT

        // Calculate 16384+i, the current screenword.
        @SCREEN
        D=D+A   // i=i+@SCREEN
        @screenword
        M=D

        // Set color at current screenword to white or black.
        @color
        D=M     // Pull the color from RAM[@color], store in D register.
        @screenword
        A=M     // Pull the screenword from data memory, becomes address.
        M=D     // RAM[RAM[@screenword]] = RAM[@color].

        // Decrement i.
        @i
        M=M-1

        // Loop again.
        @SETSCREEN
        0;JMP
