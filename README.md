# 🍌 BananaTech Support Core

> **Sistema Integrado de Gestão de Clientes, Suporte Técnico e Base de Conhecimento para Revenda de Sistemas de PDV.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask-black?logo=flask)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205-purple?logo=bootstrap)

---

## 🛠️ Autoria e Desenvolvimento

Este projeto foi desenvolvido em colaboração de engenharia de software entre Inteligência Artificial e Inteligência Humana:

* **Desenvolvimento e Arquitetura Inicial:** Gemini AI
* **Engenharia de Requisitos, Sanitização, Testes e Revisão:** [Arthur Oliveira (@Bambuzitos)](https://github.com/Bambuzitos)

---

## 📋 Visão Geral

O **BananaTech Support Core** é uma aplicação web local de helpdesk e CRM operacional projetada especificamente para as necessidades operacionais de uma revenda de software de automação comercial (PDV), com suporte predominante aos sistemas **TK2000** e **Pallas**, além de soluções **GenPack** e **ControlID**.

O sistema centraliza a operação técnica para lidar com clientes de baixa maturidade digital, rotinas fiscais recorrentes (envio mensal de XMLs), cobranças manuais de boletos, gestão de certificados digitais, acessos remotos a caixas/servidores e automação de atendimento via WhatsApp.

---

## ✨ Funcionalidades Principais

### 🏢 1. Gestão Completa de Empresas (Clientes)
* **Cadastramento Unificado:** Razão Social, CNPJ, endereço completo e controle de status (`Ativo`, `Inativo`, `Inadimplente`).
* **Módulo Financeiro & Fiscal:** Mapeamento do banco utilizado, indicador de boleto manual, dia de vencimento, dia de fechamento fiscal e controle do vencimento de certificado digital (com indicação se a compra foi realizada com a revenda).
* **Painel de Avisos Críticos:** Sistema de alertas visuais destacados nas telas do cliente e no dashboard operacional para sinalizar restrições de atendimento (ex: cliente inadimplente ou pendência fiscal).

### 👥 2. Gestão de Contatos Vinculados (1:N)
* **Perfis de Atendimento:** Cadastro de múltiplos contatos por empresa categorizados em `Dono`, `Operador` ou `Contador`.
* **Ações Rápidas:** Disparo direto de conversas via WhatsApp com um clique.
* **Flag Fiscal:** Sinalizador visual para indicar se o contato é o responsável por receber arquivos XML e relatórios mensais.

### 🖥️ 3. Controle de Equipamentos e Acesso Remoto (1:N)
* **Mapeamento do Parque Tecnológico:** Cadastro individualizado por tipo (`Caixa`, `Servidor`, `Impressora`, `Balança`).
* **Credenciais Rápidas:** Armazenamento seguro de IDs e senhas de acesso remoto (AnyDesk / TeamViewer).
* **Repositório de Suporte:** Links diretos para drivers e anexos de manuais técnicos por equipamento.

### 🎫 4. Sistema de Tickets de Suporte
* **Categorização Operacional:** Registro de chamados por canal (`WhatsApp`, `Telefone`, `Presencial`) e categoria (`Erro TK2000`, `Rejeição Sefaz`, `Hardware`, `Dúvida Fiscal`).
* **Vínculo Direto:** Associação de tickets a um cliente, contato solicitante e a um procedimento da Base de Conhecimento.
* **Gestão de Anexos:** Upload e visualização de prints de erro e arquivos de log.

### 📚 5. Base de Conhecimento (Procedimentos Técnicos)
* **Repositório de Soluções:** Passo a passo técnico detalhado para resoluções de erros de PDV e Sefaz, categorizado por sistema e indexado por tags de busca.
* **Scripts Prontos para WhatsApp:** Mensagens padronizadas com botão de cópia em 1 clique para envio rápido ao cliente.
* **Anexos e Links Úteis:** Centralização de imagens de erro original e links de documentação.

### 💾 6. Módulo Integrado de Backup & Restauração
* **Exportação Completa:** Geração com 1 clique de arquivo `.zip` contendo o banco de dados `bananatech.db` e a pasta de anexos `/uploads`.
* **Restauração em Quente:** Upload do pacote `.zip` para restauração integral do estado do sistema sem perda de vinculações.

### ⚡ 7. Importação em Lote via CLI
* Scripts Python inclusos (`importar_clientes.py` e `importar_lista.py`) para leitura e cadastro automático em lote a partir de arquivos CSV ou relatórios em texto bruto de clientes.

---

## 📂 Arquitetura de Pastas do Projeto

```text
bananatech_system/
├── app.py                  # Ponto de entrada da aplicação Flask
├── config.py               # Configurações de ambiente e constantes
├── models.py               # Modelos de dados SQLAlchemy (ORM)
├── utils.py                # Utilitários de manipulação de arquivos e Zip
├── requirements.txt        # Dependências Python do projeto
├── .env.example            # Modelo de variáveis de ambiente
├── .gitignore              # Proteção contra envio de dados sensíveis
├── importar_lista.py       # Script CLI para carga de dados em massa
├── instance/
│   └── bananatech.db       # Banco de dados SQLite local (gerado automaticamente)
├── uploads/                # Armazenamento de anexos e mídias
├── routes/                 # Controllers / Módulos de Rotas (Blueprints)
│   ├── __init__.py
│   ├── main.py             # Dashboard principal
│   ├── empresas.py         # CRUD de empresas
│   ├── equipamentos.py     # CRUD de equipamentos
│   ├── contatos.py         # CRUD de contatos
│   ├── tickets.py          # Módulo de chamados
│   ├── procedimentos.py    # Base de conhecimento
│   └── backup.py           # Gestão de backup e restauração
└── templates/              # Interfaces HTML (Jinja2 + Bootstrap 5)
    ├── base.html
    ├── index.html
    ├── empresas/
    ├── equipamentos/
    ├── contatos/
    ├── tickets/
    ├── procedimentos/
    └── backup/
```

---

## ⚙️ Pré-requisitos e Dependências

* **Python:** 3.10 ou superior
* **Bibliotecas Principais:**
  * `Flask==3.0.2`
  * `Flask-SQLAlchemy==3.1.1`
  * `Werkzeug==3.0.1`

---

## 🚀 Guia de Instalação e Execução Local

### 1. Clonar o Repositório
```bash
git clone https://github.com/Bambuzitos/bananatech-support-core.git
cd bananatech-support-core
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Copie o arquivo de exemplo `.env.example` para `.env`:
```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

### 5. Executar a Aplicação
```bash
python app.py
```
Acesse a aplicação no navegador através do endereço: `http://127.0.0.1:5000`

---

## 📄 Licença e Uso

Este projeto foi desenvolvido de forma personalizada para a operação da **BananaTech**. Todos os direitos de modificação e evolução pertencem ao mantenedor do repositório.