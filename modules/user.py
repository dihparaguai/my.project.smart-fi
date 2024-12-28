class User:
    def __init__(self, id, email, name, birthdate, password):
        self.id = id
        self.email = email
        self.name = name
        self.birthdate = birthdate
        self.password = password
        
    def __repr__(self):
        return f'''
        id = {self.id}
        email = {self.email}
        nome = {self.name}
        birthdate = {self.birthdate}
        password = {self.password}
        '''