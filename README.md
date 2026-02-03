🇵🇹 Português
📌 Descrição do Projeto

O Gestor de Despesas é uma aplicação web desenvolvida em Python com Flask, criada para registar, consultar e analisar despesas pessoais de forma simples e organizada.
Este projeto foi desenvolvido no âmbito da UFCD de Programação Avançada com Python, aplicando conceitos fundamentais e avançados da linguagem, bem como boas práticas de desenvolvimento.

🎯 Objetivos do Projeto

Desenvolver aplicação web com Flask
Aplicar Programação Orientada a Objetos
Utilizar Decoradores para validação e registo de ações
Trabalhar com análise de dados usando Pandas e NumPy
Criar estrutura modular profissional
Implementar persistência de dados

⚙️ Funcionalidades
✅ Registo de Despesas

Permite inserir:
Data
Descrição
Categoria
Valor

✅ Consulta e Filtros

Listagem completa de despesas
Ordenação por data
Filtro por categoria

✅ Resumo Estatístico

Utilizando Pandas e NumPy:
Total de despesas
Média de gastos
Desvio padrão
Total por categoria

✅ Persistência de Dados

Os dados são armazenados em:
data/despesas.csv
O sistema cria automaticamente o ficheiro caso não exista.

🧠 Conceitos Aplicados
Estruturas Python

Listas
Dicionários
Tuplas
Sets
Programação Orientada a Objetos
Classe principal:
Despesa

Decoradores

Utilizados para:
Validação de dados
Registo de ações
Modularização

Divisão do projeto em módulos independentes.

gestor_despesas
│
├── app.py
├── models.py
├── utils.py
├── requirements.txt
│
├── data
│   └── despesas.csv
│
├── templates
│   ├── base.html
│   ├── index.html
│   └── resumo.html
│
└── static
    └── style.css

🧩 Como Executar
Criar ambiente virtual
python -m venv venv

Ativar ambiente virtual
venv\Scripts\activate

Executar aplicação
python app.py

Abrir no navegador
http://127.0.0.1:5000

🧪 Testes Funcionais

✔ Inserir despesas
✔ Filtrar por categoria
✔ Visualizar resumo estatístico
✔ Confirmar gravação no CSV

🚀 Melhorias Futuras

Integração com Base de Dados SQL
Autenticação de utilizadores
Exportação para Excel ou PDF
Dashboard com gráficos
Deploy online


🇬🇧 English
📌 Project Description

The Expense Manager is a web application developed using Python and Flask, designed to register, manage and analyse personal expenses in a simple and organized way.

This project was developed as part of an Advanced Python Programming course, applying fundamental and advanced programming concepts and software development best practices.

🎯 Project Goals

Develop a web application using Flask

Apply Object-Oriented Programming

Use decorators for validation and logging

Perform data analysis with Pandas and NumPy

Implement professional modular project structure

Implement data persistence

⚙️ Features
✅ Expense Registration

Allows input of:

Date

Description

Category

Amount

✅ Listing and Filtering

Full expense listing

Sorting by date

Category filtering

✅ Statistical Summary

Using Pandas and NumPy:

Total expenses

Average spending

Standard deviation

Total per category

✅ Data Persistence

Data is stored in:
data/despesas.csv
The system automatically creates the file if it does not exist.

🧠 Applied Concepts
Python Data Structures

Lists
Dictionaries
Tuples
Sets
Object-Oriented Programming

Main class:

Expense
Decorators

Used for:

Data validation
Action logging
Modular Architecture

Project divided into independent modules.

📁 Project Structure

(Same structure as Portuguese version)

🧩 How to Run
Create virtual environment
python -m venv venv

Activate environment
venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Run application
python app.py

Open in browser
http://127.0.0.1:5000

🧪 Functional Testing

✔ Add expenses
✔ Filter by category
✔ View statistical summary
✔ Verify CSV storage

🚀 Future Improvements
SQL database integration
User authentication
Excel/PDF export
Dashboard with charts
Cloud deployment

👩‍💻 Author | Autora

Palmira Solochi
Curso Técnico de Programação – IEFP
2026



