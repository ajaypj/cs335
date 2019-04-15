factorial:
	push %ebp
	mov %esp, %ebp
	sub $0, %esp
	push %ebx
	push %esi
	push %edi
	mov 8(%ebp), %eax
	cmp $1, %eax
	setle %eax
	cmp $0, %eax
	jle label0
	mov $1, 24(%ebp)
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	mov %ebp, %esp
	pop %ebp
	ret
label0:
	mov 8(%ebp), %eax
	sub $1, %eax
	sub $4, %esp
	push %eax
	push %ecx
	push %edx
	push %eax
	call factorial
	add $4, %esp
	pop %edx
	pop %ecx
	pop %eax
	mov 8(%ebp), %eax
	imul -16(%ebp), %eax
	mov %eax, 24(%ebp)
	sub $4, %esp
	pop %edi
	pop %esi
	pop %ebx
	mov %ebp, %esp
	pop %ebp
	ret
main:
	push %ebp
	mov %esp, %ebp
	sub $4, %esp
	push %ebx
	push %esi
	push %edi
	sub $4, %esp
	push %eax
	push %ecx
	push %edx
	push $10
	call factorial
	add $4, %esp
	pop %edx
	pop %ecx
	pop %eax
	mov -20(%ebp), %eax
	mov %eax, -4(%ebp)
	sub $4, %esp
	pop %edi
	pop %esi
	pop %ebx
	mov %ebp, %esp
	pop %ebp
	ret
