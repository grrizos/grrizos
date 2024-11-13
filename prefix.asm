;PROJECT NAME: MATRIX IPS 
;AUTHOR:GEORGE RIZOS
;DATE CREATED:12/11/24
;LAST DAY ACCESED:

data segment
    ;  I define the 2 arrays one with 
    ;  'random' nums, one with zeros.
    
    arin    dw  5,10,1,1,1
            dw  4,5,6,4,5
            dw  7,8,9,7,8     
            
    arout   dw  0,0,0,0,0
            dw  0,0,0,0,0
            dw  0,0,0,0,0
            
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
        
        

        mov si, arin    ;load base adress of arin to si
        mov ax, bx      ;Load row number (bi) into ax
        mov cx, 5       ;get the 5 for the mul
        mul cx          ;Multiply row number (ax) by 5 (bx)
        shl ax, 1       ;shift left to multiply by 2,because its element a word = 2 bytes  
        mov si, ax      ;si = arin + (row_number * 5 * 2) to get the row offset
        mov di, ax
        
        mov cx, 05d     ;set up the counter 
        LOOP2:
        
        add dx,[si+arin]    ;add each loop's shel into dx
        add [arout+si],dx   ;add each loop's dx into arout to complete each shel of arout
        add si,2            ;add 2 to si because each shell is 2 bytes
    
        
        loop LOOP2: 
    
    inc bx 
    cmp bx,3
    jl  FOR        
    
    
    
       
    
    jmp exit
    
    exit:

  
ends

end start ; set entry point and stop the assembler.
