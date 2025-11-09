import pandas as pd
import re
import matplotlib.pyplot as plt
import os

# ======= CONFIGURAÇÃO =======
arquivos = {
    "Round Robin": "logs_roundrobin.txt",
    "Least Conn": "logs_leastconn.txt",
    "IP Hash": "logs_iphash.txt"
}

# ======= FUNÇÃO DE PARSE =======
def carregar_logs(arquivo):
    linhas = []
    regex = re.compile(r'upstream_addr=(\S+).*request_time=(\S+)')
    with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
        for linha in f:
            if "GET /" not in linha:  # ignora mensagens de inicialização
                continue
            match = regex.search(linha)
            if match:
                servidor = match.group(1).split(":")[0]
                tempo = float(match.group(2))
                linhas.append((servidor, tempo))
    if not linhas:
        print(f"[⚠️] Nenhum dado válido encontrado em {arquivo}")
        return pd.DataFrame(columns=["servidor", "tempo"])
    df = pd.DataFrame(linhas, columns=["servidor", "tempo"])
    return df

# ======= GERAÇÃO DE GRÁFICOS =======
os.makedirs("graficos", exist_ok=True)

for nome, arquivo in arquivos.items():
    if not os.path.exists(arquivo):
        print(f"[!] Arquivo {arquivo} não encontrado, pulando...")
        continue

    df = carregar_logs(arquivo)
    if df.empty:
        continue

    # Estatísticas básicas
    resumo = df.groupby("servidor")["tempo"].agg(["count", "mean"]).reset_index()
    resumo["mean_ms"] = resumo["mean"] * 1000  # converte p/ milissegundos
    print(f"\n=== {nome} ===")
    print(resumo[["servidor", "count", "mean_ms"]].to_string(index=False))

    # Gráfico 1 – Tempo médio por servidor
    plt.figure(figsize=(6,4))
    plt.bar(resumo["servidor"], resumo["mean_ms"], color="steelblue")
    plt.title(f"Tempo médio por servidor – {nome}")
    plt.ylabel("Tempo médio (ms)")
    plt.xlabel("Servidor")
    plt.tight_layout()
    plt.savefig(f"graficos/tempo_medio_{nome.replace(' ', '_').lower()}.png")

    # Gráfico 2 – Distribuição de requisições
    plt.figure(figsize=(6,4))
    plt.bar(resumo["servidor"], resumo["count"], color="orange")
    plt.title(f"Distribuição de requisições – {nome}")
    plt.ylabel("Quantidade de requisições")
    plt.xlabel("Servidor")
    plt.tight_layout()
    plt.savefig(f"graficos/distribuicao_{nome.replace(' ', '_').lower()}.png")

print("\n✅ Gráficos salvos na pasta 'graficos/'.")
print("Use esses arquivos nas seções de resultados do relatório (comparando os 3 algoritmos).")
