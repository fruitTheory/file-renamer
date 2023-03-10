# file-renamer
WIP of a file renaming tool that can rename all files in a directory. Right now it gives a name and extension option, and if there's multiple files it will increment by 1. For ex: filename1, filename2, etc. It can also give information about a directory, such as file/folder names and their correlating sizes. Right now supported memory types are bytes, KB, MB, and GB.

<b>Update 3/9/23</b> - Added delete files functionality. The target of this was to deal with mass file output regarding batch imaging from an AI resizer. The AI was outputting duplicate names .jpg and .png.
The tool now checks for files that have the same name and it narrows down to delete one set of those based on the users extension input. Ex: It can delete specified duplicates of type .jpg, png, .exr, etc. Please note this is WIP and no error catching assigned.
