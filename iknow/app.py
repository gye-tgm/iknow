import os

from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import ClauseElement

app = Flask(__name__)

# The SQLite database is located in the execution dir
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)

api = Api(app)

# Association table between Tags and Knowledge 
tags = db.Table('tags', db.Model.metadata,
                db.Column('tag_id', db.String, db.ForeignKey('tag.id')),
                db.Column('knowledge_id', db.INTEGER,
                          db.ForeignKey('knowledge.id')))

@app.after_request
def after_request(response):
    """
    This method permits cross domain calls. 
    :param response: the response
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

class Knowledge(db.Model):
    """
    A model class to represent a knowledge entry in the underlying database. 
    """

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('knowledges', lazy='dynamic'))

    def __init__(self, content):
        """
        Creates a new instance with the given content. 
        """
        self.content = content

    def __repr__(self):
        return '<Content %r>' % self.content

    def mapped(self):
        """
        Returns the attributes the instance has as a dictionary. 
        :return: a dictionary with id, content and tags with their
        corresponding values. 
        """
        return {
            'id': self.id,
            'content': self.content,
            'tags': [tt.id for tt in self.tags]
        }


class Tag(db.Model):
    """
    A model class to represent a tag in the underlying database. 

    The id is not an integer, it is instead the name of the tag that it
    represents. 
    """
    id = db.Column(db.String, primary_key=True)

    def __init__(self, tag):
        """
        Creates a new instance with the given tag name. 
        """
        self.id = tag


class KnowledgeListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=str)
        self.reqparse.add_argument('tags', type=str)

    def post(self):
        """
        Stores a new knowledge entry into the database. The missing tags will be
        created along with the entry. 
        """
        args = self.reqparse.parse_args()
        knowledge = Knowledge(args['content'])
        for tag in args['tags'].split(','):
            t = Tag.query.filter_by(id=tag).first()
            if t is None:
                t = Tag(tag)
                db.session.add(t)
            knowledge.tags.append(t)
        db.session.add(knowledge)
        db.session.commit()
        return {'msg': 'Success'}

class KnowledgeAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('content', type=str)
        self.reqparse.add_argument('tags', type=str)

    def get(self, id):
        """
        Returns the entry with the given id. 
        """
        knowledge = Knowledge.query.filter_by(id=id).first()
        if knowledge is None:
            return {}
        return knowledge.mapped()

    def put(self, id):
        """
        Updates the entry with the given id and the values in the POST
        arguments. 
        """
        args = self.reqparse.parse_args()
        knowledge = Knowledge.query.filter_by(id=id).first()
        knowledge.content = args['content']
        knowledge.tags = [Tag(tag) for tag in args['tags'].split(',')]
        db.session.commit()
        return {'msg': 'Success'}

    def delete(self, id):
        """
        Deletes the entry with the given id. 
        """
        knowledge = Knowledge.query.filter_by(id=id).first()
        db.session.delete(knowledge)
        db.session.commit()
        return {'msg': 'Success'}


class KnowledgeQueryAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('tag', type=str)

    def get(self):
        """
        Searches for all entries that have the given tag.  
        """

        args = self.reqparse.parse_args()

        tag = Tag.query.filter_by(id=args['tag']).first()
        return {'list': [k.mapped() for k in tag.knowledges]}


api.add_resource(KnowledgeQueryAPI, '/q')
api.add_resource(KnowledgeListAPI, '/knowledge')
api.add_resource(KnowledgeAPI, '/knowledge/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, use_evalex=False)
