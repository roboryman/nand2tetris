# nand2tetris (The Elements of Computing Systems)
My code for the hardware and software projects as described in The Elements of Computing Systems by Noam Nisan and Shimon Schocken.\
Abstraction rules all.

### Chapter 01 - Boolean Logic
HDL for NOT, NOT16, AND, AND16, OR, OR16, OR8WAY, XOR, MUX, MUX16, MUX4WAY16, MUX8WAY16, DMUX, DMUX4WAY, DMUX8WAY gates.

### Chapter 02 - Boolean Arithmetic
HDL for HalfAdder, FullAdder, Add16, Inc16, ALU chips.

### Chapter 03 - Sequential Logic
HDL for Bit, Register, PC, RAM8, RAM64, RAM512, RAM4K, RAM16K chips.

### Chapter 04 - Machine Language
ASM and assembled Hack machine code for Mult and Fill ROM programs.

### Chapter 05 - Computer Architecture
HDL for Memory, Mux8Way, CPU chips.\
HDL for Hack machine.

### Chapter 06 - Assembler
Python3 for Hack Assembler and Hack Assembler(No Symbols).\
Python3 for Assembler modules Code, Command, Parser, and SymbolTable.
* **UPDATE 3/18/19:** Assembler module Parser v2.0 is now out! This adds support for macro-commands.
  * *For an example of this*, take a look at Max_no_macros.asm, Max_macros.asm, and their respective Hack files in the 06 project directory.
  * *Note that the Hack machine code is equivalent*, while the asm file with macro-commands has essentially halved.
Also take note that all A-Instructions have essentially 'piggy backed' onto C-Instructions using brackets.
  * *Macro-commands are like so:* 'M=D[123]' is equivalent to '@123' followed by 'M=D'.
Of course, this also works for symbols: 'M=D[foo]' is equivalent to '@foo' followed by 'M=D'.

### Chapter 07 - Virtual Machine I: Stack Arithmetic
Python3 for Virtual Machine Translator.\
Python3 for VMT modules CodeWriter, Parser, and Command.
Implements Stage I and Stage II of the VM.

### Chapter 08 - Virtual Machine II: Program Control
Python3 for Virtual Machine Translator.\
Python3 for VMT modules CodeWriter, Parser, and Command.
Implements Stage I - Stage IV of the VM.

### Chapter 09 - High-Level Language
Jack for the PerfectlyBalanced program.

### Chapter 10 - Compiler I: Syntax Analysis
#### In Progress.

### Chapter 11 - Compiler II: Code Generation
#### In Progress.

### Chapter 12 - Operating System
#### In Progress.

## My Projects
#### In Progress.
