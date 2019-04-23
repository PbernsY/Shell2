import os
import sys
from multiprocessing import *
import subprocess
import shlex
import copy 
class Shellins:
	def __init__(self, input_arg = None, output_argv = sys.__stdout__, background_exe = None):
		self.stdin_param = input_arg
		self.stdout_param = output_argv
		self.background_param = background_exe
		self.environ = os.environ
		self.path = os.getcwd()
		self.commands = {
			"cd" : self.change_dir,
			"dir" : self.list_dir,
			"clr": self.clear_screen,
			"environ": self.list_environ,
			"echo" : self.echo,
			"help" : self.help,
			"pause": self.pause,
			"quit": self.quit,
			"sp" : self.spawn_subprocess,
			"path":self.list_path,
			"alias": self.alias,
			"revert" : self.revert_alias
			}	



	def change_dir(self, target = None):
		if target is None:
			print(self.path, file=self.stdout_param)

		else:
			try:
				os.chdir(target)
				self.path = os.getcwd()
				print(self.path, file=self.stdout_param)
			except FileNotFoundError:
				print("No such directory", file=self.stdout_param)
	
	def list_dir(self, target = None):
		indexable_path = self.path.split("/")
		if target is None or target == indexable_path[-1]:
			print(*os.listdir(self.path), file = self.stdout_param)
		else:
			try:
				print(*os.listdir(target), file=self.stdout_param)
			except FileNotFoundError:
				print("The directory does not exist")
	def clear_screen(self):
		for i in range(100):
			print()

	def list_environ(self):
		print(self.environ, file=self.stdout_param)


	def echo(self, args1):
		if type(args1) is list:
			print(*args1, file = self.stdout_param)
		else:
			print(args1, file = self.stdout_param)


	def help(self, more_filter = None):
		if more_filter is not None:
			with open("readme", "r") as man:
				a = man.readlines()
				x = 0
				while x < len(a):
					if input() == "":
						print(*a[x:x + 20])
						x += 20
				return
		with open("readme", "r") as man:
			a = man.readlines()
			print(*a[0:92])





	def alias(self, target_command, new_command):
		global alias_dict
		alias_dict = dict(self.commands)
		self.commands[new_command] = self.commands[target_command]

	def revert_alias(self):
		self.commands = alias_dict



	def list_path(self):
		print(self.path, file = self.stdout_param)

	def pause(self):
		input()

	def quit(self):
		sys.exit()

		
	def spawn_subprocess(self, target_func, arguments = None):
		if arguments is None:

			background_proc = Process(target = target_func)
		else:
			background_proc = Process(target = target_func, args = (arguments,))
		print("[2] " + str(os.getpid()))
		
		background_proc.run()


## if i call something to use a process, it requires to be passed a tuple or string, so join it 
## dont do this * !!!!!!
