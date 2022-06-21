import discord
from  LinuxConsole import Console
from data_manager import JsonManager as jm
from datetime import date, datetime
import data_manager

LOGS_PATH:str = data_manager.PATH + "/data/logs.txt"

#sets default path when restarting a bot or for the first time bot was launched
def default_path_setter():
    default_path = Console.get_path(0, False)
    data = jm.read_from_json()
    default_paths={"previous_path": "",
        "current_path": default_path}
    data["paths"] = default_paths
    jm.write_to_json(data)
    return data

def create_log(message):
    today = date.today()
    current_date = today.strftime("%d/%B/%Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    log = f"""Day: {current_date} Time: {current_time}
    Server: {message.guild.name} Channel: {message.channel}
    User: {message.author} Log: {message.content}\n"""
    data_manager.TxtManager.save_txt(log, LOGS_PATH)
    
def is_admin(message, admin_list):
    if message.author.id in admin_list:
        return True
