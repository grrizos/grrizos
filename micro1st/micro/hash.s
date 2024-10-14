.global hash_calculate
hash_calculate:
	PUSH {LR}
    MOV r3, #0
    MOV r4, #0
	MOV r1, r0
	MOV r6,	#0
	LDR r5, =char_values
loop:
	LDRB r0, [r1], #1
    CMP r0, #0
    BEQ end_loop

    CMP r0, #'A'
    BLT numeric
    CMP r0, #'Z'
    BGT lower_case

	SUB r0, r0, #'A' 
    LDR r6, [r5, r0, LSL #2]  
    ADD r3, r3, r6  

    B loop

lower_case:
    CMP r0, #'a'
    BLT numeric
    CMP r0, #'z'
    BGT end_loop

    SUB r0, r0, #'a'
    LDR r6, [r5, r0, LSL #2]  
    SUB r3, r3, r6 
	
	B loop
	
numeric:
    CMP r0, #'0'
    BLT next_char
    CMP r0, #'9'
    BGT next_char

    SUB r0, r0, #'0'
    ADD r3, r3, r0
    B loop

next_char:
    ADD r4, r4, #1
    B loop


end_loop:

    STR r3, [r2]
	MOV r0,r3
    POP {PC}

.data
char_values:
    .word 10, 42, 12, 21, 7, 5, 67, 48, 69, 2, 36, 3, 19, 1, 14, 51, 71, 8, 26, 54, 75, 15, 6, 59, 13, 25