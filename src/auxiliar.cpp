// Programa Auxiliar - Gera duas matrizes aleatorias e salva em arquivos;
// Este programa recebe 4 argumentos pela linha de comando: n1, m1, n2, m2;
// Neste caso, n1 e m1 sao as dimensoes da primeira matriz, e n2 e m2 da segunda;
// Isso faz com que o programa produza dois arquivos de matriz prontos para uso nos demais programas;

#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <string>

// Classe que representa uma matriz bidimensional de doubles;
class Matriz_ {
public:
    // Numero de linhas da matriz;
    int linhas_;
    // Numero de colunas da matriz;
    int colunas_;
    // Vetor de dados que armazena os elementos da matriz em formato plano (linha x coluna);
    double* dados_;

    // Construtor que inicializa a matriz com as dimensoes fornecidas;
    // Neste caso, a alocacao e feita de forma continua para facilitar o acesso;
    Matriz_(int linhas, int colunas) {
        linhas_  = linhas;
        colunas_ = colunas;
        // Aloca memoria para todos os elementos da matriz;
        // Isso faz com que tenhamos um bloco continuo de memoria para a matriz;
        dados_ = new double[linhas_ * colunas_];
    }

    // Destrutor que libera a memoria alocada para os dados;
    ~Matriz_() {
        delete[] dados_;
    }

    // Retorna uma referencia ao elemento na posicao (i, j);
    // Neste caso, o acesso e feito de forma linear no vetor de dados;
    double& elemento_(int i, int j) {
        return dados_[i * colunas_ + j];
    }

    // Preenche a matriz com valores aleatorios entre 0.0 e 99.99;
    // Isso faz com que cada execucao gere uma matriz diferente;
    void preencherAleatorio_() {
        for (int i_ = 0; i_ < linhas_; i_++) {
            for (int j_ = 0; j_ < colunas_; j_++) {
                // Gera um valor aleatorio no intervalo [0, 99.99];
                elemento_(i_, j_) = (double)(rand() % 10000) / 100.0;
            }
        }
    }

    // Salva a matriz em um arquivo no formato padrao do trabalho;
    // Neste caso, a primeira linha contem as dimensoes e as seguintes os valores;
    void salvarEmArquivo_(const std::string& nomeArquivo_) {
        // Abre o arquivo para escrita;
        std::ofstream arquivo_(nomeArquivo_);
        if (!arquivo_.is_open()) {
            // Neste caso, se o arquivo nao puder ser aberto, exibe erro e encerra;
            std::cerr << "Erro ao abrir arquivo para escrita: " << nomeArquivo_ << std::endl;
            return;
        }
        // Escreve as dimensoes na primeira linha do arquivo;
        // Isso faz com que os programas leitores saibam o tamanho da matriz;
        arquivo_ << linhas_ << " " << colunas_ << "\n";

        // Escreve cada elemento da matriz no arquivo;
        // Neste caso, cada linha do arquivo corresponde a uma linha da matriz;
        for (int i_ = 0; i_ < linhas_; i_++) {
            for (int j_ = 0; j_ < colunas_; j_++) {
                arquivo_ << elemento_(i_, j_);
                // Separa os valores com espaco, exceto no final da linha;
                if (j_ < colunas_ - 1) arquivo_ << " ";
            }
            arquivo_ << "\n";
        }
        arquivo_.close();
        std::cout << "Matriz salva em: " << nomeArquivo_ << std::endl;
    }
};

int main(int argc, char* argv[]) {
    // Verifica se o numero correto de argumentos foi fornecido;
    // Neste caso, sao necessarios exatamente 4 argumentos alem do nome do programa;
    if (argc != 5) {
        std::cerr << "Uso: " << argv[0] << " n1 m1 n2 m2" << std::endl;
        std::cerr << "Exemplo: " << argv[0] << " 100 100 100 100" << std::endl;
        return 1;
    }

    // Converte os argumentos da linha de comando para inteiros;
    // Isso faz com que possamos usar os valores como dimensoes das matrizes;
    int n1_ = std::atoi(argv[1]);
    int m1_ = std::atoi(argv[2]);
    int n2_ = std::atoi(argv[3]);
    int m2_ = std::atoi(argv[4]);

    // Valida as dimensoes fornecidas para garantir que a multiplicacao e possivel;
    // Neste caso, o numero de colunas de M1 deve ser igual ao numero de linhas de M2;
    if (m1_ != n2_) {
        std::cerr << "Erro: Para multiplicar M1 (n1xm1) * M2 (n2xm2), e necessario que m1 == n2." << std::endl;
        std::cerr << "Fornecido: m1=" << m1_ << " n2=" << n2_ << std::endl;
        return 1;
    }

    // Verifica que todas as dimensoes sao positivas;
    if (n1_ <= 0 || m1_ <= 0 || n2_ <= 0 || m2_ <= 0) {
        std::cerr << "Erro: Todas as dimensoes devem ser maiores que zero." << std::endl;
        return 1;
    }

    // Inicializa o gerador de numeros aleatorios com o tempo atual;
    // Isso faz com que cada execucao do programa produza matrizes diferentes;
    srand((unsigned int)time(NULL));

    std::cout << "Gerando matriz M1 de dimensao " << n1_ << "x" << m1_ << "..." << std::endl;

    // Cria e preenche a primeira matriz M1 com valores aleatorios;
    // Neste caso, a matriz tem dimensao n1 x m1;
    Matriz_ m1Matriz_(n1_, m1_);
    m1Matriz_.preencherAleatorio_();
    m1Matriz_.salvarEmArquivo_("matrix1.txt");

    std::cout << "Gerando matriz M2 de dimensao " << n2_ << "x" << m2_ << "..." << std::endl;

    // Cria e preenche a segunda matriz M2 com valores aleatorios;
    // Neste caso, a matriz tem dimensao n2 x m2;
    Matriz_ m2Matriz_(n2_, m2_);
    m2Matriz_.preencherAleatorio_();
    m2Matriz_.salvarEmArquivo_("matrix2.txt");

    std::cout << "Concluido. Arquivos matrix1.txt e matrix2.txt foram gerados." << std::endl;
    std::cout << "M1: " << n1_ << "x" << m1_ << " | M2: " << n2_ << "x" << m2_ << std::endl;
    std::cout << "Resultado esperado C: " << n1_ << "x" << m2_ << std::endl;

    return 0;
}
