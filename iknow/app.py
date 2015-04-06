"""
RESTful webservice
"""
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)

excerpts = {
    {
        'id': 0,
        'book': 'A Song of Ice and Fire',
        'excerpt': 'Winter is coming'
    }
}


class ExcerptListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('')

    def get(self):
        pass


class ExcerptAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def post(self, id):
        pass


api.add_resource(ExcerptListAPI, '/excerpts')
api.add_resource(ExcerptAPI, '/excerpts/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)