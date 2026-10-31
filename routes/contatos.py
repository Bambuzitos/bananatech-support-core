from flask import Blueprint, request, redirect, url_for, flash, render_template
from models import db, Contato, Empresa

contatos_bp = Blueprint('contatos', __name__, url_prefix='/contatos')

@contatos_bp.route('/novo/<int:empresa_id>', methods=['GET', 'POST'])
def criar(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    if request.method == 'POST':
        novo_contato = Contato(
            empresa_id=empresa.id,
            nome=request.form['nome'],
            whatsapp=request.form['whatsapp'],
            funcao=request.form['funcao'],
            recebe_arquivo_fiscal=(request.form.get('recebe_arquivo_fiscal') == 'Sim'),
            observacoes=request.form.get('observacoes')
        )
        db.session.add(novo_contato)
        db.session.commit()
        flash('Contato adicionado com sucesso!', 'success')
        return redirect(url_for('empresas.detalhes', id=empresa.id))

    return render_template('contatos/form.html', empresa=empresa, contato=None)

@contatos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    contato = Contato.query.get_or_404(id)
    if request.method == 'POST':
        contato.nome = request.form['nome']
        contato.whatsapp = request.form['whatsapp']
        contato.funcao = request.form['funcao']
        contato.recebe_arquivo_fiscal = (request.form.get('recebe_arquivo_fiscal') == 'Sim')
        contato.observacoes = request.form.get('observacoes')

        db.session.commit()
        flash('Contato atualizado com sucesso!', 'success')
        return redirect(url_for('empresas.detalhes', id=contato.empresa_id))

    return render_template('contatos/form.html', empresa=contato.empresa, contato=contato)

@contatos_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    contato = Contato.query.get_or_404(id)
    empresa_id = contato.empresa_id
    db.session.delete(contato)
    db.session.commit()
    flash('Contato removido!', 'warning')
    return redirect(url_for('empresas.detalhes', id=empresa_id))