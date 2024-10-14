.global sum_of_natural_numbers
sum_of_natural_numbers:
	PUSH{LR}
	MOV r1, #0
 loop:
	CMP r0, #0            // Check if n is zero or negative
    BLE end_recursion    // If n <= 0, return 0

    ADD r1,r1,r0          // Initialize result to 0
    SUB r0, r0, #1        // Decrement n by 1
	
    B loop//Recursively call sum_of_natural_numbers with n-1
    

end_recursion:
	MOV r0,r1
    POP{PC}                 // Return from the function
