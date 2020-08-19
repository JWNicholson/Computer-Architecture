"""CPU functionality."""

import sys

SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # RAM
        self.ram = [0] * 256
        # registers
        self.reg = [0] * 8
        # program counter
        self.pc = 0
        # points to the stack
        self.sp = 7
        # Memory address register
        self.MAR = None
        # Memory data register
        self.MDR = None
        # set default is programming running to False
        self.running = False
        # set eaual default to False
        self.equal = False
        
    def load(self):
        """Load a program into memory."""

        address = 0

        #with open("/mnt/h/CS32/Comp_Arc/Computer-Architecture/ls8/examples/mult.ls8") as program:
        with open("/mnt/h/CS32/Comp_Arc/Computer-Architecture/ls8/examples/stack.ls8") as program:
            for instructions in program:
                value = instructions.split()[0].strip()
                if value == "":
                    continue
                x = int(value, 2)
                self.ram[address] = x
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] == reg[reg_b]:
                self.equal = True
            else:
                self.equal = False
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # adding MAR and MDR to CPU class for ram_read and ram_write
    def ram_read(self, address):
        self.MAR = address
        self.MDR = self.ram[self.MAR]
        return self.MDR

    def ram_write(self, address, value):
        self.MAR = address
        self.MDR = value
        self.ram[MAR] = self.MDR
    
    #define apush valut to setup PUSH
    def push_val(self, value):
        self.ram_write(value, self.reg[self.SP])
        self.reg[self.SP] -= 1
    
    #define pop value to setup PUSH
    def pop_val(self):
        value = self.ram_read(self.reg[self.SP])
        self.reg[SP] += 1
        return value

    # Print the numeric value stored in the given register.
    def PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    #Set value of a register to an int. Note - LDI byte value is constant
    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    #Halts the CPU and exits the emulator
    def HLT(self, operand_a, operand_b):
        self.pc += 1
        sys.exit(0)
    
    #Push the value in this register onto the stack
    def PUSH(self, operand_a, operand_b):
        self.push_val(self.reg[operand_a])
        self.pc += 2
    
    #Pop the value from the top of stack into the given register
    def POP(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop_val()
        self.pc += 2
    
    # call a subroutine at the address stored in the register. Then push address of the instruction onto the stack so we can return to where we left off when the subroutine finishes.
    def CALL(self, operand_a, operand_b):
        self.push_val(self.pc + 2)
        self.pc = self.reg[operand_a]
    
    #Return from the subroutine and pop the value from top of stack and store it in the PC
    def RET(self, operand_a, operand_b):
        self.pc = self.pop_val()

    #Multiplies values in two register and store result in register a
    def MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc +=3

    # add two registers and store sum in register a
    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc +=3

    #Jump to the address stored in the given register and set PC to address stored in this register
    def JMP(self, operand_a, operand_b):
        self.pc = self.reg[operand_a]

    #Jump to address in this register if the equal flag is set True
    def JEQ(self, operand_a, operand_b):
        if self.equal == True:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    # Jump to address in this register if equal flag is set False
    def JNE(self, operand_a, operand_b):
        if self.equal == False:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    #Compare values in two registers. 
    # If they are equal set Eqaul E flag to one, otherwise 0
    # If register a is less than register b set the Less-than L flag to 1, otherwise 0
    # If register a is greater than register b set the Greater-than G flag to 1, otherwise 0
    def CMP(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3

    # read teh memory address stored in register PC and store result in IR
    def run(self):
        self.pc = 0
        run_inst = {
            1: self.HLT,
            17: self.RET,
            71: self.PRN,
            69: self.PUSH,
            70: self.POP,
            80: self.CALL,
            130: self.LDI,
            160: self.ADD,
            162: self.MUL,
            84: self.JMP,
            85: self.JEQ,
            86: self.JNE,
            167: self.CMP,
           }
        while not self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            run_inst[IR](operand_a, operand_b)

        return self.running
