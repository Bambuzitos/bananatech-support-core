from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import db, Empresa, EnvioFiscal


envios_fiscais_bp = Blueprint(
    'envios_fiscais', __name__, url_prefix='/envios-fiscais'
)


def competencia_atual():
    """Retorna a competência do mês atual no formato AAAA-MM."""
    return date.today().strftime('%Y-%m')


def competencia_valida(valor):
    """Valida e normaliza uma competência recebida do formulário."""
    try:
        datetime.strptime(valor, '%Y-%m')
        return valor
    except (TypeError, ValueError):
        return competencia_atual()


@envios_fiscais_bp.route('/')
def listar():
    competencia = competencia_valida(request.args.get('competencia'))
    busca = request.args.get('q', '').strip()
    filtro = request.args.get('filtro', 'todos')
    if filtro not in ('todos', 'enviado', 'pendente'):
        filtro = 'todos'

    # Todas as empresas cadastradas são consideradas, inclusive inativas.
    todas_empresas = Empresa.query.order_by(Empresa.nome_razao_social.asc()).all()

    # Só existem registros para empresas/mês que já tiveram alguma alteração.
    # A ausência de registro significa automaticamente "Pendente" naquela competência.
    registros = EnvioFiscal.query.filter_by(competencia=competencia).all()
    envios_por_empresa = {registro.empresa_id: registro for registro in registros}

    total_empresas = len(todas_empresas)
    total_enviados = sum(
        1 for empresa in todas_empresas
        if (envios_por_empresa.get(empresa.id) is not None
            and envios_por_empresa[empresa.id].enviado)
    )
    total_pendentes = total_empresas - total_enviados
    percentual = round((total_enviados / total_empresas) * 100) if total_empresas else 0

    empresas = todas_empresas
    if busca:
        empresas = [
            empresa for empresa in empresas
            if busca.casefold() in empresa.nome_razao_social.casefold()
            or busca.casefold() in empresa.cnpj.casefold()
        ]

    if filtro == 'enviado':
        empresas = [
            empresa for empresa in empresas
            if envios_por_empresa.get(empresa.id)
            and envios_por_empresa[empresa.id].enviado
        ]
    elif filtro == 'pendente':
        empresas = [
            empresa for empresa in empresas
            if not envios_por_empresa.get(empresa.id)
            or not envios_por_empresa[empresa.id].enviado
        ]

    return render_template(
        'envios_fiscais/list.html',
        empresas=empresas,
        envios_por_empresa=envios_por_empresa,
        competencia=competencia,
        busca=busca,
        filtro=filtro,
        total_empresas=total_empresas,
        total_enviados=total_enviados,
        total_pendentes=total_pendentes,
        percentual=percentual,
    )


@envios_fiscais_bp.route('/<int:empresa_id>/<acao>', methods=['POST'])
def atualizar_envio(empresa_id, acao):
    empresa = Empresa.query.get_or_404(empresa_id)
    competencia = competencia_valida(request.form.get('competencia'))

    if acao not in ('marcar', 'desmarcar'):
        flash('Ação de envio fiscal inválida.', 'danger')
        return redirect(url_for('envios_fiscais.listar', competencia=competencia))

    registro = EnvioFiscal.query.filter_by(
        empresa_id=empresa.id,
        competencia=competencia,
    ).first()

    if acao == 'marcar':
        if registro is None:
            registro = EnvioFiscal(
                empresa_id=empresa.id,
                competencia=competencia,
                enviado=True,
                data_envio=datetime.now(),
            )
            db.session.add(registro)
        else:
            registro.enviado = True
            registro.data_envio = datetime.now()
        flash(f'Envio fiscal de {empresa.nome_razao_social} marcado como enviado.', 'success')
    else:
        if registro is not None:
            registro.enviado = False
            registro.data_envio = None
        flash(f'Envio fiscal de {empresa.nome_razao_social} voltou para pendente.', 'warning')

    db.session.commit()

    return redirect(url_for(
        'envios_fiscais.listar',
        competencia=competencia,
        q=request.form.get('q', ''),
        filtro=request.form.get('filtro', 'todos'),
    ))
