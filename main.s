jmp 5
@sub:
mov .A 15
rts
@main:
mov .B 3
brn @sub
mov .C 15
add 15