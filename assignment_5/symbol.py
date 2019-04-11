class symbolTable:

    def __init__(self, par=None):
        self.table = {}
        self.parent = par

    # Checks whether "name" lies in the symbol table
    def lookUp(self, name):
        return (name in self.table)

    # Inserts if already not present
    def insert(self, name):
        if (not self.lookUp(name)):
            (self.table)[name] = {}

    # Returns the argument list of the variable else returns None
    # Note that type is always a key in argument list
    def getInfo(self, name):
        if(self.lookUp(name)):
            return (self.table)[name]
        return None

    # Updates the variable of NAME name with arg list of KEY key with VALUE value
    def update(self, name, key, value):
        if (self.lookUp(name)):
            (self.table)[name][key] = value
        else:
            raise KeyError("Symbol " + name + " doesn't exist, cant update")

    def setParent(self, parent):
        self.parent = parent
