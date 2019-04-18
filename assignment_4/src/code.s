.data
	fmt_int: .string "%d\n"
	scan_int: .string "%d"
	.text
	.global main
	.type main, @function
partition:
	push %ebp
	movl %esp, %ebp
	sub $16, %esp
	push %ebx
	push %esi
	push %edi
	movl $4, %ecx
	imul 16(%ebp), %ecx
	movl 8(%ebp), %ebx
	add %ecx, %ebx
	movl 0(%ebx), %ecx
	movl %ecx, -4(%ebp)
	movl 12(%ebp), %ecx
	movl %ecx, -8(%ebp)
label1:
	movl -8(%ebp), %ecx
	cmp 16(%ebp), %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label2
	movl $4, %ecx
	imul -8(%ebp), %ecx
	movl 8(%ebp), %ebx
	add %ecx, %ebx
	movl 0(%ebx), %ecx
	movl %ecx, %ebx
	cmp -4(%ebp), %ebx
	movl $0, %eax
	setle %al
	movl %eax, %ebx
	cmp $0, %ebx
	jle label0
	movl $4, %ecx
	imul -8(%ebp), %ecx
	movl 8(%ebp), %ebx
	add %ecx, %ebx
	movl 0(%ebx), %ecx
	movl %ecx, -12(%ebp)
	movl $4, %ecx
	imul -8(%ebp), %ecx
	movl 8(%ebp), %ebx
	add %ecx, %ebx
	movl $4, %ecx
	imul 12(%ebp), %ecx
	movl 8(%ebp), %esi
	add %ecx, %esi
	movl 0(%esi), %ecx
	movl %ecx, 0(%ebx)
	movl $4, %ecx
	imul 12(%ebp), %ecx
	movl 8(%ebp), %ebx
	add %ecx, %ebx
	movl -12(%ebp), %ecx
	movl %ecx, 0(%ebx)
	incl 12(%ebp)
label0:
	incl -8(%ebp)
	jmp label1
label2:
	movl $4, %ecx
	imul 12(%ebp), %ecx
	movl 8(%ebp), %ebx
	add %ecx, %ebx
	movl 0(%ebx), %ecx
	movl %ecx, -16(%ebp)
	movl $4, %ecx
	imul 12(%ebp), %ecx
	movl 8(%ebp), %ebx
	add %ecx, %ebx
	movl $4, %ecx
	imul 16(%ebp), %ecx
	movl 8(%ebp), %esi
	add %ecx, %esi
	movl 0(%esi), %ecx
	movl %ecx, 0(%ebx)
	movl $4, %ecx
	imul 16(%ebp), %ecx
	movl 8(%ebp), %ebx
	add %ecx, %ebx
	movl -16(%ebp), %ecx
	movl %ecx, 0(%ebx)
	movl 12(%ebp), %ecx
	movl %ecx, 32(%ebp)
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
quickSort:
	push %ebp
	movl %esp, %ebp
	sub $4, %esp
	push %ebx
	push %esi
	push %edi
	movl 12(%ebp), %ecx
	cmp 16(%ebp), %ecx
	movl $0, %eax
	setg %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label3
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
label3:
	sub $4, %esp
	push %eax
	push %ecx
	push %edx
	push 16(%ebp)
	push 12(%ebp)
	push 8(%ebp)
	call partition
	add $12, %esp
	pop %edx
	pop %ecx
	pop %eax
	add $4, %esp
	movl -20(%ebp), %ecx
	movl %ecx, -4(%ebp)
	movl -4(%ebp), %ecx
	sub $1, %ecx
	sub $0, %esp
	push %eax
	push %ecx
	push %edx
	push %ecx
	push 12(%ebp)
	push 8(%ebp)
	call quickSort
	add $12, %esp
	pop %edx
	pop %ecx
	pop %eax
	movl -4(%ebp), %ecx
	add $1, %ecx
	sub $0, %esp
	push %eax
	push %ecx
	push %edx
	push 16(%ebp)
	push %ecx
	push 8(%ebp)
	call quickSort
	add $12, %esp
	pop %edx
	pop %ecx
	pop %eax
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
	sub $28, %esp
	push %ebx
	push %esi
	push %edi
	movl $0, %ecx
	imul $4, %ecx
	movl $16, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl $10, 0(%ecx)
	movl $1, %ecx
	imul $4, %ecx
	movl $16, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl $90, 0(%ecx)
	movl $2, %ecx
	imul $4, %ecx
	movl $16, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl $8, 0(%ecx)
	movl $3, %ecx
	imul $4, %ecx
	movl $16, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl $7, 0(%ecx)
	lea -16(%ebp), %ecx
	movl %ecx, -20(%ebp)
	sub $0, %esp
	push %eax
	push %ecx
	push %edx
	push $3
	push $0
	push -20(%ebp)
	call quickSort
	add $12, %esp
	pop %edx
	pop %ecx
	pop %eax
	movl $0, -24(%ebp)
label4:
	movl -24(%ebp), %ecx
	cmp $4, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label5
	movl -24(%ebp), %ecx
	imul $4, %ecx
	movl $16, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl 0(%ecx), %ebx
	movl %ebx, -28(%ebp)
	push %eax
	push %ebx
	push %ecx
	push %edx
	push %esi
	push %edi
	movl -28(%ebp), %eax
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
	incl -24(%ebp)
	jmp label4
label5:
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
