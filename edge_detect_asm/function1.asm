
.386
.model flat
.code

bmptogray_conversion proc
    push ebp
	mov ebp,esp
	
	;[ebp+8]    height
    ;[ebp+12]   width
    ;[ebp+16]   input_color base pointer
    ;[ebp+20]   output_gray base pointer


	;we know ebp+8 is a and +4 is every parameter of the function including the pointers of the array
	xor ecx,ecx ; zero out i
	;make to pushes to stack to have the local variables x and y
	push ecx	; push y
	push ecx	; push x


	outer_loop:
	mov ecx,[ebp - 4] ;pop y from stack
	cmp ecx,[ebp + 8] ; if y >= height, exit loop
	jge end_func

	
	
	inner_loop:
	mov ecx,[ebp - 8]		; get x
	cmp ecx,[ebp + 12]		; if x >= width, exit loop
	jge next_row

	;calculate the input_color
	mov eax , [ebp - 4]	;get y row index
	mov edx , [ebp - 8]	; get x column index
	mov ebx , [ebp + 12]	; get width
	
	
	mul ebx
	add eax, edx		;add the offset in column
	shl eax,2d				; multiply by 4 because BGRQ is 4 byte
	add eax,[ebp + 16]	;add the base pointer of the input image in memory

	;according to the struct of RGBQUAD the order is BLUE,GREEN,RED -> BGR
	;so we have
	mov eax,[eax]
	mov ebx,[eax+1]	; green in ebx
	mov ecx,[eax+2]	; red in ecx and blue in eax

	;but each one is 1 byte->8bit so eaxh one is actually just in al,bl,cl
	
	;now we just have to to the calculation
	 
	imul eax,1140d	;calculate blue value
	imul ebx,5870d	;calculate green value
	imul ecx,2989d	;calculate red value
	
	;I dont use imul because the values of the colors are 0-255 so no need for negative numbers
	
	xor edx,edx		;zero out edx

	add edx,ebx		;add to edx all the values of the colors
	add edx,eax
	add edx,ecx

	mov ebx,edx		;ebx has the total value now
	mov eax,100d	;eax=100 for the division

	div ebx			;the eax=left part of the float number and the edx= right part of the float number
	mov ax,dx

	;now left part of eax_16bitleft=left part of float number and eax_16bitright=ax=right part of float number
	push eax
	;calculate the outpy_color[x][y]
	mov eax , [ebp - 4]	;get y row index
	mov edx , [ebp - 8]	; get x column index
	mov ebx , [ebp + 12]	; get width
	
	
	mul ebx
	add eax, edx		;add the offset in column
	shl eax,2d				; multiply by 4 because BGRQ is 4 byte
	add eax,[ebp + 20]	;add the base pointer of the input image in memory

	;on eax is the pointer of output_colir[x][y]
	mov ecx,[ebp - 12]
	mov [eax],ecx	;put in the memory space of output_color[x][y] the value of eax 
	
	jmp inner_loop	;go to begging of loop , will exit when finished with all x of width

	next_row:
	mov ecx,[ebp - 8]
	inc ecx
	mov [ebp - 8],ecx
	jmp outer_loop

end_func:

	mov eax,0
	pop ebp
	
	ret

bmptogray_conversion endp
					 end			 