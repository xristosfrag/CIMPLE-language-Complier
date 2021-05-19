.data
newline: .asciiz "\n"
.text


L0: b L_MAX
L_1: 
	sw $ra, -0($sp)
L_2: 
	lw $t1, -12($sp)
	lw $t2, -16($sp)
	bgt $t1, $t2, L_4
L_3: b L_6
L_4: 
	lw $t1, -12($sp)
	lw $t0, -8($sp)
	sw $t1, ($t0)
	lw $ra, -0($sp)
	jr $ra
L_5: b L_7
L_6: 
	lw $t1, -16($sp)
	lw $t0, -8($sp)
	sw $t1, ($t0)
	lw $ra, -0($sp)
	jr $ra
L_7: 
	lw $ra, -0($sp)
	jr $ra
