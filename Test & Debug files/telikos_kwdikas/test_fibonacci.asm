.data
newline: .asciiz "\n"
.text


L0: b L_fibonacci
L_1: 
	sw $ra, -0($sp)
L_2: 
	lw $t1, -12($sp)
	li $t2, 2
	blt $t1, $t2, L_4
L_3: b L_6
L_4: 
	li $t1, 1
	lw $t0, -8($sp)
	sw $t1, ($t0)
	lw $ra, -0($sp)
	jr $ra
L_5: b L_16
L_6: 
	lw $t1, -12($sp)
	li $t2, 1
	sub $t1,$t1,$t2
	sw $t1, -16($sp)
L_7: 
	addi $fp, $sp, 36
	lw $t0, -16($sp)
	sw $t0, -12($fp)
L_8: 
	addi $t0, $sp, -20
	sw $t0,-8($fp)
L_9: 
	sw $sp, -4($fp)
	addi $sp, $sp, 36
	jal L_1
	addi $sp, $sp, -36
L_10: 
	lw $t1, -12($sp)
	li $t2, 2
	sub $t1,$t1,$t2
	sw $t1, -24($sp)
L_11: 
	addi $fp, $sp, 36
	lw $t0, -24($sp)
	sw $t0, -12($fp)
L_12: 
	addi $t0, $sp, -28
	sw $t0,-8($fp)
L_13: 
	sw $sp, -4($fp)
	addi $sp, $sp, 36
	jal L_1
	addi $sp, $sp, -36
L_14: 
	lw $t1, -20($sp)
	lw $t2, -28($sp)
	add $t1,$t1,$t2
	sw $t1, -32($sp)
L_15: 
	lw $t1, -32($sp)
	lw $t0, -8($sp)
	sw $t1, ($t0)
	lw $ra, -0($sp)
	jr $ra
L_16: 
	lw $ra, -0($sp)
	jr $ra
L_fibonacci: 
L_17: 
	addi $sp, $sp, 20
	move $s0,$sp
L_18: 
	li $v0, 5
	syscall
	sw $v0, -12($s0)
L_19: 
	addi $fp, $sp, 36
	lw $t0, -12($s0)
	sw $t0, -12($fp)
L_20: 
	addi $t0, $sp, -16
	sw $t0,-8($fp)
L_21: 
	sw $sp, -4($fp)
	addi $sp, $sp, 36
	jal L_1
	addi $sp, $sp, -36
L_22:
	li $v0, 1
	lw $a0, -16($sp)
	syscall
	li $v0, 4
	la $a0, newline
	syscall
L_23: 
L_24: 
