addi r1 r0 84 
tty r1

addi r2 r1 33
tty r2

addi r2 r0 32

space:
tty r2
blez r1 cro

#Tu 
bgtz r1 cont
bgtz r1 jump

cont:
addi r3 r0 25
add r4 r3 r1
tty r4

addi r3 r0 4
sub r1 r4 r3
tty r1
#mi

nor r1 r0 r1
addi r29 r0 11
addi r29 r0 33
addi r28 r0 3
mulu r29 r28
mflo r27
tty r27

addi r29 r0 15
add r28 r27 r29
tty r28

addi r4 r0 113
addi r8 r0 2
sub r29 r4 r8
tty r29

#cro
j space

cro:
addi r22 r0 194
push r22
addi r20 r0 2
#previous insertion of a on stack

addi r15 r0 102
push r15
pop r15
tty r15

sltu r10 r15 r22
bne r0 r10 keep
j jump

keep:
addi r5 r0 117
tty r5

rnd r5
bne r0 r5 skip
beq r0 r5 skip
j jump

skip:
addi r21 r0 196
jr r21
j jump
addi r15 r15 8
tty r15

tty r27

addi r28 r0 210
addi r29 r0 211
div r28 r29
mfhi r27
divu r27 r8
mflo r26
tty r26

addi r28 r0 111
#sw r28 520(r0)
#addi r20 r0 564133998
#sw r20 256(r0)
nop
#addi r27 r0 520
#addi r28 r0 0
#lw r28 0(r27)
tty r28

addi r13 r0 110
#addi r13 r0 33
tty r13

a:
pop r22
div r22 r20
mflo r22
tty r22

halt

jump:
addi r1 r0 33
tty r1

halt

#prints Tu micro funciona
#If it prints some ! in the sentence, its wrong!