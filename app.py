from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

### Config ################################################
### Config ################################################
### Config ################################################


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
ma = Marshmallow(app)


### Database (Table) Management (Routes) ################################
### Database (Table) Management (Routes) ################################
### Database (Table) Management (Routes) ################################


@app.route('/create', methods=['GET'])
def db_create():
    db.create_all()
    return jsonify(message='Database created!')


@app.route('/drop', methods=['GET'])
def db_drop():
    db.drop_all()
    return jsonify(message='Database dropped!')


@app.route('/seed', methods=['GET'])
def db_seed():
    default_item = Item(title='generic title', content='generic content')
    db.session.add(default_item)
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



### Routes ################################################
### Routes ################################################
### Routes ################################################


@app.route('/items/<id>', methods=['GET'])
def get_item(id):
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


@app.route('/items/<id>', methods=['PATCH'])
def update_item(id):
    updated = request.get_json()
    item = Item.query.filter_by(id=id).first()
    item.title = updated['title']
    item.content = updated['content']
    db.session.commit()
    return "Item Updated"


@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return "Item deleted"


### Serializers ################################################
### Serializers ################################################
### Serializers ################################################


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)