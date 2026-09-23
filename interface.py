import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from funcoes import extrair_livros, salvar_dados, carregar_dados, comparar_precos, filtrar_por_preco, ordenar_por_preco, salvar_csv, mostrar_grafico

janela = tk.Tk()
janela.title("Bot de Preços")
janela.geometry("600x400")

def acao_extrair():
    livros = extrair_livros()
    salvar_dados(livros)
    resultado.delete(1.0, tk.END)
    resultado.insert(tk.END, f"{len(livros)} livros extraídos e salvos!\n")

def acao_comparar():
    antigos = carregar_dados()
    novos = extrair_livros()
    
    resultado.delete(1.0, tk.END)
    
    if antigos:
        resultados = comparar_precos(antigos["livros"], novos)
        
        if resultados:
            for linha in resultados:
                resultado.insert(tk.END, linha + "\n")
        else:
            resultado.insert(tk.END, "Nenhuma mudança de preço!\n")
    else:
        resultado.insert(tk.END, "Sem dados antigos!\n")

def acao_estatisticas():
    livros = extrair_livros()
    resultado.delete(1.0, tk.END)

    if livros:
        mais_caro = max(livros, key=lambda x: x["preco"]) 
        mais_barato = min(livros, key=lambda x: x["preco"]) 
        precos = [livro["preco"] for livro in livros]
        media = sum(precos) / len(precos)

        resultado.insert(tk.END, f"Total: {len(livros)} livros\n")
        resultado.insert(tk.END, f"Mais caro: {mais_caro['titulo']} - {mais_caro['preco']}\n")
        resultado.insert(tk.END, f"Mais barato: {mais_barato['titulo']} - {mais_barato['preco']}\n")
        resultado.insert(tk.END, f"Média: £{media:.2f}\n")

def acao_mostrar_grafico():
    mostrar_grafico()

def acao_ordenar():
    livros = extrair_livros()
    
    ordem = simpledialog.askinteger("Ordenar", "1. Mais barato\n2. Mais caro")
    
    if ordem == 1:
        ordenados = ordenar_por_preco(livros)
    else:
        ordenados = ordenar_por_preco(livros, decrescente=True)
    
    resultado.delete(1.0, tk.END)
    for livro in ordenados:
        resultado.insert(tk.END, f"{livro['titulo']} - £{livro['preco']}\n")

def acao_filtrar():
    livros = extrair_livros()
    maximo = simpledialog.askfloat("Filtrar", "Preço máximo (£):")

    if maximo is None:
        return

    filtrados = filtrar_por_preco(livros, maximo)
    resultado.delete(1.0, tk.END)
    resultado.insert(tk.END, f"{len(filtrados)} livros abaixo de £{maximo}\n")

    for livro in filtrados:
        resultado.insert(tk.END, f"{livro['titulo']} - £{livro['preco']}\n")
    
def acao_salvar_csv():
    livros = extrair_livros()
    salvar_csv(livros)
    resultado.delete(1.0, tk.END)
    resultado.insert(tk.END, "Salvo em livros.csv!\n")

def acao_ver_historico():
    try:
        with open("historico.json", "r") as file:
            historico = json.load(file)
    except FileNotFoundError:
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "Sem histórico!\n")
        return

    resultado.delete(1.0, tk.END)
    resultado.insert(tk.END, f"===== HISTÓRICO ({len(historico)} execuções) =====\n")

    for i, execucao in enumerate(historico, start=1):
        data = execucao["data"]
        total = len(execucao["livros"])
        resultado.insert(tk.END, f"{i}. {data} - {total} livros\n")

def acao_sair():
    resposta = messagebox.askyesno("Sair", "Tem certeza?")
    if resposta:
        janela.destroy()

botao_extrair = tk.Button(janela, text="Extrair e Salvar", width=30, command=acao_extrair)
botao_extrair.pack(pady=5)

botao_comparar = tk.Button(janela, text="Comparar", width=30, command=acao_comparar)
botao_comparar.pack(pady=5)

botao_estatisticas = tk.Button(janela, text="Estatisticas", width=30, command=acao_estatisticas)
botao_estatisticas.pack(pady=5)

botao_mostrar_grafico = tk.Button(janela, text="Gráfico da evolução dos preços", width=30, command=acao_mostrar_grafico)
botao_mostrar_grafico.pack(pady=5)

botao_ordenar = tk.Button(janela, text="Ordenar", width=30, command=acao_ordenar)
botao_ordenar.pack(pady=5)

botao_filtrar = tk.Button(janela,text="Filtra", width=30, command=acao_filtrar)
botao_filtrar.pack(pady=5)

botao_salvar_csv = tk.Button(janela,text="Salvar CSV", width=30, command=acao_salvar_csv)
botao_salvar_csv.pack(pady=5)

botao_ver_historico = tk.Button(janela,text="Ver histórico", width=30, command=acao_ver_historico)
botao_ver_historico.pack(pady=5)

botao_sair = tk.Button(janela, text="Sair", width=30, command=acao_sair)
botao_sair.pack(pady=5)

resultado = tk.Text(janela, height=15, width=70)
resultado.pack(pady=10)


janela.mainloop()