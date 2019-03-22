import os
import sys
from multiprocessing import Process, Queue
import subprocess
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
		if args1:
			print(args1)
		else:
			
			init = args1.split()
			return_val = " ".join(init)

			print(return_val,  file=self.stdout_param)
			
	def help(self, more_filter = None):
		if more_filter is None:
			with open("Readme.txt") as help_manual:
				for line in help_manual:
					print(line)


	def alias(self, target_command, new_command):
		global alias_dict
		alias_dict = dict(self.commands)
		self.commands[new_command] = self.commands[target_command]

	def revert_alias(self):
		self.commands = alias_dict



	def list_path(self):
		print(self.path)

	def pause(self):
		input()

	def quit(self):
		sys.exit(0)

	def spawn_subprocess(self, target_func, arguments = None):
		background_proc = Process(target = target_func, args = (arguments,))
		background_proc.start()






def main():
	if sys.argv[0]:
		shell = Shellins()
		while True:
			command = input("[" + shell.path + "]" + " : ").strip().split()
		
			if command[0] not in shell.commands:
				print("myshell: command not found: " + command[0])
				continue
			if (len(command) - 1) > 1 and command[0] != "alias":
				shell.commands[command[0]](command[1:])
			else:
				shell.commands[command[0]](*command[1:])
			
	


if __name__ == '__main__':
	main()

