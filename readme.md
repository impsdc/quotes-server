## Lauch Api

#### Build container

` docker build -t name . --no-cache`

#### Lauch container

` docker run -dp 3000:3000 name`

#### Local serve for development

`FLASK_APP=app.py FLASK_DEBUG=true flask run`

#### Testing api

`curl -i -H "Content-Type: application/json" charset=utf-8 -X POST -d '{"email":"lol@gmail.com", "password":"trucmuch"}' 127.0.0.1:5000/login`


### production

.env need to be in ./app

### deploy to gloud run 
```
gcloud run deploy --port=5000
```
