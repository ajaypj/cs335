.data
	fmt_int: .string "%d\n"
	.text
	.global main
	.type main, @function
add:
	push %ebp
	movl %esp, %ebp
	sub $0, %esp
	push %ebx
	push %esi
	push %edi
	movl 8(%ebp), %eax
	add 12(%ebp), %eax
	movl %eax, 28(%ebp)
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
main:
	push %ebp
	movl %esp, %ebp
	sub $8, %esp
	push %ebx
	push %esi
	push %edi
	movl $0, -4(%ebp)
	movl $0, -8(%ebp)
label0:
	movl -8(%ebp), %eax
	cmp $10, %eax
	movl $0, %eax
	setl %al
	cmp $0, %eax
	jle label1
	sub $4, %esp
	push %eax
	push %ecx
	push %edx
	push -8(%ebp)
	push -4(%ebp)
	call add
	add $8, %esp
	pop %edx
	pop %ecx
	pop %eax
	add $4, %esp
	movl -24(%ebp), %eax
	movl %eax, -4(%ebp)
	mov $1, %eax
	add %eax, -8(%ebp)
	jmp label0
label1:
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
