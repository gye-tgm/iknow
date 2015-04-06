"""
RESTful webservice
"""
import os
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)

api = Api(app)

tags = db.Table('tags', db.Model.metadata,
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

    def __init__(self, tag):
        self.id = tag


class KnowledgeAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=str)
        self.reqparse.add_argument('tags', type=str, action='append')
        self.reqparse.add_argument('id', type=id)

    def get(self):
        args = self.reqparse.parse_args()
        # TODO: multiple or single tags?
        tag = Tag.query.filter_by(id=args['tags'][0]).first()

        l = []
        for k in tag.knowledges:
            l.append({
                'id': k.id,
                'content': k.content,
                'tags': [tt.id for tt in k.tags]}
            )
        return {'list': l}

    def put(self, id):
        """
        Update
        """
        pass

    def delete(self):
        """
        Deletes the entry
        """
        args = self.reqparse.parse_args()
        knowledge = Knowledge.query.filter_by(id=args['id']).first()
        db.session.delete(knowledge)
        db.session.commit()

    def post(self):
        """
        Stores a new knowledge entry into the database. The tags will also be
        created.
        """
        args = self.reqparse.parse_args()
        knowledge = Knowledge(args['content'])

        print(args)

        for tag in args['tags']:
            knowledge.tags.append(Tag(tag))
        db.session.add(knowledge)
        db.session.commit()


api.add_resource(KnowledgeAPI, '/knowledge')

if __name__ == '__main__':
    app.run(debug=True, use_evalex=False)