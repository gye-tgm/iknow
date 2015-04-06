"""
RESTful webservice
"""
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

api = Api(app)

tags = db.Table('tags',
                db.Column('tag_id', db.String, db.ForeignKey('tag.id')),
                db.Column('knowledge_id', db.INTEGER,
                          db.ForeignKey('knowledge.id')))


class Knowledge(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('knowledges', lazy='dynamic'))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Content %r>' % self.content


class Tag(db.Model):
    id = db.Column(db.String, primary_key=True)


class ExcerptAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=str)
        self.reqparse.add_argument('tags', type=str, actions='append')

    def get(self):
        args = self.reqparse.parse_args()
        # TODO: multiple or single tags?
        tag = Tag.query.filter_by(id=args['tag'])

        l = []
        for k in tag.knowledges:
            l.append({'content': k.content})
        return {'list': l}

    def put(self, id):
        """
        Update
        """
        pass

    def delete(self, id):
        """
        Delete
        """
        pass

    def post(self):
        """
        Stores a new knoledge entry into the database. The tags will also be
        created.
        """

        args = self.reqparse.parse_args()
        knowledge = Knowledge(args['content'])
        knowledge.tags.extend(args['tags'])
        db.session.add(knowledge)
        db.session.commit()


api.add_resource(ExcerptAPI, '/excerpts')

if __name__ == '__main__':
    app.run(debug=True)