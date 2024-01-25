from flask import Flask, jsonify
from pymongo import MongoClient
import os  # Import the 'os' module
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load environment variables from .env file



# Access environment variables
mongodb_uri = os.getenv('MONGODB_URI')
mongodb_db = os.getenv('MONGODB_DB')
mongodb_collection = os.getenv('MONGODB_COLLECTION')
client = MongoClient(mongodb_uri)
db = client[mongodb_db]
collection = db[mongodb_collection]
@app.route('/get_data', methods=['GET'])
def get_data():
    # Récupérer les données de la collection
    data = list(collection.find({}, {'_id': 0}))  # Exclure le champ _id de la réponse JSON si nécessaire

    # Retourner les données en format JSON
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)