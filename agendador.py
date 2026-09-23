import schedule
import time
from funcoes import extrair_livros, salvar_dados

def tarefa():
    livros = extrair_livros()
    salvar_dados(livros)

schedule.every().day.at("10:00").do(tarefa)

while True:
    schedule.run_pending()
    time.sleep(1)