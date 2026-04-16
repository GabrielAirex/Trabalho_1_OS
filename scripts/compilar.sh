#!/bin/bash
# Script de compilacao dos 4 programas do Trabalho 1;
# Neste caso, cada programa e compilado separadamente com g++;
# Isso faz com que qualquer erro de compilacao seja identificado facilmente;

echo "=== Compilando Trabalho 1 - Processos e Threads ==="

# Compila o programa auxiliar;
echo "Compilando auxiliar.cpp..."
g++ -O2 -Wall -std=c++11 -o auxiliar auxiliar.cpp
if [ $? -eq 0 ]; then
    echo "  [OK] auxiliar compilado com sucesso."
else
    echo "  [ERRO] Falha ao compilar auxiliar."
    exit 1
fi

# Compila o programa sequencial;
echo "Compilando sequencial.cpp..."
g++ -O2 -Wall -std=c++11 -o sequencial sequencial.cpp
if [ $? -eq 0 ]; then
    echo "  [OK] sequencial compilado com sucesso."
else
    echo "  [ERRO] Falha ao compilar sequencial."
    exit 1
fi

# Compila o programa paralelo com threads;
# Neste caso, e necessario linkar a biblioteca pthread (-lpthread);
echo "Compilando paralelo_threads.cpp..."
g++ -O2 -Wall -std=c++11 -o paralelo_threads paralelo_threads.cpp -lpthread
if [ $? -eq 0 ]; then
    echo "  [OK] paralelo_threads compilado com sucesso."
else
    echo "  [ERRO] Falha ao compilar paralelo_threads."
    exit 1
fi

# Compila o programa paralelo com processos;
echo "Compilando paralelo_processos.cpp..."
g++ -O2 -Wall -std=c++11 -o paralelo_processos paralelo_processos.cpp
if [ $? -eq 0 ]; then
    echo "  [OK] paralelo_processos compilado com sucesso."
else
    echo "  [ERRO] Falha ao compilar paralelo_processos."
    exit 1
fi

echo ""
echo "=== Todos os programas compilados com sucesso! ==="
echo ""
echo "Para executar um teste rapido:"
echo "  ./auxiliar 100 100 100 100"
echo "  ./sequencial matrix1.txt matrix2.txt resultado_seq.txt"
echo "  ./paralelo_threads matrix1.txt matrix2.txt resultado_thr 4"
echo "  ./paralelo_processos matrix1.txt matrix2.txt resultado_proc 4"
echo ""
echo "Para executar todos os testes da Etapa 2:"
echo "  chmod +x executar_testes.sh && ./executar_testes.sh"
