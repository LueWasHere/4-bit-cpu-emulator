# TODO: Fix the assembler to split 8-bit numbers into four bit numbers and fix the emulator to gather them in multiple clock cycles





from colorama import Fore
from cb4 import CB4

def main():
    file = input("Name of file > ")
    out  = input("Name of output file > ")
    
    try:
        with open(file, "r") as f:
            dat = f.read()
            f.close()
    except FileNotFoundError:
        print(f"\"{file}\" does not exist.")
        exit(1)
    
    dat = dat.split()
    
    index = 0
    
    prog = []
    value = None
    
    labels = []
    labels_addr = []
    
    alpha = []
    
    for i in range(65, 123):
        if i not in range(91, 97):
            alpha.append(chr(i))
    
    while index in range(0, len(dat)):
        curr_tok = dat[index]
    
        if curr_tok != '\n' and curr_tok[0] != '@':
            if curr_tok.lower() == 'db':
                index += 1
                curr_tok = dat[index]
                try:
                    value = int(curr_tok)
                except:
                    print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                    exit(1)
                if value > 15:
                    print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                    exit(1)
                elif value < 0:
                    print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                    exit(1)
                prog.append(value.to_bytes(1, 'big'))
                value = None
            elif curr_tok.lower() == 'brn':
                prog.append(int(4).to_bytes(1, 'big'))
                index += 1
                curr_tok = dat[index]
                if curr_tok[0] == "@":
                    index_loc = 0
                    build = ""
                    build += curr_tok[index_loc]
                    index_loc += 1
                    try:
                        while curr_tok[index_loc] in alpha:
                            build += curr_tok[index_loc]
                            index_loc += 1
                    except IndexError:
                        if index_loc > len(curr_tok)-1:
                            pass
                        else:
                            print(f"{Fore.RED}Syntax error: in \"{curr_tok}\" label \"{build}\" not parsed fully{Fore.RESET}")
                            exit(1)      
                    try:
                        prog.append(labels_addr[labels.index(build)].to_bytes(1, 'big'))
                    except:
                        print(f"{Fore.RED}Syntax error: label \"{build}\" does not exist{Fore.RESET}")
                        exit(1)
                else:
                    try:
                        prog.append(int(curr_tok))
                    except:
                        print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                        exit(1)
                    if prog[len(prog)-1] > 255:
                        print(f"{Fore.RED}Overflow error: value is greater than 255, \"{value}\"{Fore.RESET}")
                        exit(1)
                    elif prog[len(prog)-1] < 0:
                        print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                        exit(1)
            elif curr_tok.lower() == 'rts':
                prog.append(int(5).to_bytes(1, 'big'))
            elif curr_tok.lower() == 'add':
                prog.append(int(3).to_bytes(1, 'big'))
                index += 1
                curr_tok = dat[index]
                try:
                    value = int(curr_tok)
                except:
                    print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                    exit(1)
                if value > 15:
                    print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                    exit(1)
                elif value < 0:
                    print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                    exit(1)
                prog.append(value.to_bytes(1, 'big'))
                value = None
            elif curr_tok.lower() == 'mul':
                prog.append(int(9).to_bytes(1, 'big'))
                index += 1
                curr_tok = dat[index]
                try:
                    value = int(curr_tok)
                except:
                    print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                    exit(1)
                if value > 15:
                    print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                    exit(1)
                elif value < 0:
                    print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                    exit(1)
                prog.append(value.to_bytes(1, 'big'))
                value = None
            elif curr_tok.lower() == 'div':
                prog.append(int(10).to_bytes(1, 'big'))
                index += 1
                curr_tok = dat[index]
                try:
                    value = int(curr_tok)
                except:
                    print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                    exit(1)
                if value > 15:
                    print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                    exit(1)
                elif value < 0:
                    print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                    exit(1)
                prog.append(value.to_bytes(1, 'big'))
                value = None
            elif curr_tok.lower() == 'sub':
                prog.append(int(2).to_bytes(1, 'big'))
                index += 1
                curr_tok = dat[index]
                try:
                    value = int(curr_tok)
                except:
                    print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                    exit(1)
                if value > 15:
                    print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                    exit(1)
                elif value < 0:
                    print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                    exit(1)
                prog.append(value.to_bytes(1, 'big'))
                value = None
            elif curr_tok.lower() in ['jmp', 'je', 'jne', 'jp']:
                prog.append(CB4.byte[CB4.readable.index(curr_tok.upper())].to_bytes(1, 'big'))
                index += 1
                curr_tok = dat[index]
                if curr_tok[0] == "@":
                    index_loc = 0
                    build = ""
                    build += curr_tok[index_loc]
                    index_loc += 1
                    try:
                        while curr_tok[index_loc] in alpha:
                            build += curr_tok[index_loc]
                            index_loc += 1
                    except IndexError:
                        if index_loc > len(curr_tok)-1:
                            pass
                        else:
                            print(f"{Fore.RED}Syntax error: in \"{curr_tok}\" label \"{build}\" not parsed fully{Fore.RESET}")
                            exit(1)      
                    try:
                        prog.append(labels_addr[labels.index(build)].to_bytes(1, 'big'))
                    except:
                        print(f"{Fore.RED}Syntax error: label \"{build}\" does not exist{Fore.RESET}")
                        exit(1)
                else:
                    try:
                        prog.append(int(curr_tok))
                    except:
                        print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                        exit(1)
                    if prog[len(prog)-1] > 255:
                        print(f"{Fore.RED}Overflow error: value is greater than 255, \"{value}\"{Fore.RESET}")
                        exit(1)
                    elif prog[len(prog)-1] < 0:
                        print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                        exit(1)
            elif curr_tok.lower() == 'mov':
                num     = False
                mem     = False
                pointer = False
                index += 1
                curr_tok = dat[index]
                if curr_tok not in ['.A', '.B', '.C', '[AB]']:
                    print(f"{Fore.RED}Syntax error: Argument \"{curr_tok}\" is not a valid register or pointer{Fore.RESET}")
                    exit(1)
                else:
                    if curr_tok == '.A':
                        num = True
                    elif curr_tok == '.B':
                        mem = True
                    elif curr_tok == '.C':
                        num = True
                    else:
                        pointer = True
                index += 1
                curr_tok = dat[index]
                if num:
                    if dat[index-1] == '.C':
                        prog.append(int(7).to_bytes(1, 'big'))
                        try:
                            value = int(curr_tok)
                        except:
                            print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                            exit(1)
                        if value > 15:
                            print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                            exit(1)
                        elif value < 0:
                            print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                            exit(1)
                    elif dat[index-1] == '.A' and curr_tok == '.B':
                        prog.append(int(15).to_bytes(1, 'big'))
                    else:
                        prog.append(int(1).to_bytes(1, 'big'))
                        try:
                            value = int(curr_tok)
                        except:
                            print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                            exit(1)
                        if value > 15:
                            print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                            exit(1)
                        elif value < 0:
                            print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                            exit(1)
                elif mem:
                    prog.append(int(6).to_bytes(1, 'big'))
                    try:
                        value = int(curr_tok)
                    except:
                        print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                        exit(1)
                    if value > 15:
                        print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                        exit(1)
                    elif value < 0:
                        print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                        exit(1)
                elif pointer:
                    prog.append(int(8).to_bytes(1, 'big'))
                    try:
                        value = int(curr_tok)
                    except:
                        print(f"{Fore.RED}Type error: value is not a number, \"{curr_tok}\"{Fore.RESET}")
                        exit(1)
                    if value > 15:
                        print(f"{Fore.RED}Overflow error: value is greater than 15, \"{value}\"{Fore.RESET}")
                        exit(1)
                    elif value < 0:
                        print(f"{Fore.RED}Overflow error: signed value is not allowed: value is less than 0, \"{value}\"{Fore.RESET}")
                        exit(1)
                if value != None:
                    prog.append(value.to_bytes(1, 'big'))
                    value = None
        elif curr_tok[0] == '@':
            build = ""
            index_loc = 0
            try:
                while curr_tok[index_loc] != ':':
                    try:
                        build += curr_tok[index_loc]
                        index_loc += 1
                    except IndexError:
                        print(f"{Fore.RED}Syntax error: Never ended label with colon{Fore.RESET}")
                        exit(1)
            except:
                pass
            labels.append(build)
            build = ""
            labels_addr.append(len(prog)-1)
        index += 1
    
    with open(out, "wb") as f:
        for i in range(0, len(prog)):
            try:
                f.write(prog[i])
            except TypeError:
                f.write(prog[i].to_bytes(1, 'big'))
        f.close()
