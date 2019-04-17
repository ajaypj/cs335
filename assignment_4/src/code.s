.data
	fmt_int: .string "%d\n"
	scan_int: .string "%d"
	.text
	.global main
	.type main, @function
ackermann:
	push %ebp
	movl %esp, %ebp
	sub $0, %esp
	push %ebx
	push %esi
	push %edi
	movl 8(%ebp), %ecx
	cmp $0, %ecx
	movl $0, %eax
	sete %al
	movl %eax, %ecx
	cmp $0, %ecx
	jg label2
	movl 8(%ebp), %ecx
	cmp $0, %ecx
	movl $0, %eax
	setg %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label1
	movl 12(%ebp), %ecx
	cmp $0, %ecx
	movl $0, %eax
	sete %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label0
	movl 8(%ebp), %ecx
	sub $1, %ecx
	sub $4, %esp
	push %eax
	push %ecx
	push %edx
	push $1
	push %ecx
	call ackermann
	add $8, %esp
	pop %edx
	pop %ecx
	pop %eax
	movl -16(%ebp), %ecx
	movl %ecx, 28(%ebp)
	sub $4, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
label0:
label1:
	jmp label3
label2:
	movl 12(%ebp), %ecx
	add $1, %ecx
	movl %ecx, 28(%ebp)
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
label3:
	movl 8(%ebp), %ecx
	sub $1, %ecx
	movl 12(%ebp), %ebx
	sub $1, %ebx
	sub $4, %esp
	push %eax
	push %ecx
	push %edx
	push %ebx
	push 8(%ebp)
	call ackermann
	add $8, %esp
	pop %edx
	pop %ecx
	pop %eax
	sub $4, %esp
	push %eax
	push %ecx
	push %edx
	add $4, %esp
	push -16(%ebp)
	push %ecx
	call ackermann
	add $8, %esp
	pop %edx
	pop %ecx
	pop %eax
	movl -16(%ebp), %ecx
	movl %ecx, 28(%ebp)
	sub $4, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
main:
	push %ebp
	movl %esp, %ebp
	sub $4, %esp
	push %ebx
	push %esi
	push %edi
	sub $4, %esp
	push %eax
	push %ecx
	push %edx
	push $3
	push $3
	call ackermann
	add $8, %esp
	pop %edx
	pop %ecx
	pop %eax
	add $4, %esp
	movl -20(%ebp), %ecx
	movl %ecx, -4(%ebp)
	push %eax
	push %ebx
	push %ecx
	push %edx
	push %esi
	push %edi
	movl -4(%ebp), %eax
	push %ebp
	mov %esp, %ebp
	push %eax
	push $fmt_int
	call printf
	add  $8, %esp
	mov %ebp, %esp
	pop %ebp
	pop %edi
	pop %esi
	pop %edx
	pop %ecx
	pop %ebx
	pop %eax
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
