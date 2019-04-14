import re
from collections import OrderedDict

regs={"eax":{"live":0},
"ebx":{"live":0},
"ecx":{"live":0},
"edx":{"live":0},
"esi":{"live":0},
"edi":{"live":0}
}

# print (regs)

named_reg=["eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp"]

unused_temp_vars=list()
temp_vars=dict()
function_width=100
temp_offset=0
code=list()

def get_reg(name, width):
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	for i in regs:
		if regs[i]["live"]==0:
			regs[i]["live"]=1
			temp_vars[name]={"ro":i, "so":-1, "width":width}
			unused_temp_vars.append(name)
			return i
	# print("ok")
	old_temp_var = unused_temp_vars[0]
	old_reg=temp_vars[old_temp_var]["ro"]
	code+= ["push %{}".format(old_reg)]
	del unused_temp_vars[0]
	unused_temp_vars.append(name)
	regs[old_reg]["live"]=1
	temp_vars[name]={"ro":old_reg, "so":-1, "width":width}
	#old reg changes
	temp_offset+= int(width)
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

def remove_used_temp_var(name):
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	unused_temp_vars.remove(name)
	del temp_vars[name]

def transfer_reg_to_left(old, new, width): #check the width of the new reg
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	if temp_vars[old]["ro"]!=-1:
		temp_vars[new]={"ro":temp_vars[old]["ro"], "so":-1, "width":width}
	else:
		temp_vars[new]={"ro":get_reg(new), "so":-1, "width":width}
	unused_temp_vars.append(new)
	remove_used_temp_var(old)

def get_type(name):
	global regs, unused_temp_vars, temp_vars, temp_offset, function_width, code
	if "var" in name:
		return "m"
	elif "tmp" in name:
		for i in temp_vars:
			if i==name:
				if temp_vars[i]["ro"]!=-1:
					return "r"
				else:
					return "m"
	elif name[1:].isdigit():
		return "c"
	else:
		return -1

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

for i in ir:
	# print(i)
	# if len(i)==1: # labels and ret
	# 	print(i[0])

	if i[0] in ["push", "pop", "call", "mov", "sub", "funcstart"]: # push and pop
		temp_str=""
		for lund in i:
			temp_str+=lund+' '
		code+= [temp_str]

	elif i[0]=="int+":
		# print("ok")
		left_temp_var_name = split_var(i[1])[0]
		width = split_var(i[1])[1]
		# print(left_temp_var_name, width)
		if (get_type(i[2]),get_type(i[3])) == ("c","c"): #c+c
			# print("ok")
			const1 = i[2]
			const2 = i[3]
			new_reg=get_reg(left_temp_var_name, width)
			code+= ["mov %{}, {}".format(new_reg, const1)]
			code+= ["add %{}, {}".format(new_reg, const2)]

		elif (get_type(i[2]),get_type(i[3])) == ("r","c"): #r+c
			temp_var_name = split_var(i[1])[0]
			const = i[3]
			code+= ["add %{}, {}".format(temp_vars[temp_var_name]["ro"], const)]
			transfer_reg_to_left(temp_var_name, left_temp_var_name)

		elif (get_type(i[2]),get_type(i[3])) == ("c","r"): #c+r
			temp_var_name = split_var(i[3])[0]
			const = i[2]
			code+= ["add %{}, {}".format(temp_vars[temp_var_name]["ro"], const)]
			transfer_reg_to_left(temp_var_name, left_temp_var_name)

		elif (get_type(i[2]),get_type(i[3])) == ("m","c"): #m+c
			if i[2]=="tmp":
				temp_var_name = split_var(i[2])[0]
				const = i[3]
				new_reg=get_reg(left_temp_var_name, width)
				code+= ["mov %{}, dword ptr [rbp - {}]".format(new_reg, temp_vars[temp_var_name]["so"])]
				code+= ["add %{}, {}".format(new_reg, const)]
				remove_used_temp_var(temp_var_name)
			elif i[2]=="var":
				var_offset = int(split_var(i[2])[1])
				const = i[3]
				new_reg=get_reg(left_temp_var_name, width)
				code+= ["mov %{}, dword ptr [rbp - {}]".format(new_reg, var_offset)]
				code+= ["add %{}, {}".format(new_reg, const)]

		elif (get_type(i[2]),get_type(i[3])) == ("c","m"): #c+m
			if i[3]=="tmp":
				temp_var_name = split_var(i[3])[0]
				const = i[2]
				new_reg=get_reg(left_temp_var_name, width)
				code+= ["mov %{}, dword ptr [rbp - {}]".format(new_reg, temp_vars[temp_var_name]["so"])]
				code+= ["add %{}, {}".format(new_reg, const)]
				remove_used_temp_var(temp_var_name)
			elif i[3]=="var":
				var_offset = int(split_var(i[3])[1])
				const = i[2]
				new_reg=get_reg(left_temp_var_name, width)
				code+= ["mov %{}, dword ptr [rbp - {}]".format(new_reg, var_offset)]
				code+= ["add %{}, {}".format(new_reg, const)]

		elif (get_type(i[2]),get_type(i[3])) == ("r","r"): #r+r
			if i[2]=="tmp" and i[3]=="tmp":
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code+= ["add %{}, %{}".format(temp_vars[temp_var_name1]["ro"], temp_vars[temp_var_name2]["ro"])]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)
				remove_used_temp_var(temp_var_name2)

		elif (get_type(i[2]),get_type(i[3])) == ("r","m"): #r+m
			if i[2]=="tmp" and i[3]=="tmp":
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code+= ["add %{}, dword ptr [rbp - {}]".format(temp_vars[temp_var_name1]["ro"], temp_vars[temp_var_name2]["so"])]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)

			if i[2]=="tmp" and i[3]=="var":
				temp_var_name1 = split_var(i[2])[0]
				var_offset = int(split_var(i[3])[1])
				code+= ["add %{}, dword ptr [rbp - {}]".format(temp_vars[temp_var_name1]["ro"], var_offset)]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)

		elif (get_type(i[2]),get_type(i[3])) == ("m","r"): #m+r
			if i[2]=="tmp" and i[3]=="tmp":
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				code+= ["add %{}, dword ptr [rbp - {}]".format(temp_vars[temp_var_name2]["ro"], temp_vars[temp_var_name1]["so"])]
				transfer_reg_to_left(temp_var_name2, left_temp_var_name, width)
				remove_used_temp_var(temp_var_name1)

			elif i[2]=="var" and i[3]=="tmp":
				var_offset = int(split_var(i[2])[1])
				temp_var_name1 = split_var(i[3])[0]
				code+= ["add %{}, dword ptr [rbp - {}]".format(temp_vars[temp_var_name1]["ro"], var_offset)]
				transfer_reg_to_left(temp_var_name1, left_temp_var_name, width)

		elif (get_type(i[2]),get_type(i[3])) == ("m","m"): #m+m
			loc1=""
			loc2=""
			new_reg=get_reg(left_temp_var_name, width)
			if i[2]=="tmp" and i[3]=="tmp":
				temp_var_name1 = split_var(i[2])[0]
				temp_var_name2 = split_var(i[3])[0]
				loc1 = temp_vars[temp_var_name1]["so"]
				loc2 = temp_vars[temp_var_name2]["so"]

			elif i[2]=="tmp" and i[3]=="var":
				temp_var_name1 = split_var(i[2])[0]
				var_offset = int(split_var(i[3])[2])
				loc1 = temp_vars[temp_var_name1]["so"]
				loc2 = var_offset

			elif i[2]=="var" and i[3]=="tmp":
				var_offset = int(split_var(i[2])[2])
				temp_var_name1 = str(split_var(i[3])[0]+split_var(i[3])[1])
				loc1 = var_offset
				loc2 = temp_vars[temp_var_name1]["so"]

			elif i[2]=="var" and i[3]=="var":
				var_offset1 = int(split_var(i[2])[2])
				var_offset1 = int(split_var(i[3])[2])
				loc1 = var_offset1
				loc2 = var_offset2

			code+= ["mov %{}, dword ptr [rbp - {}]".format(new_reg, loc1)]
			code+= ["add %{}, dword ptr [rbp - {}]".format(new_reg, loc2)]

for i in code:
	print(i)
