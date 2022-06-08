import json
import os
import pathlib

class JsonManager:
    PATH:str = str(pathlib.Path(__file__).parent.resolve())
    JSON_PATH:str = PATH + "/data.json"

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
        os.mkdir(JsonManager.PATH + folder_name)