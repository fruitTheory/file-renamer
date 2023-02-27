import os
import tkinter as tk
from tkinter import filedialog
# from tkinter import StringVar
from tkinter import *
from tkinter import messagebox


# Root variables
root = tk.Tk()
root.title("File Renamer")
root.geometry("400x200")


# Create 2 StringVar objects
file_name_var = StringVar()
file_ext_var = StringVar()

# Create 2 textfields
entry_name = Entry(root, textvariable=file_name_var)
entry_ext = Entry(root, textvariable=file_ext_var)

# Pack the textfields onto the window
entry_name.pack()
entry_ext.pack()

# Insert pre-text
entry_name.insert(0, "filename")
entry_ext.insert(0, ".png")

# Create a StringVar to hold the selected directory
selected_dir = StringVar()

# Create a text field to display the selected directory
dir_text = Entry(root, textvariable=selected_dir, width=60)
dir_text.pack()

# Create a button to open the directory selector
directory_button = Button(root, text="Select Directory", command=lambda: selected_dir.set(filedialog.askdirectory()))
directory_button.pack()


# Show user a message
def error_message():
    result = messagebox.showinfo("Error", "Please fill in all 3 fields", parent=root)

# File rename function
def file_rename():
    
    file_number = 0
    
    file_new_name = file_name_var.get()
    file_type = file_ext_var.get()
    directory = selected_dir.get() + "//"
    
    new_name_list = []
    
    # NOTE: if file name is changed while program is running it gets confused of whether the file is there or not
    # Check this out
    if file_name_var.get() == "" or file_ext_var.get() == "" or selected_dir.get() == "":
        error_message()
        raise ValueError("Missing text fields")
        
    else:
    
        for file in os.listdir(directory):

            #print(directory)
            #print(file_new_name+file_type)
            
            file_number +=1
            '''
            # This will print each file in the directory and in what order it is in.
            print("file number "+str(file_number)+":")
            print(file)
            print()
            '''
            
            old_file_path = os.path.join(directory+file)
            
            filepath_replace = old_file_path.replace(file, file_new_name) 
            
            new_file_path = filepath_replace+str(file_number)+file_type

            # Appends new names to empty list
            new_name_list.append(new_file_path)
            
            #print(old_file_path)
            #print(new_file_path)

            
            #WARNING: renames the files
            #os.rename(old_file_path, new_file_path)
            
            # break
            
    return new_name_list
print("Active")

def file_info():

    # Below gets selected direction and stores files in that directory into a list
    directory = selected_dir.get() + "//"
    base_directory = selected_dir.get()

    # Storage for files information
    file_list = []
    file_names = []
    file_count = 0

    for file in os.listdir(directory):
        # Take current filename and append to file name list
        file_names.append(file)

        # Just take current file path and append to file list
        current_file_path = os.path.join(directory+file)
        file_list.append(current_file_path)
    
    # Below loops through list of files and prints whether file or folder and size
    for file in file_list:
        
        # store size in bytes and convert to kb, if greater than 999 convert to MB and again to GB
        file_size = os.path.getsize(file)

        is_bytes = False
        is_kb = False
        is_mb = False
        is_gb = False

        # Find size in bytes and convert to kb, mb, gb, etc based on number of digits(bytes)
        size_length = len(str(file_size)) # get number of digits in sequence

        if size_length <= 3:
            # print("leave as bytes")
            is_bytes = True
        elif size_length >= 4 and size_length < 7: # greater than thousand less than a million
            # print("convert to kb")
            file_size = int(file_size/1024)
            is_kb = True
        elif size_length >= 7 and size_length < 10: # greater than million less than bilion
            # print("convert to mb")
            file_size = int((file_size/1024)/1024)
            is_mb = True
        elif size_length >= 10 and size_length < 13: # greater than a billion less than a trillion
            # print("convert to gb")
            file_size = round(((file_size/1024)/1024)/1024, 2)
            is_gb = True
        else:
            print("undefined size")
        
        if os.path.isfile(file) and is_bytes:
            print("The size of file " + file_names[file_count] + " is " + str(file_size) +" bytes")
        if os.path.isfile(file) and is_kb:
            print("The size of file " + file_names[file_count] + " is " + str(file_size) +" KB")
        if os.path.isfile(file) and is_mb:
            print("The size of file " + file_names[file_count] + " is " + str(file_size) +" MB")
        if os.path.isfile(file) and is_gb:
            print("The size of file " + file_names[file_count] + " is " + str(file_size) +" GB")

        file_count += 1


    '''
    functionality splits here -- gathering folder names and sizes
    
    '''

    total_size = 0
    memory_list = []
    folder_list = []
    folder_directory_list = []
    folder_count = 0

    for dirpath, dirnames, filenames in os.walk(base_directory):
        # print(dirpath)
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)
        
        folder_list.append(str(dirnames))

        # print(total_size)
        memory_list.append(str(total_size)) #important this occurs after for loop for last folder to get apended
        total_size -= total_size # clear out value after apendng to list

        folder_directory_list.append(str(dirpath))

        # if len(dirnames) > 0:
        #     print("one")
        
        #print(len(dirnames))
        
        folder_count += 1
    

    # stored memory values of folders in 
    del memory_list[0] # delete first index in folder memory list

    folder_list_0 = folder_list.pop(0) # first index of fodler list
    evaluated_folder_list = eval(folder_list_0) # apparently popped input was reading as a string not a list, so used eval()

    del folder_directory_list[0] # delete first index in directory list

    '''
    functionality splits here -- implementing folder names and sizes

    '''
    for i in range(folder_count-1):

        # loops through folder count range(some number) to control index position for memory list
        folder_size_len = len(str(memory_list[i]))

        is_bytes = False
        is_kb = False
        is_mb = False
        is_gb = False

        memory_list_int = int(memory_list[i])

        if folder_size_len <= 3:
            #print("leave as bytes")
            is_bytes = True
        elif folder_size_len >= 4 and folder_size_len < 7: # greater than thousand less than a million
            #print("convert to kb")
            memory_list_int = int(memory_list_int/1024)
            is_kb = True
        elif folder_size_len >= 7 and folder_size_len < 10: # greater than million less than bilion
            #print("convert to mb")
            memory_list_int = int((memory_list_int/1024)/1024)
            is_mb = True
        elif folder_size_len >= 10 and folder_size_len < 13: # greater than a billion less than a trillion
            #print("convert to gb")
            memory_list_int = round(((memory_list_int/1024)/1024)/1024, 2)
            is_gb = True
        else:
            print("undefined size")


        if os.path.isdir(folder_directory_list[i]) and is_bytes:
            print("The size of folder " + str(evaluated_folder_list[i]) + " is " + str(memory_list_int) +" bytes")

        if os.path.isdir(folder_directory_list[i]) and is_kb:
            print("The size of folder " + str(evaluated_folder_list[i]) + " is " + str(memory_list_int) +" KB")

        if os.path.isdir(folder_directory_list[i]) and is_mb:
            print("The size of folder " + str(evaluated_folder_list[i]) + " is " + str(memory_list_int) +" MB")

        if os.path.isdir(folder_directory_list[i]) and is_gb:
            print("The size of folder " + str(evaluated_folder_list[i]) + " is " + str(memory_list_int) +" GB")

    
    return 0


def file_select():

    # Option for just selected files 
    selected_files = filedialog.askopenfilenames()
    print("selected files = "+ str(selected_files))

    # output_window = tk.Toplevel(root)
    # output_window.title("Output")

    # output_label = tk.Label(output_window, text=file_info())
    # output_label.pack()

# Simple setup for outputing in tkinter
# output_button = tk.Button(root, text="Display output", command=file_select)
# output_button.pack()

# Rename button
button = Button(root, text="Rename", command=file_rename)
button.pack()

# Show directory info
button = Button(root, text="Show Directory Info", command=file_info)
button.pack()

# Select file button
button = Button(root, text="Select Files", command=file_select)
button.pack()


root.mainloop()

'''
Note: Can add functionality to list all names of files and choose what to do with that ability

'''
