#!/bin/bash
# Script de automacao da Etapa 2 - Sequencial vs Paralelo;
# Neste caso, o script executa todos os testes necessarios e coleta os tempos medios;
# Isso faz com que a comparacao entre as implementacoes seja feita de forma sistematica;

# Numero de repeticoes de cada teste;
NUM_REPETICOES_=10

# Tamanhos de matrizes a testar (quadradas NxN);
# Neste caso, comecamos com 100 e dobramos ate encontrar tempo >= 3 minutos;
TAMANHOS_=(100 200 400 800)

# Numeros de threads/processos a testar;
# Neste caso, testamos T e P iguais a 2, 4, 8 e 16;
PARALELOS_=(2 4 8 16)

# Arquivo de log com os resultados;
# Isso faz com que todos os tempos sejam gravados para posterior analise;
LOG_="resultados.csv"

# Cria o cabecalho do arquivo de resultados;
echo "tamanho,tipo,param,execucao,tempo_us" > "$LOG_"

echo "=== Iniciando testes - Etapa 2 ==="
echo "Resultados serao salvos em: $LOG_"

# Loop sobre os tamanhos de matrizes;
for TAM_ in "${TAMANHOS_[@]}"; do
    echo ""
    echo "--- Tamanho: ${TAM_}x${TAM_} ---"

    # Gera as matrizes para este tamanho;
    # Neste caso, a matriz e quadrada, entao n1=m1=n2=m2=TAM_;
    echo "Gerando matrizes ${TAM_}x${TAM_}..."
    ./auxiliar "$TAM_" "$TAM_" "$TAM_" "$TAM_"

    # =====================================================
    # Testes com o codigo SEQUENCIAL (10 repeticoes);
    # =====================================================
    echo "Testando sequencial (${NUM_REPETICOES_} repeticoes)..."
    SOMA_SEQ_=0
    for ((exec_=1; exec_<=NUM_REPETICOES_; exec_++)); do
        # Executa a multiplicacao sequencial e captura o tempo do arquivo de saida;
        ./sequencial matrix1.txt matrix2.txt resultado_seq.txt > /dev/null 2>&1
        # Le o tempo da ultima linha do arquivo de resultado;
        # Neste caso, a ultima linha contem o tempo em microsegundos;
        TEMPO_=$(tail -1 resultado_seq.txt)
        echo "${TAM_},sequencial,1,${exec_},${TEMPO_}" >> "$LOG_"
        SOMA_SEQ_=$((SOMA_SEQ_ + TEMPO_))
    done
    MEDIA_SEQ_=$((SOMA_SEQ_ / NUM_REPETICOES_))
    echo "  Sequencial - Media: ${MEDIA_SEQ_} us"

    # Verifica se o tempo sequencial e de pelo menos 3 minutos (180000000 us);
    # Neste caso, se o tempo for suficiente, exibe aviso;
    if [ "$MEDIA_SEQ_" -ge 180000000 ]; then
        echo "  [OK] Tempo sequencial >= 3 minutos para ${TAM_}x${TAM_}!"
    fi

    # =====================================================
    # Testes com o codigo PARALELO THREADS;
    # =====================================================
    for T_ in "${PARALELOS_[@]}"; do
        echo "Testando threads T=${T_} (${NUM_REPETICOES_} repeticoes)..."
        SOMA_THR_=0
        for ((exec_=1; exec_<=NUM_REPETICOES_; exec_++)); do
            # Executa a multiplicacao com T threads;
            ./paralelo_threads matrix1.txt matrix2.txt resultado_thr_t${T_} "$T_" > /dev/null 2>&1

            # Encontra o maior tempo entre os arquivos de cada thread;
            # Neste caso, o tempo total e o da thread mais lenta;
            TEMPO_MAX_=0
            for ((t_=0; t_<T_; t_++)); do
                ARQUIVO_="resultado_thr_t${T_}_thread${t_}.txt"
                if [ -f "$ARQUIVO_" ]; then
                    TEMPO_T_=$(tail -1 "$ARQUIVO_")
                    if [ "$TEMPO_T_" -gt "$TEMPO_MAX_" ]; then
                        TEMPO_MAX_="$TEMPO_T_"
                    fi
                fi
            done

            echo "${TAM_},threads,${T_},${exec_},${TEMPO_MAX_}" >> "$LOG_"
            SOMA_THR_=$((SOMA_THR_ + TEMPO_MAX_))
        done
        MEDIA_THR_=$((SOMA_THR_ / NUM_REPETICOES_))
        echo "  Threads T=${T_} - Media: ${MEDIA_THR_} us"
    done

    # =====================================================
    # Testes com o codigo PARALELO PROCESSOS;
    # =====================================================
    for P_ in "${PARALELOS_[@]}"; do
        echo "Testando processos P=${P_} (${NUM_REPETICOES_} repeticoes)..."
        SOMA_PROC_=0
        for ((exec_=1; exec_<=NUM_REPETICOES_; exec_++)); do
            # Executa a multiplicacao com P processos;
            ./paralelo_processos matrix1.txt matrix2.txt resultado_proc_p${P_} "$P_" > /dev/null 2>&1

            # Encontra o maior tempo entre os arquivos de cada processo filho;
            # Isso faz com que o tempo total seja o do processo mais lento;
            TEMPO_MAX_=0
            for ((p_=0; p_<P_; p_++)); do
                ARQUIVO_="resultado_proc_p${P_}_processo${p_}.txt"
                if [ -f "$ARQUIVO_" ]; then
                    TEMPO_P_=$(tail -1 "$ARQUIVO_")
                    if [ "$TEMPO_P_" -gt "$TEMPO_MAX_" ]; then
                        TEMPO_MAX_="$TEMPO_P_"
                    fi
                fi
            done

            echo "${TAM_},processos,${P_},${exec_},${TEMPO_MAX_}" >> "$LOG_"
            SOMA_PROC_=$((SOMA_PROC_ + TEMPO_MAX_))
        done
        MEDIA_PROC_=$((SOMA_PROC_ / NUM_REPETICOES_))
        echo "  Processos P=${P_} - Media: ${MEDIA_PROC_} us"
    done

done

echo ""
echo "=== Testes concluidos ==="
echo "Dados salvos em: $LOG_"
echo "Use o script gerar_graficos.py para visualizar os resultados."
