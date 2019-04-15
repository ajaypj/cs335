main:
push %ebp
mov %esp, %ebp
sub $8, %esp
push %ebx
push %esi
push %edi
mov -4(%ebp), %eax
imul $5, %eax
mov $4, %ecx
sub %eax, %ecx
mov %ecx, -8(%ebp)
mov -8(%ebp), %eax
mov %eax, -4(%ebp)
sub $0, %esp
pop %edi
pop %esi
pop %ebx
mov %ebp, %esp
pop %ebp
