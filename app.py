import os

from flask import Flask, send_from_directory

from config import Config
from models import db

from routes.main import main_bp
from routes.empresas import empresas_bp
from routes.equipamentos import equipamentos_bp
from routes.contatos import contatos_bp
from routes.tickets import tickets_bp
from routes.procedimentos import procedimentos_bp
from routes.backup import backup_bp
from routes.envios_fiscais import envios_fiscais_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(app.config['BASE_DIR'], 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(empresas_bp)
    app.register_blueprint(equipamentos_bp)
    app.register_blueprint(contatos_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(procedimentos_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(envios_fiscais_bp)

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
