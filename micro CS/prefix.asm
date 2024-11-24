;PROJECT NAME: MATRIX IPS 
;AUTHOR:GEORGE RIZOS
;DATE CREATED:12/11/24
;LAST DAY ACCESED:15/11/24

data segment
    ;  I define the 2 arrays one with 
    ;  'random' nums, one with zeros.
    
    N    dw  10,6,1,1,5
            dw  4,5,1,4,5
            dw  1,2,3,7,8     
            
    U   dw  0
            
ends

stack segment
    dw   128  dup(0)
ends

code segment
start:
;segment registers:
    MOV ax, data
    MOV ds, ax
    MOV es, ax
    

    MOV bx, 0    ;Initialize row counter (row_number = 0)
    
    FOR:    
        
        MOV si, N   ;load base adress of arin to si
        MOV ax, bx      ;Load row number (bi) into ax
        MOV cx, 5       ;get the 5 for the mul
        MUL cx          ;Multiply row number (ax) by 5 (bx)
        SHL ax, 1       ;shift left to multiply by 2,because word=2bytes
        MOV si, ax      ;si = arin + (row_number * 5 * 2) to get the row offset
      
        XOR dx,dx
        MOV cx, 05d     ;set up the counter 
        
        LOOP2:
        
        ADD dx,[si+N]    ;add each loop's shel into dx
        ADD [U+si],dx   ;add each loop's dx into arout to complete each shel of arout
        ADD si,2            ;add 2 to si because each shell is 2 bytes
    
        
        LOOP LOOP2: 
    
    INC BX      ;incriment bx everyloop as a counter 
    CMP BX,3    ;compare bx with 3 
    JL  FOR
    

;;;;;;;  ARIN

;PRINT ARIN TEXT
    MOV BX,0 
    ADD BX,2 
    MOV DX, 0B800h ; Video memory
    MOV DS, DX
    MOV DL, 'N'       ; Set ASCII character for tens
    MOV DH, 11011111b ; Set color attribute

    MOV [BX], DX     ; Write to video memory  
    
PRINT_MATRICES:

    MOV SI,0

    MOV BX, 10H  ;set up the video memory shell
    MOV DX,5 
    PUSH DX
    MOV CX,15
    PUSH CX
PRINT_INPUT:  
    MOV AX,DATA
    MOV DS,AX
    MOV AX,0
    ADD AX,[si+N]; Load number from the input matrix
    JMP PRINT_NUMBER ; Print the number to video memory
     AGAIN:

    ADD SI, 2 ; Move to the next input element  
                    ;counter for 5 elements second in stack  
    POP CX
    DEC CX
    
    POP DX
    DEC DX
    PUSH DX
    PUSH CX
    CMP DX,0                
    JNZ PRINT_INPUT ; Continue row loop
    
    ADD BX,290 ; Move to the next line in video memory (80 chars per line)
                    ;counter for 15 elements check once so first in stack 
    POP CX
    POP DX
    MOV DX,5
    PUSH DX
    PUSH CX
    CMP CX,0
    JNZ PRINT_INPUT ;If not on 15 element continue with next row
    
    JMP endarin
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
    SUB BX, 2       ; Move to the next position

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
 
 
;;;;;;;;;;;;;;; 
 
 
 
 
;;;;;;;;;AROUT  
endarin:
    MOV BX, 502H
    ;PRINT AROUT TEXT
     
    MOV DX, 0B800h ; Video memory
    MOV DS, DX
    MOV DL, 'U'       ; Set ASCII character for tens
    MOV DH, 11011111b ; Set color attribute

    MOV [BX], DX     ; Write to video memory  
    
PRINT_MATRICES_arout:

    MOV SI,0

    MOV BX, 510H  ;set up the video memory shell
    MOV DX,5 
    PUSH DX
    MOV CX,15
    PUSH CX
PRINT_INPUT_arout:  
    MOV AX,DATA
    MOV DS,AX
    MOV AX,0
    ADD AX,[si+U]; Load number from the input matrix
    JMP PRINT_NUMBER_arout ; Print the number to video memory
     AGAIN_arout:

    ADD SI, 2 ; Move to the next input element  
                    ;counter for 5 elements second in stack  
    POP CX
    DEC CX
    
    POP DX
    DEC DX
    PUSH DX
    PUSH CX
    CMP DX,0                
    JNZ PRINT_INPUT_arout ; Continue row loop
    
    ADD BX,286 ; Move to the next line in video memory (80 chars per line)
                    ;counter for 15 elements check once so first in stack 
    POP CX
    POP DX
    MOV DX,5
    PUSH DX
    PUSH CX
    CMP CX,0
    JNZ PRINT_INPUT_arout ;If not on 15 element continue with next row
    
    JMP exit:
    RET
    
PRINT_NUMBER_arout PROC
    ; Input: AX contains the number to print  
    
LOOP_START_arout: 

    MOV DL, 10
    DIV DL            ; AX / 10 -> AL (piliko), AH (ipolipo)
    CMP AL,0          
    JZ  LASTONE_arout 
    
    MOV CX, 0B800h ; Video memory
    MOV DS, CX
    MOV DH, AH       ; store to dh to ipolipo
    ADD DH, 48       ; Convert to ipolipo to ASCII ('0' = 48)
    MOV CL, DH       ; Set ASCII character for tens
    MOV CH, 11011111b ; Set color attribute

    MOV [BX], CX     ; Write to video memory
    SUB BX, 2       ; Move to the next position

    XOR AH,AH
    
    JMP LOOP_START_arout 
    
    LASTONE_arout: 
    
    MOV CX, 0B800h ; Video memory
    MOV DS, CX
    MOV DH, AH       ; store to dh to ipolipo
    ADD DH, 48       ; Convert to ipolipo to ASCII ('0' = 48)
    MOV CL, DH       ; Set ASCII character for tens
    MOV CH, 11011111b ; Set color attribute

    MOV [BX], CX     ; Write to video memory
    ADD BX, 8        ; Move to the next position
    
    
    JMP AGAIN_arout
    
    jmp exit
    
    exit:

  
ends

end start ; set entry point and stop the assembler.
