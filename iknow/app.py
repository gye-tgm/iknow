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

    def mapped(self):
        return {
            'id': self.id,
            'content': self.content,
            'tags': [tt.id for tt in self.tags]
        }


class Tag(db.Model):
    id = db.Column(db.String, primary_key=True)

    def __init__(self, tag):
        self.id = tag


class KnowledgeListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=str)
        self.reqparse.add_argument('tags', type=str, action='append')

    def post(self):
        """
        Stores a new knowledge entry into the database. The tags will also be
        created.
        """
        args = self.reqparse.parse_args()
        knowledge = Knowledge(args['content'])
        knowledge.tags = [Tag(tag) for tag in args['tags']]
        db.session.add(knowledge)
        db.session.commit()


class KnowledgeAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=str)
        self.reqparse.add_argument('tags', type=str, action='append')

    def get(self, id):
        knowledge = Knowledge.query.filter_by(id=id).first()
        if knowledge is None:
            return {}
        return knowledge.mapped()

    def put(self, id):
        args = self.reqparse.parse_args()
        knowledge = Knowledge.query.filter_by(id=id).first()
        knowledge.content = args['content']
        knowledge.tags = [Tag(tag) for tag in args['tags']]
        db.session.commit()

    def delete(self, id):
        """
        Deletes the entry
        """
        knowledge = Knowledge.query.filter_by(id=id).first()
        db.session.delete(knowledge)
        db.session.commit()


class KnowledgeQueryAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('tags', type=str, action='append')

    def get(self):
        # TODO: multiple or single tags?
        args = self.reqparse.parse_args()
        tag = Tag.query.filter_by(id=args['tags'][0]).first()
        return {'list': [k.mapped() for k in tag.knowledges]}


api.add_resource(KnowledgeQueryAPI, '/query')
api.add_resource(KnowledgeListAPI, '/knowledge')
api.add_resource(KnowledgeAPI, '/knowledge/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, use_evalex=False)