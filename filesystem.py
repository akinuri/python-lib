def path_pop(path, count=0, dirname=False, filename=False):
    if os.path.isdir(path):
        dirs = path.split("\\")
        while count > 0:
            dirs.pop(len(dirs)-1)
            count -= 1
        if dirname:
            return dirs[len(dirs)-1]
        return "\\".join(dirs)
    elif os.path.isfile(path):
        dirs = path.split("\\")
        filename = dirs.pop(len(dirs)-1)
        if filename:
            return filename
        else:
            while count > 0:
                dirs.pop(len(dirs)-1)
                count -= 1
            if dirname:
                return dirs[len(dirs)-1]
        return "\\".join(dirs)
    return None


# Node() dependencies:
#    path_pop()
#    str_pad_right()
#    tabspace()

class Node:
    
    def __init__(self, path, exclude=None, parent=None):
        self.path     = path
        self.parent   = parent
        self.children = []
        if os.path.isdir(path):
            self.type = "Folder"
            self.name = path_pop(path, 0, True)
            self.walk(exclude)
        elif os.path.isfile(path):
            self.type = "File"
            self.name = path_pop(path, 0, True, True)
    
    def walk(self, exclude):
        items = os.listdir(self.path)
        if len(items) != 0:
            for item in items:
                if exclude is not None and item != exclude:
                    child = Node(self.path + "\\" + item, exclude, self)
                    self.children.append(child)
    
    def debug(self, indent=0):
        field_str_length = 7
        children_count = len(self.children)
        if children_count > 0:
            field_str_length = 9
        print(tabspace(indent) + "[")
        print(tabspace(indent + 1) + str_pad_right("name", field_str_length, " ") + ": " + self.name)
        print(tabspace(indent + 1) + str_pad_right("type", field_str_length, " ") + ": " + self.type)
        print(tabspace(indent + 1) + str_pad_right("path", field_str_length, " ") + ": " + self.path)
        if self.parent is not None:
            print(tabspace(indent + 1) + str_pad_right("parent", field_str_length, " ") + ": " + self.parent.name + " (Node)")
        else:
            print(tabspace(indent + 1) + str_pad_right("parent", field_str_length, " ") + ": " + "None")
        if len(self.children) != 0:
            print(tabspace(indent + 1) + str_pad_right("children", field_str_length, " ") + ": [")
            if len(self.children) != 0:
                for item in self.children:
                    item.debug(indent + 2)
            print(tabspace(indent + 1) + "]")
        print(tabspace(indent) + "]")

