import json
import os
import pathlib
from datetime import date, datetime


PATH:str = str(pathlib.Path(__file__).parent.resolve())

class JsonManager:
    JSON_PATH:str = PATH + "/data/config.json"

    @staticmethod
    def write_to_json(data)->None:
        with open(JsonManager.JSON_PATH, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        json_file.close()

    @staticmethod
    def read_from_json()->dict:
        with open(JsonManager.JSON_PATH, 'r') as json_file:
            loaded_json_data = json.load(json_file)
        json_file.close()
        return loaded_json_data
    
    
class SystemManager:   
    
    @staticmethod
    def create_dir(folder_name)->None: 
        os.mkdir(PATH + folder_name)
        

class TxtManager:
    LOGS_PATH:str = PATH + "/data/logs.txt"
    
    @staticmethod
    def add_log(data):
        logs_txt = open(TxtManager.LOGS_PATH, 'a')
        logs_txt.write(data)
        logs_txt.close()
        
    @staticmethod
    def create_log(message):
        today = date.today()
        current_date = today.strftime("%d/%B/%Y")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        log = "Day: {day} Time: {time} User: {usr} Log: {log}\n".format(day=current_date, time=current_time, usr=message.author,log=message.content)
        TxtManager.add_log(log)

