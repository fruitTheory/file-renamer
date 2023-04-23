import functionality
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from send2trash import send2trash
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button, Entry
import subprocess

# Root variables
root = ttk.Window()
root.title("File Renamer")
root.geometry("450x400")
root.iconbitmap("icon.ico")
# Starts the window in light mode
style = Style(theme="cosmo")


# Create 2 StringVar objects
file_name_var = tk.StringVar()
file_ext_var = tk.StringVar()


theme_image_light = tk.PhotoImage(file="light.png").subsample(2, 2)
theme_image_dark = tk.PhotoImage(file="dark.png").subsample(2, 2)

# Function to change the theme and button image
def change_theme():
    if style.theme_use() == "cosmo":
        style.theme_use("darkly")
        dark_mode_button.config(image=theme_image_light)
    elif style.theme_use() == "darkly":
        style.theme_use("cosmo")
        dark_mode_button.config(image=theme_image_dark)


dark_mode_button = ttk.Button(root, image=theme_image_dark, command=change_theme)
dark_mode_button.place(relx=1, x=-10, y=10, anchor='ne')

# Create a label for the name textfield
label_file_name = tk.Label(root, text="Filename", font=("Helvetica", 14))

# Create a label for the extension textfield
label_file_ext = tk.Label(root, text="File extension", font=("Helvetica", 14))

label_select_dir = tk.Label(root, text="Directory", font=("Helvetica", 14))

# Create 2 textfields
entry_name = Entry(root, textvariable=file_name_var)
entry_ext = Entry(root, textvariable=file_ext_var)

# Pack the labels and textfields
label_file_name.pack()
entry_name.pack()
label_file_ext.pack()
entry_ext.pack()
label_select_dir.pack()


# Insert pre-text
entry_name.insert(0, "filename")
entry_ext.insert(0, ".png")

# Create a StringVar to hold the selected directory
selected_dir = tk.StringVar()

# Create a text field to display the selected directory
dir_text = Entry(root, textvariable=selected_dir, width=60)
dir_text.pack(pady=10)

# Define a row for the buttons
button_row = tk.Frame(root)
button_row.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

#* This function will open a directory selector and store the selected directory in the selected_dir variable, and then create a table with the files in the directory
def select_dir():
    selected_dir.set(filedialog.askdirectory())
    file_info()

# Create a button to open the directory selector
directory_button = Button(button_row, text="Select Directory", command=select_dir)
directory_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

def error_message():
    result = messagebox.showinfo("Error", "Please fill in all 3 fields", parent=root)

def file_rename():
        file_number = 0
        file_new_name = file_name_var.get()
        file_type = file_ext_var.get()
        directory = selected_dir.get() + "//" 
        new_name_list = []
        old_name_list = []

        if file_name_var.get() == "" or file_ext_var.get() == "" or selected_dir.get() == "":
            error_message()
            raise ValueError("Missing text fields")
            
        for file in os.listdir(directory):
                
            file_number +=1 #increment per file
            old_file_path = os.path.join(directory+file) #get current path
            filepath_replace = old_file_path.replace(file, file_new_name) #replace w/ new           
            new_file_path = filepath_replace+str(file_number)+file_type #store path

            # Appends new names to empty list
            new_name_list.append(new_file_path)
            # Appends old names to empty list
            old_name_list.append(old_file_path)
        
        # Create a new window to confirm the changes
        confirm_window = tk.Toplevel(root)
        confirm_window.title("Confirm")
        confirm_window.geometry("500x500")
        confirm_window.iconbitmap("icon.ico")
        label_confirm = tk.Label(confirm_window, text="Are you sure you want to rename these files?", font=("Helvetica", 14))
        label_confirm.pack(pady=10)

        # Function to rename the files
        def rename_files():
            for i in range(len(new_name_list)):
                os.rename(old_name_list[i], new_name_list[i])
            confirm_window.destroy()
            file_info()

            #? Maybe add some code to really confirm the changes were successful? for now it just shows a message box without checking, cause im lazy :)
            messagebox.showinfo("Success", "Files renamed successfully", parent=root)
        confirm_button = Button(confirm_window, text="Confirm", command=rename_files)

        confirm_button.pack(pady=10)
        table_confirm = ttk.Treeview(confirm_window, columns=(1,2), show="headings", height="18")
        table_confirm.heading(1, text="Old Name", anchor=tk.W)
        table_confirm.heading(2, text="New Name", anchor=tk.W)
        table_confirm.column(1, width=200)
        table_confirm.column(2, width=200)

        #* Old code to insert the old and new names into the table, this was replace by the code below it, because it provides a way for the user to edit the names
        # for i in range(len(new_name_list)):
        #     table_confirm.insert("", "end", values=(str(old_name_list[i]).split("//")[1], str(new_name_list[i]).split("//")[1]), open=True)
        # table_confirm.pack(pady=10)
        # confirm_window.mainloop()
        
        

        #* New code mentioned above
        #Code to edit the table, so that the user can change the names of the files

        # Loop through the lists and insert the old and new names into the table
        for i in range(len(new_name_list)):
            # Insert the old and new names into the table, the whole path is split and only the file name is inserted
            table_confirm.insert("", "end", values=(str(old_name_list[i]).split("//")[1], str(new_name_list[i]).split("//")[1]), open=True)
            

        
            # Function to edit the table
            def on_cell_double_click(event):
                # Get the row and column of the cell that was double clicked
                row_id = table_confirm.identify_row(event.y)
                column = table_confirm.identify_column(event.x)

                if row_id:
                    # Get the index of the column
                    column_index = int(column[1:]) - 1
                    # Get the old value of the cell
                    old_value = table_confirm.item(row_id, "values")[column_index]
                    # Add the directory to the old value
                    old_value = directory + old_value
                    # Create an entry widget to replace the cell
                    entry = ttk.Entry(table_confirm, textvariable=tk.StringVar())
                    entry.place(x=event.x, y=event.y, anchor="w")

                    # Function to update the table and the lists with the new value, when the user presses enter
                    def on_entry_confirm(_):
                        # Get the new value of the cell
                        new_value = entry.get()
                        # Update the table with the new value
                        table_confirm.set(row_id, column, new_value)
                        # Check which column was edited and update the lists with the new value
                        if column == "#1":
                            # Get the index of the old value in the "old_name_list" list
                            old_name_index:int = old_name_list.index(old_value)
                            # Update the list with the new value
                            old_name_list[old_name_index]:list = new_value
                        # Check which column was edited and update the lists with the new value
                        elif column == "#2":
                            # Get the index of the old value in the "new_name_list" list
                            new_name_index:int = new_name_list.index(old_value)
                            # Update the list with the new value
                            new_name_list[new_name_index]:list = directory + new_value
                        # Destroy the entry widget
                        entry.destroy()
                    # Bind the function to the entry widget, so that when the user presses enter, the function above is called
                    entry.bind("<Return>", on_entry_confirm)
                    entry.focus()


        table_confirm.pack(pady=10)
        # Bind the function to the table, so that when the user double clicks a cell, it becomes editable
        table_confirm.bind("<Double-1>", on_cell_double_click)
        # Function to delete the selected rows
        def delete_selected_rows():
            # Get the selected rows
            selected_items = table_confirm.selection()
            for item in selected_items:
                # Get the values of each cell in the row
                row_values = table_confirm.item(item)['values'] 
                for i in range(len(row_values)):
                    # Add the directory to the value
                    row_values[i] = directory + row_values[i]
                # Get the index of the old name in the "old_name_list" list
                old_name_index = old_name_list.index(str(row_values[0]))
                # Get the index of the new name in the "new_name_list" list
                new_name_index = new_name_list.index(str(row_values[1]))
                # Delete the old name from the "old_name_list" list
                del old_name_list[old_name_index]
                # Delete the new name from the "new_name_list" list
                del new_name_list[new_name_index]

                # Delete the selected rows from the table
                table_confirm.delete(item) 


                


        # Button to delete the selected rows
        delete_button = Button(confirm_window, text="Remove selected rows from renaming", command=delete_selected_rows)
        delete_button.pack(pady=10)
        confirm_window.mainloop()

#! Old function, not in use anymore
# File rename function
# def file_rename():
#     file_number = 0
#     file_new_name = file_name_var.get()
#     file_type = file_ext_var.get()
#     directory = selected_dir.get() + "//" 
#     new_name_list = []
    
#     # To-do: if file name is changed while program is running can get confused whether the file is there or not
#     if file_name_var.get() == "" or file_ext_var.get() == "" or selected_dir.get() == "":
#         error_message()
#         raise ValueError("Missing text fields")
    
#     else:
#         confirm = messagebox.askquestion("Confirm", "Are you sure you want to rename these files?\nThis will rename ALL files in the selected directory", parent=root)
#         if confirm == "yes":
    
#             for file in os.listdir(directory):
                
#                 file_number +=1 #increment per file
#                 old_file_path = os.path.join(directory+file) #get current path
#                 filepath_replace = old_file_path.replace(file, file_new_name) #replace w/ new           
#                 new_file_path = filepath_replace+str(file_number)+file_type #store path

#                 # Appends new names to empty list
#                 new_name_list.append(new_file_path)
            
#                 #WARNING: renames the files
#                 os.rename(old_file_path, new_file_path)
#             file_info()
#             return new_name_list
#         else:
#             pass


#? what is this for?
print("Active")



def file_info():

    #! horrible way of doing this, redo later, probably using something to monitor the directory for changes
    #* This line of code will call the function again after 2 seconds, so that the table will update every 2 seconds
    # root.after(2000, file_info)

    #* Table needs to be global, so that when the function is called again, it can destroy the old table and create a new one
    global table
    # Try to destroy table if it exists, so that a new one can be created
    try: 
        table.destroy()
    except:
        pass

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

    
    # Get number of files in directory
    table_height = len(file_list)

    # Create a table to display file information
    table = ttk.Treeview(root, columns=(1,2,3), show="headings", height=table_height)
    table.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    table.column(1, width=200)
    table.column(2, width=100)
    table.column(3, width=100)
    table.heading(1, text="File Name", anchor=tk.W, command=lambda: functionality.sort_treeview(table, 1, False, False))
    table.heading(2, text="File Type", anchor=tk.W, command=lambda: functionality.sort_treeview(table, 2, False, False))
    table.heading(3, text="File Size", anchor=tk.W, command=lambda: functionality.sort_treeview(table, 3, False, True))

    
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
            is_bytes = True
        elif size_length >= 4 and size_length < 7: # greater than thousand less than a million
            file_size = int(file_size/1024)
            is_kb = True
        elif size_length >= 7 and size_length < 10: # greater than million less than bilion
            file_size = int((file_size/1024)/1024)
            is_mb = True
        elif size_length >= 10 and size_length < 13: # greater than a billion less than a trillion
            file_size = round(((file_size/1024)/1024)/1024, 2)
            is_gb = True
        else:
            print("undefined size")
        table_file_size = ""
        if os.path.isfile(file) and is_bytes:
            # print("The size of file " + file_names[file_count] + " is " + str(file_size) +" bytes")
            table_file_size = str(file_size) + " bytes"
        if os.path.isfile(file) and is_kb:
            # print("The size of file " + file_names[file_count] + " is " + str(file_size) +" KB")
            table_file_size = str(file_size) + " KB"
        if os.path.isfile(file) and is_mb:
            # print("The size of file " + file_names[file_count] + " is " + str(file_size) +" MB")
            table_file_size = str(file_size) + " MB"
        if os.path.isfile(file) and is_gb:
            # print("The size of file " + file_names[file_count] + " is " + str(file_size) +" GB")
            table_file_size = str(file_size) + " GB"
        
        table.insert("", "end", values=(file_names[file_count], "File", table_file_size), open=True)
        


        file_count += 1

    '''
    functionality splits here -- gathering folder names and sizes
    '''
    #? While testing other functions, I see some errors probably caused by this, any idea why?

    total_size = 0
    memory_list = []
    folder_list = []
    folder_directory_list = []
    folder_count = 0

    for dirpath, dirnames, filenames in os.walk(base_directory):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)
        
        folder_list.append(str(dirnames))

        memory_list.append(str(total_size)) #important this occurs after for loop for last folder to get apended
        total_size -= total_size # clear out value after apendng to list

        folder_directory_list.append(str(dirpath))
        
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

        if folder_size_len <= 3: # base bytes
            is_bytes = True
        elif folder_size_len >= 4 and folder_size_len < 7: # (bytes to kb)
            memory_list_int = int(memory_list_int/1024)
            is_kb = True
        elif folder_size_len >= 7 and folder_size_len < 10: # (kb to mb)
            memory_list_int = int((memory_list_int/1024)/1024)
            is_mb = True
        elif folder_size_len >= 10 and folder_size_len < 13: # (mb to gb)
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

# File delete function
def file_delete():
    
    #get file extension from user
    file_ext = file_ext_var.get()
    #get directory +//
    directory = selected_dir.get() + "//"
    
    #file name list
    deleted_file_list = []

    # basic files list
    base_file_list = []
    base_extension_list = []
    
    if file_ext_var.get() == "" or selected_dir.get() == "":
        error_message()
        raise ValueError("Missing directory or file extension")
    
    else:
    # for loop to cycle files and separate/append data to lists
        for file in os.listdir(directory):

            # Split each file and extension
            base_files, base_extension = os.path.splitext(file)

            base_file_list.append(base_files)
            base_extension_list.append(base_extension) #this goes unused

    #for each basic file in the list, if theres duplicates"(count() > 1)" 
    # then append those to the list of files to delete
        for file in base_file_list:
            if base_file_list.count(file) > 1:
                deleted_file_list.append(file)

        # delete every second element (counting from the first)
        del deleted_file_list[::2]

        final_deleted_files = [] #set list for our final form files to delete
        # Now we need to re-add the directory path, and the type of extension we want to delete
        for each_file in deleted_file_list:
            dir_each_file = directory + each_file + file_ext #note that this adds the users select ext to to listed is --
            final_deleted_files.append(dir_each_file) #thus hardcoding it to an extent

        # In this code str() is used to convert each element to string, and
        #  join() concatenates these strings together with a comma between each element
        deleted_files_str = ', '.join(str(x) for x in final_deleted_files)
        print("Deleted files = " + deleted_files_str)

        # The final remove loop.
        for final_file in final_deleted_files:
            #WARNING: removes the files
            os.remove(final_file)

        return deleted_file_list

def file_select():
    # Option for just selected files 
    selected_files = filedialog.askopenfilenames()
    print("selected files = "+ str(selected_files))

# Rename button
button = Button(button_row, text="Rename", command=file_rename)
button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

#* This button is not really needed, the only reason it has to exist is to refresh the file list if needed
# Show directory info
# button = Button(button_row, text="Show Directory Info", command=file_info)
# button.pack(side=tk.LEFT, padx=5, pady=5)

# delete file button
button = Button(button_row, text="Delete Files", command=file_delete)
button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()

'''

Extra code:

# This will print each file in the directory and in what order it is in.
#print("file number "+str(file_number)+":")
#print(str(file)+" ")

'''
