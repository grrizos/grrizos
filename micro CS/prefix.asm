;PROJECT NAME: MATRIX IPS 
;AUTHOR:GEORGE RIZOS
;DATE CREATED:12/11/24
;LAST DAY ACCESED:15/11/24

data segment
    ;  I define the 2 arrays one with 
    ;  'random' nums, one with zeros.
    
    arin    dw  245,6,1,1,5
            dw  4,5,1,4,5
            dw  1,2,3,7,8     
            
    arout   dw  0
            
ends

stack segment
    dw   128  dup(0)
ends

code segment
start:
;segment registers:
    mov ax, data
    mov ds, ax
    mov es, ax
    

    mov bx, 0    ;Initialize row counter (row_number = 0)
    
    FOR:    
        
        mov si, arin   ;load base adress of arin to si
        mov ax, bx      ;Load row number (bi) into ax
        mov cx, 5       ;get the 5 for the mul
        mul cx          ;Multiply row number (ax) by 5 (bx)
        shl ax, 1       ;shift left to multiply by 2,because word=2bytes
        mov si, ax      ;si = arin + (row_number * 5 * 2) to get the row offset
      
        xor dx,dx
        mov cx, 05d     ;set up the counter 
        
        LOOP2:
        
        add dx,[si+arin]    ;add each loop's shel into dx
        add [arout+si],dx   ;add each loop's dx into arout to complete each shel of arout
        add si,2            ;add 2 to si because each shell is 2 bytes
    
        
        loop LOOP2: 
    
    inc bx      ;incriment bx everyloop as a counter 
    cmp bx,3    ;compare bx with 3 
    jl  FOR
    
    MOV AX,AROUT
    MOV BX,AROUT+12
    MOV CX,AROUT+24
;;;;;;;;;;;;;;;;;;

  
PRINT_MATRICES:

    MOV SI,0

    MOV BX, 10H  ;set up the video memory shell
PRINT_INPUT_ROW:
    MOV DX, 5 ; Number of elements per row 
    
PRINT_INPUT_COLUMN:  
    MOV AX,DATA
    MOV DS,AX
    MOV AX,0
    ADD AX,[si+arout]; Load number from the input matrix
    CALL PRINT_NUMBER ; Print the number to video memory
     AGAIN:

    ADD SI, 2 ; Move to the next input element  

    
    DEC DX 
    CMP DX,0
    JNZ PRINT_INPUT_COLUMN ; Continue column loop

    ADD BX, 160 - 10 ; Move to the next line in video memory (80 chars per line)
    POP CX
    DEC CX
    PUSH CX
    JNZ PRINT_INPUT_ROW ; Continue row loop
    RET
    
PRINT_NUMBER PROC
    ; Input: AX contains the number to print  
    
LOOP_START: 

    MOV DL, 10
    DIV DL            ; AX / 10 -> AL (piliko), AH (ipolipo)
    CMP AL,0          
    JZ  LASTONE 
    
    MOV CX, 0B800h ; Video memory
    MOV DS, CX
    MOV DH, AH       ; store to dh to ipolipo
    ADD DH, 48       ; Convert to ipolipo to ASCII ('0' = 48)
    MOV CL, DH       ; Set ASCII character for tens
    MOV CH, 11011111b ; Set color attribute

    MOV [BX], CX     ; Write to video memory
    ADD BX, 2       ; Move to the next position

    XOR AH,AH
    
    JMP LOOP_START 
    
    LASTONE: 
    
    MOV CX, 0B800h ; Video memory
    MOV DS, CX
    MOV DH, AH       ; store to dh to ipolipo
    ADD DH, 48       ; Convert to ipolipo to ASCII ('0' = 48)
    MOV CL, DH       ; Set ASCII character for tens
    MOV CH, 11011111b ; Set color attribute

    MOV [BX], CX     ; Write to video memory
    ADD BX, 6        ; Move to the next position
    
    
    JMP AGAIN

  
    
    jmp exit
    
    exit:

  
ends

end start ; set entry point and stop the assembler.
