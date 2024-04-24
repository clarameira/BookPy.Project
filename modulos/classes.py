class User():
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email

class Post():
    def __init__(self, title= None, author= None, publisher= None, product_quality= None, user_author= None, content= None):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.user_author = user_author
        self.content = content