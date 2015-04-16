How to use the webservice
========================

First the schema has to be imported into the sqlite database. 

```
$ python
>>> from iknow.app import db
>>> db.create_all()
```

With sqlite3 the schema can be checked. 

```
$ sqlite3 iknow/test.db
sqlite3> .schema
```

Afterwards the webservice has to be started on port 5000. Make sure that no
processes have been bound on 5000. 

```
$ python iknow/service.py
```

The webservice can either be called with the famous `curl` command or by using
the webinterface provided in the `ui/` directory. Just open the
`ui/restful.html` HTML file with the webbrowser. 

For entering new entries use the POST command on the following URL: 

```
http://localhost:5000/knowledge
```

Make sure that in the large textarea the following JSON object is inside. 

```
{
  "content": "Here goes your content",
  "tags": "multiple,tags,separated,by,awesome,commas"
}
```

Now you can search for a special entry with a particular tag by performing a
GET query on `http://localhost:5000/q?tag=commas`. 

If an entry with a particular id should be deleted, then use the DELETE
command on `http://localhost:5000/knowledge/<id>`. 


Generating some data
--------------------

This may take some time:

```
$ python scripts/sentences.py /usr/share/dict/words
```

The package must be installed first beforehand. 




