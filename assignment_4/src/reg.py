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

unused_temp_vars=list()
temp_vars=dict()
function_width=100
temp_offset=0
code=list()

def get_reg(name, width):
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	for i in regs:
		if regs[i]==0:
			regs[i]=1
			temp_vars[name]={"ro":i, "so":-1, "width":width}
			unused_temp_vars.append(name)
			return i
	old_temp_var = unused_temp_vars[0]
	old_reg = temp_vars[old_temp_var]["ro"]
	code += ["push %{}".format(old_reg)]
	# print(unused_temp_vars[0])
	del unused_temp_vars[0]
	unused_temp_vars.append(name)
	temp_vars[name]={"ro":old_reg, "so":-1, "width":width}
	#old reg changes
	regs[old_reg]=1
	temp_offset += int(width)
	temp_vars[old_temp_var]["so"]=function_width+temp_offset
	temp_vars[old_temp_var]["ro"]=-1
	return old_reg

def split_var(var_name):
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	name=re.split(":", var_name)
	return name

def write_list(file, a_list):
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	for i in a_list:
		file.write(i)
		file.write(" ")
	file.write("\n")

def remove_used_temp_var_in_reg(name):
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	# print("DELETING", name)
	unused_temp_vars.remove(name)
	del temp_vars[name]

def transfer_reg_to_left(old, new, width): #check the width of the new reg
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	if temp_vars[old]["ro"]!=-1:
		temp_vars[new]={"ro":temp_vars[old]["ro"], "so":-1, "width":width}
	else:
		temp_vars[new]={"ro":get_reg(new), "so":-1, "width":width}
	unused_temp_vars.append(new)
	remove_used_temp_var_in_reg(old)

def get_type(name):
	# print(name)
	name=split_var(name)[0]
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	if "var" in name:
		return "m"
	elif "tmp" in name:
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
	data=re.split(" |,|\n", line)
	new_data=list()
	for i in data:
		if i:
			new_data.append(i)
	data=new_data
	# print(data)
	ir.append(data)
	line=file.readline()
file.close()
# print(ir)

################################ Code generation ###############################
for i in ir:
	# print(i)
	# print(regs)
	# print(temp_vars)
	if i[0] ==  "funcstart":
		function_width = int(i[1])
		code += [i[2]]

	elif i[0] in ["push", "pop", "call", "mov", "sub"]: # push and pop
		temp_str=""
		for word in i:
			temp_str += word+' '
		code += [temp_str]

	elif i[0]=="int+":
		left_temp_var_name = split_var(i[1])[0]
		width = split_var(i[1])[1]
		# print(left_temp_var_name, width)
		if (get_type(i[2]),get_type(i[3])) == ("c","c"): #c+c
			const1 = i[2]
			const2 = i[3]
			new_reg=get_reg(left_temp_var_name, width)
			code += ["mov %{}, {}".format(new_reg, const1)]
			code += ["add %{}, {}".format(new_reg, const2)]

		elif (get_type(i[2]),get_type(i[3])) == ("r","c"): #r+c
			temp_var_name = split_var(i[2])[0]
			const = i[3]
			code += ["add %{}, {}".format(temp_vars[temp_var_name]["ro"], const)]
			transfer_reg_to_left(temp_var_name, left_temp_var_name, width)

		elif (get_type(i[2]),get_type(i[3])) == ("c","r"): #c+r
			temp_var_name = split_var(i[3])[0]
			const = i[2]
			code+= ["add %{}, {}".format(temp_vars[temp_var_name]["ro"], const)]
			transfer_reg_to_left(temp_var_name, left_temp_var_name, width)

		elif (get_type(i[2]),get_type(i[3])) == ("m","c"): #m+c
			if "tmp" in i[2]:
				temp_var_name = split_var(i[2])[0]
				const = i[3]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov %{}, dword ptr [rbp - {}]".format(new_reg, temp_vars[temp_var_name]["so"])]
				code += ["add %{}, {}".format(new_reg, const)]
				del temp_vars[temp_var_name]
			elif "var" in i[2]:
				var_offset = int(split_var(i[2])[1])
				const = i[3]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov %{}, dword ptr [rbp - {}]".format(new_reg, var_offset)]
				code += ["add %{}, {}".format(new_reg, const)]

		elif (get_type(i[2]),get_type(i[3])) == ("c","m"): #c+m
			if "tmp" in i[3]:
				temp_var_name = split_var(i[3])[0]
				const = i[2]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov %{}, dword ptr [rbp - {}]".format(new_reg, temp_vars[temp_var_name]["so"])]
				code += ["add %{}, {}".format(new_reg, const)]
				del temp_vars[temp_var_name]
			elif "var" in i[3]:
				var_offset = int(split_var(i[3])[1])
				const = i[2]
				new_reg=get_reg(left_temp_var_name, width)
				code += ["mov %{}, dword ptr [rbp - {}]".format(new_reg, var_offset)]
				code += ["add %{}, {}".format(new_reg, const)]

		elif (get_type(i[2]),get_type(i[3])) == ("r","r"): #r+r
			if "tmp" in i[2] and "tmp" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code += ["add %{}, %{}".format(temp_vars[temp_var_name1]["ro"], temp_vars[temp_var_name2]["ro"])]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)
				remove_used_temp_var_in_reg(temp_var_name2)

		elif (get_type(i[2]),get_type(i[3])) == ("r","m"): #r+m
			if "tmp" in i[2] and "tmp" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code += ["add %{}, dword ptr [rbp - {}]".format(temp_vars[temp_var_name1]["ro"], temp_vars[temp_var_name2]["so"])]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)
			if "tmp" in i[2] and "var" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				var_offset = int(split_var(i[3])[1])
				code += ["add %{}, dword ptr [rbp - {}]".format(temp_vars[temp_var_name1]["ro"], var_offset)]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)

		elif (get_type(i[2]),get_type(i[3])) == ("m","r"): #m+r
			if "tmp" in i[2] and "tmp" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code += ["add %{}, dword ptr [rbp - {}]".format(temp_vars[temp_var_name2]["ro"], temp_vars[temp_var_name1]["so"])]
				transfer_reg_to_left(temp_var_name2, left_temp_var_name, width)
				del temp_vars[temp_var_name1]
			elif "var" in i[2] and "tmp" in i[3]:
				var_offset = int(split_var(i[2])[1])
				temp_var_name1 = split_var(i[3])[0]
				code += ["add %{}, dword ptr [rbp - {}]".format(temp_vars[temp_var_name1]["ro"], var_offset)]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)

		elif (get_type(i[2]),get_type(i[3])) == ("m","m"): #m+m
			loc1=""
			loc2=""
			new_reg=get_reg(left_temp_var_name, width)
			if "tmp" in i[2] and "tmp" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				loc1 = temp_vars[temp_var_name1]["so"]
				loc2 = temp_vars[temp_var_name2]["so"]
			elif "tmp" in i[2] and "var" in i[3]:
				temp_var_name1 = split_var(i[2])[0]
				var_offset = int(split_var(i[3])[2])
				loc1 = temp_vars[temp_var_name1]["so"]
				loc2 = var_offset
			elif "var" in i[2] and "tmp" in i[3]:
				var_offset = int(split_var(i[2])[2])
				temp_var_name1 = str(split_var(i[3])[0]+split_var(i[3])[1])
				loc1 = var_offset
				loc2 = temp_vars[temp_var_name1]["so"]
			elif "var" in i[2] and "var" in i[3]:
				var_offset1 = int(split_var(i[2])[2])
				var_offset1 = int(split_var(i[3])[2])
				loc1 = var_offset1
				loc2 = var_offset2
			code += ["mov %{}, dword ptr [rbp - {}]".format(new_reg, loc1)]
			code += ["add %{}, dword ptr [rbp - {}]".format(new_reg, loc2)]

for i in code:
	print(i)
