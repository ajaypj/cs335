main:
push %ebp
mov %esp, %ebp
sub $8, %esp
push %ebx
push %esi
push %edi
mov $2, %eax
imul $5, %eax
mov $4, %ecx
sub %eax, %ecx
sub $0, %esp
pop %edi
pop %esi
pop %ebx
mov %ebp, %esp
pop %ebp
