# 📊 Gestor de Despesas | Expense Manager

## 🇵🇹 Português

### 📌 Descrição

O **Gestor de Despesas** é uma aplicação web desenvolvida com **Python e Flask**, que permite registar, consultar, filtrar e analisar despesas pessoais de forma simples, organizada e intuitiva.

Este projeto foi desenvolvido no âmbito da UFCD de **Programação Avançada com Python**, aplicando conceitos fundamentais e avançados da linguagem, bem como boas práticas de desenvolvimento de software.

> 🔹 **Este projeto é 100% da minha autoria**, desde a conceção da ideia até à implementação técnica final, tendo sido desenvolvido de forma autónoma com foco em organização, robustez e clareza do código.

---

### 🎯 Objetivos

- Desenvolver uma aplicação web utilizando Flask  
- Aplicar Programação Orientada a Objetos  
- Utilizar Decoradores para validação e controlo de ações 
- Trabalhar com análise de dados usando Pandas e NumPy  
- Criar arquitetura modular e proficional  
- Implementar persistência de dados com SQLite 

---

### ⚙️ Funcionalidades

#### ✅ Registo de Despesas
Permite inserir:
- Data  
- Descrição  
- Categoria  
- Valor  

#### ✅ Consulta e Filtros
- Listagem completa  
- Ordenação por data  
- Filtro por categoria  

#### ✅ Resumo Estatístico
Utilizando Pandas e NumPy:
- Total de despesas  
- Média de gastos  
- Desvio padrão  
- Total por categoria  

#### ✅ Persistência de Dados
Os dados são armazenados em:


---

### 🧠 Conceitos Aplicados

- Estruturas de dados (List, Dict, Tuple, Set)  
- Programação Orientada a Objetos  
- Decoradores  
- Modularização  
- Desenvolvimento Web com Flask  
- Análise de dados com Pandas e NumPy  

---

### 📁 Estrutura do Projeto
```

## 🗂️ Estrutura do Projeto

```text
gestor_despesas/
├─ app.py                # Rotas Flask + lógica da aplicação
├─ models.py             # Classe Despesa (OOP)
├─ utils.py              # Decoradores + validações
├─ requirements.txt      # Dependências
├─ .gitignore            # Ficheiros ignorados pelo Git
│
├─ data/
│  └─ despesas.csv       # Dados (gerado automaticamente)
│
├─ templates/            # HTML (Jinja2)
│  ├─ base.html
│  ├─ index.html
│  └─ resumo.html
│
└─ static/               # CSS e assets
   └─ style.css


```

---

### 🧩 Como Executar

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
http://127.0.0.1:5000

---
### 🧪 Testes Funcionais

✔ Inserir despesas
✔ Filtrar por categoria
✔ Visualizar resumo
✔ Confirmar gravação no CSV


###🚀 Melhorias Futuras

Integração com Base de Dados SQL
Sistema de autenticação
Exportação Excel/PDF
Dashboard com gráficos
Deploy online

---
## 🇬🇧 English

📌 Description

The Expense Manager is a web application built with Python and Flask that allows users to register, manage and analyse personal expenses.

This project was developed as part of an Advanced Python Programming course, applying modern development practices and advanced programming concepts.

---

### 🎯 Goals

Develop web application using Flask
Apply Object-Oriented Programming
Use decorators for validation
Perform data analysis using Pandas and NumPy
Implement modular architecture
Implement data persistence

### ⚙️ Features
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
---

✅ Statistical Summary

Using Pandas and NumPy:
Total expenses
Average spending
Standard deviation
Total per category
---

✅ Data Persistence

Data is stored in:
data/despesas.csv

---
### 🧠 Applied Concepts

Data structures
Object-Oriented Programming
Decorators
Modular architecture
Flask Web Development
Data analysis with Pandas and NumPy

### 🧩 How to Run
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

---
## Open in browser:
http://127.0.0.1:5000

---
## 🧪 Functional Testing
✔ Add expenses
✔ Filter by category
✔ View summary
✔ Verify CSV storage
---

👩‍💻 Author

Palmira Solochi
Curso Técnico de Programação – IEFP
2025-2026


