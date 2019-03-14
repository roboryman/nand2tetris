// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// + Preserves R0 and R1.

        // Setup i counter variable
        @R1
        D=M
        @i
        M=D     // RAM[@i] = R1

        // Make sure R2 is zero-ed out
        @R2
        M=0     // RAM[@R2] = 0

(LOOP)
        // If i == 0, jump to END.
        @i
        D=M
        @END
        D;JEQ

        // Do SUM stuff here. R2 = R2 + R0
        @R0
        D=M
        @R2
        M=M+D   // RAM[@R2] = RAM[@R2] + RAM[@R0]

        // Decrement i.
        @i
        M=M-1   // RAM[@i] -= 1

        // Loop again.
        @LOOP
        0;JMP

(END)
        // Infinite loop, effectively halting the Hack program.
        @END
        0;JMP
