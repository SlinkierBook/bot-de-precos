# Bot de Preços

## O que é

Um bot que monitora preços de livros automaticamente. Ele acessa o site `books.toscrape.com`, extrai os dados de todos os livros, salva o histórico e avisa por email quando algum preço baixa.

## Como funciona

O bot tem três partes principais:

1. **Scraping** — usa `requests` e `BeautifulSoup` pra baixar e extrair os dados do site.
2. **Armazenamento** — salva cada execução em `historico.json`, guardando a data e os preços.
3. **Notificação** — quando um preço baixa, envia email automaticamente.

## Funcionalidades

- **Extrair livros** — raspa todos os livros do site
- **Extrair por categoria** — filtra por categoria específica
- **Histórico** — salva cada execução em JSON
- **Comparar preços** — mostra o que subiu e o que baixou
- **Estatísticas** — mais caro, mais barato, média
- **Ordenar** — por preço crescente ou decrescente
- **Filtrar** — por preço máximo
- **Exportar CSV** — pra abrir no Excel
- **Gráfico** — evolução dos preços
- **Enviar email** — avisa quando um preço baixa
- **Agendador** — roda automaticamente
- **Interface gráfica** — feita com Tkinter

## Tecnologias

- Python 3.14
- requests
- BeautifulSoup4
- Tkinter
- matplotlib
- smtplib
- python-dotenv
- schedule

## Como instalar

pip install requests beautifulsoup4 matplotlib python-dotenv schedule

## Como configurar

1. Crie um arquivo `.env` na raiz do projeto
2. Adicione as credenciais:

banana=sua_senha_de_app_aqui

O `banana` é o nome que dei pra variável (nome genérico, por segurança).

## Como usar

Interface gráfica:
python interface.py

Menu no terminal:
python funcoes.py

Agendador:
python agendador.py

## Estrutura do projeto

BOT de precos/
  ├── funcoes.py
  ├── interface.py
  ├── agendador.py
  ├── .gitignore
  └── .env

## Aviso de segurança

O arquivo `.env` contém credenciais e NÃO deve ser enviado ao GitHub.

## Autor

SlinkierBook

## Licença

Este projeto é de uso livre para estudo e portfólio.