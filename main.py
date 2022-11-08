import platform
version = float(platform.python_version()[0:3])

if version > 3.9:
    print("Importing 3.10 version.")
    from cb4 import CB4
else:
    print("Importing 3.9 and lower version")
    from cb3_9 import CB4
from colorama import Back, Cursor
from platform import system
from os import system as call
from time import sleep
from assembler import main as asmain

compile = input("Do you wan't to compile something? (Y/N): ")
if compile.lower() == 'y':
    asmain()

file = input('File name: ')
while True:
    try:
        cycles = (float(input("How many Hz should the clock cycle at?: ")))
        cycles_disp = cycles
        cycles = 1/cycles
        print(f"running at {cycles}")
        break
    except:
        print("Enter a number!")
try:
    with open(file, "rb") as rb:
        dat = bytearray(rb.read())
        rb.close()
except FileNotFoundError:
    print(f"\"{file}\" does not exist.")
    exit(1)

if system() == 'Windows':
    call('cls')
else:
    call('clear')

cpu = CB4(dat)
while True:
    print("    0123456789ABCDEF")
    try:
        sleep(cycles)
        counter = 0
        print("00: ", end="")
        for i in range(0, len(dat)):
            counter += 1
            if i == cpu.instruction_pointer:
                print(f"{Back.CYAN}{str(hex(cpu.mem_block[i])[2::])}{Back.RESET}", end="")
            else:
                print(f"{str(hex(cpu.mem_block[i])[2::])}", end="")
            if counter == 16:
                print(f"\n{((str(hex(i))[2::]).zfill(2))}: ", end="")
                counter = 0
        print(f"\n.A: {cpu.low_A} ; .B: {cpu.low_B} ; .C: {cpu.low_C} ; F: {cpu.flag}   Current instruction: {cpu.readable[cpu.byte.index(cpu.current_instruction)]}            ")
        print(f"Running at: {cycles_disp} Hz.{Cursor.POS(0, 0)}", end="")
        cpu.execute()
    except KeyboardInterrupt:
        if system() == 'Windows':
            call('cls')
        else:
            call('clear')
        print("Exited.")
        exit(0)