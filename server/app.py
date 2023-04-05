from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        ordered_message = Message.query.order_by(Message.created_at.asc()).all()
        ordered_message_serialized = [message.to_dict() for message in ordered_message]

        response = make_response(
            jsonify(ordered_message_serialized),
            200
        )

        return response


    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(
            jsonify(new_message_dict),
            201
        )

        return response


@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).all()

    if request.method == 'GET':
        messages_serialized = [message.to_dict() for message in message]

        response = make_response(
            jsonify(messages_serialized),
            200
        )

        return response
    
    elif request.method == 'PATCH':
        
        message = Message.query.filter(Message.id == id).first()
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
        )
        
        return response

    elif request.method == 'DELETE':
        message = Message.query.filter(Message.id == id).first()
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_succesful": True,
            "message": "Message deleted successfully"
        }

        response = make_response(
            response_body,
            200
        )

        return response

    

if __name__ == '__main__':
    app.run(port=5555)
