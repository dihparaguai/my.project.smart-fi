class User:
    def __init__(self, user_id, email, name, password):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.password = password
        
    def __repr__(self):
        return f'''
        user_id = {self.user_id}
        nome = {self.name}
        password = {self.password}
        '''