from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Empresa(db.Model):
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True)
    nome_razao_social = db.Column(db.String(150), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False, unique=True)
    status = db.Column(db.String(20), nullable=False, default='Ativo')  # Ativo, Inativo, Inadimplente
    endereco = db.Column(db.String(255), nullable=True)

    # Sistema & Financeiro
    sistema_principal = db.Column(db.String(50), nullable=False)  # TK2000, Pallas, GenPack, ControlID
    banco = db.Column(db.String(50), nullable=True)
    enviar_boleto_manual = db.Column(db.Boolean, default=False)
    dia_vencimento_boleto = db.Column(db.Integer, nullable=True)

    # Fiscal & Serviços
    dia_fechamento_fiscal = db.Column(db.Integer, nullable=True)
    compra_certificado_conosco = db.Column(db.Boolean, default=False)
    vencimento_certificado = db.Column(db.Date, nullable=True)

    # Operacional
    avisos_criticos = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    equipamentos = db.relationship('Equipamento', backref='empresa', cascade='all, delete-orphan', lazy=True)
    contatos = db.relationship('Contato', backref='empresa', cascade='all, delete-orphan', lazy=True)
    tickets = db.relationship('Ticket', backref='empresa', cascade='all, delete-orphan', lazy=True)


class Equipamento(db.Model):
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Caixa, Servidor, Impressora, Balança
    identificacao = db.Column(db.String(100), nullable=False)  # ex: Caixa 01
    acesso_remoto_id = db.Column(db.String(50), nullable=True)
    acesso_remoto_senha = db.Column(db.String(50), nullable=True)
    anexo_path = db.Column(db.String(255), nullable=True)
    url_drivers = db.Column(db.String(255), nullable=True)
    observacoes_tecnicas = db.Column(db.Text, nullable=True)


class Contato(db.Model):
    __tablename__ = 'contatos'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(30), nullable=False)
    funcao = db.Column(db.String(50), nullable=False)  # Dono, Operador, Contador
    recebe_arquivo_fiscal = db.Column(db.Boolean, default=False)
    observacoes = db.Column(db.Text, nullable=True)
    tickets = db.relationship('Ticket', backref='contato', lazy=True)


class Procedimento(db.Model):
    __tablename__ = 'procedimentos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    sistema_relacionado = db.Column(db.String(50), nullable=False)  # TK2000, Pallas, GenPack, ControlID, Geral
    tags = db.Column(db.String(200), nullable=True)  # Separadas por virgula
    solucao_passo_a_passo = db.Column(db.Text, nullable=False)
    script_whatsapp = db.Column(db.Text, nullable=True)
    anexo_path = db.Column(db.String(255), nullable=True)
    links_uteis = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    tickets = db.relationship('Ticket', backref='procedimento', lazy=True)


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'), nullable=True)
    procedimento_id = db.Column(db.Integer, db.ForeignKey('procedimentos.id'), nullable=True)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    canal = db.Column(db.String(30), nullable=False)  # WhatsApp, Telefone, Presencial
    categoria = db.Column(db.String(50), nullable=False)  # Erro TK2000, Rejeição Sefaz, Hardware, Dúvida Fiscal
    descricao = db.Column(db.Text, nullable=False)
    solucao_aplicada = db.Column(db.Text, nullable=True)
    anexo_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Aberto')  # Aberto, Pendente, Resolvido
    observacoes = db.Column(db.Text, nullable=True)


class EnvioFiscal(db.Model):
    """Registra o envio dos arquivos fiscais de uma empresa em cada competência."""
    __tablename__ = 'envios_fiscais'
    __table_args__ = (
        db.UniqueConstraint(
            'empresa_id', 'competencia',
            name='uq_envio_fiscal_empresa_competencia'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    competencia = db.Column(db.String(7), nullable=False)  # Formato: AAAA-MM
    enviado = db.Column(db.Boolean, nullable=False, default=False)
    data_envio = db.Column(db.DateTime, nullable=True)

    empresa = db.relationship(
        'Empresa',
        backref=db.backref('envios_fiscais', cascade='all, delete-orphan', lazy=True)
    )
