from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Empresa
from datetime import datetime

empresas_bp = Blueprint('empresas', __name__, url_prefix='/empresas')

@empresas_bp.route('/')
def listar():
    busca = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()
    query = Empresa.query

    if busca:
        query = query.filter((Empresa.nome_razao_social.ilike(f'%{busca}%')) | (Empresa.cnpj.ilike(f'%{busca}%')))
    if status_filter:
        query = query.filter(Empresa.status == status_filter)

    empresas = query.order_by(Empresa.nome_razao_social.asc()).all()
    return render_template('empresas/list.html', empresas=empresas, busca=busca, status_filter=status_filter)

@empresas_bp.route('/nova', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        venc_cert = request.form.get('vencimento_certificado')
        venc_cert_date = datetime.strptime(venc_cert, '%Y-%m-%d').date() if venc_cert else None

        nova_empresa = Empresa(
            nome_razao_social=request.form['nome_razao_social'],
            cnpj=request.form['cnpj'],
            status=request.form['status'],
            endereco=request.form.get('endereco'),
            sistema_principal=request.form['sistema_principal'],
            banco=request.form.get('banco'),
            enviar_boleto_manual=(request.form.get('enviar_boleto_manual') == 'Sim'),
            dia_vencimento_boleto=int(request.form['dia_vencimento_boleto']) if request.form.get('dia_vencimento_boleto') else None,
            dia_fechamento_fiscal=int(request.form['dia_fechamento_fiscal']) if request.form.get('dia_fechamento_fiscal') else None,
            compra_certificado_conosco=(request.form.get('compra_certificado_conosco') == 'Sim'),
            vencimento_certificado=venc_cert_date,
            avisos_criticos=request.form.get('avisos_criticos'),
            observacoes=request.form.get('observacoes')
        )
        db.session.add(nova_empresa)
        db.session.commit()
        flash('Empresa cadastrada com sucesso!', 'success')
        return redirect(url_for('empresas.detalhes', id=nova_empresa.id))

    return render_template('empresas/form.html', empresa=None)

@empresas_bp.route('/<int:id>')
def detalhes(id):
    empresa = Empresa.query.get_or_404(id)
    return render_template('empresas/detail.html', empresa=empresa)

@empresas_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    empresa = Empresa.query.get_or_404(id)
    if request.method == 'POST':
        venc_cert = request.form.get('vencimento_certificado')
        venc_cert_date = datetime.strptime(venc_cert, '%Y-%m-%d').date() if venc_cert else None

        empresa.nome_razao_social = request.form['nome_razao_social']
        empresa.cnpj = request.form['cnpj']
        empresa.status = request.form['status']
        empresa.endereco = request.form.get('endereco')
        empresa.sistema_principal = request.form['sistema_principal']
        empresa.banco = request.form.get('banco')
        empresa.enviar_boleto_manual = (request.form.get('enviar_boleto_manual') == 'Sim')
        empresa.dia_vencimento_boleto = int(request.form['dia_vencimento_boleto']) if request.form.get('dia_vencimento_boleto') else None
        empresa.dia_fechamento_fiscal = int(request.form['dia_fechamento_fiscal']) if request.form.get('dia_fechamento_fiscal') else None
        empresa.compra_certificado_conosco = (request.form.get('compra_certificado_conosco') == 'Sim')
        empresa.vencimento_certificado = venc_cert_date
        empresa.avisos_criticos = request.form.get('avisos_criticos')
        empresa.observacoes = request.form.get('observacoes')

        db.session.commit()
        flash('Dados da empresa atualizados com sucesso!', 'success')
        return redirect(url_for('empresas.detalhes', id=empresa.id))

    return render_template('empresas/form.html', empresa=empresa)

@empresas_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    empresa = Empresa.query.get_or_404(id)
    db.session.delete(empresa)
    db.session.commit()
    flash('Empresa excluída com sucesso!', 'warning')
    return redirect(url_for('empresas.listar'))