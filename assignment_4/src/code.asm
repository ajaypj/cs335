main:
push %ebp
mov %esp, %ebp
sub $4, %esp
push %ebx
push %esi
push %edi
mov $0, %eax
imul $0, %eax
mov $1, %ecx
imul $1, %ecx
mov $2, %edx
imul $2, %edx
mov $3, %ebx
imul $3, %ebx
mov $4, %esi
imul $4, %esi
mov $5, %edi
imul $5, %edi
push %eax
mov $6, %eax
imul $6, %eax
push %ecx
mov $7, %ecx
imul $7, %ecx
add %ecx, %eax
add %eax, %edi
add %edi, %esi
add %esi, %ebx
add %ebx, %edx
add -24(%ebp), %edx
add -20(%ebp), %edx
