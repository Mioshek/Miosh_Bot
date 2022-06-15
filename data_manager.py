import json
import os
import pathlib

PATH:str = str(pathlib.Path(__file__).parent.resolve())

class JsonManager:
    CONFIG_JSON:str = PATH + "/data/config.json"

    @staticmethod
    def write_to_json(data)->None:
        with open(JsonManager.CONFIG_JSON, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        json_file.close()

    @staticmethod
    def read_from_json()->dict:
        with open(JsonManager.CONFIG_JSON, 'r') as json_file:
            loaded_json_data = json.load(json_file)
        json_file.close()
        return loaded_json_data
    
    
class SystemManager:   
    
    @staticmethod
    def create_dir(folder_name)->None: 
        os.mkdir(PATH + folder_name)
        

class TxtManager:
    
    @staticmethod
    def save_txt(data, path):
        txt_file = open(path, 'a')
        txt_file.write(data)
        txt_file.close()