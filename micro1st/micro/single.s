.global mono_digit_calculator

mono_digit_calculator:        
    PUSH {LR}                 
    MOV R1, R0               
    MOV R0, #0                

    MOV R5, #10               

initial:
    MOV R2, #0                // initilation R2 as 0

sum_of_digits:
    UDIV R3, R1, R5           // Divide R1 by 10 , get R3 as result
    MUL R4, R3, R5            // Mult by 10
    SUB R4, R1, R4           // Subto get whats left
    ADD R2, R2, R4            // Add remainder to R2
    MOV R1, R3                // Update R1 
    CMP R3, #0                // Check if quotient is 0
    BNE sum_of_digits            // If not, continue 

    MOV R1, R2                // Move the sum back to R1 for reduction check
    CMP R1, #9                // Check if the result is a single digit
    BLE end                   // If R1 <= 9,done
    B initial                // Otherwise, reduce the sum again

end:
    MOV R0, R1                // Move result to R0
    POP {PC}                  // Return from function
