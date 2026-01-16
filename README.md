# Biblioteca Online

Projeto Fullstack feito com **Flask, SQLite, HTML, CSS e JavaScript puro**.  
Permite visualizar livros, consultar preços médios, redirecionar para lojas online e pedir livros emprestados entre usuários.

---

## Funcionalidades

- Cadastro e login de usuários  
- Catálogo de livros com filtros por gênero e preço  
- Redirecionamento para compra em lojas (Amazon, Mercado Livro, etc.)  
- Sistema de empréstimos entre usuários  
- Avaliações e histórico de livros emprestados

---

## Estrutura do Projeto
Biblioteca/
    ├── app.py
    ├── database.db
    ├── requirements.txt 
    ├── .git/ 
    ├── .gitignore 
    ├── .env 
    ├── static/ 
    │   ├── css/ 
    │   ├── js/ 
    │   └── img/ 
    └── templates/

---

## Como Rodar

1. Criar e ativar um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Rodar o servidor Flask:

```bash
python app.py
```

4. Acessar no navegador:

```
http://127.0.0.1:5000/
```

# Observações

- Certifique-se de ter o .env configurado com SECRET_KEY e DATABASE_URL
- Banco SQLite é usado apenas para desenvolvimento
