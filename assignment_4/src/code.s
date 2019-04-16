.data
	fmt_int: .string "%d\n"
	scan_int: .string "%d"
	.text
	.global main
	.type main, @function
main:
	push %ebp
	movl %esp, %ebp
	sub $8, %esp
	push %ebx
	push %esi
	push %edi
	push %eax
	push %ebx
	push %ecx
	push %edx
	push %esi
	push %edi
	lea -4(%ebp), %eax
	push %ebp
	mov %esp, %ebp
	push %eax
	push $scan_int
	call scanf
	add  $8, %esp
	mov %ebp, %esp
	pop %ebp
	pop %edi
	pop %esi
	pop %edx
	pop %ecx
	pop %ebx
	pop %eax
	movl -4(%ebp), %eax
	cmp $1, %eax
	movl $0, %eax
	sete %al
	cmp $0, %eax
	jle label0
	movl $10, -8(%ebp)
	jmp label3
label0:
	movl -4(%ebp), %eax
	cmp $2, %eax
	movl $0, %eax
	sete %al
	cmp $0, %eax
	jle label1
	movl $20, -8(%ebp)
	jmp label3
label1:
	movl -4(%ebp), %eax
	cmp $3, %eax
	movl $0, %eax
	sete %al
	cmp $0, %eax
	jle label2
	movl $30, -8(%ebp)
	jmp label3
label2:
label3:
	push %eax
	push %ebx
	push %ecx
	push %edx
	push %esi
	push %edi
	movl -8(%ebp), %eax
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
