from flask import Flask, jsonify
from flask_pymongo import PyMongo
import os  # Import the 'os' module

app = Flask(__name__)

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Access environment variables
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    collection = mongo.db.votre_collection
    result = collection.find({}, {"_id": 0})
    data = [doc for doc in result]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)