from asyncore import read
import subprocess
import json_manager
from pathlib import Path
import os

class Console:
    def determine_command(message, read_data_raw)->str:
        path:dict = read_data_raw["paths"]
        command:list = message.content[1:].split(" ")
        command_copy:list = command
        for index, argument in enumerate(command_copy):
            if argument == "" or argument == " " or argument == "   ":
                command.pop(index)
        if path["current_path"] != "":
            current_path = path["current_path"]
            previous_path = path["previous_path"]
        
        if "cd" in command[0]: 
            return ChangeDirectory.execute_proper_cd_type(cmd=command, cp=current_path, pp=previous_path, json_data=read_data_raw)
        else:
            return Console.execute_command(command, current_path, previous_path, read_data_raw)
    
    @staticmethod
    def get_path(dir_counter:int, path)->str: #dir_counter determines whether get upper or lower directory
        if path == False:
            path:str = ""
            path_raw:list = []
            process  = subprocess.Popen("pwd",
                            stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            path_raw:list = str(stdout)[2:-3].split("/")
        else: path_raw = path.split("/")
        if dir_counter == 0: 
            for element in path_raw[1:]:
                path += "/" + element 
        else:
            path = ""
            for element in path_raw[1:dir_counter]:
                path += "/" + element 
        return path + "/"
    
    @staticmethod
    def execute_command(command, current_path, previous_path, read_data_raw):
        output:str = ""
        try:
                print("command: ", command)
                process:subprocess.Popen = subprocess.Popen(command,
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                cwd=current_path)
                stdout, stderr = process.communicate()
                output_list:list = str(stdout)[2:-1].split("\\n")
                for index, element in enumerate (output_list[:-1]):
                    output += str(index+1) + ".  " + element + "\n"
                read_data_raw["paths"] = {"previous_path": previous_path, "current_path":current_path} 
                json_manager.JsonManager.write_to_json(read_data_raw)

        except Exception as exc: output = str(exc)
        return "```"+ "\n" + output + "```"

    
    
def simulate_console()->None:   #temporary checking function
    while True:
        Console.determine_command(input())

class ChangeDirectory:
    
    @staticmethod        
    def execute_proper_cd_type(**kwargs)->tuple or str or bool or list:
        command = kwargs["cmd"]
        current_path = kwargs["cp"]
        previous_path = kwargs["pp"]
        json_data = kwargs["json_data"]
        command_length = len(command)
        if command_length == 2:
            second_argument = command[1]
            #goes up a directory
            if second_argument == "..": return ChangeDirectory.go_up_dir(current_path, json_data)
            #moves to home path
            elif second_argument == "/": return Console.execute_command("pwd", "/", current_path, json_data)
            #returnes last used path and current path, backs you up to last used path
            elif second_argument == "-": return ChangeDirectory.go_previous_dir(current_path, previous_path, json_data)
            #moves you to user directory /home/user
            elif second_argument == "~": return ChangeDirectory.go_user_directory(current_path, json_data)
            #moves you to specified directory
            else: return ChangeDirectory.go_specyfic_directory(current_path, second_argument, json_data)
        elif command_length == 1:
            return ChangeDirectory.go_user_directory(current_path, json_data)
        else: return "No such file or directory: '{path}' ". format(path=second_argument)
        
    @staticmethod
    def go_previous_dir(c_path, p_path, json_data)->tuple: #returns a tuple of current path and last used path
        current_path = p_path
        previous_path = c_path
        return Console.execute_command("pwd", current_path, previous_path, json_data)
    
    @staticmethod
    def go_up_dir(current_path, json_data):
        previous_path = current_path
        current_path = Console.get_path(-2, current_path)
        return Console.execute_command("pwd", current_path, previous_path, json_data)
    
    @staticmethod
    def go_user_directory(current_path, json_data):
        previous_path = current_path
        current_path = str(Path.home())
        return Console.execute_command("pwd", current_path, previous_path, json_data)
    
    @staticmethod
    def go_specyfic_directory(current_path, second_argument, json_data):
        avaliable_dirs = os.listdir(current_path)
        previous_path = current_path
        if second_argument in avaliable_dirs:
            is_dir = os.path.isdir(current_path + "/" + second_argument)
            if is_dir:
                current_path =  (current_path + "/" + second_argument + "/")
        return Console.execute_command("pwd", current_path, previous_path, json_data)