from flask import Blueprint, render_template
from models import Empresa, Ticket, Procedimento

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    total_empresas = Empresa.query.count()
    empresas_inadimplentes = Empresa.query.filter_by(status='Inadimplente').count()
    tickets_abertos = Ticket.query.filter(Ticket.status.in_(['Aberto', 'Pendente'])).count()
    total_procedimentos = Procedimento.query.count()

    ultimos_tickets = Ticket.query.order_by(Ticket.data_hora.desc()).limit(5).all()
    empresas_alertas = Empresa.query.filter(Empresa.avisos_criticos.isnot(None), Empresa.avisos_criticos != '').limit(5).all()

    return render_template('index.html',
                           total_empresas=total_empresas,
                           empresas_inadimplentes=empresas_inadimplentes,
                           tickets_abertos=tickets_abertos,
                           total_procedimentos=total_procedimentos,
                           ultimos_tickets=ultimos_tickets,
                           empresas_alertas=empresas_alertas)