from flask import Blueprint, jsonify, request
from db.cve_collection import CveCollection
from .classifier import CVEclassifier

# Créez un objet Blueprint pour les routes
api_bp = Blueprint('api', __name__)

cve_collection = CveCollection()
cve_classifier=CVEclassifier()
@api_bp.route('/', methods=['GET'])
def get_data():
    classifier=cve_classifier.classify_cve()
    # Retourner les résultats en tant que JSON
    return jsonify(classifier)