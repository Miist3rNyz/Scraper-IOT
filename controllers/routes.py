from flask import Blueprint, jsonify, request
import json
from db.cve_collection import CveCollection

# Créez un objet Blueprint pour les routes
api_bp = Blueprint('api', __name__)

cve_collection = CveCollection()

@api_bp.route('/S', methods=['GET'])
def get_data_s():
    datas=cve_collection.find({ "category": "S"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/P', methods=['GET'])
def get_data_p():
    datas=cve_collection.find({"category": "P"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/H', methods=['GET'])
def get_data_h():
    datas=cve_collection.find({ "category": "H"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/E', methods=['GET'])
def get_data_e():
    datas=cve_collection.find({ "category": "E"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/M', methods=['GET'])
def get_data_m():
    datas=cve_collection.find({ "category": "M"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/A', methods=['GET'])
def get_data_a():
    datas=cve_collection.find({ "category": "A"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents