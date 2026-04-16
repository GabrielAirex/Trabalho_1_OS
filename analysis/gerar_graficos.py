#!/usr/bin/env python3
# Script para gerar os graficos da Etapa 3 a partir dos dados coletados;
# Neste caso, lemos o CSV de resultados e geramos um grafico por tamanho de matriz;
# Isso faz com que a comparacao visual entre as implementacoes seja facilitada;

import csv
import matplotlib.pyplot as plt
from collections import defaultdict

# Nome do arquivo CSV com os resultados;
ARQUIVO_CSV_ = "resultados.csv"

# Dicionario para armazenar os tempos medios por (tamanho, tipo, param);
# Neste caso, a estrutura permite agrupar facilmente os resultados;
dados_ = defaultdict(list)

# Le o arquivo CSV e agrupa os tempos;
print(f"Lendo dados de: {ARQUIVO_CSV_}")
with open(ARQUIVO_CSV_, "r") as f_:
    reader_ = csv.DictReader(f_)
    for linha_ in reader_:
        chave_ = (int(linha_["tamanho"]), linha_["tipo"], int(linha_["param"]))
        dados_[chave_].append(int(linha_["tempo_us"]))

# Calcula a media dos tempos para cada configuracao;
# Isso faz com que os graficos mostrem o valor medio de 10 execucoes;
medias_ = {}
for chave_, tempos_ in dados_.items():
    medias_[chave_] = sum(tempos_) / len(tempos_)

# Encontra todos os tamanhos distintos;
tamanhos_ = sorted(set(chave_[0] for chave_ in medias_))
print(f"Tamanhos encontrados: {tamanhos_}")

# Numeros de threads/processos testados;
paralelos_ = [2, 4, 8, 16]

# Gera um grafico para cada tamanho de matriz;
# Neste caso, cada grafico mostra sequencial, threads e processos no mesmo eixo;
for tam_ in tamanhos_:
    fig_, ax_ = plt.subplots(figsize=(10, 6))

    # Eixo X: numero de threads/processos;
    x_ = paralelos_

    # Tempo sequencial (constante para todos os valores de T e P);
    # Neste caso, exibimos o sequencial em todos os pontos para facilitar a comparacao;
    tempo_seq_ = medias_.get((tam_, "sequencial", 1), None)
    if tempo_seq_ is not None:
        # Converte de microsegundos para segundos para melhor leitura;
        tempo_seq_s_ = tempo_seq_ / 1_000_000
        ax_.plot(x_, [tempo_seq_s_] * len(x_),
                 label="Sequencial", marker="o", linestyle="--",
                 color="blue", linewidth=2)

    # Tempos com threads para cada valor de T;
    tempos_thr_ = []
    for t_ in paralelos_:
        val_ = medias_.get((tam_, "threads", t_), None)
        tempos_thr_.append(val_ / 1_000_000 if val_ is not None else None)
    ax_.plot(x_, tempos_thr_,
             label="Threads", marker="s", linestyle="-",
             color="orange", linewidth=2)

    # Tempos com processos para cada valor de P;
    tempos_proc_ = []
    for p_ in paralelos_:
        val_ = medias_.get((tam_, "processos", p_), None)
        tempos_proc_.append(val_ / 1_000_000 if val_ is not None else None)
    ax_.plot(x_, tempos_proc_,
             label="Processos", marker="^", linestyle="-",
             color="green", linewidth=2)

    # Configuracoes do grafico;
    ax_.set_title(f"Tempo Medio de Execucao - Matriz {tam_}x{tam_}", fontsize=14)
    ax_.set_xlabel("Numero de Threads ou Processos", fontsize=12)
    ax_.set_ylabel("Tempo (segundos)", fontsize=12)
    ax_.set_xticks(x_)
    ax_.legend(fontsize=11)
    ax_.grid(True, linestyle="--", alpha=0.5)

    # Salva o grafico como imagem PNG;
    nome_arquivo_ = f"grafico_{tam_}x{tam_}.png"
    plt.tight_layout()
    plt.savefig(nome_arquivo_, dpi=150)
    print(f"Grafico salvo: {nome_arquivo_}")
    plt.close()

print("Todos os graficos foram gerados.")
