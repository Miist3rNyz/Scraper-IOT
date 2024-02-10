from flask import Blueprint, jsonify, request
import json
import re
from db.cve_collection import CveCollection
from db.cpe_collection import CpeCollection

# Créez un objet Blueprint pour les routes
api_bp = Blueprint('api', __name__)

cve_collection = CveCollection()
cpe_collection = CpeCollection()

@api_bp.route('/S', methods=['GET'])
def get_data_s():
    datas=cve_collection.find({ "category": "S"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/S', methods=['POST'])
def get_cve_with_brand_and_category_S():
    brand=request.args.get('brand')
    product=request.args.get('product')
    datas=cve_collection.get_cpe_by_brand_and_category(brand,product,'S')
    return jsonify(datas)

@api_bp.route('/P', methods=['GET'])
def get_data_p():
    datas=cve_collection.find({"category": "P"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/P', methods=['POST'])
def get_cve_with_brand_and_category_P():
    brand=request.args.get('brand')
    product=request.args.get('product')
    datas=cve_collection.get_cpe_by_brand_and_category(brand,product,'P')
    return jsonify(datas)

@api_bp.route('/H', methods=['GET'])
def get_data_h():
    datas=cve_collection.find({ "category": "H"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/H', methods=['POST'])
def get_cve_with_brand_and_category_H():
    brand=request.args.get('brand')
    product=request.args.get('product')
    datas=cve_collection.get_cpe_by_brand_and_category(brand,product,'H')
    return jsonify(datas)

@api_bp.route('/E', methods=['GET'])
def get_data_e():
    datas=cve_collection.find({ "category": "E"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents

@api_bp.route('/E', methods=['POST'])
def get_cve_with_brand_and_category_E():
    brand=request.args.get('brand')
    product=request.args.get('product')
    datas=cve_collection.get_cpe_by_brand_and_category(brand,product,'E')
    return jsonify(datas)

@api_bp.route('/M', methods=['GET'])
def get_data_m():
    datas=cve_collection.find({ "category": "M"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents
@api_bp.route('/M', methods=['POST'])
def get_cve_with_brand_and_category_M():
    brand=request.args.get('brand')
    product=request.args.get('product')
    datas=cve_collection.get_cpe_by_brand_and_category(brand,product,'M')
    return jsonify(datas)

@api_bp.route('/A', methods=['GET'])
def get_data_a():
    datas=cve_collection.find({ "category": "A"})
    json_documents = [json.dumps(doc, default=str) for doc in datas]
    return json_documents


@api_bp.route('/A', methods=['POST'])
def get_cve_with_brand_and_category_A():
    brand=request.args.get('brand')
    product=request.args.get('product')
    datas=cve_collection.get_cpe_by_brand_and_category(brand,product,'A')
    return jsonify(datas)

@api_bp.route('/cpe', methods=['GET'])
def send_cpes_with_id_and_brand_and_product():
    datas=cpe_collection.get_all_cpe()
    brand_id_list = []
    for item in datas:
        cpe_string = item["criteria"]
        # Utilisation de regex pour extraire la marque et l'ID
        match = re.search(r"(?:[^:]+:){3}([^:]+):(.*?):", cpe_string)
        if match:
            print(match.group(0))
            brand_id_list.append({
                "brand": match.group(1),
                "product": match.group(2),
                "id": item["_id"]
            })
    return brand_id_list

@api_bp.route('/cpe', methods=['POST'])
def get_cpes_with_brand_and_product():
    motif_marque = request.args.get('marque')
    motif_produit = request.args.get('produit')
    test=cpe_collection.get_cpe_by_brand_and_product(motif_marque,motif_produit)
    json_documents = [json.dumps(doc, default=str) for doc in test]
    return json_documents