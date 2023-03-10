# file-renamer
WIP of a file renaming tool that can rename all files in a directory. Right now it gives a name and extension option, and if there's multiple files it will increment by 1. For ex: filename1, filename2, etc. There will be an additional selected files option. It can also give information about a directory, such as file/folder names and their correlating sizes. Right now supported memory types are bytes, KB, MB, and GB.

Update 3/9/23 - Added delete files functionality. The target of this was to deal with mass file output regarding batch images that are AI resized. It was outputting double namess one .jpg and a heavier .png file.
The tool now checks for files that have the same name and narrows it down to delete one set of those based on the extension user input. ex: if want can delete only the duplicates in .jpg, png, .exr, etc. Please note this is WIP and no error catching assigned, so use at own risk.
