.data
	fmt_int: .string "%d\n"
	scan_int: .string "%d"
	.text
	.global main
	.type main, @function
main:
	push %ebp
	movl %esp, %ebp
	sub $100, %esp
	push %ebx
	push %esi
	push %edi
	movl $0, -52(%ebp)
label2:
	movl -52(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label3
	movl $0, -56(%ebp)
label0:
	movl -56(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label1
	movl $0, -60(%ebp)
	push %eax
	push %ebx
	push %ecx
	push %edx
	push %esi
	push %edi
	lea -60(%ebp), %eax
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
	movl -52(%ebp), %ecx
	imul $8, %ecx
	movl $32, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl -56(%ebp), %ebx
	imul $4, %ebx
	movl %ecx, %esi
	add %ebx, %esi
	movl -60(%ebp), %ecx
	movl %ecx, 0(%esi)
	incl -56(%ebp)
	jmp label0
label1:
	incl -52(%ebp)
	jmp label2
label3:
	movl $0, -64(%ebp)
label6:
	movl -64(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label7
	movl $0, -68(%ebp)
label4:
	movl -68(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label5
	movl $0, -72(%ebp)
	push %eax
	push %ebx
	push %ecx
	push %edx
	push %esi
	push %edi
	lea -72(%ebp), %eax
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
	movl -64(%ebp), %ecx
	imul $8, %ecx
	movl $48, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl -68(%ebp), %ebx
	imul $4, %ebx
	movl %ecx, %esi
	add %ebx, %esi
	movl -72(%ebp), %ecx
	movl %ecx, 0(%esi)
	incl -68(%ebp)
	jmp label4
label5:
	incl -64(%ebp)
	jmp label6
label7:
	movl $0, -76(%ebp)
	movl $0, -80(%ebp)
label12:
	movl -80(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label13
	movl $0, -84(%ebp)
label10:
	movl -84(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label11
	movl $0, -88(%ebp)
label8:
	movl -88(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label9
	movl -80(%ebp), %ecx
	imul $8, %ecx
	movl $32, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl -88(%ebp), %ebx
	imul $4, %ebx
	movl %ecx, %esi
	add %ebx, %esi
	movl 0(%esi), %ecx
	movl -88(%ebp), %ebx
	imul $8, %ebx
	movl $48, %esi
	sub %ebx, %esi
	movl %ebp, %ebx
	sub %esi, %ebx
	movl -84(%ebp), %esi
	imul $4, %esi
	movl %ebx, %edi
	add %esi, %edi
	movl 0(%edi), %ebx
	movl %ecx, %esi
	imul %ebx, %esi
	movl -76(%ebp), %ecx
	add %esi, %ecx
	movl %ecx, -76(%ebp)
	incl -88(%ebp)
	jmp label8
label9:
	movl -80(%ebp), %ecx
	imul $8, %ecx
	movl $16, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl -84(%ebp), %ebx
	imul $4, %ebx
	movl %ecx, %esi
	add %ebx, %esi
	movl -76(%ebp), %ecx
	movl %ecx, 0(%esi)
	movl $0, -76(%ebp)
	incl -84(%ebp)
	jmp label10
label11:
	incl -80(%ebp)
	jmp label12
label13:
	movl $0, -92(%ebp)
label16:
	movl -92(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label17
	movl $0, -96(%ebp)
label14:
	movl -96(%ebp), %ecx
	cmp $2, %ecx
	movl $0, %eax
	setl %al
	movl %eax, %ecx
	cmp $0, %ecx
	jle label15
	movl -92(%ebp), %ecx
	imul $8, %ecx
	movl $16, %ebx
	sub %ecx, %ebx
	movl %ebp, %ecx
	sub %ebx, %ecx
	movl -96(%ebp), %ebx
	imul $4, %ebx
	movl %ecx, %esi
	add %ebx, %esi
	movl 0(%esi), %ecx
	movl %ecx, -100(%ebp)
	push %eax
	push %ebx
	push %ecx
	push %edx
	push %esi
	push %edi
	movl -100(%ebp), %eax
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
	incl -96(%ebp)
	jmp label14
label15:
	incl -92(%ebp)
	jmp label16
label17:
	sub $0, %esp
	pop %edi
	pop %esi
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret
