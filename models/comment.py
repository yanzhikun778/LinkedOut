from controller import constants
from controller.database import Database
import uuid
from datetime import datetime


class Comment(object):
    def __init__(self, blog_id, content, author, created_at=datetime.now(), _id=None):
        #  default parameters are allowed in end
        self._id = uuid.uuid4().hex if not _id else _id
        self.blog_id = blog_id
        self.content = content
        self.author = author
        self.likes = 0
        self.dislikes = 0
        self.created_at = created_at

    def save_to_mongo(self):
        Database.insert(collection=constants.COMMENT_COLLECTION,
                        data=self.json()
                        )
    @classmethod
    def delete_from_mongo_viaid(self, _id):
        Database.delete(collection=constants.COMMENT_COLLECTION,
                        query={'_id': _id})

    @classmethod
    def get_by_id(cls, post_id):
        post = Database.find_one(collection=constants.COMMENT_COLLECTION,
                                 query={"_id": post_id})
        if post:
            return cls(**post)
        return None

    def json(self):
        return {
            '_id': self._id,
            'content': self.content,
            'author': self.author,
            'blog_id': self.blog_id,
            'created_at': self.created_at,
            'likes': self.likes,
            'dislikes': self.dislikes
        }

    @classmethod
    def from_mongo(cls, uid):
        post_elem = Database.find_one(
            collection=constants.COMMENT_COLLECTION,
            query={'_id': uid}
        )
        return cls(**post_elem).json()


    @staticmethod
    def from_blog(uid):
        return [post for post in Database.find(
            collection=constants.COMMENT_COLLECTION,
            query={'blog_id': uid}
        )]

