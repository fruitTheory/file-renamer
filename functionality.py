def sort_treeview(treeview, column, reverse:bool, is_file_size:bool):
    # Get all items in treeview
    items = [(treeview.set(child, column), child) for child in treeview.get_children('')]

    # If the column is a file size, convert it to a float to be sorted
    if is_file_size:
        processed_items = []
        for item in items:
            size = 0.0
            # Split the string into a list of strings, for example: ['1.2', 'GB'] or ['13', 'bytes'], so that the unit can be determined
            size_str = item[0].split(' ')
            try: 
                #* All of these lines here are to convert the string to a float, based on the unit, so that it can be sorted
                if size_str[1] == 'bytes':
                    size = float(size_str[0])
                elif size_str[1] == 'KB':
                    size = float(size_str[0]) * 1024
                elif size_str[1] == 'MB':
                    size = float(size_str[0]) * 1024 * 1024
                elif size_str[1] == 'GB':
                    size = float(size_str[0]) * 1024 * 1024 * 1024
                elif size_str[1] == 'TB':
                    size = float(size_str[0]) * 1024 * 1024 * 1024 * 1024
            except:
                #* This is to handle the case it is a directory, which has no clear size
                size = 0
            # Add the size and the child to the list
            processed_items.append((size, item[1]))
        # Set the items to the processed items
        items = processed_items
    # Sort the items
    items.sort(reverse=reverse)
    # Move the items in the treeview
    for index, (_, child) in enumerate(items):
        treeview.move(child, '', index)
    # Makes the heading clickable, and reverse the sort order
    treeview.heading(column, command=lambda: sort_treeview(treeview, column, not reverse, is_file_size))
