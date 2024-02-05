from flask import Flask
from controllers.routes import api_bp  # Importez le Blueprint défini dans controllers/routes.py
from db.cve_collection import CveCollection
cve_collection = CveCollection()

app = Flask(__name__)

# Enregistrez le Blueprint dans l'application
app.register_blueprint(api_bp, url_prefix='/api')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)