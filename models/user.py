import uuid
from flask import session
from controller import constants
from controller.database import Database
from .blog import Blog

class User(object):
    def __init__(self, email, password, sex, name, _id=None):
        self.email = email
        self.password = password
        self.sex = sex
        self.name = name
        self._id = uuid.uuid4().hex if not _id else _id

    @classmethod
    def get_by_email(cls, email):
        #find user in database via email

        return

    @classmethod
    def get_by_id(cls, _id):
        #find user in database via id
        return

    def is_login_valid(self, password):
        """
        Check if the email and password are valid
        :return: Boolean
        """
        return self.password == password


    @classmethod
    def register(cls, email, password, sex, skill, name, school):
        #register user into database
        return

    @staticmethod
    def login(email, name):
        session.__setitem__('email', email)
        session.__setitem__('name', name)

    @staticmethod
    def logout():
        session.__setitem__('email', None)
        session.__setitem__('name', None)

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)


    def new_comment(self,blog_id, title, content):
        blog = Blog.from_mongo(blog_id)
        blog.new_comment(title=title, content=content, author=self.name)


    def new_blog(self, title, description):
        blog = Blog(
            author=self.name,
            title=title,
            description=description,
            author_id=self._id
        )
        blog.save_to_mongo()



