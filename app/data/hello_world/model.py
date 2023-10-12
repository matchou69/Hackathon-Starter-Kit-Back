from shared import db


class HelloWorldModel(db.Model):
    __tablename__ = "helloworld"
    id = db.Column(db.UUID,
                   primary_key=True,
                   unique=True)
    name = db.Column(db.String())
