addi r1 r0 1
addi r2 r0 130
addi r3 r0 325
cicle:
div r3 r2
add r3 r2 r0
mfhi r2
bgtz r2 cicle
tty r3
halt

#prints A