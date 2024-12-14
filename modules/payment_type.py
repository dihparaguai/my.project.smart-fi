class Payment_type:
    def __init__(self, id, name, owner):
        self.id = id
        self.name = name
        self.owner = owner
        
    def __repr__(self):
        return f'''
        id = {self.id}
        name = {self.name}
        owner = {self.owner}
        
        '''