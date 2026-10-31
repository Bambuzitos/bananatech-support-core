from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Ticket, Empresa, Contato, Procedimento
from utils import salvar_arquivo
from datetime import datetime

tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')

@tickets_bp.route('/')
def listar():
    status_filter = request.args.get('status', '').strip()
    categoria_filter = request.args.get('categoria', '').strip()
    empresa_id = request.args.get('empresa_id', '').strip()

    query = Ticket.query

    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    if categoria_filter:
        query = query.filter(Ticket.categoria == categoria_filter)
    if empresa_id:
        query = query.filter(Ticket.empresa_id == int(empresa_id))

    tickets = query.order_by(Ticket.data_hora.desc()).all()
    empresas = Empresa.query.order_by(Empresa.nome_razao_social.asc()).all()

    return render_template('tickets/list.html', tickets=tickets, empresas=empresas,
                           status_filter=status_filter, categoria_filter=categoria_filter, empresa_id=empresa_id)

@tickets_bp.route('/novo', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        anexo = salvar_arquivo(request.files.get('anexo_file'), 'tickets')

        empresa_id = int(request.form['empresa_id'])
        contato_id = int(request.form['contato_id']) if request.form.get('contato_id') else None
        procedimento_id = int(request.form['procedimento_id']) if request.form.get('procedimento_id') else None

        novo_ticket = Ticket(
            empresa_id=empresa_id,
            contato_id=contato_id,
            procedimento_id=procedimento_id,
            data_hora=datetime.now(),
            canal=request.form['canal'],
            categoria=request.form['categoria'],
            descricao=request.form['descricao'],
            solucao_aplicada=request.form.get('solucao_aplicada'),
            anexo_path=anexo,
            status=request.form['status'],
            observacoes=request.form.get('observacoes')
        )
        db.session.add(novo_ticket)
        db.session.commit()
        flash('Ticket de atendimento registrado!', 'success')
        return redirect(url_for('tickets.detalhes', id=novo_ticket.id))

    empresas = Empresa.query.order_by(Empresa.nome_razao_social.asc()).all()
    contatos = Contato.query.all()
    procedimentos = Procedimento.query.order_by(Procedimento.titulo.asc()).all()
    empresa_pre_selected = request.args.get('empresa_id', type=int)

    return render_template('tickets/form.html', ticket=None, empresas=empresas,
                           contatos=contatos, procedimentos=procedimentos, empresa_pre_selected=empresa_pre_selected)

@tickets_bp.route('/<int:id>')
def detalhes(id):
    ticket = Ticket.query.get_or_404(id)
    return render_template('tickets/detail.html', ticket=ticket)

@tickets_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    ticket = Ticket.query.get_or_404(id)
    if request.method == 'POST':
        ticket.empresa_id = int(request.form['empresa_id'])
        ticket.contato_id = int(request.form['contato_id']) if request.form.get('contato_id') else None
        ticket.procedimento_id = int(request.form['procedimento_id']) if request.form.get('procedimento_id') else None
        ticket.canal = request.form['canal']
        ticket.categoria = request.form['categoria']
        ticket.descricao = request.form['descricao']
        ticket.solucao_aplicada = request.form.get('solucao_aplicada')
        ticket.status = request.form['status']
        ticket.observacoes = request.form.get('observacoes')

        if request.files.get('anexo_file'):
            novo_anexo = salvar_arquivo(request.files.get('anexo_file'), 'tickets')
            if novo_anexo:
                ticket.anexo_path = novo_anexo

        db.session.commit()
        flash('Ticket de atendimento atualizado!', 'success')
        return redirect(url_for('tickets.detalhes', id=ticket.id))

    empresas = Empresa.query.order_by(Empresa.nome_razao_social.asc()).all()
    contatos = Contato.query.filter_by(empresa_id=ticket.empresa_id).all()
    procedimentos = Procedimento.query.order_by(Procedimento.titulo.asc()).all()

    return render_template('tickets/form.html', ticket=ticket, empresas=empresas,
                           contatos=contatos, procedimentos=procedimentos)

@tickets_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    ticket = Ticket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket excluído!', 'warning')
    return redirect(url_for('tickets.listar'))