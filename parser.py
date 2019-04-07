import sys
import shlex
import myshell

# Flags are as follows, [background_exec, output]


def set_flags(string):
	global flags
	global output
	global parseable
	flags = []
	output = []
	parseable = shlex.split(string)
	if parseable[-1] == "&":
		flags.append(parseable.pop())

	if ">>" in string or ">" in string:
		flags.append(parseable.pop())
		output.append(parseable.pop())

	return flags, parseable, output




def checkwrite(output_list):
	return "Append" if ">>" in output_list else "Truncate"

def parser(string):
	print(set_flags(string))
	

	#if len(flags) > 1:
	#	command = parseable[0]
	#	args = " ".join(parseable[1:])

	if len(flags) == 2:
		if checkwrite(output) == "Append":
			with open(output[0], "a") as current_file:
				shellins.stdout_param = current_file
				exece = parseable[0]
				args = " ".join(parseable[1:])
				shellins.commands["sp"](shellins.commands[exece], args)
		else:
			with open(flags[-1], "w") as current_file:
				shellins.stdout_param = current_file
				exece = parseable[0]
				args = " ".join(parseable[1:])
				shellins.commands["sp"](shellins.commands[exece], args)



#	if len(flags) == 1 and "&" not in flags:
#
#		command = parseable[0]
#		args = " ".join(parseable[1:])
#		return shellins.commands[command](args)

#	else:
#		command = string
#		return shellins.commands[command]

#print(set_flags("dir >> hello.txt"))
shellins = myshell.Shellins()
parser("dir ../ > j.txt &")
