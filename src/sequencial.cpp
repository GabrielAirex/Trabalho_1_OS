// Programa Sequencial - Multiplica duas matrizes de forma convencional (sequencial);
// Este programa recebe como argumentos dois arquivos de matrizes e um arquivo de saida;
// Neste caso, a multiplicacao e feita linha por linha, coluna por coluna, sem paralelismo;
// Isso faz com que sirva como baseline para comparacao com as versoes paralelas;

#include <iostream>
#include <fstream>
#include <string>
#include <sys/time.h>

// Classe que representa uma matriz bidimensional de doubles;
// Neste caso, a classe encapsula os dados e operacoes da matriz;
class Matriz_ {
public:
    // Numero de linhas da matriz;
    int linhas_;
    // Numero de colunas da matriz;
    int colunas_;
    // Vetor de dados que armazena os elementos da matriz de forma linear;
    double* dados_;

    // Construtor padrao necessario para declaracao antes de carregar;
    Matriz_() : linhas_(0), colunas_(0), dados_(nullptr) {}

    // Construtor que inicializa a matriz com as dimensoes fornecidas e zera os dados;
    // Neste caso, todos os elementos comecam com o valor zero;
    Matriz_(int linhas, int colunas) {
        linhas_  = linhas;
        colunas_ = colunas;
        dados_ = new double[linhas_ * colunas_];
        // Inicializa todos os elementos com zero;
        // Isso faz com que a matriz resultado comece limpa antes do calculo;
        for (int i_ = 0; i_ < linhas_ * colunas_; i_++) {
            dados_[i_] = 0.0;
        }
    }

    // Destrutor que libera a memoria alocada;
    ~Matriz_() {
        if (dados_ != nullptr) {
            delete[] dados_;
        }
    }

    // Acessa o elemento na posicao (i, j) por referencia;
    double& elemento_(int i, int j) {
        return dados_[i * colunas_ + j];
    }

    // Acessa o elemento na posicao (i, j) como constante (para leitura);
    const double& elemento_(int i, int j) const {
        return dados_[i * colunas_ + j];
    }

    // Carrega a matriz a partir de um arquivo no formato do trabalho;
    // Neste caso, a primeira linha contem as dimensoes e as seguintes os valores;
    // Isso faz com que a matriz seja preenchida com os dados do arquivo;
    bool carregarDeArquivo_(const std::string& nomeArquivo_) {
        std::ifstream arquivo_(nomeArquivo_);
        if (!arquivo_.is_open()) {
            std::cerr << "Erro: nao foi possivel abrir o arquivo: " << nomeArquivo_ << std::endl;
            return false;
        }
        // Le as dimensoes da primeira linha do arquivo;
        arquivo_ >> linhas_ >> colunas_;

        // Aloca memoria com base nas dimensoes lidas;
        // Neste caso, a alocacao ocorre depois de ler o tamanho;
        dados_ = new double[linhas_ * colunas_];

        // Le todos os elementos da matriz do arquivo;
        for (int i_ = 0; i_ < linhas_; i_++) {
            for (int j_ = 0; j_ < colunas_; j_++) {
                arquivo_ >> elemento_(i_, j_);
            }
        }
        arquivo_.close();
        return true;
    }

    // Salva a matriz resultado no formato da Figura 2 do trabalho;
    // Neste caso, o formato e: dimensoes, seguido dos elementos nomeados, depois o tempo;
    // Isso faz com que o arquivo fique legivel e padronizado para comparacao;
    void salvarResultado_(const std::string& nomeArquivo_, long long tempoMicros_) {
        std::ofstream arquivo_(nomeArquivo_);
        if (!arquivo_.is_open()) {
            std::cerr << "Erro ao abrir arquivo de saida: " << nomeArquivo_ << std::endl;
            return;
        }
        // Escreve as dimensoes da matriz resultado na primeira linha;
        arquivo_ << linhas_ << " " << colunas_ << "\n";

        // Escreve cada elemento com seu identificador de posicao;
        // Neste caso, o nome do elemento e formado por 'c' seguido da linha e coluna (1-indexado);
        for (int i_ = 0; i_ < linhas_; i_++) {
            for (int j_ = 0; j_ < colunas_; j_++) {
                arquivo_ << "c" << (i_ + 1) << (j_ + 1) << " " << elemento_(i_, j_) << "\n";
            }
        }
        // Escreve o tempo de execucao em microsegundos ao final do arquivo;
        // Isso faz com que o tempo fique registrado junto ao resultado para comparacao;
        arquivo_ << tempoMicros_ << "\n";
        arquivo_.close();
    }
};

// Funcao que realiza a multiplicacao de duas matrizes de forma sequencial;
// Neste caso, utiliza tres loops aninhados (algoritmo classico O(n^3));
// Isso faz com que cada elemento c[i][j] seja calculado como produto escalar da linha i por coluna j;
Matriz_* multiplicarMatrizes_(const Matriz_& m1_, const Matriz_& m2_) {
    // Verifica se as dimensoes sao compativeis para multiplicacao;
    // Neste caso, o numero de colunas de M1 deve ser igual ao numero de linhas de M2;
    if (m1_.colunas_ != m2_.linhas_) {
        std::cerr << "Erro: dimensoes incompativeis para multiplicacao." << std::endl;
        std::cerr << "M1 colunas=" << m1_.colunas_ << " M2 linhas=" << m2_.linhas_ << std::endl;
        return nullptr;
    }

    // Cria a matriz resultado com dimensoes n1 x m2;
    Matriz_* resultado_ = new Matriz_(m1_.linhas_, m2_.colunas_);

    // Loop externo percorre as linhas da matriz M1;
    for (int i_ = 0; i_ < m1_.linhas_; i_++) {
        // Loop intermediario percorre as colunas da matriz M2;
        for (int j_ = 0; j_ < m2_.colunas_; j_++) {
            // Neste caso, c[i][j] e a soma dos produtos a[i][k] * b[k][j];
            double soma_ = 0.0;
            // Loop interno realiza o produto escalar entre linha i de M1 e coluna j de M2;
            for (int k_ = 0; k_ < m1_.colunas_; k_++) {
                soma_ += m1_.dados_[i_ * m1_.colunas_ + k_] * m2_.dados_[k_ * m2_.colunas_ + j_];
            }
            // Isso faz com que o elemento resultado seja atribuido apos o calculo completo;
            resultado_->elemento_(i_, j_) = soma_;
        }
    }
    return resultado_;
}

int main(int argc, char* argv[]) {
    // Verifica se os argumentos necessarios foram fornecidos;
    // Neste caso, sao necessarios: arquivo_m1, arquivo_m2 e arquivo_saida;
    if (argc != 4) {
        std::cerr << "Uso: " << argv[0] << " arquivo_m1 arquivo_m2 arquivo_saida" << std::endl;
        return 1;
    }

    // Nomes dos arquivos recebidos como argumentos;
    std::string arquivoM1_(argv[1]);
    std::string arquivoM2_(argv[2]);
    std::string arquivoSaida_(argv[3]);

    // Declara as matrizes que serao lidas dos arquivos;
    Matriz_ m1_, m2_;

    std::cout << "Lendo arquivo da matriz M1: " << arquivoM1_ << std::endl;
    // Carrega a primeira matriz do arquivo;
    // Neste caso, se o carregamento falhar, o programa encerra;
    if (!m1_.carregarDeArquivo_(arquivoM1_)) {
        return 1;
    }

    std::cout << "Lendo arquivo da matriz M2: " << arquivoM2_ << std::endl;
    // Carrega a segunda matriz do arquivo;
    if (!m2_.carregarDeArquivo_(arquivoM2_)) {
        return 1;
    }

    std::cout << "M1: " << m1_.linhas_ << "x" << m1_.colunas_
              << " | M2: " << m2_.linhas_ << "x" << m2_.colunas_ << std::endl;
    std::cout << "Iniciando multiplicacao sequencial..." << std::endl;

    // Registra o tempo de inicio da multiplicacao;
    // Neste caso, usamos gettimeofday para alta precisao em microsegundos;
    struct timeval tempoInicio_, tempoFim_;
    gettimeofday(&tempoInicio_, NULL);

    // Executa a multiplicacao sequencial das matrizes;
    // Isso faz com que o resultado seja armazenado em uma nova matriz alocada dinamicamente;
    Matriz_* resultado_ = multiplicarMatrizes_(m1_, m2_);

    // Registra o tempo de fim da multiplicacao;
    gettimeofday(&tempoFim_, NULL);

    if (resultado_ == nullptr) {
        // Neste caso, a multiplicacao falhou por dimensoes incompativeis;
        return 1;
    }

    // Calcula o tempo total de execucao em microsegundos;
    // Isso faz com que tenhamos a duracao exata do calculo para comparacao;
    long long tempoMicros_ = ((long long)tempoFim_.tv_sec  * 1000000 + tempoFim_.tv_usec) -
                             ((long long)tempoInicio_.tv_sec * 1000000 + tempoInicio_.tv_usec);

    std::cout << "Multiplicacao concluida em " << tempoMicros_ << " microsegundos." << std::endl;

    // Salva o resultado da multiplicacao no arquivo de saida;
    // Neste caso, o tempo tambem e gravado no final do arquivo;
    resultado_->salvarResultado_(arquivoSaida_, tempoMicros_);
    std::cout << "Resultado salvo em: " << arquivoSaida_ << std::endl;

    // Libera a memoria alocada para a matriz resultado;
    delete resultado_;

    return 0;
}
