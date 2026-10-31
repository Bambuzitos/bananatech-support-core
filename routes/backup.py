import os
from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash, current_app
from utils import gerar_backup_zip, restaurar_backup_zip
from models import db

backup_bp = Blueprint('backup', __name__, url_prefix='/backup')

@backup_bp.route('/')
def index():
    return render_template('backup/index.html')

@backup_bp.route('/exportar')
def exportar():
    zip_path = gerar_backup_zip()
    return send_file(zip_path, as_attachment=True, download_name='backup_bananatech.zip')

@backup_bp.route('/restaurar', methods=['POST'])
def restaurar():
    if 'backup_zip' not in request.files:
        flash('Nenhum arquivo enviado!', 'danger')
        return redirect(url_for('backup.index'))

    file = request.files['backup_zip']
    if file.filename == '':
        flash('Selecione um arquivo .zip válido.', 'danger')
        return redirect(url_for('backup.index'))

    if file and file.filename.endswith('.zip'):
        temp_path = os.path.join(current_app.config['BASE_DIR'], 'temp_restore.zip')
        file.save(temp_path)
        try:
            restaurar_backup_zip(temp_path, db.engine)
            if os.path.exists(temp_path):
                os.remove(temp_path)
            flash('Sistema restaurado com sucesso do arquivo de backup!', 'success')
        except Exception as e:
            flash(f'Erro ao restaurar backup: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))

    flash('Formato de arquivo inválido. Por favor envie um arquivo .zip', 'danger')
    return redirect(url_for('backup.index'))