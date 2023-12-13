from flask import request, jsonify, Blueprint
from data.events.schemas import EventsSchema
from data.events.models import EventsModel
from marshmallow import ValidationError
from shared import db

NAME= 'events'

events_blueprint = Blueprint(f"{NAME}_events_blueprint", __name__)


@events_blueprint.post(f"{NAME}/create_event")
def register():
    data = request.json

    if 'name' not in data or 'description' not in data or 'date' not in data or 'photo' not in data:
        return jsonify({'message': 'name or dateDeEvent or photo or description'}), 400

    name = data['name']
    description = data['description']
    date = data['date']
    photo = data['photo']

    # Check if the username already exists in the database
    existing_event = EventsModel.query.filter_by(name=name).first()
    if existing_event:
        return jsonify({'message': 'name already in use. Please choose a different name.'}), 400

    try:
        entity: EventsModel = EventsSchema().load(data)
    except ValidationError as error:
        return jsonify({'message': f"The payload doesn't correspond to a valid eventModel: {error}"}), 400

    db.session.add(entity)
    db.session.commit()

    return jsonify({'message': 'Adding new event successful !', 'user': EventsSchema().dump(entity)}), 200


@events_blueprint.get(f"{NAME}/get_events")
def get_events():
    events = EventsModel.query.all()
    return jsonify({'events': EventsSchema(many=True).dump(events)})


@events_blueprint.delete(f"{NAME}/delete_event/<int:event_id>")
def delete_event(event_id):
    event = EventsModel.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({'message': 'Event deleted successfully'}), 200
