from flask import Blueprint, request, redirect, url_for, flash, render_template
from models import db, Equipamento, Empresa
from utils import salvar_arquivo

equipamentos_bp = Blueprint('equipamentos', __name__, url_prefix='/equipamentos')

@equipamentos_bp.route('/novo/<int:empresa_id>', methods=['GET', 'POST'])
def criar(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    if request.method == 'POST':
        anexo = salvar_arquivo(request.files.get('anexo_file'), 'equipamentos')
        novo_equipamento = Equipamento(
            empresa_id=empresa.id,
            tipo=request.form['tipo'],
            identificacao=request.form['identificacao'],
            acesso_remoto_id=request.form.get('acesso_remoto_id'),
            acesso_remoto_senha=request.form.get('acesso_remoto_senha'),
            anexo_path=anexo,
            url_drivers=request.form.get('url_drivers'),
            observacoes_tecnicas=request.form.get('observacoes_tecnicas')
        )
        db.session.add(novo_equipamento)
        db.session.commit()
        flash('Equipamento adicionado com sucesso!', 'success')
        return redirect(url_for('empresas.detalhes', id=empresa.id))

    return render_template('equipamentos/form.html', empresa=empresa, equipamento=None)

@equipamentos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    equipamento = Equipamento.query.get_or_404(id)
    if request.method == 'POST':
        equipamento.tipo = request.form['tipo']
        equipamento.identificacao = request.form['identificacao']
        equipamento.acesso_remoto_id = request.form.get('acesso_remoto_id')
        equipamento.acesso_remoto_senha = request.form.get('acesso_remoto_senha')
        equipamento.url_drivers = request.form.get('url_drivers')
        equipamento.observacoes_tecnicas = request.form.get('observacoes_tecnicas')

        if request.files.get('anexo_file'):
            novo_anexo = salvar_arquivo(request.files.get('anexo_file'), 'equipamentos')
            if novo_anexo:
                equipamento.anexo_path = novo_anexo

        db.session.commit()
        flash('Equipamento atualizado com sucesso!', 'success')
        return redirect(url_for('empresas.detalhes', id=equipamento.empresa_id))

    return render_template('equipamentos/form.html', empresa=equipamento.empresa, equipamento=equipamento)

@equipamentos_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    equipamento = Equipamento.query.get_or_404(id)
    empresa_id = equipamento.empresa_id
    db.session.delete(equipamento)
    db.session.commit()
    flash('Equipamento removido!', 'warning')
    return redirect(url_for('empresas.detalhes', id=empresa_id))