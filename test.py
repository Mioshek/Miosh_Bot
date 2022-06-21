# from pathlib import Path
# import os

# parent_dir = Path(__file__).parent.resolve()
# path = os.path.join(parent_dir, "test")
  
# # Create the directory
# # 'GeeksForGeeks' in
# # '/home / User / Documents'
# os.mkdir(path)
# path = os.path.join(parent_dir, "test")
# print("PAHT")
# print(path)
# string = "ls  a  l ls a"
# print(string.split(" "))
# import subprocess
# process  = subprocess.Popen("pwd",
#                         stdout=subprocess.PIPE, 
#                          stderr=subprocess.PIPE)
# stdout, stderr = process.communicate()
# path = str(stdout)[2:-3].split("/")
# new_path = ""
# for element in path:
#     new_path += element + "/"
# print(new_path)


# process = subprocess.Popen("pwd", 
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.PIPE,
#                     cwd=new_path)
# stdout, stderr = process.communicate()
# path = str(stdout)[2:-3].split("/")
# new_path = ""
# for element in path[:-1]:
#     new_path += element + "/"
# print(new_path)
# def test():
#     return 1,5
# print(type(test()))
# cos = ("frisk")
# coss = ["list"]

# if cos is tuple:
#     print("tuple")
# if type(coss) is list:
#     print('list')
# import pathlib

# print(str(pathlib.Path(__file__).parent.resolve())+ "/cos.py")


# x = [1,2,3,4,5,6]
# print(x[:-1])

# from pathlib import Path
# home = str(Path.home())
# print(home)

# def main():
#     return 1, 2
# print(main())
# cd
# x = " cd"
# if "cd" in x:
#     print("yes")
# dictionary = {
#     1:"one",
#     2:"two",
#     3:"three"
# }
# if "two" in dictionary:
#     print(True)
# else: print(False)

def add(x):
    return x+5

def divide(x):
    return x/5

def subtract(x):
    return x-5

dictionary = {}
dictionary["add"] = add
dictionary["divide"] = divide
dictionary["subtract"] = subtract


print(dictionary["add"](5))