import os
import re
from app import create_app
from models import db, Empresa, Contato

app = create_app()

def extrair_dados_bloco(bloco_texto):
    linhas = [linha.strip() for linha in bloco_texto.strip().split('\n') if linha.strip()]
    if not linhas:
        return None

    primeira_linha = linhas[0]
    
    # Identifica o Sistema
    sistema = "TK2000" if "[TK2000]" in primeira_linha else "TK2000"
    
    # Limpa a Razão Social / Nome da Empresa
    nome_empresa = re.sub(r'\s*-\s*\[TK2000\]', '', primeira_linha, flags=re.IGNORECASE).strip()
    
    texto_unificado = " ".join(linhas)

    # Extrai CNPJ ou CPF
    match_cnpj = re.search(r'\b\d{2,3}[\.,]?\d{3}[\.,]?\d{3}[/-]?\d{4}[-]?\d{2}\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', texto_unificado)
    cnpj = match_cnpj.group(0) if match_cnpj else "00.000.000/0000-00"

    # Extrai Telefone / WhatsApp
    match_tel = re.search(r'\(?\d{2}\)?\s?9?\d{4,5}[-.\s]?\d{4}', texto_unificado)
    whatsapp = match_tel.group(0) if match_tel else ""
    whatsapp_limpo = re.sub(r'\D', '', whatsapp)

    # Extrai E-mail
    match_email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto_unificado)
    email = match_email.group(0) if match_email else ""

    # Extrai Código CM
    match_cm = re.search(r'CM-\d+', texto_unificado)
    codigo_cm = match_cm.group(0) if match_cm else ""

    return {
        'nome': nome_empresa,
        'cnpj': cnpj,
        'sistema': sistema,
        'whatsapp': whatsapp_limpo,
        'email': email,
        'codigo_cm': codigo_cm
    }

def executar_importacao():
    caminho_txt = os.path.join(app.config['BASE_DIR'], 'lista_clientes.txt')
    if not os.path.exists(caminho_txt):
        print(f"Erro: O arquivo {caminho_txt} não foi encontrado!")
        return

    with open(caminho_txt, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Separa os clientes agrupando por blocos de texto
    blocos = []
    bloco_atual = []
    
    for linha in conteudo.splitlines():
        linha_str = linha.strip()
        if not linha_str:
            if bloco_atual:
                blocos.append("\n".join(bloco_atual))
                bloco_atual = []
        else:
            # Detecta início de um novo cliente
            eh_novo_cliente = (
                not linha_str.startswith('|') and 
                not re.match(r'^\(?\d{2}\)?', linha_str) and 
                not re.match(r'^[0-9\.\/-]+$', linha_str) and 
                '@' not in linha_str and 
                not linha_str.startswith('CM-') and 
                bloco_atual
            )
            if eh_novo_cliente:
                blocos.append("\n".join(bloco_atual))
                bloco_atual = [linha_str]
            else:
                bloco_atual.append(linha_str)
                
    if bloco_atual:
        blocos.append("\n".join(bloco_atual))

    with app.app_context():
        empresas_importadas = 0
        contatos_importados = 0
        ignorados = 0

        for b in blocos:
            dados = extrair_dados_bloco(b)
            if not dados or not dados['nome']:
                continue

            # Verifica duplicação por CNPJ ou por Razão Social
            empresa_existente = Empresa.query.filter(
                (Empresa.cnpj == dados['cnpj']) | (Empresa.nome_razao_social == dados['nome'])
            ).first()

            if not empresa_existente:
                obs_empresa = f"Código Interno: {dados['codigo_cm']}" if dados['codigo_cm'] else ""
                nova_empresa = Empresa(
                    nome_razao_social=dados['nome'],
                    cnpj=dados['cnpj'],
                    status='Ativo',
                    sistema_principal=dados['sistema'],
                    observacoes=obs_empresa
                )
                db.session.add(nova_empresa)
                db.session.flush()  # Gera o ID da empresa para vinculação no relacionamento

                # Cria o Contato associado (Dono / Responsável)
                if dados['whatsapp'] or dados['email']:
                    obs_contato = f"E-mail: {dados['email']}" if dados['email'] else ""
                    novo_contato = Contato(
                        empresa_id=nova_empresa.id,
                        nome="Contato Principal",
                        whatsapp=dados['whatsapp'],
                        funcao="Dono",
                        recebe_arquivo_fiscal=True,
                        observacoes=obs_contato
                    )
                    db.session.add(novo_contato)
                    contatos_importados += 1

                empresas_importadas += 1
            else:
                ignorados += 1

        db.session.commit()
        print(f"✅ Sucesso! {empresas_importadas} empresas e {contatos_importados} contatos cadastrados no banco de dados.")
        if ignorados > 0:
            print(f"⚠️ {ignorados} registros já existiam e foram ignorados.")

if __name__ == '__main__':
    executar_importacao()