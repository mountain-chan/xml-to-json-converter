import json
import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234567aA@@sv2.vn.boot.ai/partner_htc_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    login_failed_attempts = db.Column(db.SmallInteger, default=0)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    title = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    group_id = db.Column(db.ForeignKey('groups.id'), index=True)
    lang = db.Column(db.String(50), default='en')
    company = db.Column(db.String(50))
    address = db.Column(db.String(255))
    mobile = db.Column(db.String(50))
    force_change_password = db.Column(db.Boolean, default=0)
    create_date = db.Column(INTEGER(unsigned=True))
    modified_date = db.Column(INTEGER(unsigned=True))
    modified_date_password = db.Column(INTEGER(unsigned=True))

    @staticmethod
    def get_all():
        return User.query.order_by(User.username).all()


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    schema = db.Column(db.String(10024))
    creator_id = db.Column(db.ForeignKey('users.id'), nullable=False, index=True)
    create_date = db.Column(INTEGER(unsigned=True), default=0)
    modify_date = db.Column(INTEGER(unsigned=True), default=0)


# load json file then covert to string and insert to db
with open("my_data.json") as my_data:
    recipe = json.load(my_data)
recipe_str = json.dumps(recipe)

new_values = Recipe(id=str(uuid.uuid1()), name="test", schema=recipe_str,
                    creator_id="a74dd5a8-9369-11ea-afb4-00e04d380507")

db.session.add(new_values)
db.session.commit()

# query from db
test = Recipe.query.first()
recipe = json.loads(test.schema)
print(type(recipe))
for i in recipe:
    print(i)
