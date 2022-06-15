import subprocess
import data_manager
from pathlib import Path
import os

class Console:
    #divides commands between cd and others (working in progress; some new commands will be added if neccessary)
    def determine_command(message, read_data_raw)->str:
        path:dict = read_data_raw["paths"]
        command:list = message.content[1:].split(" ")
        print(command)
        command_copy:list = command
        for index, argument in enumerate(command_copy):
            if argument == "" or argument == " " or argument == "   ":
                command.pop(index)
        if path["current_path"] != "":
            current_path = path["current_path"]
            previous_path = path["previous_path"]
        
        if "cd" in command[0]: 
            return ChangeDirectory.proper_cd_type(cmd=command, cp=current_path, pp=previous_path, json_data=read_data_raw)
        else:
            return Console.execute_command(command, current_path, previous_path, read_data_raw)
    
    #returns ready path
    @staticmethod
    def get_path(dir_counter:int, path)->str: #dir_counter determines whether get upper or same directory
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
    
    #executes linux command in bash
    @staticmethod
    def execute_command(command, current_path, previous_path, read_data_raw)->str:
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
                data_manager.JsonManager.write_to_json(read_data_raw)

        except Exception as exc: output = str(exc)
        return "```" + output + "```"
    
    def simulate_console()->None:   #temporary checking function
        while True:
            Console.determine_command(input())
    
class ChangeDirectory:
    
    #defines type of cd command and returns output(path or error)
    @staticmethod        
    def proper_cd_type(**kwargs)->str:
        command:list = kwargs["cmd"]
        current_path:str = kwargs["cp"]
        previous_path:str = kwargs["pp"]
        json_data:dict = kwargs["json_data"]
        command_length:int = len(command)
        if command_length == 2:
            second_argument:str = command[1]
            if second_argument == "..": return ChangeDirectory.go_up_dir(current_path, json_data)
            #moves to home path
            elif second_argument == "/": return Console.execute_command("pwd", "/", current_path, json_data)
            elif second_argument == "-": return ChangeDirectory.go_previous_dir(current_path, previous_path, json_data)
            elif second_argument == "~": return ChangeDirectory.go_user_directory(current_path, json_data)
            else: return ChangeDirectory.go_specyfic_directory(current_path, second_argument, json_data)
        elif command_length == 1:
            return ChangeDirectory.go_user_directory(current_path, json_data)
        else: return f"```No such file or directory: {current_path + command[1]}\n The only avaliable are: \n{os.listdir(current_path)}```"
        
    #returnes last used path and current path, backs you up to last used path
    @staticmethod
    def go_previous_dir(c_path, p_path, json_data)->str:
        current_path = p_path
        previous_path = c_path
        return Console.execute_command("pwd", current_path, previous_path, json_data)
    
    #goes up a directory
    @staticmethod
    def go_up_dir(current_path, json_data)->str:
        previous_path = current_path
        current_path = Console.get_path(-2, current_path)
        return Console.execute_command("pwd", current_path, previous_path, json_data)
    
    #moves you to user directory /home/user
    @staticmethod
    def go_user_directory(current_path, json_data)->str:
        previous_path = current_path
        current_path = str(Path.home())
        return Console.execute_command("pwd", current_path, previous_path, json_data)
    
    #moves you to specified directory
    @staticmethod
    def go_specyfic_directory(current_path, second_argument, json_data)->str:
        avaliable_dirs:list = os.listdir(current_path)
        print(type(avaliable_dirs))
        previous_path = current_path
        if second_argument in avaliable_dirs:
            is_dir = os.path.isdir(current_path + "/" + second_argument)
            if is_dir:
                current_path =  (current_path + "/" + second_argument + "/")
        else: return "```No such file or directory: {path}\n The only avaliable are: \n{avaliable}```". format(path=current_path + second_argument, avaliable=os.listdir(current_path))
        return Console.execute_command("pwd", current_path, previous_path, json_data)