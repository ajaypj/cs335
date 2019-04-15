add:
push %ebp
mov %esp, %ebp
sub $0, %esp
push %ebx
push %esi
push %edi
mov 8(%ebp), %eax
add 12(%ebp), %eax
mov %eax, %eax
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
label1:
mov -8(%ebp), %eax
cmp $10, %eax
setl %eax
cmp $0, %eax
jle label2
mov $0, -12(%ebp)
mov -12(%ebp), %eax
cmp $2, %eax
setne %eax
cmp $0, %eax
jle label0
mov -4(%ebp), %eax
add -8(%ebp), %eax
mov %eax, -4(%ebp)
label0:
jump label1
label2:
sub $0, %esp
pop %edi
pop %esi
pop %ebx
mov %ebp, %esp
pop %ebp
ret
