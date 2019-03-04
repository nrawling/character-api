# loosely based on  https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''

mysql.init_app(app)

characters = [
	{
		"name": "Gunthar",
		"race": "Dragonborn",
		"class": "Paladin",
		"level": 1
	},
]

class Character(Resource):
	def get(self, name):
		for character in characters:
			if(name == character["name"]):
				return character, 200
		return "Character not found", 404

	def post(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument("race")
		parser.add_argument("class")
		parser.add_argument("level")
		args = parser.parse_args()

		for character in characters:
			if(name == character["name"]):
				return "Character with name {} already exists".format(name), 400

		character = {
			"name": name,
			"race": args["race"],
			"class": args["class"],
			"level": args["level"]
		}
		characters.append(characters)
		return character, 201

	def put(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument("race")
		parser.add_argument("class")
		parser.add_argument("level")
		args = parser.parse_args()

		for character in characters:
			if(name == character["name"]):
				character["race"] = args["race"]
				character["class"] = args["class"]
				character["level"] = args["level"]
				return character, 200

		character = {
			"name": name,
			"race": args["race"],
			"class": args["class"],
			"level": args["level"]
		}
		characters.append(character)
		return character, 201

	def delete(self, name):
		global characters
		characters = [character for character in characters if character["name"] != name]
		return "{} is deleted.".format(name), 200

api.add_resource(Character, "/character/<string:name>")

app.run(debug=True)
