import discord
from  LinuxConsole import Console
from json_manager import JsonManager as jm

def path_setter():
    default_path = Console.get_path(0, False)
    data = jm.read_from_json()
    default_paths={"previous_path": "",
        "current_path": default_path}
    data["paths"] = default_paths
    jm.write_to_json(data)
    return data