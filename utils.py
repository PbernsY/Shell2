import sys
import os
import os.path
import shlex
import subprocess
import myshell


# Flags are as follows, [background_exec, output_destination]
def set_flags(string):
	''' This is a function to set a list of flags. These flags are then used to perform tasks
	like background execution etc '''
	global flags
	global output
	global parseable
	# set up global variables so they can be passed to the other relevant parsing functions
	flags = []
	output = []
	parseable = shlex.split(string)
	if not len(string):
		return
		# this prevent us trying to index an empty string
	if parseable[-1] == "&":
		# we know, if the ampersand is present, it can only be the last character of the input string
		# if thats the case, append the ampersand to the flags list while removing it from the end of the input string
		flags.append(parseable.pop())

	if ">>" in string or ">" in string:
		# append the redirection file name to the flags list

		flags.append(parseable.pop())
		# append the redirection symbol to the output list
		output.append(parseable.pop())

	return flags, parseable, output



def check_background_redirect(command):
	''' this function is solely used to execute NON WRITTEN commands in the background and redirect their output '''
	if len(flags) == 2:
		#here we have both an output redirect and a background exec
		with open(flags[-1], checkwrite(output)) as current_file:
			subprocess.run(command, stdout = current_file)
			

	elif len(flags) == 1 and not len(output):
		# here we simply have a background exec
		subprocess.run(command)

	elif len(flags) == 1 and len(output):
		# redirection, no background
		with open(flags[-1], checkwrite(output)) as current_file:
			subprocess.run(command, stdout = current_file)

	else:
		sys_binary(command)




def sys_binary(list):
	''' i said this shell didnt use the force, but theres some unwordly action going on here ;)'''
	pid = os.fork()
	# if pid > 0 -> Parent process control
	# else -> Child process control
	if pid > 0:
		wpid = os.waitpid(pid, 0)

	else:
		try:
			# try to execute in the format below
			os.execvp(parseable[0], parseable)
		except:
			#catch an error if one is thrown
			print("myshell: command not found " + parseable[0])
			#sys exit closes the fork that otherwise would be left opened by the error
			sys.exit()

	
def spawn_process(target, args):
	''' this is a utility function to call the spawn process function within the shell class'''
	shellins.spawn_process(target,args)



def bothflags(exece, args):
	current_command = shellins.commands[exece]
	''' this function is called when both flags are set [background_exec, outputfilename]'''
	with open(flags[-1], checkwrite(output)) as current_file:
		# open the file name with file mode depending on the checkwrite function
		shellins.stdout_param = current_file
		# modify the stdout of our shell based on file we opened
		# spawn a process for our shell to exec 
		spawn_process(current_command, args)

def oneflag(exece, args):
	''' this function is called when one flag is set in our flags list'''
	current_command = shellins.commands[exece]
	if len(output) == 0:
		# if the length of the output list is 0, we just have to background exec
		spawn_process(current_command, args)
		#spawns a process for the command
		return
	else:
		# we simply have to redirect output, not background exec
		with open(flags[-1], checkwrite(output)) as current_file:
			# open the file in the appropriate mode
			shellins.stdout_param = current_file
			# change stdout to the file
			if len(args):
				# this implies our command has arguments, pass them
					current_command(args)
			else:
				# run the 0 arg command
					current_command()

def checkwrite(output_list):
	''' handy little function to determine the filemode'''
	return "a" if ">>" in output_list else "w"

def runner(string):
	if len(string) is 0:
		return
		# utility to prevent erros
	set_flags(string)
	if parseable[0][0] == "$":
		environ_var = os.path.expandvars(parseable[0])
		print(environ_var, file = shellins.stdout_param)
		return
	#set flags as applicable
	shellins.stdout_param = sys.__stdout__
	# ensure stdout is reverted back to default
	exece = parseable[0]
	# exece is the command
	new_args = " ".join(parseable[1:])
	args = os.path.expandvars(new_args)
	try:
		if exece not in shellins.commands :
			# if the command isnt in our dictionary, try to exec it as a sys binary/programme invocation
			try:
				check_background_redirect(parseable)
			except FileNotFoundError:
				# this catches if the command was not found 
				print("myshell: command not found " + string)
			return
		current_command = shellins.commands[exece]
		# reference the code like above, helps improve appearance
		if len(flags) == 2:
			# call both flags function is they are both set
			bothflags(exece, args)

		elif len(flags) == 1:
			# same as above, call one flag if one is set
			oneflag(exece, args)
		else:
			# we are dealing with  a standard command
			if len(args):
				try:
					# execute it from the commands dictionary with args
					current_command(args)
				except TypeError:
					# we have supplied inneficient args, correct this
					current_command(*parseable[1:])
			else:
				# func takes no args, pass none 
				current_command()
	except KeyError:
		print("command not found " + string)
	
	except TypeError:
		print("incorrect amount of args supplied to " + exece)




def starter():
	commands = sys.argv[1:]
	if len(commands):
		return myshell.Shellins(commands[0])
	else:
		return myshell.Shellins()
	




