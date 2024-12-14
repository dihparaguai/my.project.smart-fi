class Category:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        
    def __repr__(self):
        return f'''
        id = {self.id}
        name = {self.name}
        description = {self.description}
        '''