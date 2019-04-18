import re
from collections import OrderedDict

init_regs = OrderedDict()
# init_regs["eax"] = 0
init_regs["ecx"] = 0
# init_regs["edx"] = 0
init_regs["ebx"] = 0
init_regs["esi"] = 0
init_regs["edi"] = 0

regs = None
unused_temp_vars_in_reg = None
temp_vars = None
function_width = None
temp_offset = None

code = list()

def get_reg(name, width):
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	for i in regs:
		if regs[i]==0:
			regs[i]=1
			temp_vars[name]={"ro":i, "so":-1, "width":width}
			unused_temp_vars_in_reg.append(name)
			return i
	old_temp_var = unused_temp_vars_in_reg[0]
	old_reg = temp_vars[old_temp_var]["ro"]
	code += ["push %{}".format(old_reg)]
	# print(unused_temp_vars_in_reg[0])
	del unused_temp_vars_in_reg[0]
	unused_temp_vars_in_reg.append(name)
	temp_vars[name]={"ro":old_reg, "so":-1, "width":width}

	temp_offset += width
	temp_vars[old_temp_var]["so"]=function_width+temp_offset
	temp_vars[old_temp_var]["ro"]=-1
	return old_reg

def split_var(var_name):
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	name=re.split(":", var_name)
	return name

def write_list(file, a_list):
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	for i in a_list:
		file.write(i)
		file.write(" ")
	file.write("\n")

def remove_used_temp_var_in_reg(name):
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	# print("DELETING", name)
	if name in temp_vars:
		unused_temp_vars_in_reg.remove(name)
		regs[temp_vars[name]["ro"]]=0
		del temp_vars[name]

def remove_used_temp_var_in_mem(name):
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	# print("DELETING", name)
	if temp_vars[name]["so"] == function_width+temp_offset:
		code += ["add $4, %esp"]
		temp_offset -= 4
	del temp_vars[name]

def get_type(name):
	# print(name)
	name=split_var(name)[0]
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	if "*" in name:
		return "*"
	elif "var" in name:
		return "m"
	elif "tmp#" in name:
		if temp_vars[name]["ro"]!=-1:
			return "r"
		else:
			return "m"
	elif name[1:].isdigit() or name[1]=='-':
		return "c"
	else:
		return -1

################################# Read IR ######################################
file=open("ir.txt")
ir=list()
line=file.readline()
while line:
	ir.append(line)
	line=file.readline()
file.close()
# print(ir)

################################ Code generation ###############################
op_dic = {'+':"add", '-':"sub", '*':"imul", '/':"idivl", '&':"and", '^':"xor", '|':"or", '<':"l", '<=':"le", '>':"g", '>=':"ge", '==':"e", '!=':"ne"}

for line in ir:
	data = re.split(" |, |\n", line)
	i = list()
	for w in data:
		if w:
			i.append(w)
	# print()
	# print(i)
	# print(regs)
	# print(temp_vars)
	# print(unused_temp_vars_in_reg)

	if i[0] == "func":
		code += ["{}:".format(split_var(i[1])[0])]
		code += ["push %ebp"]
		code += ["movl %esp, %ebp"]
		code += ["sub ${}, %esp".format(split_var(i[1])[2])]
		code += ["push %ebx", "push %esi", "push %edi"]

		regs = init_regs.copy()
		unused_temp_vars_in_reg = list()
		temp_vars = dict()
		function_width = 12+int(split_var(i[1])[2])
		temp_offset = 0

	elif i[0] == "putretval":
		offset=int(i[2])
		if get_type(i[1]) == "c":
			code += ["movl {}, {}(%ebp)".format(i[1], -offset)]
		elif get_type(i[1]) == "r":
			temp_var_name = split_var(i[1])[0]
			code += ["movl %{}, {}(%ebp)".format(temp_vars[temp_var_name]["ro"], -offset)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[1]) == "m":
			offset2=0
			if "var" in i[1]:
				offset2 = int(split_var(i[1])[1])
			elif "tmp#" in i[1]:
				temp_var_name = split_var(i[1])[0]
				offset2 = temp_vars[temp_var_name]["so"]
			reg=get_reg("#", 4)
			code += ["movl {}(%ebp), %{}".format(-offset2, reg)]
			code += ["movl %{}, {}(%ebp)".format(reg, -offset)]
			remove_used_temp_var_in_reg("#")

	elif i[0] == "return":
		code += ["sub ${}, %esp".format(temp_offset)]
		code += ["pop %edi", "pop %esi", "pop %ebx", "movl %ebp, %esp"]
		code += ["pop %ebp"]
		code += ["ret"]
		temp_offset = 0

	elif i[0] == "returnsize":
		code += ["sub ${}, %esp".format(i[1])]
		code += ["push %eax", "push %ecx", "push %edx"]

	elif i[0] == "pass":
		if get_type(i[1]) == "c":
			code += ["push {}".format(i[1])]
		elif get_type(i[1]) == "r":
			temp_var_name = split_var(i[1])[0]
			code += ["push %{}".format(temp_vars[temp_var_name]["ro"])]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[1]) == "m":
			offset = 0
			if "var" in i[1]:
				offset = int(split_var(i[1])[1])
			elif "tmp#" in i[1]:
				temp_var_name = split_var(i[1])[0]
				offset = temp_vars[temp_var_name]["so"]
				remove_used_temp_var_in_mem(temp_var_name)
			code += ["push {}(%ebp)".format(-offset)]

	elif i[0] == "call":
		code += ["call {}".format(split_var(i[1])[0])]
		code += ["add ${}, %esp".format(split_var(i[1])[1])]
		code += ["pop %edx", "pop %ecx", "pop %eax"]

	elif i[0] == "getretval":
		width = int(split_var(i[1])[1])
		temp_var_name = split_var(i[1])[0]
		temp_vars[temp_var_name] = {"ro":-1, "so":function_width+temp_offset+width, "width":width}
		temp_offset += width

	elif i[0] == "unary&":
		temp_var_name = split_var(i[1])[0]
		width = int(split_var(i[1])[1])
		new_reg = get_reg(temp_var_name, width)
		offset = int(split_var(i[2])[1])
		code += ["lea {}(%ebp), %{}".format(-offset, new_reg)]

	elif i[0] == "unary*":
		temp_var_name = split_var(i[1])[0]
		width = int(split_var(i[1])[1])
		new_reg = get_reg(temp_var_name, width)
		if get_type(i[2]) == "r":
			addr_var_name = split_var(i[2])[0]
			code += ["movl 0(%{}), %{}".format(temp_vars[addr_var_name]["ro"], new_reg)]
			remove_used_temp_var_in_reg(addr_var_name)
		elif get_type(i[2]) == "m":
			offset=0
			if "var" in i[2]:
				offset = int(split_var(i[2])[1])
			elif "tmp#" in i[2]:
				offset = temp_vars[split_var(i[2])[0]]["so"]
				remove_used_temp_var_in_mem(split_var(i[2])[0])
			code += ["movl {}(%ebp), %{}".format(-offset, new_reg)]
			code += ["movl 0(%{}), %{}".format(new_reg, new_reg)]

	elif i[0] == "unary-":
		temp_var_name = split_var(i[1])[0]
		width = int(split_var(i[1])[1])
		new_reg = get_reg(temp_var_name, width)
		if get_type(i[2]) == "c":
		    code += ["mov {}, %{}".format(i[2], new_reg)]
		elif get_type(i[2]) == "r":
		    temp_var_name = split_var(i[2])[0]
		    reg_old = temp_vars[temp_var_name]["ro"]
		    code += ["mov %{}, %{}".format(reg_old, new_reg)]
		    remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[2]) == "m":
		    if "tmp#" in i[2]:
		        temp_var_name = split_var(i[2])[0]
		        temp_offset = int(temp_vars[temp_var_name]["so"])
		        code += ["mov {}(%ebp), %{}".format(-temp_offset, new_reg)]
		        remove_used_temp_var_in_mem(temp_var_name)
		    else:
		        var_offset = int(split_var(i[2])[1])
		        code += ["mov {}(%ebp), %{}".format(-var_offset, new_reg)]
		code += ["neg %{}".format(new_reg)]

	elif i[0] in ["inc", "dec"]:
	    op="decl"
	    if i[0] == "inc":
	        op="incl"
	    if get_type(i[1])=='m':
	        if "tmp#" in i[1]:
	            temp_var_name = split_var(i[1])[0]
	            temp_offset = int(temp_vars[temp_var_name]["so"])
	            code += ["{} {}(%ebp)".format(op, -temp_offset)]
	        else:
	            var_offset = int(split_var(i[1])[1])
	            code += ["{} {}(%ebp)".format(op, -var_offset)]
	    elif get_type(i[1])=='r':
	        temp_var_name=split_var(i[1])[0]
	        reg = temp_vars[temp_var_name]["ro"]
	        code += ["{} %{}".format(op, reg)]

	elif i[0] in ["int+=", "int-=", "int*=", "int/=", "int"]:
	    op=op_dic[i[0][3]]
	    var_offset = split_var(i[1])[1]
	    # print(left_temp_var_name, width)
	    new_reg = get_reg("#", 4)
	    if get_type(i[2]) == "c":
	        code += ["mov {}, %{}".format(i[2], new_reg)]
	    elif get_type(i[2]) == "r":
	        temp_var_name = split_var(i[2])[0]
	        code += ["mov %{}, %{}".format(temp_vars[temp_var_name]["ro"], new_reg)]
	        remove_used_temp_var_in_reg(temp_var_name)
	    elif get_type(i[2]) == "m":
	        if "tmp#" in i[2]:
	            temp_var_name = split_var(i[2])[0]
	            code += ["mov {}(%ebp), %{}".format(-temp_vars[temp_var_name]["so"], new_reg)]
	            remove_used_temp_var_in_mem(temp_var_name)
	        elif "var" in i[2]:
	            var_offset = int(split_var(i[2])[1])
	            code += ["mov {}(%ebp), %{}".format(-var_offset, new_reg)]
	    var_offset = int(split_var(i[1])[1])
	    code += ["{} %{}, {}(%ebp)".format(op, new_reg, -var_offset)]
	    remove_used_temp_var_in_reg("#")

	elif i[0] == "=":
		dest = ''
		addr_var_name = ''
		if get_type(i[1]) == "*":
			if get_type(i[1][1:]) == "*": # Handling only **var = _
				offset = int(split_var(i[1][2:])[1])
				reg = get_reg("##", 4)
				code += ["movl {}(%ebp), %{}".format(-offset, reg)]
				code += ["movl 0(%{}), %{}".format(reg, reg)]
				dest = "0(%{})".format(reg)
			elif get_type(i[1][1:]) == "r":
				addr_var_name = split_var(i[1][1:])[0]
				dest = "0(%{})".format(temp_vars[addr_var_name]["ro"])
			elif get_type(i[1][1:]) == "m":
				offset = int(split_var(i[1][1:])[1])
				reg = get_reg("##", width)
				code += ["movl {}(%ebp), %{}".format(-offset, reg)]
				dest = "0(%{})".format(reg)
		elif get_type(i[1]) == "m":
			offset_to = int(split_var(i[1])[1])
			dest = "{}(%ebp)".format(-offset_to)

		if get_type(i[2]) == "c": #m=c
			code += ["movl {}, {}".format(i[2], dest)]
		elif get_type(i[2]) == "r": #m=r
			temp_var_name = split_var(i[2])[0]
			code += ["movl %{}, {}".format(temp_vars[temp_var_name]["ro"], dest)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[2]) == "m": #m=m
			offset_from = 0
			if "var" in i[2]:
				offset_from = int(split_var(i[2])[1])
			elif "tmp#" in i[2]:
				offset_from = temp_vars[split_var(i[2])[0]]["so"]
				remove_used_temp_var_in_mem(split_var(i[2])[0])
			reg = get_reg("#", 4)
			code += ["movl {}(%ebp), %{}".format(-offset_from, reg)]
			code += ["movl %{}, {}".format(reg, dest)]
			remove_used_temp_var_in_reg("#")
		remove_used_temp_var_in_reg("##")
		remove_used_temp_var_in_reg(addr_var_name)

	elif i[0] in ["int+", "int-", "int*", "int/", "int&", "int^", "int|"]:
		op = op_dic[i[0][3:]]
		width = int(split_var(i[1])[1])
		left_temp_var_name = split_var(i[1])[0]
		# print(left_temp_var_name, width)
		new_reg = ''
		if op == 'idivl':
			new_reg = 'eax'
		else:
			new_reg = get_reg(left_temp_var_name, width)

		if get_type(i[2]) == "c" or get_type(i[2]) == -1:
			code += ["movl {}, %{}".format(i[2], new_reg)]
		elif get_type(i[2]) == "r":
			temp_var_name = split_var(i[2])[0]
			code += ["movl %{}, %{}".format(temp_vars[temp_var_name]["ro"], new_reg)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[2]) == "m":
			if "tmp#" in i[2]:
				temp_var_name = split_var(i[2])[0]
				code += ["movl {}(%ebp), %{}".format(-temp_vars[temp_var_name]["so"], new_reg)]
				remove_used_temp_var_in_mem(temp_var_name)
			elif "var" in i[2]:
				var_offset = int(split_var(i[2])[1])
				code += ["movl {}(%ebp), %{}".format(-var_offset, new_reg)]
		if op == 'idivl':
			code += ["cdq"]

		if get_type(i[3]) == "c" or get_type(i[3]) == -1:
			if op == 'idivl':
				reg = get_reg("#", 4)
				code += ["movl {}, %{}".format(i[3], reg)]
				code += ["{} %{}".format(op, reg)]
				remove_used_temp_var_in_reg("#")
			else:
				code += ["{} {}, %{}".format(op, i[3], new_reg)]
		elif get_type(i[3]) == "r":
			temp_var_name = split_var(i[3])[0]
			if op == 'idivl':
				code += ["{} %{}".format(op, temp_vars[temp_var_name]["ro"])]
			else:
				code += ["{} %{}, %{}".format(op, temp_vars[temp_var_name]["ro"], new_reg)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[3]) == "m":
			if "tmp#" in i[3]:
				temp_var_name = split_var(i[3])[0]
				if op == 'idivl':
					code += ["{} {}(%ebp)".format(op, -temp_vars[temp_var_name]["so"])]
				else:
					code += ["{} {}(%ebp), %{}".format(op, -temp_vars[temp_var_name]["so"], new_reg)]
				remove_used_temp_var_in_mem(temp_var_name)
			elif "var" in i[3]:
				var_offset = int(split_var(i[3])[1])
				if op == 'idivl':
					code += ["{} {}(%ebp)".format(op, -var_offset)]
				else:
					code += ["{} {}(%ebp), %{}".format(op, -var_offset, new_reg)]
		if op == 'idivl':
			new_reg = get_reg(left_temp_var_name, width)
			code += ["movl %eax, %{}".format(new_reg)]

	elif i[0] in ["int<=", "int>=", "int==", "int!=", "int>", "int<", "bool<=", "bool>=", "bool>", "bool<", "bool==", "bool!="]:
		# print i[0][3:]
		# print len(i[0])
		if 'int' in i[0]:
			op = op_dic[i[0][3:]]
		else:
			op = op_dic[i[0][4:]]
		width = int(split_var(i[1])[1])
		left_temp_var_name = split_var(i[1])[0]
		# print(left_temp_var_name, width)
		new_reg = get_reg(left_temp_var_name, width)

		if get_type(i[2]) == "c" or get_type(i[2]) == -1:
			code += ["movl {}, %{}".format(i[2], new_reg)]
		elif get_type(i[2]) == "r":
			temp_var_name = split_var(i[2])[0]
			code += ["movl %{}, %{}".format(temp_vars[temp_var_name]["ro"], new_reg)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[2]) == "m":
			if "tmp#" in i[2]:
				temp_var_name = split_var(i[2])[0]
				code += ["movl {}(%ebp), %{}".format(-temp_vars[temp_var_name]["so"], new_reg)]
				remove_used_temp_var_in_mem(temp_var_name)
			elif "var" in i[2]:
				var_offset = int(split_var(i[2])[1])
				code += ["movl {}(%ebp), %{}".format(-var_offset, new_reg)]

		if get_type(i[3]) == "c" or get_type(i[3]) == -1:
			code += ["cmp {}, %{}".format(i[3], new_reg)]
		elif get_type(i[3]) == "r":
			temp_var_name = split_var(i[3])[0]
			code += ["cmp %{}, %{}".format(temp_vars[temp_var_name]["ro"], new_reg)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[3]) == "m":
			if "tmp#" in i[3]:
				temp_var_name = split_var(i[3])[0]
				code += ["cmp {}(%ebp), %{}".format(-temp_vars[temp_var_name]["so"], new_reg)]
				remove_used_temp_var_in_mem(temp_var_name)
			elif "var" in i[3]:
				var_offset = int(split_var(i[3])[1])
				code += ["cmp {}(%ebp), %{}".format(-var_offset, new_reg)]
		code += ["movl $0, %eax"]
		code += ["set{} %al".format(op)]
		code += ["movl %eax, %{}".format(new_reg)]

	elif i[0] in ["gotoZeroNeg", "gotoPos"]:
		jump_command=""
		if i[0]=="gotoZeroNeg":
			jump_command="jle"
		else:
			jump_command="jg"
		if get_type(i[1]) == "c":
			reg = get_reg("#", 4)
			code += ["movl {}, %{}".format(i[1], reg)]
			code += ["cmp $0, %{}".format(reg)]
			code += ["{} {}".format(jump_command, i[2])]
			remove_used_temp_var_in_reg('#')
		elif get_type(i[1]) == "r":
			temp_var_name=split_var(i[1])[0]
			reg = temp_vars[temp_var_name]["ro"]
			code += ["cmp $0, %{}".format(reg)]
			code += ["{} {}".format(jump_command, i[2])]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[1]) == "m":
			reg = get_reg("#", 4)
			if "tmp#" in i[1]:
				temp_var_name = split_var(i[1])[0]
				temp_offset = int(temp_vars[temp_var_name]["so"])
				code += ["movl {}(%ebp), %{}".format(-temp_offset, reg)]
				code += ["cmp $0, %{}".format(reg)]
				code += ["{} {}".format(jump_command, i[2])]
				remove_used_temp_var_in_mem(temp_var_name)
			else:
				var_offset = int(split_var(i[1])[2])
				code += ["movl {}(%ebp), %{}".format(-var_offset, reg)]
				code += ["cmp $0, %{}".format(reg)]
				code += ["{} {}".format(jump_command, i[2])]
			remove_used_temp_var_in_reg('#')

	elif i[0] == "goto":
	    code += ["jmp {}".format(i[1])]

	elif i[0][:5]=="label":
	    code += [line[:-1]]

	elif i[0] == "print": # this assumes all other instructions are finished
		var_offset = int(split_var(i[1])[1])
		code.append("push %eax")
		code.append("push %ebx")
		code.append("push %ecx")
		code.append("push %edx")
		code.append("push %esi")
		code.append("push %edi")
		code.append("movl {}(%ebp), %eax".format(-var_offset))
		code.append("push %ebp")
		code.append("mov %esp, %ebp")
		code.append("push %eax")
		code.append("push $fmt_int")
		code.append("call printf")
		code.append("add  $8, %esp")
		code.append("mov %ebp, %esp")
		code.append("pop %ebp")
		code.append("pop %edi")
		code.append("pop %esi")
		code.append("pop %edx")
		code.append("pop %ecx")
		code.append("pop %ebx")
		code.append("pop %eax")

	elif i[0] == "scan":# this assumes all other instructions are finished
		code.append("push %eax")
		code.append("push %ebx")
		code.append("push %ecx")
		code.append("push %edx")
		code.append("push %esi")
		code.append("push %edi")
		code.append("lea {}(%ebp), %eax".format(-int(split_var(i[1])[1])))
		code.append("push %ebp")
		code.append("mov %esp, %ebp")
		code.append("push %eax")
		code.append("push $scan_int")
		code.append("call scanf")
		code.append("add  $8, %esp")
		code.append("mov %ebp, %esp")
		code.append("pop %ebp")
		code.append("pop %edi")
		code.append("pop %esi")
		code.append("pop %edx")
		code.append("pop %ecx")
		code.append("pop %ebx")
		code.append("pop %eax")

print(".data")
print('\tfmt_int: .string \"%d\\n\"')
print('\tscan_int: .string \"%d\"')
print("\t.text")
print("\t.global main")
print("\t.type main, @function")
for i in code:
	if ":" in i:
		print(i)
	else:
		print("\t"+i)
