.data
print_int:
	.string "%d"
add:
	push %ebp
	mov %esp, %ebp
	sub $0, %esp
	push %ebx
	push %esi
	push %edi
	mov 8(%ebp), %eax
	add 12(%ebp), %eax
	mov %eax, 28(%ebp)
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	mov %ebp, %esp
	pop %ebp
	ret
main:
	push %ebp
	mov %esp, %ebp
	sub $12, %esp
	push %ebx
	push %esi
	push %edi
	mov $0, -4(%ebp)
	mov $0, -8(%ebp)
label2:
	mov -8(%ebp), %eax
	cmp $10, %eax
	setl %eax
	cmp $0, %eax
	jle label3
	mov $0, -12(%ebp)
	mov -12(%ebp), %eax
	cmp $2, %eax
	setne %eax
	cmp $0, %eax
	jg label0
	mov -4(%ebp), %eax
	sub -8(%ebp), %eax
	mov %eax, -4(%ebp)
	jump label1
label0:
	mov -4(%ebp), %eax
	add -8(%ebp), %eax
	mov %eax, -4(%ebp)
label1:
	jump label2
label3:
	push %ebp
	mov %esp, %ebp
	push %eax
	push $print_int
	call printf
	add  $8, %esp
	mov %ebp, %esp
	pop %ebp
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	mov %ebp, %esp
	pop %ebp
	ret
