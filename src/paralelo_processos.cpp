// Programa Paralelo com Processos - Multiplica duas matrizes usando P processos via fork();
// Cada processo filho e responsavel por calcular N1/P linhas da matriz resultado C;
// Neste caso, as matrizes sao lidas dos arquivos ANTES de criar os processos filhos;
// Isso faz com que a leitura seja feita uma unica vez pelo processo pai, que e mais eficiente;

#include <iostream>
#include <fstream>
#include <string>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <cstdlib>
#include <cstring>

// Funcao auxiliar que carrega uma matriz de um arquivo para arrays de dimensoes e dados;
// Neste caso, a funcao aloca dinamicamente o vetor de dados e preenche com os valores lidos;
// Isso faz com que a leitura seja feita de forma centralizada antes do fork;
bool carregarMatriz_(const std::string& nomeArquivo_, int& linhas_, int& colunas_, double*& dados_) {
    std::ifstream arquivo_(nomeArquivo_);
    if (!arquivo_.is_open()) {
        std::cerr << "Erro: nao foi possivel abrir o arquivo: " << nomeArquivo_ << std::endl;
        return false;
    }
    // Le as dimensoes da primeira linha do arquivo;
    arquivo_ >> linhas_ >> colunas_;
    // Aloca o vetor de dados com o tamanho total da matriz;
    dados_ = new double[linhas_ * colunas_];
    // Le todos os elementos linha por linha e coluna por coluna;
    for (int i_ = 0; i_ < linhas_; i_++) {
        for (int j_ = 0; j_ < colunas_; j_++) {
            arquivo_ >> dados_[i_ * colunas_ + j_];
        }
    }
    arquivo_.close();
    return true;
}

// Funcao que realiza a multiplicacao de uma faixa de linhas e salva em arquivo;
// Neste caso, cada processo filho chama esta funcao com sua porcao de linhas;
// Isso faz com que cada processo seja responsavel por sua parte do resultado;
void calcularESalvar_(double* dadosM1_, double* dadosM2_,
                      int colunasM1_, int colunasM2_,
                      int linhaInicio_, int linhaFim_,
                      const std::string& nomeArquivo_, int idProcesso_) {
    // Calcula o numero de linhas que este processo deve calcular;
    int numLinhas_ = linhaFim_ - linhaInicio_;

    // Aloca o vetor de resultado para as linhas deste processo;
    // Neste caso, cada processo tem seu proprio espaco de memoria para o resultado;
    double* dadosC_ = new double[numLinhas_ * colunasM2_];
    // Inicializa o vetor de resultado com zeros;
    memset(dadosC_, 0, numLinhas_ * colunasM2_ * sizeof(double));

    // Registra o tempo de inicio do calculo neste processo;
    // Neste caso, medimos apenas o tempo de multiplicacao, sem contar a leitura;
    struct timeval inicio_, fim_;
    gettimeofday(&inicio_, NULL);

    // Loop que percorre as linhas atribuidas a este processo;
    // Isso faz com que cada processo calcule apenas sua porcao da matriz resultado;
    for (int i_ = linhaInicio_; i_ < linhaFim_; i_++) {
        // Indice local desta linha no vetor resultado deste processo;
        int iLocal_ = i_ - linhaInicio_;
        // Loop sobre as colunas da matriz resultado;
        for (int j_ = 0; j_ < colunasM2_; j_++) {
            // Neste caso, c[i][j] e calculado como produto escalar;
            double soma_ = 0.0;
            // Produto escalar: soma dos produtos a[i][k] * b[k][j];
            for (int k_ = 0; k_ < colunasM1_; k_++) {
                soma_ += dadosM1_[i_ * colunasM1_ + k_] * dadosM2_[k_ * colunasM2_ + j_];
            }
            // Armazena o resultado na posicao local deste processo;
            dadosC_[iLocal_ * colunasM2_ + j_] = soma_;
        }
    }

    // Registra o tempo de fim do calculo;
    gettimeofday(&fim_, NULL);

    // Calcula o tempo total de execucao deste processo em microsegundos;
    // Isso faz com que o tempo individual de cada processo fique registrado no arquivo;
    long long tempoMicros_ = ((long long)fim_.tv_sec  * 1000000 + fim_.tv_usec) -
                             ((long long)inicio_.tv_sec * 1000000 + inicio_.tv_usec);

    // Abre o arquivo de saida exclusivo deste processo;
    // Neste caso, cada processo filho cria seu proprio arquivo de resultado;
    std::ofstream arquivo_(nomeArquivo_);
    if (!arquivo_.is_open()) {
        std::cerr << "Erro ao abrir arquivo de saida do processo " << idProcesso_ << std::endl;
        delete[] dadosC_;
        return;
    }

    // Escreve o cabecalho com as dimensoes da porcao calculada por este processo;
    arquivo_ << numLinhas_ << " " << colunasM2_ << "\n";

    // Escreve os elementos calculados por este processo no formato padrao do trabalho;
    // Neste caso, os indices de linha usados no nome do elemento sao globais (1-indexados);
    // Isso faz com que seja possivel reconstruir a matriz completa a partir dos arquivos;
    for (int i_ = 0; i_ < numLinhas_; i_++) {
        for (int j_ = 0; j_ < colunasM2_; j_++) {
            int linhaGlobal_ = linhaInicio_ + i_ + 1;
            arquivo_ << "c" << linhaGlobal_ << (j_ + 1) << " "
                     << dadosC_[i_ * colunasM2_ + j_] << "\n";
        }
    }
    // Escreve o tempo de execucao deste processo ao final do arquivo;
    arquivo_ << tempoMicros_ << "\n";
    arquivo_.close();

    std::cout << "[Processo " << idProcesso_ << " PID=" << getpid()
              << "] Concluido. Tempo: " << tempoMicros_ << " us. Arquivo: " << nomeArquivo_ << std::endl;

    // Libera o vetor de resultado deste processo;
    delete[] dadosC_;
}

int main(int argc, char* argv[]) {
    // Verifica se os argumentos necessarios foram fornecidos;
    // Neste caso, sao necessarios: arquivo_m1, arquivo_m2, prefixo_saida e numero_processos;
    if (argc != 5) {
        std::cerr << "Uso: " << argv[0] << " arquivo_m1 arquivo_m2 prefixo_saida P" << std::endl;
        return 1;
    }

    // Argumentos da linha de comando;
    std::string arquivoM1_(argv[1]);
    std::string arquivoM2_(argv[2]);
    std::string prefixoSaida_(argv[3]);
    // Numero de processos filhos a serem criados;
    int numProcessos_ = std::atoi(argv[4]);

    if (numProcessos_ <= 0) {
        std::cerr << "Erro: o numero de processos deve ser maior que zero." << std::endl;
        return 1;
    }

    // Variaveis para armazenar as dimensoes e dados das matrizes;
    int linhasM1_ = 0, colunasM1_ = 0;
    int linhasM2_ = 0, colunasM2_ = 0;
    double* dadosM1_ = nullptr;
    double* dadosM2_ = nullptr;

    std::cout << "Lendo matriz M1 de: " << arquivoM1_ << std::endl;
    // Leitura da primeira matriz ANTES de criar os processos filhos;
    // Neste caso, o pai le o arquivo e os filhos herdam os dados via fork (copy-on-write);
    if (!carregarMatriz_(arquivoM1_, linhasM1_, colunasM1_, dadosM1_)) {
        return 1;
    }

    std::cout << "Lendo matriz M2 de: " << arquivoM2_ << std::endl;
    // Leitura da segunda matriz ANTES de criar os processos filhos;
    // Isso faz com que ambas as matrizes estejam em memoria antes do fork;
    if (!carregarMatriz_(arquivoM2_, linhasM2_, colunasM2_, dadosM2_)) {
        delete[] dadosM1_;
        return 1;
    }

    // Valida a compatibilidade das dimensoes para multiplicacao;
    // Neste caso, colunasM1 deve ser igual a linhasM2;
    if (colunasM1_ != linhasM2_) {
        std::cerr << "Erro: dimensoes incompativeis. colunasM1=" << colunasM1_
                  << " linhasM2=" << linhasM2_ << std::endl;
        delete[] dadosM1_;
        delete[] dadosM2_;
        return 1;
    }

    std::cout << "M1: " << linhasM1_ << "x" << colunasM1_
              << " | M2: " << linhasM2_ << "x" << colunasM2_ << std::endl;
    std::cout << "Criando " << numProcessos_ << " processos filhos..." << std::endl;

    // Calcula quantas linhas cada processo filho deve calcular;
    // Neste caso, as linhas sao divididas igualmente entre os processos;
    int linhasPorProcesso_ = linhasM1_ / numProcessos_;
    // O resto da divisao e distribuido para os primeiros processos;
    int resto_             = linhasM1_ % numProcessos_;

    // Array para armazenar os PIDs dos processos filhos criados;
    pid_t* pids_ = new pid_t[numProcessos_];

    int linhaAtual_ = 0;
    // Loop que cria cada um dos P processos filhos;
    for (int p_ = 0; p_ < numProcessos_; p_++) {
        // Calcula o inicio e fim da faixa de linhas deste processo;
        // Neste caso, processos com indice menor ao resto recebem uma linha extra;
        int linhaInicio_ = linhaAtual_;
        int linhaFim_    = linhaAtual_ + linhasPorProcesso_ + (p_ < resto_ ? 1 : 0);
        linhaAtual_      = linhaFim_;

        // Monta o nome do arquivo de saida deste processo;
        std::string nomeArquivo_ = prefixoSaida_ + "_processo" + std::to_string(p_) + ".txt";

        // Cria o processo filho via fork();
        // Isso faz com que o filho herde toda a memoria do pai, incluindo as matrizes carregadas;
        pid_t pid_ = fork();

        if (pid_ < 0) {
            // Neste caso, o fork falhou e o programa encerra com erro;
            std::cerr << "Erro ao criar processo filho " << p_ << std::endl;
            pids_[p_] = -1;
        } else if (pid_ == 0) {
            // Este bloco e executado APENAS pelo processo filho;
            // Neste caso, o filho calcula sua porcao e salva no arquivo;
            // Isso faz com que o filho termine logo apos completar seu calculo;
            calcularESalvar_(dadosM1_, dadosM2_,
                             colunasM1_, colunasM2_,
                             linhaInicio_, linhaFim_,
                             nomeArquivo_, p_);
            // O processo filho libera sua memoria e encerra;
            delete[] dadosM1_;
            delete[] dadosM2_;
            delete[] pids_;
            exit(0);
        } else {
            // Este bloco e executado APENAS pelo processo pai;
            // Neste caso, o pai armazena o PID do filho criado;
            pids_[p_] = pid_;
            std::cout << "Processo filho " << p_ << " criado com PID=" << pid_
                      << " (linhas " << linhaInicio_ << " a " << (linhaFim_ - 1) << ")" << std::endl;
        }
    }

    // O processo pai aguarda o termino de todos os processos filhos;
    // Neste caso, o pai usa wait() para sincronizar com cada filho;
    // Isso faz com que o pai saiba quando todos os calculos foram concluidos;
    std::cout << "Aguardando conclusao de todos os processos..." << std::endl;
    for (int p_ = 0; p_ < numProcessos_; p_++) {
        if (pids_[p_] > 0) {
            // Aguarda o processo filho com o PID armazenado;
            waitpid(pids_[p_], NULL, 0);
        }
    }

    std::cout << "Todos os processos finalizaram." << std::endl;
    std::cout << "Para o tempo total, use o maior tempo entre os arquivos gerados." << std::endl;
    std::cout << "Arquivos gerados com prefixo: " << prefixoSaida_ << std::endl;

    // Libera a memoria alocada pelo processo pai;
    delete[] dadosM1_;
    delete[] dadosM2_;
    delete[] pids_;

    return 0;
}
