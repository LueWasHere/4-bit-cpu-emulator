# OP CODES:
# 0: NOP # No operation
# 1: Mov .A # Move a number into the .A register
# 2: Sub # Subtract a number from .A
# 3: Add # Add a number to .A
# 4: Brn # Branch if .A is not equal to zero
# 5: Rts # Return from sub routine
# 6: Mov .B # Move a number from memory into the .B register
# 7: Mov .C # Move a number into the .C register
# 8: Mov [BC] # Store a value at the value at .B combined with .C (If .B is 0010 and .C is 0111 the value will be stored at 00100111)
# 9: Mul # Multiply the value in the .A register
# A: Div # Divide the value in the .A register
# B: Jmp # jump execution to a certain address
# C: Jne # jump execution to a certain address if .A is not equal to zero
# D: Jp # jump execution to a certain address if the parity flag is set
# E: Je # jump execution to a certain address if .A is equal to zero
# F: Mov .A .B # Move .B into .A

class CB4:
    readable = ["NOP", "MOV .A", "SUB", "ADD", "BRN", "RTS", "MOV .B", "MOV .C", "MOV [BC]", "MUL", "DIV", "JMP", "JNE", "JP", "JE", "MOV .A .B"]
    byte     = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    
    low_A = 0
    low_B = 0
    low_C = 0

    flag = 'n'

    stack_pointer = 253

    instruction_pointer = 0

    def __init__(self, mem_block: bytearray) -> None:
        self.mem_block           = mem_block
        self.current_instruction = self.mem_block[0]
        while len(self.mem_block) != 256:
            self.mem_block.append(0)

    def advanced(self) -> None:
        self.instruction_pointer += 1
        if self.instruction_pointer >= 255:
            self.instruction_pointer = 0

        self.current_instruction = self.mem_block[self.instruction_pointer]

    def execute(self) -> None:
        if self.current_instruction != '\x00':
            if self.current_instruction == 1:
                self.advanced()
                self.low_A = self.current_instruction
            elif self.current_instruction == 2:
                self.advanced()
                sub = self.current_instruction
                self.low_A -= sub
                if self.low_A < 0:
                    self.flag = 'p'
                    self.low_A = 0
            elif self.current_instruction == 3:
                self.advanced()
                sub = self.current_instruction
                self.low_A += sub
                if self.low_A > 0:
                    self.flag = 'p'
                    self.low_A = 0
            elif self.current_instruction == 4:
                if self.low_A == 0:
                    self.mem_block[self.stack_pointer] = self.instruction_pointer+1
                    self.stack_pointer += 1
                    self.advanced()
                    self.instruction_pointer = self.current_instruction
                else:
                    self.advanced()
            elif self.current_instruction == 5:
                self.instruction_pointer = self.mem_block[self.stack_pointer-1]
                self.mem_block[self.stack_pointer] = 0
                self.stack_pointer -= 1
                self.mem_block[self.stack_pointer] = 0
            elif self.current_instruction == 6:
                self.advanced()
                addr = self.current_instruction
                self.low_B = self.mem_block[addr]
            elif self.current_instruction == 7:
                self.advanced()
                self.low_C = self.current_instruction
            elif self.current_instruction == 8:
                byte_addr = ""
                byte_addr += str(self.low_B)
                byte_addr += str(self.low_C)
                byte_addr = int(byte_addr, 15)
                self.advanced()
                self.mem_block[byte_addr] = self.current_instruction
            elif self.current_instruction == 9:
                self.advanced()
                self.low_A = self.low_A * self.current_instruction
                if self.low_A > 15:
                    self.low_A = 0
                    self.flag = 'p'
            elif self.current_instruction == 10:
                self.advanced()
                try:
                    self.low_A = self.low_A / self.current_instruction
                except:
                    self.low_A = 0
                    self.flag = 'p'
            elif self.current_instruction == 11:
                self.advanced()
                self.instruction_pointer = self.current_instruction-1
            elif self.current_instruction == 12:
                if self.low_A != 0:
                    self.advanced()
                    self.instruction_pointer = self.current_instruction-1
                else:
                    self.advanced()
            elif self.current_instruction == 13:
                if self.flag == 'p':
                    self.advanced()
                    self.instruction_pointer = self.current_instruction, 'big'-1
                else:
                    self.advanced()
            elif self.current_instruction == 14:
                if self.low_A == 0:
                    self.advanced()
                    self.instruction_pointer = self.current_instruction-1
                else:
                    self.advanced()
            elif self.current_instruction == 15:
                self.low_A = self.low_B
        self.advanced()