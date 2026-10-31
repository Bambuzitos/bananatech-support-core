import os
import shutil
import zipfile
from werkzeug.utils import secure_filename
from flask import current_app

def salvar_arquivo(file_obj, subpasta=''):
    if not file_obj or file_obj.filename == '':
        return None
    filename = secure_filename(file_obj.filename)
    time_prefix = os.path.splitext(filename)[0] + '_' + os.urandom(4).hex() + os.path.splitext(filename)[1]
    target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subpasta)
    os.makedirs(target_dir, exist_ok=True)
    filepath = os.path.join(target_dir, time_prefix)
    file_obj.save(filepath)
    rel_path = os.path.join(subpasta, time_prefix) if subpasta else time_prefix
    return rel_path.replace('\\', '/')

def gerar_backup_zip():
    zip_filename = "backup_bananatech.zip"
    zip_path = os.path.join(current_app.config['BASE_DIR'], zip_filename)

    db_path = os.path.join(current_app.config['BASE_DIR'], 'instance', 'bananatech.db')
    uploads_dir = current_app.config['UPLOAD_FOLDER']

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.exists(db_path):
            zipf.write(db_path, arcname='bananatech.db')

        if os.path.exists(uploads_dir):
            for root, _, files in os.walk(uploads_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=current_app.config['BASE_DIR'])
                    zipf.write(full_path, arcname=arcname)

    return zip_path

def restaurar_backup_zip(zip_file_path, db_engine):
    instance_dir = os.path.join(current_app.config['BASE_DIR'], 'instance')
    target_db = os.path.join(instance_dir, 'bananatech.db')
    uploads_dir = current_app.config['UPLOAD_FOLDER']

    db_engine.dispose()

    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        for member in zipf.namelist():
            if member == 'bananatech.db':
                os.makedirs(instance_dir, exist_ok=True)
                with zipf.open(member) as source, open(target_db, 'wb') as target:
                    shutil.copyfileobj(source, target)
            elif member.startswith('uploads/'):
                zipf.extract(member, path=current_app.config['BASE_DIR'])