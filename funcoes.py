from email.message import EmailMessage
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import smtplib
import json
import datetime
import csv
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def extrair_livros():
    url = ("https://books.toscrape.com/")
    resposta = requests.get(url)
    resposta.encoding = "utf-8"
    soup = BeautifulSoup(resposta.text, "html.parser")

    livros = soup.find_all("article", class_="product_pod")

    lista = []
    for livro in livros:
        titulo = livro.h3.a.get("title")
        preco_texto = livro.find("p", class_="price_color").text
        preco = float(preco_texto.replace("£",""))
        lista.append({"titulo": titulo, "preco": preco})

    return lista

def extrair_por_categoria(categoria):
    url = f"https://books.toscrape.com/catalogue/category/books/{categoria}/index.html"

    resposta = requests.get(url)
    resposta.encoding = "utf-8"
    soup = BeautifulSoup(resposta.text, "html.parser")

    livros = soup.find_all("article", class_="product_pod")

    lista = []
    for livro in livros:
        titulo = livro.h3.a.get("title")
        preco_text = livro.find("p", class_="price_color").text
        preco = float(preco_text.replace("£",""))
        lista.append({"titulo": titulo, "preco": preco})

    return lista
                         
def salvar_dados(livros):
    data = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    try:
        with open("historico.json", "r") as file:
            historico = json.load(file)
    except FileNotFoundError:
        historico = []
    
    historico.append({
        "data": data,
        "livros": livros
        })

    with open("historico.json", "w") as file:
        json.dump(historico, file, indent=4)

    print(f"Salvo em {data}!")

def salvar_csv(livros, nome="livros.csv"):
    with open(nome, "w", newline="", encoding="utf-8") as file:
        escritor = csv.writer(file)
        escritor.writerow(["titulo", "preco"])

        for livro in livros:
            escritor.writerow([livro['titulo'], livro['preco']])

    print(f"Salvo em {nome}!")

def carregar_dados():
    try:
        with open("historico.json", "r") as file:
            historico = json.load(file)
        return historico[-1]
    except FileNotFoundError:
        return None

def comparar_precos(antigos, novos):
    resultados = []
    baixaram = []

    for livro_novo in novos:
        for livro_antigo in antigos:
            if livro_novo["titulo"] == livro_antigo["titulo"]:
                if livro_novo["preco"] < livro_antigo["preco"]:
                    resultados.append(f"BAIXOU: {livro_novo['titulo']} - £{livro_antigo['preco']} → £{livro_novo['preco']}")
                    baixaram.append(livro_novo['titulo'])
                elif livro_novo["preco"] > livro_antigo["preco"]:
                    resultados.append(f"SUBIU: {livro_novo['titulo']} - £{livro_antigo['preco']} → £{livro_novo['preco']}")

    if baixaram:
        corpo = "livros que baixaram:\n\n" + "\n".join(baixaram)
        enviar_email("Preços baixaram!", corpo)

    return resultados

def enviar_email(assunto, corpo):
    load_dotenv()
    remetente = "seuemail@gmail.com"
    Guacamole = os.getenv("NANANA")
    destinatario = "seuemail@gmail.com"

    msg= EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario 
    msg.set_content(corpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remetente, Guacamole)
        smtp.send_message(msg)

    print("Email enviado!")

def mostrar_estatisticas(livros):
    if not livros:
        print("Sem livros")
        return

    mais_caro = max(livros, key=lambda x: x["preco"])
    mais_barato = min(livros, key=lambda x: x["preco"])

    precos = [livro['preco'] for livro in livros]
    media = sum(precos) / len(precos)

    print(f"\n===== ESTATÍSTICAS =====")
    print(f"Total de livros: {len(livros)}")
    print(f"Mais caro: {mais_caro['titulo']} - £{mais_caro['preco']}")
    print(f"Mais barato: {mais_barato['titulo']} - £{mais_barato['preco']}")
    print(f"Média: £{media:.2f}")

def mostrar_grafico():
    try:
        with open("historico.json", "r") as file:
            historico = json.load(file)
    except FileNotFoundError:
        print("Sem histórico!")
        return
    precos = []
    datas = []

    for execucao in historico:
        precos.append(execucao["livros"][0]["preco"])
        datas.append(execucao["data"])

    plt.plot(datas, precos, marker="o")
    plt.title("Evolução do Preço")
    plt.xlabel("Data")
    plt.ylabel("Preço (£)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    
def ver_historico():
    try:
        with open("historico.json", "r") as file:
            historico = json.load(file)
    except FileNotFoundError:
        print("Sem histórico!")
        return

    print(f"\n===== HISTÓRICO ({len(historico)} execuções) =====")

    for i, execucao in enumerate(historico, start=1):
        data = execucao["data"]
        total = len(execucao["livros"])
        print(f"{i}. {data} - {total} livros")

def ordenar_por_preco(livro, decrescente=False):
    return sorted(livro, key=lambda x: x["preco"], reverse=decrescente)

def filtrar_por_preco(livros, maximo):
    return [livro for livro in livros if livro['preco'] <= maximo]    

def menu():
    while True:
        print("\n===== BOT DE PREÇOS =====\n")
        print("1. Extrair e salvar")
        print("2. Salvar em csv")
        print("3. Comparar com anterior")
        print("4. Extrair por categoria")
        print("5. Mostrar estatisticas")
        print("6. Ordenar por preço")
        print("7. Filtrar por preço")
        print("8. Ver histórico")
        print("9. Mostrar gráfico")
        print("10. Sair")
        
        escolha = input("\nEscolha: ")
        
        if escolha == "1":
            livros = extrair_livros()
            salvar_dados(livros)
        
        elif escolha == "2":
            livros = extrair_livros()
            salvar_csv(livros)
        
        elif escolha == "3":
            antigos = carregar_dados()
            novos = extrair_livros()
            
            if antigos:
                comparar_precos(antigos["livros"], novos)
            else:
                print("Sem dados antigos!")
        
        elif escolha == "4":
            categoria = input("Categoria (ex: travel_2): ")
            livros = extrair_por_categoria(categoria)
            
            if livros:
                print(f"\n{len(livros)} livros encontrados")
                for livro in livros:
                    print(f"{livro['titulo']} - £{livro['preco']}")
            else:
                print("Categoria não encontrada!")
        
        elif escolha == "5":
            livros = extrair_livros()
            mostrar_estatisticas(livros)
        
        elif escolha == "6":
            livros = extrair_livros()
            print("\n1. Mais barato primeiro")
            print("2. Mais caro primeiro")
            
            ordem = input("Escolha: ")
            
            if ordem == "1":
                ordenados = ordenar_por_preco(livros)
            else:
                ordenados = ordenar_por_preco(livros, decrescente=True)
            
            for livro in ordenados:
                print(f"{livro['titulo']} - £{livro['preco']}")
        
        elif escolha == "7":
            livros = extrair_livros()
            maximo = float(input("Preço máximo (£): "))
            filtrados = filtrar_por_preco(livros, maximo)
            
            print(f"{len(filtrados)} livros abaixo de £{maximo}")
            
            for livro in filtrados:
                print(f"{livro['titulo']} - £{livro['preco']}")
        
        elif escolha == "8":
            ver_historico()
        
        elif escolha == "9":
            mostrar_grafico()
        
        elif escolha == "10":
            print("Saindo...")
            break

if __name__ == "__main__":
    menu()