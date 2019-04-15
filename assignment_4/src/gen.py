import re
from collections import OrderedDict

init_regs = OrderedDict()
init_regs["eax"] = 0
init_regs["ecx"] = 0
init_regs["edx"] = 0
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

	temp_offset += int(width)
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
	unused_temp_vars_in_reg.remove(name)
	regs[temp_vars[name]["ro"]]=0
	del temp_vars[name]

def remove_used_temp_var_in_mem(name):
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	# print("DELETING", name)
	del temp_vars[name]

def get_type(name):
	# print(name)
	name=split_var(name)[0]
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	if "var" in name:
		return "m"
	elif "tmp#" in name:
		if temp_vars[name]["ro"]!=-1:
			return "r"
		else:
			return "m"
	elif name[1:].isdigit():
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
op_dic = {'+':"add", '-':"sub", '*':"imul", '/':"idiv", '&':"and", '^':"xor", '|':"or", '<':"l", '<=':"le", '>':"g", '>=':"ge", '==':"e", '!=':"ne"}

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

	if i[0] == "funcstart":
		regs = init_regs.copy()
		unused_temp_vars_in_reg = list()
		temp_vars = dict()
		function_width = int(i[1])
		temp_offset = 0
		code += [i[2]]

	if i[0] == "funcend":
		code += ["sub ${}, %esp".format(temp_offset)]

	if i[0] == "getretval":
		width = int(split_var(i[1])[1])
		temp_var_name = split_var(i[1])[0]
		temp_vars[temp_var_name] = {"ro":-1, "so":function_width+temp_offset+width, "width":width}
		temp_offset += width

	if i[0] == "putretval":
		offset=int(i[2])
		if get_type(i[1]) == "c":
			code += ["mov {}, {}(%ebp)".format(i[1],-offset)]
		elif get_type(i[1]) == "r":
			temp_var_name = split_var(i[1])[0]
			code += ["mov %{}, {}(%ebp)".format(temp_vars[temp_var_name]["ro"],-offset)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[1]) == "m":
			offset2=0
			if "var" in i[1]:
				offset2 = int(split_var(i[1])[1])
			elif "tmp#" in i[1]:
				temp_var_name = split_var(i[1])[0]
				offset2 = temp_vars[temp_var_name]["so"]
			reg=get_reg("#",4)
			code += ["mov {}(%ebp), %{}".format(-offset2,reg)]
			code += ["mov %{}, {}(%ebp)".format(reg,-offset)]
			remove_used_temp_var_in_reg("#")

	elif i[0] in ["pop", "call", "mov", "add", "sub", "ret"]: # push and pop
		code += [line[:-1]]

	elif i[0] == "push":
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
			code += ["push {}(%ebp)".format(-offset)]
		elif get_type(i[1]) == -1:
			code += ["push {}".format(i[1])]

	elif i[0] == "=":
		if (get_type(i[1]), get_type(i[2])) == ("m", "c"): #m=c
			var_offset = int(split_var(i[1])[1])
			code += ["mov {}, {}(%ebp)".format(i[2], -var_offset)]
		elif (get_type(i[1]), get_type(i[2])) == ("m", "r"): #m=r
			var_offset = int(split_var(i[1])[1])
			temp_var_name = split_var(i[2])[0]
			code += ["mov %{}, {}(%ebp)".format(temp_vars[temp_var_name]["ro"], -var_offset)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif (get_type(i[1]), get_type(i[2])) == ("m", "m"): #m=m
			var_offset_from=0
			if "var" in i[2]:
				var_offset_from = int(split_var(i[2])[1])
			elif "tmp#" in i[2]:
				temp_var_name =	split_var(i[2])[0]
				var_offset_from = temp_vars[temp_var_name]["so"]

			var_width = int(split_var(i[2])[-1])
			var_offset_to = int(split_var(i[1])[1])
			reg=get_reg("#", var_width)
			code += ["mov {}(%ebp), %{}".format(-var_offset_from, reg)]
			code += ["mov %{}, {}(%ebp)".format(reg, -var_offset_to)]
			remove_used_temp_var_in_reg("#")

	elif i[0] in ["int+", "int-", "int*", "int/", "int&", "int^", "int|", "bool&", "bool^", "bool|"]:
		op = op_dic[i[0][3:]]
		width = split_var(i[1])[1]
		left_temp_var_name = split_var(i[1])[0]
		# print(left_temp_var_name, width)

		new_reg = get_reg(left_temp_var_name, width)
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

		if get_type(i[3]) == "c":
			code += ["{} {}, %{}".format(op, i[3], new_reg)]
		elif get_type(i[3]) == "r":
			temp_var_name = split_var(i[3])[0]
			code += ["{} %{}, %{}".format(op, temp_vars[temp_var_name]["ro"], new_reg)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[3]) == "m":
			if "tmp#" in i[3]:
				temp_var_name = split_var(i[3])[0]
				code += ["{} {}(%ebp), %{}".format(op, -temp_vars[temp_var_name]["so"], new_reg)]
				remove_used_temp_var_in_mem(temp_var_name)
			elif "var" in i[3]:
				var_offset = int(split_var(i[3])[1])
				code += ["{} {}(%ebp), %{}".format(op, -var_offset, new_reg)]

	elif i[0] in ["int<=", "int>=", "int==", "int!=", "int>", "int<", "bool<=", "bool>=", "bool>", "bool<", "bool==", "bool!="]:
		# print i[0][3:]
		# print len(i[0])
		if 'int' in i[0]:
			op = op_dic[i[0][3:]]
		else:
			op = op_dic[i[0][4:]]
		width = split_var(i[1])[1]
		left_temp_var_name = split_var(i[1])[0]
		# print(left_temp_var_name, width)

		new_reg = get_reg(left_temp_var_name, width)
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

		if get_type(i[3]) == "c":
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
		code += ["set{} %{}".format(op, new_reg)]

	elif i[0] in ["gotoZeroNeg", "gotoPos"]:
		jump_command=""
		if i[0]=="gotoZeroNeg":
			jump_command="jle"
		else:
			jump_command="jg"
		if get_type(i[1]) == "c":
			reg = get_reg("#", 4)
			code += ["mov {}, %{}".format(i[1], reg)]
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
				code += ["mov {}(%ebp), %{}".format(-temp_offset, reg)]
				code += ["cmp $0, %{}".format(reg)]
				code += ["{} {}".format(jump_command, i[2])]
				remove_used_temp_var_in_mem(temp_var_name)
			else:
				var_offset = int(split_var(i[1])[2])
				code += ["mov {}(%ebp), %{}".format(-var_offset, reg)]
				code += ["cmp $0, %{}".format(reg)]
				code += ["{} {}".format(jump_command, i[2])]
			remove_used_temp_var_in_reg('#')

	elif i[0] == "goto":
	    code += ["jump {}".format(i[1])]

	elif i[0][:5]=="label":
	    code += [line[:-1]]
	elif i[0] == "print":# this assumes all other instructions are finished
		code.append("push %ebp")
		code.append("mov %esp, %ebp")
		code.append("push %eax")
		code.append("push $print_int")
		code.append("call printf")
		code.append("add  $8, %esp")
		code.append("mov %ebp, %esp")
		code.append("pop %ebp")

print(".data")
print("print_int:")
print("\t.string \"%d\"")
for i in code:
	if ":" in i:
		print(i)
	else:
		print("\t"+i)