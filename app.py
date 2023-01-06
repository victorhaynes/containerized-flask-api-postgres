from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os


### Config ################################################
### Config ################################################
### Config ################################################


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


### Database (Table) Management (Routes) ################################
### Database (Table) Management (Routes) ################################
### Database (Table) Management (Routes) ################################


@app.route('/create', methods=['GET'])
@jwt_required()
def db_create():
	db.create_all()
	return jsonify(message='Database created!')


@app.route('/drop', methods=['GET'])
@jwt_required()
def db_drop():
	db.drop_all()
	return jsonify(message='Database dropped!')


@app.route('/seed', methods=['GET'])
@jwt_required()
def db_seed():
	default_item = Item(title='generic title', content='generic content')
	admin_user = User(email="admin@victorhaynes.com", password="admin")
	db.session.add(default_item)
	db.session.add(admin_user)
	db.session.commit()
	return jsonify(message="Database Seeded")


### Models ################################################
### Models ################################################
### Models ################################################


class Item(db.Model):
	__tablename__ = "items"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), unique=True, nullable=False)
	content = db.Column(db.String(120), unique=True, nullable=False)

	def __init__(self, title, content):
		self.title = title
		self.content = content


class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, email, password):
		self.email = email
		self.password = password


### Routes ################################################
### Routes ################################################
### Routes ################################################


@app.route('/items/<int:id>', methods=['GET'])
def get_item(id: int):
	item = Item.query.get(id)
	return jsonify(item_schema.dump(item))


@app.route('/items', methods=['GET'])
def get_items():
	items = Item.query.all()
	return jsonify(items_schema.dump(items))


@app.route('/items', methods=['POST'])
def create_item():
	item = request.get_json()
	db.session.add(Item(item['title'], item['content']))
	db.session.commit()
	return "Item Created"


@app.route('/items/<int:id>', methods=['PATCH'])
def update_item(id: int):
	updated = request.get_json()
	item = Item.query.filter_by(id=id).first()
	item.title = updated['title']
	item.content = updated['content']
	db.session.commit()
	return "Item Updated"


@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id: int):
	item = Item.query.filter_by(id=id).first()
	db.session.delete(item)
	db.session.commit()
	return "Item deleted"


@app.route('/users', methods=['GET'])
def get_users():
	users = User.query.all()
	return jsonify(users_schema.dump(users))


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id: int):
	user = User.query.get(id)
	return jsonify(user_schema.dump(user))


### User Management ############################################
### User Management ############################################
### User Management ############################################


@app.route('/register', methods=['POST'])
def register():
	details = request.json
	email = details['email']
	exists = User.query.filter_by(email=email).first()
	if exists:
		return jsonify(message='Email already associated with an accoun.'), 409
	else:
		email = details['email']
		password = details['password']
		user = User(email=email, password=password)
		db.session.add(user)
		db.session.commit()
		return jsonify(message="User Created Successfully."), 201


@app.route('/login', methods=['POST'])
def login():
	details = request.json
	email = details['email']
	password = details['password']
	found = User.query.filter_by(email=email, password=password).first()
	if found:
		access_token = create_access_token(identity=email)
		return jsonify(message="Login Successful!", access_token=access_token)
	else:
		return jsonify(message="Incorrect email or password."), 401


### Serializers ################################################
### Serializers ################################################
### Serializers ################################################


class ItemSchema(ma.Schema):
	class Meta:
		fields = ('title', 'content')
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


class UserSchema(ma.Schema):
	class Meta:
		fields = ('email',)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


if __name__ == '__main__':
	app.run(debug=True)