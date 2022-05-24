import json

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import db, AdvertismentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


class AdvertismentsView(Resource):

    def get(self):
        advs = AdvertismentModel.query.all()
        return jsonify([adv.to_dict() for adv in advs])

    def post(self):
        data = request.get_json()
        new_adv = AdvertismentModel(data['author'],
                                    data['title'],
                                    data['description'])
        db.session.add(new_adv)
        db.session.commit()
        return new_adv.to_dict_wd(), 201


class AdvertismentView(Resource):

    def get(self, adv_id):
        adv = AdvertismentModel.query.get(adv_id)
        if adv:
            return jsonify(adv.to_dict())
        return {'message': 'adv not found'}, 404

    def put(self, adv_id):
        data = request.get_json()

        adv = AdvertismentModel.query.get(adv_id)

        if adv:
            adv.title = data["title"]
            adv.description = data["description"]
        else:
            adv = AdvertismentModel(id=adv_id, **data)

        db.session.add(adv)
        db.session.commit()

        return jsonify(adv.to_dict())

    def delete(self, adv_id):
        adv = AdvertismentModel.query.get(adv_id)
        if adv:
            db.session.delete(adv)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'adv not found'}, 404


api.add_resource(AdvertismentsView, '/api/v1/advs/')
api.add_resource(AdvertismentView, '/api/v1/adv/<int:adv_id>')

app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5050)