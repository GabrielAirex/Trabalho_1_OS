// Programa Paralelo com Threads - Multiplica duas matrizes usando T threads POSIX;
// Cada thread e responsavel por calcular N1/T linhas da matriz resultado C;
// Neste caso, as matrizes sao lidas dos arquivos ANTES de criar as threads;
// Isso faz com que a leitura seja feita de forma sequencial e segura no processo principal;

#include <iostream>
#include <fstream>
#include <string>
#include <pthread.h>
#include <sys/time.h>
#include <cstdlib>

// Estrutura que armazena os dados necessarios para cada thread realizar seu calculo;
// Neste caso, cada thread recebe ponteiros para as matrizes e sua faixa de linhas;
struct DadosThread_ {
    // Ponteiro para os dados da matriz M1 (somente leitura pela thread);
    double* dadosM1_;
    // Ponteiro para os dados da matriz M2 (somente leitura pela thread);
    double* dadosM2_;
    // Ponteiro para os dados da matriz resultado C (escrita pela thread);
    double* dadosC_;
    // Dimensoes das matrizes;
    int linhasM1_;
    int colunasM1_;
    int colunasM2_;
    // Faixa de linhas que esta thread deve calcular (inicio inclusivo, fim exclusivo);
    int linhaInicio_;
    int linhaFim_;
    // Identificador da thread para nomear o arquivo de saida;
    int idThread_;
    // Prefixo do arquivo de saida desta thread;
    std::string prefixoArquivo_;
    // Tempo de execucao desta thread em microsegundos (preenchido pela propria thread);
    long long tempoMicros_;
};

// Funcao executada por cada thread para calcular sua porcao da matriz resultado;
// Neste caso, a thread calcula apenas as linhas no intervalo [linhaInicio_, linhaFim_);
// Isso faz com que o trabalho seja dividido igualmente entre todas as threads;
void* funcaoThread_(void* arg_) {
    // Recupera os dados passados para esta thread;
    DadosThread_* dados_ = (DadosThread_*)arg_;

    // Registra o tempo de inicio desta thread especificamente;
    // Neste caso, o tempo e medido apenas para a parte de calculo desta thread;
    struct timeval inicio_, fim_;
    gettimeofday(&inicio_, NULL);

    // Loop que percorre apenas as linhas atribuidas a esta thread;
    // Isso faz com que cada thread trabalhe em uma secao independente da matriz resultado;
    for (int i_ = dados_->linhaInicio_; i_ < dados_->linhaFim_; i_++) {
        // Loop sobre as colunas da matriz resultado;
        for (int j_ = 0; j_ < dados_->colunasM2_; j_++) {
            // Neste caso, calcula-se o elemento c[i][j] como produto escalar;
            double soma_ = 0.0;
            // Produto escalar entre a linha i de M1 e a coluna j de M2;
            for (int k_ = 0; k_ < dados_->colunasM1_; k_++) {
                soma_ += dados_->dadosM1_[i_ * dados_->colunasM1_ + k_]
                       * dados_->dadosM2_[k_ * dados_->colunasM2_ + j_];
            }
            // Atribui o resultado ao elemento correspondente na matriz C;
            dados_->dadosC_[i_ * dados_->colunasM2_ + j_] = soma_;
        }
    }

    // Registra o tempo de fim desta thread;
    gettimeofday(&fim_, NULL);

    // Calcula o tempo de execucao desta thread em microsegundos;
    // Isso faz com que o tempo individual de cada thread fique registrado;
    dados_->tempoMicros_ = ((long long)fim_.tv_sec  * 1000000 + fim_.tv_usec) -
                           ((long long)inicio_.tv_sec * 1000000 + inicio_.tv_usec);

    // Monta o nome do arquivo de saida para esta thread;
    // Neste caso, cada thread gera seu proprio arquivo com sua porcao do resultado;
    std::string nomeArquivo_ = dados_->prefixoArquivo_ + "_thread" +
                               std::to_string(dados_->idThread_) + ".txt";

    // Abre o arquivo de saida para esta thread;
    std::ofstream arquivo_(nomeArquivo_);
    if (!arquivo_.is_open()) {
        std::cerr << "Erro ao abrir arquivo de saida da thread " << dados_->idThread_ << std::endl;
        pthread_exit(NULL);
    }

    // Escreve o cabecalho com o numero de linhas desta porcao e o numero de colunas;
    // Neste caso, o numero de linhas e a faixa calculada por esta thread;
    int numLinhas_ = dados_->linhaFim_ - dados_->linhaInicio_;
    arquivo_ << numLinhas_ << " " << dados_->colunasM2_ << "\n";

    // Escreve os elementos calculados por esta thread no formato padrao;
    // Isso faz com que o arquivo siga o mesmo formato da Figura 2 do trabalho;
    for (int i_ = dados_->linhaInicio_; i_ < dados_->linhaFim_; i_++) {
        for (int j_ = 0; j_ < dados_->colunasM2_; j_++) {
            arquivo_ << "c" << (i_ + 1) << (j_ + 1) << " "
                     << dados_->dadosC_[i_ * dados_->colunasM2_ + j_] << "\n";
        }
    }
    // Escreve o tempo de execucao desta thread ao final do arquivo;
    arquivo_ << dados_->tempoMicros_ << "\n";
    arquivo_.close();

    pthread_exit(NULL);
}

// Funcao auxiliar que carrega uma matriz de um arquivo para arrays de dimensoes e dados;
// Neste caso, a funcao aloca dinamicamente o vetor de dados e retorna via ponteiro;
// Isso faz com que a leitura seja centralizada e reutilizavel;
bool carregarMatriz_(const std::string& nomeArquivo_, int& linhas_, int& colunas_, double*& dados_) {
    std::ifstream arquivo_(nomeArquivo_);
    if (!arquivo_.is_open()) {
        std::cerr << "Erro: nao foi possivel abrir o arquivo: " << nomeArquivo_ << std::endl;
        return false;
    }
    // Le as dimensoes da primeira linha do arquivo;
    arquivo_ >> linhas_ >> colunas_;
    // Aloca o vetor de dados com o tamanho necessario;
    dados_ = new double[linhas_ * colunas_];
    // Le todos os elementos da matriz do arquivo;
    for (int i_ = 0; i_ < linhas_; i_++) {
        for (int j_ = 0; j_ < colunas_; j_++) {
            arquivo_ >> dados_[i_ * colunas_ + j_];
        }
    }
    arquivo_.close();
    return true;
}

int main(int argc, char* argv[]) {
    // Verifica se os argumentos necessarios foram fornecidos;
    // Neste caso, sao necessarios: arquivo_m1, arquivo_m2, prefixo_saida e numero_threads;
    if (argc != 5) {
        std::cerr << "Uso: " << argv[0] << " arquivo_m1 arquivo_m2 prefixo_saida T" << std::endl;
        return 1;
    }

    // Argumentos da linha de comando;
    std::string arquivoM1_(argv[1]);
    std::string arquivoM2_(argv[2]);
    std::string prefixoSaida_(argv[3]);
    // Numero de threads a serem criadas;
    int numThreads_ = std::atoi(argv[4]);

    if (numThreads_ <= 0) {
        std::cerr << "Erro: o numero de threads deve ser maior que zero." << std::endl;
        return 1;
    }

    // Variaveis para armazenar as dimensoes e dados das matrizes;
    int linhasM1_ = 0, colunasM1_ = 0;
    int linhasM2_ = 0, colunasM2_ = 0;
    double* dadosM1_ = nullptr;
    double* dadosM2_ = nullptr;

    std::cout << "Lendo matriz M1 de: " << arquivoM1_ << std::endl;
    // Leitura da primeira matriz ANTES de criar as threads;
    // Neste caso, isso garante que os dados estejam prontos antes do paralelismo comecar;
    if (!carregarMatriz_(arquivoM1_, linhasM1_, colunasM1_, dadosM1_)) {
        return 1;
    }

    std::cout << "Lendo matriz M2 de: " << arquivoM2_ << std::endl;
    // Leitura da segunda matriz ANTES de criar as threads;
    // Isso faz com que ambas as matrizes estejam completamente carregadas em memoria;
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

    // Aloca a matriz resultado C compartilhada entre todas as threads;
    // Neste caso, todas as threads escrevem em posicoes distintas desta matriz;
    // Isso faz com que nao haja conflito de escrita entre as threads;
    double* dadosC_ = new double[linhasM1_ * colunasM2_]();

    // Aloca o array de threads e seus respectivos dados;
    pthread_t* threads_ = new pthread_t[numThreads_];
    DadosThread_* dadosThreads_ = new DadosThread_[numThreads_];

    // Calcula quantas linhas cada thread deve processar;
    // Neste caso, as linhas sao divididas igualmente entre as threads;
    int linhasPorThread_ = linhasM1_ / numThreads_;
    // O resto da divisao e distribuido para as primeiras threads;
    int resto_         = linhasM1_ % numThreads_;

    std::cout << "Criando " << numThreads_ << " threads..." << std::endl;

    int linhaAtual_ = 0;
    // Cria cada uma das T threads e atribui sua faixa de linhas;
    for (int t_ = 0; t_ < numThreads_; t_++) {
        // Configura os dados desta thread;
        dadosThreads_[t_].dadosM1_    = dadosM1_;
        dadosThreads_[t_].dadosM2_    = dadosM2_;
        dadosThreads_[t_].dadosC_     = dadosC_;
        dadosThreads_[t_].linhasM1_   = linhasM1_;
        dadosThreads_[t_].colunasM1_  = colunasM1_;
        dadosThreads_[t_].colunasM2_  = colunasM2_;
        dadosThreads_[t_].idThread_   = t_;
        dadosThreads_[t_].prefixoArquivo_ = prefixoSaida_;
        dadosThreads_[t_].tempoMicros_ = 0;

        // Calcula o inicio e fim da faixa de linhas desta thread;
        // Neste caso, threads com indice menor ao resto recebem uma linha extra;
        dadosThreads_[t_].linhaInicio_ = linhaAtual_;
        dadosThreads_[t_].linhaFim_    = linhaAtual_ + linhasPorThread_ + (t_ < resto_ ? 1 : 0);
        linhaAtual_ = dadosThreads_[t_].linhaFim_;

        // Cria a thread e passa seus dados como argumento;
        // Isso faz com que cada thread comece a executar sua funcao independentemente;
        int status_ = pthread_create(&threads_[t_], NULL, funcaoThread_, (void*)&dadosThreads_[t_]);
        if (status_ != 0) {
            std::cerr << "Erro ao criar thread " << t_ << ". Codigo: " << status_ << std::endl;
        }
    }

    // Aguarda o termino de todas as threads antes de prosseguir;
    // Neste caso, o processo principal fica bloqueado ate todas finalizarem;
    // Isso faz com que o tempo total seja o tempo da thread mais lenta;
    long long tempoMaximo_ = 0;
    for (int t_ = 0; t_ < numThreads_; t_++) {
        pthread_join(threads_[t_], NULL);
        // Verifica se esta thread teve o maior tempo de execucao;
        if (dadosThreads_[t_].tempoMicros_ > tempoMaximo_) {
            tempoMaximo_ = dadosThreads_[t_].tempoMicros_;
        }
    }

    std::cout << "Todas as threads finalizaram." << std::endl;
    std::cout << "Tempo maximo entre as threads: " << tempoMaximo_ << " microsegundos." << std::endl;
    std::cout << "Arquivos de resultado gerados com prefixo: " << prefixoSaida_ << std::endl;

    // Libera toda a memoria alocada antes de encerrar o programa;
    delete[] dadosM1_;
    delete[] dadosM2_;
    delete[] dadosC_;
    delete[] threads_;
    delete[] dadosThreads_;

    return 0;
}
