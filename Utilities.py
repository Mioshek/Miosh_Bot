from datetime import datetime, timedelta
from threading import currentThread
from time import sleep

class Utilities():
    def swap(arr, beg_index, end_index):
        temp = arr[beg_index]
        arr[beg_index] = arr[end_index]
        arr[end_index] = temp
        return arr
############################################################     
    def split_into_parts(string:str, splitter:str, ignore_multiple_occurrence:bool):
        if ignore_multiple_occurrence: return string.split(splitter)
        list_of_split_elements:list = []
        current__word:str = ""
        string_length = len(string)
        for index, letter in enumerate(string):
            if index == string_length-1:
                if letter != splitter:
                    list_of_split_elements.append(current__word+letter)
                elif letter == splitter and current__word != "":
                    list_of_split_elements.append(current__word)
            elif letter == splitter and current__word != "":
                list_of_split_elements.append(current__word)
                current__word = ""
            elif letter != splitter: current__word +=letter
        return list_of_split_elements
############################################################    
    class Sorting():
        def bubble_sorting(arr):
            arr_size = len(arr)
            for first_element in arr:
                for second_element in arr:
                    if first_element > second_element: Utilities.swap(arr, first_element, second_element) 
            return arr
############################################################        
        def counting_sort(arr):
            size = len(arr)
            largest_el = max(arr)
            output = [0] * size

            # count array initialization
            count = [0] * (largest_el + 1)

            # storing the count of each element 
            for m in range(0, size):
                count[arr[m]] = count[arr[m]] + 1

            # storing the cumulative count
            for m in range(1, largest_el):
                count[m] += count[m - 1]

            # place the elements in output array after finding the index of each element of original array in count array
            m = size - 1
            while m >= 0:
                output[count[arr[m]] - 1] = arr[m]
                count[arr[m]] -= 1
                m -= 1

            for m in range(0, size):
                arr[m] = output[m]
            
            arr[size-1] = largest_el
            
            print(arr)
################################################################
    def check_current_time():                      
        return datetime.now()
    
    def time_benchmark(start_time, end_time):
        print("Start Time: ", start_time)
        print("End Time: ", end_time)
        print("Taken Time: ", (end_time- start_time))