from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)  # Enable Cross-Origin Resource Sharing
migrate = Migrate(app, db)

db.init_app(app)

# Route to get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# Route to get a single message by its ID
@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    message = Message.query.get_or_404(id)
    return jsonify(message.to_dict())

# Route to update a message by its ID
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict())

# Route to delete a message by its ID
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'})

if __name__ == '__main__':
    app.run(port=5555)
