from shared import db


class HelloWorldModel(db.Model):
    __tablename__ = "helloworld"
    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True)
    name = db.Column(db.String())
