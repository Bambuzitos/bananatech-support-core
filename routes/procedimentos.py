from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Procedimento
from utils import salvar_arquivo

procedimentos_bp = Blueprint('procedimentos', __name__, url_prefix='/procedimentos')

@procedimentos_bp.route('/')
def listar():
    busca = request.args.get('q', '').strip()
    sistema_filter = request.args.get('sistema', '').strip()

    query = Procedimento.query

    if busca:
        query = query.filter(
            (Procedimento.titulo.ilike(f'%{busca}%')) |
            (Procedimento.tags.ilike(f'%{busca}%')) |
            (Procedimento.solucao_passo_a_passo.ilike(f'%{busca}%'))
        )
    if sistema_filter:
        query = query.filter(Procedimento.sistema_relacionado == sistema_filter)

    procedimentos = query.order_by(Procedimento.titulo.asc()).all()
    return render_template('procedimentos/list.html', procedimentos=procedimentos, busca=busca, sistema_filter=sistema_filter)

@procedimentos_bp.route('/novo', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        anexo = salvar_arquivo(request.files.get('anexo_file'), 'procedimentos')

        novo_procedimento = Procedimento(
            titulo=request.form['titulo'],
            sistema_relacionado=request.form['sistema_relacionado'],
            tags=request.form.get('tags'),
            solucao_passo_a_passo=request.form['solucao_passo_a_passo'],
            script_whatsapp=request.form.get('script_whatsapp'),
            anexo_path=anexo,
            links_uteis=request.form.get('links_uteis'),
            observacoes=request.form.get('observacoes')
        )
        db.session.add(novo_procedimento)
        db.session.commit()
        flash('Procedimento/Base de Conhecimento cadastrado!', 'success')
        return redirect(url_for('procedimentos.detalhes', id=novo_procedimento.id))

    return render_template('procedimentos/form.html', procedimento=None)

@procedimentos_bp.route('/<int:id>')
def detalhes(id):
    procedimento = Procedimento.query.get_or_404(id)
    return render_template('procedimentos/detail.html', procedimento=procedimento)

@procedimentos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    procedimento = Procedimento.query.get_or_404(id)
    if request.method == 'POST':
        procedimento.titulo = request.form['titulo']
        procedimento.sistema_relacionado = request.form['sistema_relacionado']
        procedimento.tags = request.form.get('tags')
        procedimento.solucao_passo_a_passo = request.form['solucao_passo_a_passo']
        procedimento.script_whatsapp = request.form.get('script_whatsapp')
        procedimento.links_uteis = request.form.get('links_uteis')
        procedimento.observacoes = request.form.get('observacoes')

        if request.files.get('anexo_file'):
            novo_anexo = salvar_arquivo(request.files.get('anexo_file'), 'procedimentos')
            if novo_anexo:
                procedimento.anexo_path = novo_anexo

        db.session.commit()
        flash('Procedimento atualizado!', 'success')
        return redirect(url_for('procedimentos.detalhes', id=procedimento.id))

    return render_template('procedimentos/form.html', procedimento=procedimento)

@procedimentos_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    procedimento = Procedimento.query.get_or_404(id)
    db.session.delete(procedimento)
    db.session.commit()
    flash('Procedimento removido da Base de Conhecimento!', 'warning')
    return redirect(url_for('procedimentos.listar'))