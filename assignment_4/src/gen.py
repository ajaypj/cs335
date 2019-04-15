import re
from collections import OrderedDict

regs = OrderedDict()
regs["eax"] = 0
regs["ecx"] = 0
regs["edx"] = 0
regs["ebx"] = 0
regs["esi"] = 0
regs["edi"] = 0

named_reg=["eax", "ecx", "edx", "ebx", "esi", "edi", "esp", "ebp"]

unused_temp_vars_in_reg=list()
temp_vars=dict()
function_width=100
temp_offset=0
code=list()

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

def transfer_reg_to_left(old, new, width): #check the width of the new reg
	global regs, unused_temp_vars_in_reg, temp_vars, temp_offset, function_width, code
	if temp_vars[old]["ro"]!=-1:
		temp_vars[new]={"ro":temp_vars[old]["ro"], "so":-1, "width":width}
	else:
		temp_vars[new]={"ro":get_reg(new), "so":-1, "width":width}
	unused_temp_vars_in_reg.append(new)
	remove_used_temp_var_in_reg(old)

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
op_dic = {'+':"add", '-':"sub", '*':"imul", '/':"idiv"}

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
		function_width = int(i[1])
		code += [i[2]]

	if i[0] == "freetmp":
		code += ["sub ${}, %esp".format(temp_offset)]

	if i[0] == "retval":
		if get_type(i[1]) == "c":
			code += ["mov {}, %eax".format(i[1])]
		elif get_type(i[1]) == "m":
			offset = 0
			if "var" in i[1]:
				offset = int(split_var(i[1])[1])
			elif "tmp#" in i[1]:
				temp_var_name = split_var(i[1])[0]
				offset = temp_vars[temp_var_name]["so"]
			code += ["mov {}(%ebp), %eax".format(-offset)]
		elif get_type(i[1]) == "r":
			temp_var_name = split_var(i[1])[0]
			code += ["mov %{}, %eax".format(temp_vars[temp_var_name]["ro"])]
			remove_used_temp_var_in_reg(temp_var_name)

	elif i[0] in ["pop", "call", "mov", "add", "sub"]: # push and pop
		code += [line[:-1]]

	elif i[0] == "push":
		if get_type(i[1]) == "c":
			code += ["push {}".format(i[1])]
		elif get_type(i[1]) == "m":
			offset = 0
			if "var" in i[1]:
				offset = int(split_var(i[1])[1])
			elif "tmp#" in i[1]:
				temp_var_name = split_var(i[1])[0]
				offset = temp_vars[temp_var_name]["so"]
			code += ["push {}(%ebp)".format(-offset)]
		elif get_type(i[1]) == "r":
			temp_var_name = split_var(i[1])[0]
			code += ["push %{}".format(temp_vars[temp_var_name]["ro"])]
			remove_used_temp_var_in_reg(temp_var_name)
		elif get_type(i[1]) == -1:
			code += ["push {}".format(i[1])]

	elif i[0] == "=":
		if (get_type(i[1]), get_type(i[2])) == ("m", "c"): #m=c
			var_offset = int(split_var(i[1])[1])
			code += ["mov {}, {}(%ebp)".format(i[2], -var_offset)]
		elif (get_type(i[1]), get_type(i[2])) == ("m", "r"): #m=r
			temp_var_name = split_var(i[2])[0]
			var_offset = int(split_var(i[1])[1])
			code += ["mov %{}, {}(%ebp)".format(temp_vars[temp_var_name]["ro"], -var_offset)]
			remove_used_temp_var_in_reg(temp_var_name)
		elif (get_type(i[1]), get_type(i[2])) == ("m", "m"): #m=m
			var_width = int(split_var(i[2])[-1])
			var_offset_to = int(split_var(i[1])[1])
			var_offset_from = int(split_var(i[2])[1])
			reg=get_reg("#", var_width)
			code += ["mov {}(%ebp), %{}".format(-var_offset_from, reg)]
			code += ["mov %{}, {}(%ebp)".format(reg, -var_offset_to)]
			remove_used_temp_var_in_reg("#")

	elif i[0][:3]=="int" or i[0][:4]=="bool":
		op = op_dic[i[0][3]]
		left_temp_var_name = split_var(i[1])[0]
		width = split_var(i[1])[1]
		# print(left_temp_var_name, width)
		if (get_type(i[2]), get_type(i[3])) == ("c", "c"): #c+c
			const1 = i[2]
			const2 = i[3]
			new_reg=get_reg(left_temp_var_name, width)
			code += ["mov {}, %{}".format(const1, new_reg)]
			code += ["{} {}, %{}".format(op, const2, new_reg)]

		elif (get_type(i[2]), get_type(i[3])) == ("r", "c"): #r+c
			temp_var_name = split_var(i[2])[0]
			const = i[3]
			code += ["{} {}, %{}".format(op, const, temp_vars[temp_var_name]["ro"])]
			transfer_reg_to_left(temp_var_name, left_temp_var_name, width)

		elif (get_type(i[2]), get_type(i[3])) == ("c", "r"): #c+r
			temp_var_name = split_var(i[3])[0]
			const = i[2]
			new_reg=get_reg(left_temp_var_name, width)
			code += ["mov {}, %{}".format(const, new_reg)]
			code+= ["{} %{}, %{}".format(op, temp_vars[temp_var_name]["ro"], new_reg)]
			remove_used_temp_var_in_reg(temp_var_name)

		elif (get_type(i[2]), get_type(i[3])) == ("m", "c"): #m+c
			if "tmp#" in i[2]:
				temp_var_name = split_var(i[2])[0]
				const = i[3]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov {}(%ebp), %{}".format(-temp_vars[temp_var_name]["so"], new_reg)]
				code += ["{} {}, %{}".format(op, const, new_reg)]
				remove_used_temp_var_in_mem(temp_var_name)
			elif "var" in i[2]:
				var_offset = int(split_var(i[2])[1])
				const = i[3]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov {}(%ebp), %{}".format(-var_offset, new_reg)]
				code += ["{} {}, %{}".format(op, const, new_reg)]

		elif (get_type(i[2]), get_type(i[3])) == ("c", "m"): #c+m
			if "tmp#" in i[3]:
				temp_var_name = split_var(i[3])[0]
				const = i[2]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov {}, %{}".format(const, new_reg)]
				code += ["{} {}(%ebp), %{}".format(op, -temp_vars[temp_var_name]["so"], new_reg)]
				remove_used_temp_var_in_mem(temp_var_name)
			elif "var" in i[3]:
				var_offset = int(split_var(i[3])[1])
				const = i[2]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov {}, %{}".format(const, new_reg)]
				code += ["{} {}(%ebp), %{}".format(op, -var_offset, new_reg)]

		elif (get_type(i[2]), get_type(i[3])) == ("r", "r"): #r+r
			if "tmp#" in i[2] and "tmp#" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code += ["{} %{}, %{}".format(op, temp_vars[temp_var_name2]["ro"], temp_vars[temp_var_name1]["ro"])]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)
				remove_used_temp_var_in_reg(temp_var_name2)

		elif (get_type(i[2]), get_type(i[3])) == ("r", "m"): #r+m
			if "tmp#" in i[2] and "tmp#" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code += ["{} {}(%ebp), %{}".format(op, -temp_vars[temp_var_name2]["so"], temp_vars[temp_var_name1]["ro"])]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)
				remove_used_temp_var_in_mem(temp_var_name2)
			if "tmp#" in i[2] and "var" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				var_offset = int(split_var(i[3])[1])
				code += ["{} {}(%ebp), %{}".format(op, -var_offset, temp_vars[temp_var_name1]["ro"])]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)

		elif (get_type(i[2]), get_type(i[3])) == ("m", "r"): #m+r
			if "tmp#" in i[2] and "tmp#" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov {}(%ebp), %{}".format(-temp_vars[temp_var_name1]["so"], new_reg)]
				code += ["{} %{}, %{}".format(op, temp_vars[temp_var_name2]["ro"], new_reg)]
				remove_used_temp_var_in_reg(temp_var_name2)
				remove_used_temp_var_in_mem(temp_var_name1)
			elif "var" in i[2] and "tmp#" in i[3]:
				var_offset = int(split_var(i[2])[1])
				temp_var_name1 = split_var(i[3])[0]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov {}(%ebp), %{}".format(-var_offset, new_reg)]
				code += ["{} %{}, %{}".format(op, temp_vars[temp_var_name1]["ro"], new_reg)]
				remove_used_temp_var_in_reg(temp_var_name1)

		elif (get_type(i[2]), get_type(i[3])) == ("m", "m"): #m+m
			loc1=""
			loc2=""
			new_reg=get_reg(left_temp_var_name, width)
			if "tmp#" in i[2] and "tmp#" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code += ["mov {}(%ebp), %{}".format(-temp_vars[temp_var_name1]["so"], new_reg)]
				code += ["{} {}(%ebp), %{}".format(op, -temp_vars[temp_var_name2]["so"], new_reg)]
				remove_used_temp_var_in_mem(temp_var_name1)
				remove_used_temp_var_in_mem(temp_var_name2)
			elif "tmp#" in i[2] and "var" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				var_offset = int(split_var(i[3])[1])
				code += ["mov {}(%ebp), %{}".format(-temp_vars[temp_var_name1]["so"], new_reg)]
				code += ["{} {}(%ebp), %{}".format(op, -var_offset, new_reg)]
				remove_used_temp_var_in_mem(temp_var_name1)
			elif "var" in i[2] and "tmp#" in i[3]:
				var_offset = int(split_var(i[2])[1])
				temp_var_name1 = str(split_var(i[3])[0]+split_var(i[3])[1])
				code += ["mov {}(%ebp), %{}".format(-var_offset, new_reg)]
				code += ["{} {}(%ebp), %{}".format(op, -temp_vars[temp_var_name1]["so"], new_reg)]
				remove_used_temp_var_in_mem(temp_var_name1)
			elif "var" in i[2] and "var" in i[3]:
				var_offset1 = int(split_var(i[2])[1])
				var_offset2 = int(split_var(i[3])[1])
				code += ["mov {}(%ebp), %{}".format(-var_offset1, new_reg)]
				code += ["{} {}(%ebp), %{}".format(op, -var_offset2, new_reg)]

for i in code:
	print(i)
