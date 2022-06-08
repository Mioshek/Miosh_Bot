import subprocess
import json_manager
from pathlib import Path
import os

class Console:
    def execute_command(message, read_data_raw)->str:
        path = read_data_raw["paths"]
        output:str = ""
        command:list = message.content[1:].split(" ")
        if path["current_path"] != "":
            current_path = path["current_path"]
            previous_path = path["previous_path"]
        content = ChangeDirectory.check_if_cd(command, current_path, previous_path)
        #retype
        if type(content) is list:
            current_path = content[0]
            previous_path = content[1]
            command:str = "pwd"
        
        if type(content) is tuple:
            previous_path = current_path
            current_path = content[0]
            command:str = "pwd"
        
        if type(content) is str:
            previous_path = current_path
            current_path = content
            command:str = "pwd"
        #retype
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
    
    
def simulate_console()->None:   #temporary checking function
    while True:
        Console.execute_command(input())

class ChangeDirectory:
    
    @staticmethod        
    def check_if_cd(command, current_path, previous_path)->tuple or str or bool or list:
        if command[0][0:2] == "cd":
            command_length = len(command)
            if command_length == 2:
                second_argument = command[1]
                #goes up a directory
                if second_argument == "..": return Console.get_path(-2, current_path)
                #moves to home path
                elif second_argument == "/": return "/"
                #returnes last used path and current path, backs you up to last used path
                elif second_argument == "-": return ChangeDirectory.dash_case(current_path, previous_path)
                #moves you to user directory /home/user
                elif second_argument == "~": return str(Path.home())
                #moves you to specified directory
                else: 
                    avaliable_dirs = os.listdir(current_path)
                    print(avaliable_dirs)
                    if second_argument in avaliable_dirs:
                        is_dir = os.path.isdir(current_path + "/" + second_argument)
                        if is_dir:
                            return (current_path + "/" + str(command[1]) + "/") 
            elif command_length == 2:
                return str(Path.home())
            else: return "No such file or directory: '{path}' ". format(path=second_argument)
        else: return False
        
    @staticmethod
    def dash_case(c_path, p_path)->tuple: #returns a tuple of current path and last used path
        current_path = p_path
        previous_path = c_path
        return current_path, previous_path
        