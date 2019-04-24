#Name: Conor Berns
#Student ID: 17456886
import os
import os.path
import sys
from multiprocessing import *
import subprocess
import shlex
import copy
import shelltools
class Shellins:
	def __init__(self, input_arg = None, output_argv = sys.__stdout__, background_exe = None):
		self.stdin_param = input_arg
		self.stdout_param = output_argv
		self.background_param = background_exe
		self.environ = os.environ
		self.path = os.getcwd()
		self.start_point = os.getcwd()
		self.commands = {
			"cd" : self.change_dir,
			"dir" : self.list_dir,
			"clr": self.clear_screen,
			"environ": self.list_environ,
			"echo" : self.echo,
			"help" : self.help,
			"pause": self.pause,
			"quit": self.quit,
			"path":self.list_path,
			"alias": self.alias,
			"revert" : self.revert_alias
			}	
		self.environ["shell"] = self.start_point
		self.environ["PWD"] = self.path
		# Initialises the shell and pwd variables. The pwd will change as the shell execs, the shell variable obviously will remain constant


	def change_dir(self, target = None):
		# if the target doesnt exist report the current directory
		if target is None:
			print(self.path, file=self.stdout_param)

		else:
			try:
				# change the directory and update the path
				os.chdir(target)
				self.path = os.getcwd()
				self.environ["PWD"] = self.path
				print(self.path, file=self.stdout_param)
			except FileNotFoundError:
				print("No such directory " + target, file=self.stdout_param)
	
	def list_dir(self, target = None):
		# split the path to be indexed easily
		indexable_path = self.path.split("/")
		# if the path hasnt been supplied OR is the same as the current path
		#print the current directories files
		if target is None or target == indexable_path[-1]:
			listconts = os.listdir(self.path)
			for i in listconts:
				print(i, file = self.stdout_param)
			#print(*os.listdir(self.path), file = self.stdout_param)
		else:
			try:
				#try list the target directories files
				listconts = os.listdir(target)
				for i in listconts:
					print(i, file = self.stdout_param)
			except FileNotFoundError:
				print("No such directory " + target , file = self.stdout_param)
			except NotADirectoryError:
				print(target + " is not a directory", file = self.stdout_param)
	def clear_screen(self):
		for i in range(100):
			print()

	def list_environ(self):
		for k,v in self.environ.items():
			print(k,v)


	def echo(self, args1 = None):
		if type(args1) is list:
			# if the arguments are a list unpack them
			print(*args1, file = self.stdout_param)
		elif args1 is None:
			print(file = self.stdout_param)
		else:
			# otherwise print them back the way they arrived
			print(args1, file = self.stdout_param)


	def help(self, more_filter = None):
		if more_filter is not None:
			# if we have been supplied the more filter
			with open("readme", "r") as man:
				# open the manual
				a = man.readlines()
				x = 0
				#read it into a list for storage and allowing us to easily print 
				while x < len(a):
					if input() == "":
						# print in blocks of 20 lines
						print(*a[x:x + 20], file = self.stdout_param)
						x += 20
					
		else:
			with open("readme", "r") as man:
				a = man.readlines()
				print(*a[0:92], file = self.stdout_param)





	def alias(self, target_command, new_command):
		global alias_dict
		# make our alias_dict global so we can revert
		alias_dict = dict(self.commands)
		#make a copy of our commands dictionary
		self.commands[new_command] = self.commands[target_command]
		# reassign the key to the target functions

	def revert_alias(self):
		# reverts the alias back
		self.commands = alias_dict

	def list_path(self):
		# trivial list path command
		print(self.path, file = self.stdout_param)

	def pause(self):
		# very simple but effective pause
		input()

	def quit(self):
		# quits preserving ALL file states
		sys.exit(0)

		
	def spawn_process(self, target_func, arguments = None):
		if arguments is None or not len(arguments) :
			# execute the target func in the background with no args
			background_proc = Process(target = target_func)
			print("[2] " + str(os.getpid()))
			background_proc.run()
		else:
			try:
			#execute the target func in the background with args
				background_proc = Process(target = target_func, args = (arguments,))
				print("[2] " + str(os.getpid()))
				background_proc.run()
			except TypeError:
				new_args = arguments.split()
				background_proc = Process(target = target_func, args = (*new_args,))
				print("[2] " + str(os.getpid()))
				background_proc.run()
		# cool little pid 
		




if len(sys.argv[1:]):
	shellins = Shellins(sys.argv[1])
else:
	shellins = Shellins()

if shellins.stdin_param is None:
	while True:
		shelltools.runner(shellins, input("[" + shellins.path + "]" + " $ "))
else:
	with open(shellins.stdin_param, "r") as reader:
		for line in reader:
			shelltools.runner(shellins, line)