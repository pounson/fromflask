from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class AdvertismentModel(db.Model):
    __tablename__ = 'Advs'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, author, title, description):
        self.author = author
        self.title = title
        self.description = description

    def to_dict(self):
        return {"author": self.author,
                "title": self.title,
                "description": self.description,
                "date": self.date
                }

    def to_dict_wd(self):
        return {"author": self.author,
                "title": self.title,
                "description": self.description,
                }

