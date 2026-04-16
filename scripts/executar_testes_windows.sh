#!/usr/bin/bash
# Script de automacao da Etapa 2 - adaptado para rodar via MSYS2 no Windows;
# Neste caso, o script executa todos os testes e coleta os tempos medios;
# Isso faz com que a comparacao entre as implementacoes seja automatizada;

export PATH="/usr/bin:/c/msys64/mingw64/bin:$PATH"

# Diretorio dos executaveis;
WORK_="/c/Users/gabri/Desktop/sistemaoperacional/trabalho1"
cd "$WORK_"

# Numero de repeticoes de cada teste;
NUM_REP_=10

# Tamanhos de matrizes a testar;
# Neste caso, comecamos com 100x100 e dobramos;
TAMANHOS_=(100 200 400 800)

# Numeros de threads/processos a testar;
PARALELOS_=(2 4 8 16)

# Arquivo CSV de resultados;
LOG_="resultados.csv"
echo "tamanho,tipo,param,execucao,tempo_us" > "$LOG_"

echo "=== Iniciando testes da Etapa 2 ==="
echo "Resultados: $LOG_"

for TAM_ in "${TAMANHOS_[@]}"; do
    echo ""
    echo "--- Tamanho: ${TAM_}x${TAM_} ---"

    # Gera as matrizes para este tamanho;
    echo "Gerando matrizes ${TAM_}x${TAM_}..."
    ./auxiliar.exe "$TAM_" "$TAM_" "$TAM_" "$TAM_" > /dev/null

    # === SEQUENCIAL ===
    echo "  Sequencial..."
    SOMA_=0
    for ((e_=1; e_<=NUM_REP_; e_++)); do
        ./sequencial.exe matrix1.txt matrix2.txt _res_seq.txt > /dev/null 2>&1
        T_=$(tail -1 _res_seq.txt)
        echo "${TAM_},sequencial,1,${e_},${T_}" >> "$LOG_"
        SOMA_=$((SOMA_ + T_))
    done
    MEDIA_=$((SOMA_ / NUM_REP_))
    echo "    Media: ${MEDIA_} us  ($(echo "scale=2; $MEDIA_/1000000" | bc) s)"

    if [ "$MEDIA_" -ge 180000000 ]; then
        echo "    [OK] >= 3 minutos - tamanho limite para Etapa 2!"
    fi

    # === THREADS ===
    for T_ in "${PARALELOS_[@]}"; do
        echo "  Threads T=${T_}..."
        SOMA_=0
        for ((e_=1; e_<=NUM_REP_; e_++)); do
            ./paralelo_threads.exe matrix1.txt matrix2.txt _res_thr_t${T_} "$T_" > /dev/null 2>&1
            TMAX_=0
            for ((t_=0; t_<T_; t_++)); do
                F_="_res_thr_t${T_}_thread${t_}.txt"
                [ -f "$F_" ] && TV_=$(tail -1 "$F_") && [ "$TV_" -gt "$TMAX_" ] && TMAX_="$TV_"
            done
            echo "${TAM_},threads,${T_},${e_},${TMAX_}" >> "$LOG_"
            SOMA_=$((SOMA_ + TMAX_))
        done
        MEDIA_=$((SOMA_ / NUM_REP_))
        echo "    T=${T_} Media: ${MEDIA_} us"
    done

    # === PROCESSOS ===
    for P_ in "${PARALELOS_[@]}"; do
        echo "  Processos P=${P_}..."
        SOMA_=0
        for ((e_=1; e_<=NUM_REP_; e_++)); do
            ./paralelo_processos.exe matrix1.txt matrix2.txt _res_proc_p${P_} "$P_" > /dev/null 2>&1
            TMAX_=0
            for ((p_=0; p_<P_; p_++)); do
                F_="_res_proc_p${P_}_processo${p_}.txt"
                [ -f "$F_" ] && TV_=$(tail -1 "$F_") && [ "$TV_" -gt "$TMAX_" ] && TMAX_="$TV_"
            done
            echo "${TAM_},processos,${P_},${e_},${TMAX_}" >> "$LOG_"
            SOMA_=$((SOMA_ + TMAX_))
        done
        MEDIA_=$((SOMA_ / NUM_REP_))
        echo "    P=${P_} Media: ${MEDIA_} us"
    done
done

# Limpa arquivos temporarios;
rm -f _res_*.txt

echo ""
echo "=== Testes concluidos! CSV salvo em: $LOG_ ==="
