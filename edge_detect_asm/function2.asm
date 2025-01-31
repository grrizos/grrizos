.386
.model flat
.code
border_pixel_calculation  proc

    push ebp
	mov ebp,esp
	push edi
	push esi

	;[ebp+8]    height
    ;[ebp+12]   width
	;[ebp+16]	ee_image[2048][2048]
	
	;push into stack y into positiob [ebp-4]
	mov ecx, 1d
	push ecx
	;push into stack x into position [ebp-8]
	xor ecx
	push ecx
	;get width and height into edi and esi to have them thoughout the whole program

	mov esi,[ebp+8]			;esi=height
	mov edi,[ebp+12]		;edi=width
	mov edx,[ebp+16]		;edx=ee_image
	loop1:
	mov eax , [ebp - 4]		;get y row index
	
	mul edi
	add eax,0				;get the offset which is zero , [0][y]
	mov ecx,eax
	add ecx, 1d				;get the offset which is one, [1][y]
							
							;no need for shifting because ee_image unsigned char
	
	add eax,[ebp+16]		;get ee_image[0][y]
	add ecx,[ebp+16]		;get ee_image[1][y]

	mov [eax],ecx
	;first line done

	mov eax, [ebp - 4]		; eax=y
	mov ebx, edi			
	sub ebx, 1d				; ebx=width-1
	
	mov ecx, edi
	sub ecx,2d				; ebx=width-2

	mul edi					;eax*width to find the row
	add ebx,eax				;add the offset in column for width-1
	add ecx,eax`			;add the offset in column for width-2

	add	ebx,edx				;add the base pointer of the adress
	add ecx,edx				;add the base pointer of the adress

	mov [ebx],ecx			;ee_image[width - 1][y] = ee_image[width - 2][y]
							;by moving in the adress that ebx is pointing the value
							;of the the adress that ecx is pointing
	
	mov eax,[ebp-4]
	inc eax
	mov [ebp-4],eax
	
	mov ebx,esi
	dec ebx

	cmp eax,ebx				;if y<height-1 go to loop1
	jl loop1

	loop2:




	jg loop2
	xor eax,eax				;get y to zero
	
	mul edi
	add eax,[ebp - 8]		;get the offset which is zero , [x][0]
	mov ecx,eax				;ecx points now  to ee_image[x][0]
	
	mov eax,1d				;get the offset which is one, [1][y]
	mul edi
	add eax,[ebp - 8]
	
	add eax,[ebp+16]		;get ee_image[0][y], add the base pointer of the adress
	add ecx,[ebp+16]		;get ee_image[1][y], add the base pointer of the adress
	
	mov [ecx],eax			;put in the adress that ecx points the eax value
	;first line done
	
	mov ebx, esi			
	sub ebx, 1d				; ebx=height-1
	mov eax, ebx			; eax=height-1
	
	mul edi					; eax*width to find the row
	add eax,[ebp - 8]
	mov ebx,eax				; ebx=ee_image[x][height - 1]
	;;;
	mov ecx, esi
	sub ecx, 2d				; ecx=height-2
	mov eax, ecx			; ecx=height-2
	
	mul edi					;eax*width to find the row
	add eax,[ebp - 8]
	mov ecx,eax				;ecx= ee_image[x][height - 2]
	

	add	ebx,[ebp + 16]		;add the base pointer of the adress
	add ecx,[ebp + 16]		;add the base pointer of the adress

	mov [ebx],ecx			;ee_image[x][height - 1] =ee_image[x][height - 2]
							;by moving in the adress that ebx is pointing the value
							;of the the adress that ecx is pointing
	
	mov eax,[ebp-8]
	inc eax
	mov [ebp-8],eax
	
	mov ebx,edi
	dec ebx

	cmp eax,ebx				;if x<width-1 go to loop1
	jl loop2


	pop esi
	pop edi
	ret
	
border_pixel_calculation endp
						 end