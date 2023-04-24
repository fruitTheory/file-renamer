import functionality
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from send2trash import send2trash
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button, Entry

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

# Create a button to change the theme
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

#* This function is working, but i've not yet tested it with a large number of files, there might be some issues
# Get the list of files and folders in the directory, this function is used to include files and subfolders in the table
def get_children(base_directory):
    # Create an empty list to store the files
    children_files = []

    # Loop through all the files in the directory
    for files in os.listdir(base_directory):
        # Get the full path of the file
        full_path = os.path.join(base_directory, files)
        # Check if the file is a folder
        if os.path.isdir(full_path):
            # Add the folder itself to the list
            children_files.append(full_path)
            # Get the files inside the folder
            for dirpath, dirnames, filenames in os.walk(full_path):
                # Loop through all the files inside the folder
                for file in filenames:
                    # Get the full path of the file
                    file_name = os.path.join(dirpath, file).replace("\\" , "/") #* This replace is needed, because the path is returned with backslashes, and we need forward slashes for to find the file in explorer
                    # Add the file to the list
                    children_files.append(file_name)

        # If the file is not a folder, just add it to the list
        else:
            children_files.append(full_path)

    # Return the list of files
    return children_files

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
        file_number = 1
        file_new_name = file_name_var.get()
        file_type = file_ext_var.get()
        directory = selected_dir.get() + "//" 
        new_name_list = []
        old_name_list = []
        old_name_list_folders = []
        new_name_list_folders = []

        if file_name_var.get() == "" or file_ext_var.get() == "" or selected_dir.get() == "":
            error_message()
            raise ValueError("Missing text fields")

        # Create a new window to confirm the changes
        confirm_window = tk.Toplevel(root)
        confirm_window.title("Confirm")
        confirm_window.geometry("500x500")
        confirm_window.iconbitmap("icon.ico")
        label_confirm = tk.Label(confirm_window, text="Are you sure you want to rename these files?", font=("Helvetica", 14))
        label_confirm.pack(pady=10)

        # Function to rename the files
        def rename_files():
            # First rename the files
            for i in range(len(new_name_list)):
                os.rename(old_name_list[i], new_name_list[i])
            # Then rename the folders
            for i in range(len(new_name_list_folders)):
                os.rename(old_name_list_folders[i], new_name_list_folders[i])
            confirm_window.destroy()
            # This function will update the main table with the new names
            file_info()

            #? Maybe add some code to really confirm the changes were successful? for now it just shows a message box without checking, cause im lazy :)
            messagebox.showinfo("Success", "Files renamed successfully", parent=root)
        confirm_button = Button(confirm_window, text="Confirm", command=rename_files)
        confirm_button.pack(pady=10)

        # Create a table to show the changes that will be made
        table_confirm = ttk.Treeview(confirm_window, columns=(1,2), show="headings", height="18")
        table_confirm.heading(1, text="Old Name", anchor=tk.W)
        table_confirm.heading(2, text="New Name", anchor=tk.W)
        table_confirm.column(1, width=200)
        table_confirm.column(2, width=200)
        
        for file in get_children(directory):
            #* If it is a file
            if os.path.isfile(file):
                # Get the name of the file without the whole path, only subfolders and the file name, like: "folder1/filename.png"
                file_path = str(file).split("//")[1].split("/")[:-1]
                # If the file is in a subfolder, add the subfolder name to the path
                if len(file_path) > 0:
                    file_path = "/".join(file_path) + "/"
                # If the file is not in a subfolder, set the path to an empty string
                else:
                    file_path = ""

                # Get the old name of the file, without the whole path
                old_file_str_table = str(file).split("//")[1]
                # Create the new name of the file
                new_file_str_table = file_path + str(file_new_name)+str(file_number)+str(file_type)
                # Add the files to the table
                table_confirm.insert("", "end", values=(old_file_str_table, new_file_str_table))
                # Add the files to the list of files to rename
                old_name_list.append(str(file))
                new_name_list.append(directory + new_file_str_table)
                file_number +=1

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

            #* If it is a folder
            else:
                # Get the name of the folder without the whole path, only subfolders, like: "folder1/folder2"
                file_path = str(file).split("//")[1].split("/")[:-1]
                # if the folder is in a subfolder, add the subfolder name to the path
                if len(file_path) > 0:
                    file_path = "/".join(file_path) + "/"
                # If the file is not in a subfolder, set the path to an empty string
                else:
                    file_path = ""

                # Get the old name of the file, without the whole path
                old_file_str_table = str(file).split("//")[1]
                # Create the new name of the file
                new_file_str_table = file_path + str(file_new_name)+str(file_number)
                # Add the files to the table
                table_confirm.insert("", "end", values=(old_file_str_table, new_file_str_table))
                # Add the files to the list of files to rename
                old_name_list_folders.append(str(file))
                new_name_list_folders.append(directory + new_file_str_table)
                file_number +=1

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
                                old_name_index:int = old_name_list_folders.index(old_value)
                                # Update the list with the new value
                                old_name_list_folders[old_name_index]:list = new_value
                            # Check which column was edited and update the lists with the new value
                            elif column == "#2":
                                # Get the index of the old value in the "new_name_list" list
                                new_name_index:int = new_name_list_folders.index(old_value)
                                # Update the list with the new value
                                new_name_list_folders[new_name_index]:list = directory + new_value
                            # Destroy the entry widget
                            entry.destroy()
                        # Bind the function to the entry widget, so that when the user presses enter, the function above is called
                        entry.bind("<Return>", on_entry_confirm)
                        entry.focus()
            
           
        table_confirm.pack(pady=10, padx=10, fill="both", expand=True)
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
                    row_values[i] = directory + str(row_values[i])
                
                # Try to delete the row from the lists
                try:
                    # Get the index of the old name in the "old_name_list" list
                    old_name_index = old_name_list_folders.index(str(row_values[0]))
                    # Get the index of the new name in the "new_name_list" list
                    new_name_index = new_name_list_folders.index(str(row_values[1]))
                    # Delete the old name from the "old_name_list" list
                    del old_name_list_folders[old_name_index]
                    # Delete the new name from the "new_name_list" list
                    del new_name_list_folders[new_name_index]
                # If it fails, it means that the row is a file, so it can't be deleted from the lists above
                except:
                    # Not a folder
                    pass
                # Delete the selected rows from the lists
                try:
                    old_name_index = old_name_list.index(str(row_values[0]))
                    # Get the index of the new name in the "new_name_list" list
                    new_name_index = new_name_list.index(str(row_values[1]))
                    # Delete the old name from the "old_name_list" list
                    del old_name_list[old_name_index]
                    # Delete the new name from the "new_name_list" list
                    del new_name_list[new_name_index]
                # If it fails, it means that the row is a folder, so it can't be deleted from the lists above
                except:
                    # Not a file
                    pass

                # Delete the selected rows from the table
                table_confirm.delete(item) 


        # Button to delete the selected rows
        delete_button = Button(confirm_window, text="Remove selected rows from renaming", command=delete_selected_rows)
        delete_button.pack(pady=10)
        confirm_window.mainloop()

# Temp cmd
print("Active")


def file_info():
    #* Table needs to be global, so that when the function is called again, it can destroy the old table and create a new one
    global table
    # Try to destroy table if it exists, so that a new one can be created
    try: 
        table.destroy()
    except:
        pass

    # Get the directory from the entry widget
    directory = selected_dir.get() + "//"


    # Function to get the size of a folder, this is used to include the size of all the files inside the folder in the table
    def get_folder_size(folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                total_size += os.path.getsize(file_path)
        return total_size
    
    # Create a table to display file information
    table = ttk.Treeview(root, columns=(1,2,3), show="headings", height=20)
    table.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    table.column(1, width=200)
    table.column(2, width=100)
    table.column(3, width=100)
    table.heading(1, text="File Name", anchor=tk.W, command=lambda: functionality.sort_treeview(table, 1, False, False))
    table.heading(2, text="File Type", anchor=tk.W, command=lambda: functionality.sort_treeview(table, 2, False, False))
    table.heading(3, text="File Size", anchor=tk.W, command=lambda: functionality.sort_treeview(table, 3, False, True))
    

    #* This code includes the files and folders in the table, using the get_children function
    for file in get_children(directory):
        if os.path.isfile(file):
            file_size = os.path.getsize(file)
            file_type = "File"
        else:
            file_size = get_folder_size(file)
            file_type = "Folder"
        
        size_suffix = ["bytes", "KB", "MB", "GB", "TB"]
        size_index = 0

        # Loop to convert file size to a human-readable format
        while file_size >= 1024 and size_index < len(size_suffix) - 1:
            # Divide file size by 1024 to convert units
            file_size /= 1024
            # Increment size_index to track the current unit
            size_index += 1 

        # Round file size to 2 decimal places for display purposes
        file_size = round(file_size, 2)

        # Create a string to display the file size and unit in the table
        table_file_size = f"{file_size} {size_suffix[size_index]}"

        # Get the relative path to display as "folder/file"
        relative_path = os.path.relpath(file, directory)

        # Insert the file information into the table
        table.insert("", "end", values=(relative_path, file_type, table_file_size), open=True)

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
            send2trash(final_file)
            # os.remove(final_file)

        return deleted_file_list

def file_select():
    # Option for just selected files 
    selected_files = filedialog.askopenfilenames()
    print("selected files = "+ str(selected_files))

# Rename button
button = Button(button_row, text="Rename", command=file_rename)
button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

#* This button is not really needed anymore, the only reason it has to exist is to refresh the file list if needed
# Refresh directory info
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
