#!/usr/bin/env python3
# Slides minimalistas em PDF – 16:9 – foco técnico com código real;

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
import numpy as np
from collections import defaultdict
import csv

# ── Dados ────────────────────────────────────────────────────────────────────
dados_ = defaultdict(list)
with open('resultados.csv') as f_:
    for row_ in csv.DictReader(f_):
        k_ = (int(row_['tamanho']), row_['tipo'], int(row_['param']))
        dados_[k_].append(int(row_['tempo_us']))

def med_(k_): v_ = dados_.get(k_, []); return sum(v_)/len(v_) if v_ else 0

TAM_ = [100, 200, 400, 800]
PAR_ = [2, 4, 8, 16]

# ── Paleta minimalista ────────────────────────────────────────────────────────
BG_    = '#0d1117'   # fundo preto GitHub-style
FG_    = '#e6edf3'   # texto principal
DIM_   = '#8b949e'   # texto secundário
BLUE_  = '#58a6ff'   # destaque azul
GREEN_ = '#3fb950'   # verde (processos)
YEL_   = '#d29922'   # amarelo (threads)
RED_   = '#f85149'   # vermelho acento
LINE_  = '#21262d'   # linhas separadoras
CODE_  = '#161b22'   # fundo de código

W_, H_ = 16, 9

def slide_(titulo_sec_=None):
    fig_ = plt.figure(figsize=(W_, H_))
    fig_.patch.set_facecolor(BG_)

    # barra topo fina
    ax_t_ = fig_.add_axes([0, 0.955, 1, 0.045])
    ax_t_.set_facecolor(LINE_)
    ax_t_.axis('off')
    if titulo_sec_:
        ax_t_.text(0.022, 0.5, titulo_sec_, va='center', color=DIM_,
                   fontsize=10, transform=ax_t_.transAxes, fontfamily='monospace')
    ax_t_.text(0.978, 0.5, 'Gabriel Aires · 20240078874', va='center', ha='right',
               color=DIM_, fontsize=10, transform=ax_t_.transAxes)

    # linha separadora topo
    ax_l_ = fig_.add_axes([0, 0.948, 1, 0.007])
    ax_l_.set_facecolor(BLUE_)
    ax_l_.axis('off')

    # rodapé
    ax_b_ = fig_.add_axes([0, 0, 1, 0.038])
    ax_b_.set_facecolor(LINE_)
    ax_b_.axis('off')
    ax_b_.text(0.022, 0.5, 'IMD0036 · Sistemas Operacionais · UFRN / IMD',
               va='center', color=DIM_, fontsize=9, transform=ax_b_.transAxes)
    ax_b_.text(0.978, 0.5, 'github.com/GabrielAirex',
               va='center', ha='right', color=BLUE_, fontsize=9,
               transform=ax_b_.transAxes)
    return fig_

def area_(fig_, left_=0.06, bottom_=0.08, width_=0.88, height_=0.84):
    ax_ = fig_.add_axes([left_, bottom_, width_, height_])
    ax_.set_facecolor(BG_)
    ax_.axis('off')
    return ax_

def titulo_principal_(ax_, txt_, y_=0.92, size_=28):
    ax_.text(0.0, y_, txt_, va='top', ha='left', fontsize=size_,
             fontweight='bold', color=FG_, transform=ax_.transAxes)

def subtitulo_(ax_, txt_, y_=0.80, size_=14):
    ax_.text(0.0, y_, txt_, va='top', ha='left', fontsize=size_,
             color=DIM_, transform=ax_.transAxes)

def tag_(ax_, txt_, x_, y_, cor_=BLUE_, size_=9):
    ax_.text(x_, y_, txt_, va='center', ha='left', fontsize=size_,
             color=cor_, fontfamily='monospace', transform=ax_.transAxes,
             bbox=dict(boxstyle='round,pad=0.3', facecolor=cor_, alpha=0.15, edgecolor='none'))

def bloco_codigo_(ax_, codigo_, x_=0.0, y_=0.70, width_=1.0, fontsize_=9.5):
    linhas_ = codigo_.strip().split('\n')
    h_ = len(linhas_) * 0.058 + 0.04
    ax_.add_patch(FancyBboxPatch((x_, y_-h_+0.01), width_, h_,
                  boxstyle='round,pad=0.015', facecolor=CODE_,
                  edgecolor=LINE_, linewidth=1.2, transform=ax_.transAxes))
    for i_, linha_ in enumerate(linhas_):
        # numero da linha
        ax_.text(x_+0.012, y_-0.02-i_*0.058, str(i_+1), va='top', fontsize=7,
                 color=DIM_, fontfamily='monospace', transform=ax_.transAxes)
        # codigo
        ax_.text(x_+0.038, y_-0.02-i_*0.058, linha_, va='top', fontsize=fontsize_,
                 color=FG_, fontfamily='monospace', transform=ax_.transAxes)
    return y_ - h_

def divisor_(ax_, y_):
    ax_.add_patch(plt.Rectangle((0.0, y_-0.003), 1.0, 0.005,
                  facecolor=LINE_, transform=ax_.transAxes))

# ════════════════════════════════════════════════════════════════════════════
with PdfPages('slides_apresentacao.pdf') as pdf_:

    # ── SLIDE 1: CAPA ────────────────────────────────────────────────────────
    fig_ = slide_()
    ax_ = area_(fig_, 0.08, 0.10, 0.84, 0.82)

    ax_.text(0.0, 0.95, 'Trabalho Prático · Unidade 1', va='top', fontsize=13,
             color=BLUE_, fontfamily='monospace', transform=ax_.transAxes)
    ax_.text(0.0, 0.80, 'Processos e Threads\nem Multiplicação de Matrizes', va='top',
             fontsize=38, fontweight='bold', color=FG_, transform=ax_.transAxes,
             linespacing=1.2)
    ax_.text(0.0, 0.46, 'C++11  ·  pthreads  ·  fork() / waitpid()', va='top',
             fontsize=14, color=DIM_, fontfamily='monospace', transform=ax_.transAxes)

    ax_.add_patch(plt.Rectangle((0.0, 0.295), 0.5, 0.008,
              facecolor=LINE_, transform=ax_.transAxes))

    campos_ = [
        ('Aluno',      'Gabriel Afonso Freitas Aires'),
        ('Matrícula',  '20240078874'),
        ('Curso',      'Engenharia de Computação / CT – Natal'),
        ('Disciplina', 'IMD0036 – Sistemas Operacionais · 2026'),
    ]
    for i_, (label_, val_) in enumerate(campos_):
        y_ = 0.24 - i_*0.085
        ax_.text(0.0,  y_, label_, va='top', fontsize=10, color=DIM_,
                 fontfamily='monospace', transform=ax_.transAxes)
        ax_.text(0.18, y_, val_,   va='top', fontsize=12, color=FG_,
                 fontweight='bold', transform=ax_.transAxes)

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 2: PROBLEMA + ALGORITMO ────────────────────────────────────────
    fig_ = slide_('01 · Problema')
    ax_ = area_(fig_)

    titulo_principal_(ax_, 'Multiplicação de Matrizes O(n³)')
    subtitulo_(ax_, 'Cada elemento c_ij é independente → paralelizável por definição', 0.80)

    tag_(ax_, 'Independência dos Dados', 0.0, 0.72, BLUE_)

    cod_seq_ = """\
// Loop clássico sequencial — baseline de comparação
for (int i_ = 0; i_ < linhasM1_; i_++) {
    for (int j_ = 0; j_ < colunasM2_; j_++) {
        double soma_ = 0.0;
        for (int k_ = 0; k_ < colunasM1_; k_++)
            soma_ += dadosM1_[i_*colunasM1_ + k_] * dadosM2_[k_*colunasM2_ + j_];
        dadosC_[i_*colunasM2_ + j_] = soma_;  // c_ij só depende de linha i e coluna j
    }
}
// → Grava resultado + tempo em microssegundos no arquivo de saída"""
    y_after_ = bloco_codigo_(ax_, cod_seq_, 0.0, 0.68, 0.62)

    # painel direito — por que paraleliza bem
    pontos_ = [
        (BLUE_,  'c_ij depende apenas da\nlinha i de M1 e coluna j de M2'),
        (GREEN_, 'Nenhuma escrita conflitante\nentre workers distintos'),
        (YEL_,   'N linhas → N tarefas\ncompletamente independentes'),
        (RED_,   'Ganho teórico ideal: N×\n(limitado pela Lei de Amdahl)'),
    ]
    for i_, (cor_, txt_) in enumerate(pontos_):
        y_p_ = 0.66 - i_*0.175
        ax_.add_patch(plt.Rectangle((0.66, y_p_-0.10), 0.005, 0.13,
                      facecolor=cor_, transform=ax_.transAxes))
        for j_, linha_ in enumerate(txt_.split('\n')):
            ax_.text(0.675, y_p_-0.005-j_*0.062, linha_, va='top', fontsize=11,
                     color=FG_ if j_==0 else DIM_, fontweight='bold' if j_==0 else 'normal',
                     transform=ax_.transAxes)

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 3: THREADS ─────────────────────────────────────────────────────
    fig_ = slide_('02 · Implementação — Threads')
    ax_ = area_(fig_)

    titulo_principal_(ax_, 'paralelo_threads.cpp')
    subtitulo_(ax_, 'T pthreads · cada thread calcula N/T linhas · matrizes lidas antes do pthread_create()', 0.80)

    cod_thr_ = """\
// Estrutura passada para cada thread — contém sua faixa de linhas
struct DadosThread_ {
    double *dadosM1_, *dadosM2_, *dadosC_;
    int colunasM1_, colunasM2_, linhaInicio_, linhaFim_, idThread_;
    long long tempoMicros_;  // preenchido pela thread após o cálculo
};

void* funcaoThread_(void* arg_) {
    DadosThread_* d_ = (DadosThread_*)arg_;
    struct timeval ini_, fim_;
    gettimeofday(&ini_, NULL);

    for (int i_ = d_->linhaInicio_; i_ < d_->linhaFim_; i_++)   // só sua faixa
        for (int j_ = 0; j_ < d_->colunasM2_; j_++) {
            double soma_ = 0.0;
            for (int k_ = 0; k_ < d_->colunasM1_; k_++)
                soma_ += d_->dadosM1_[i_*d_->colunasM1_+k_] * d_->dadosM2_[k_*d_->colunasM2_+j_];
            d_->dadosC_[i_*d_->colunasM2_+j_] = soma_;
        }

    gettimeofday(&fim_, NULL);
    d_->tempoMicros_ = (fim_.tv_sec-ini_.tv_sec)*1000000 + (fim_.tv_usec-ini_.tv_usec);
    // → salva sua parcela em arquivo próprio + tempoMicros_
    pthread_exit(NULL);
}"""
    bloco_codigo_(ax_, cod_thr_, 0.0, 0.72, 0.60, fontsize_=8.6)

    # notas direita
    notas_ = [
        (BLUE_,  'M1 e M2 lidos ANTES\nde pthread_create()'),
        (GREEN_, 'Sem mutex: cada thread\nescreve em faixas distintas'),
        (YEL_,   'tempo total = max(tempos)\nentre todas as threads'),
        (DIM_,   'Cada thread gera 1 arquivo\ncom sua parcela + tempo'),
    ]
    for i_, (cor_, txt_) in enumerate(notas_):
        y_n_ = 0.70 - i_*0.185
        ax_.add_patch(FancyBboxPatch((0.635, y_n_-0.13), 0.36, 0.14,
                      boxstyle='round,pad=0.01', facecolor=CODE_,
                      edgecolor=cor_, linewidth=1.5, transform=ax_.transAxes))
        for j_, linha_ in enumerate(txt_.split('\n')):
            ax_.text(0.65, y_n_-0.01-j_*0.058, linha_, va='top', fontsize=10.5,
                     color=FG_ if j_==0 else DIM_, fontweight='bold' if j_==0 else 'normal',
                     transform=ax_.transAxes)

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 4: PROCESSOS ───────────────────────────────────────────────────
    fig_ = slide_('03 · Implementação — Processos')
    ax_ = area_(fig_)

    titulo_principal_(ax_, 'paralelo_processos.cpp')
    subtitulo_(ax_, 'P processos via fork() · matrizes lidas antes do fork() · pai aguarda com waitpid()', 0.80)

    cod_proc_ = """\
// Pai lê M1 e M2 ANTES do fork — filhos herdam via copy-on-write
for (int p_ = 0; p_ < numProcessos_; p_++) {
    int inicio_ = p_ * (linhasM1_/numProcessos_);
    int fim_    = (p_ == numProcessos_-1) ? linhasM1_ : inicio_ + linhasM1_/numProcessos_;

    pid_t pid_ = fork();

    if (pid_ == 0) {          // bloco executado SOMENTE pelo filho
        // calcula sua faixa de linhas e mede o tempo
        gettimeofday(&ini_, NULL);
        for (int i_ = inicio_; i_ < fim_; i_++)
            for (int j_ = 0; j_ < colunasM2_; j_++) { /* produto escalar */ }
        gettimeofday(&fim_tf_, NULL);

        // salva parcela + tempo no arquivo exclusivo deste processo
        salvarArquivo_(prefixo_ + "_processo" + to_string(p_) + ".txt");
        exit(0);              // filho encerra aqui

    } else {
        pids_[p_] = pid_;     // pai armazena o PID e continua o loop
    }
}
for (int p_ = 0; p_ < numProcessos_; p_++)
    waitpid(pids_[p_], NULL, 0);   // pai aguarda todos os filhos"""
    bloco_codigo_(ax_, cod_proc_, 0.0, 0.72, 0.60, fontsize_=8.6)

    notas2_ = [
        (BLUE_,  'fork() duplica o processo\ncopy-on-write em M1 e M2'),
        (GREEN_, 'Cada filho: espaço de\nmemória isolado'),
        (YEL_,   'tempo total = max(tempos)\nentre todos os filhos'),
        (RED_,   'Overhead maior que threads\npor isolamento de memória'),
    ]
    for i_, (cor_, txt_) in enumerate(notas2_):
        y_n_ = 0.70 - i_*0.185
        ax_.add_patch(FancyBboxPatch((0.635, y_n_-0.13), 0.36, 0.14,
                      boxstyle='round,pad=0.01', facecolor=CODE_,
                      edgecolor=cor_, linewidth=1.5, transform=ax_.transAxes))
        for j_, linha_ in enumerate(txt_.split('\n')):
            ax_.text(0.65, y_n_-0.01-j_*0.058, linha_, va='top', fontsize=10.5,
                     color=FG_ if j_==0 else DIM_, fontweight='bold' if j_==0 else 'normal',
                     transform=ax_.transAxes)

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 5: RESULTADOS — GRÁFICO ────────────────────────────────────────
    fig_ = slide_('04 · Resultados')
    ax_text_ = area_(fig_, 0.06, 0.70, 0.88, 0.24)
    titulo_principal_(ax_text_, 'Tempo médio — 10 execuções por configuração')
    subtitulo_(ax_text_, '4 tamanhos testados: 100×100 · 200×200 · 400×400 · 800×800', 0.50)

    # 4 subgraficos
    for idx_, tam_ in enumerate(TAM_):
        col_ = idx_ % 2; row_ = idx_ // 2
        ax_ = fig_.add_axes([0.07+col_*0.475, 0.10+(1-row_)*0.295, 0.40, 0.255])
        ax_.set_facecolor(CODE_)

        seq_ms_ = med_((tam_,'sequencial',1))/1e3
        thr_ms_ = [med_((tam_,'threads',  p_))/1e3 for p_ in PAR_]
        prc_ms_ = [med_((tam_,'processos',p_))/1e3 for p_ in PAR_]

        ax_.plot(PAR_,[seq_ms_]*4,'--',color=DIM_, lw=1.5, label='Sequencial', zorder=2)
        ax_.plot(PAR_,thr_ms_,'-o',color=YEL_,lw=2,ms=6,label='Threads',  zorder=3)
        ax_.plot(PAR_,prc_ms_,'-s',color=GREEN_,lw=2,ms=6,label='Processos',zorder=3)

        ax_.set_title(f'{tam_}×{tam_}', fontsize=11, fontweight='bold',
                      color=FG_, pad=5)
        ax_.set_xlabel('T / P', fontsize=9, color=DIM_)
        ax_.set_ylabel('ms', fontsize=9, color=DIM_)
        ax_.set_xticks(PAR_)
        ax_.tick_params(colors=DIM_, labelsize=8)
        ax_.legend(fontsize=8, facecolor=BG_, labelcolor=FG_,
                   edgecolor=LINE_, loc='upper right')
        ax_.grid(True, linestyle=':', alpha=0.3, color=DIM_)
        for spine_ in ax_.spines.values():
            spine_.set_color(LINE_)

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 6: RESULTADOS — TABELA NUMÉRICA ────────────────────────────────
    fig_ = slide_('05 · Resultados Numéricos — 800×800')
    ax_ = area_(fig_)

    titulo_principal_(ax_, 'Números — Matriz 800×800')
    subtitulo_(ax_, 'Média de 10 execuções · tempo do worker mais lento (gargalo real)', 0.80)

    # cabeçalho tabela
    cols_x_  = [0.0, 0.28, 0.50, 0.68, 0.84]
    cols_h_  = ['Configuração', 'Tempo médio', 'Speedup', 'vs T=2', 'Eficiência']
    for cx_, ch_ in zip(cols_x_, cols_h_):
        ax_.text(cx_, 0.71, ch_, va='top', fontsize=10, color=BLUE_,
                 fontfamily='monospace', transform=ax_.transAxes)
    ax_.add_patch(plt.Rectangle((0.0, 0.685), 1.0, 0.006, facecolor=LINE_, transform=ax_.transAxes))

    seq_800_ = med_((800,'sequencial',1))
    linhas_ = [
        ('sequencial',   None,  DIM_),
        ('threads',      None,  YEL_),
        ('processos',    None,  GREEN_),
    ]
    rows_ = [('Sequencial', seq_800_, 1.0, DIM_)]
    for p_ in PAR_:
        rows_.append((f'Threads   T={p_}',  med_((800,'threads',  p_)), p_, YEL_))
    for p_ in PAR_:
        rows_.append((f'Processos P={p_}',  med_((800,'processos',p_)), p_, GREEN_))

    thr2_ = med_((800,'threads',2))
    for i_, (cfg_, us_, workers_, cor_) in enumerate(rows_):
        y_r_ = 0.655 - i_*0.058
        sp_  = seq_800_/us_
        ef_  = sp_/workers_*100 if cfg_!='Sequencial' else 100.0
        vt2_ = thr2_/us_ if cfg_!='Sequencial' else 1.0
        ms_  = us_/1000

        # barra de speedup inline
        bar_w_ = min(sp_/16, 1.0) * 0.15
        ax_.add_patch(plt.Rectangle((0.28, y_r_+0.005), bar_w_, 0.035,
                      facecolor=cor_, alpha=0.25, transform=ax_.transAxes))

        vals_ = [cfg_, f'{ms_:.1f} ms', f'{sp_:.2f}×',
                 f'{vt2_:.2f}×' if cfg_!='Sequencial' else '—',
                 f'{ef_:.0f}%'  if cfg_!='Sequencial' else '100%']
        for cx_, v_ in zip(cols_x_, vals_):
            c_ = cor_ if cx_==0 else (FG_ if cx_<0.65 else
                 (GREEN_ if ef_>60 else YEL_) if cx_==0.84 else FG_)
            ax_.text(cx_, y_r_+0.015, v_, va='center', fontsize=10,
                     color=c_, fontfamily='monospace', transform=ax_.transAxes)

        if i_ in [0, 4]:  # separadores
            ax_.add_patch(plt.Rectangle((0.0, y_r_-0.008), 1.0, 0.004,
                          facecolor=LINE_, transform=ax_.transAxes))

    # destaque
    ax_.add_patch(FancyBboxPatch((0.0, 0.02), 1.0, 0.085,
                  boxstyle='round,pad=0.01', facecolor=CODE_,
                  edgecolor=BLUE_, linewidth=1.5, transform=ax_.transAxes))
    ax_.text(0.5, 0.065, '800×800 · Threads T=16  →  354 ms → 57 ms  ·  speedup 6.2×  ·  redução de 84%',
             ha='center', va='center', fontsize=12, fontweight='bold',
             color=FG_, transform=ax_.transAxes)

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 7: SPEEDUP + AMDAHL ────────────────────────────────────────────
    fig_ = slide_('06 · Análise — Speedup')
    ax_text_ = area_(fig_, 0.06, 0.78, 0.88, 0.16)
    titulo_principal_(ax_text_, 'Speedup vs. Lei de Amdahl', size_=24)
    subtitulo_(ax_text_, 'Ganho nunca linear — porção serial (I/O, fork, criação de threads) limita o máximo', 0.40)

    # speedup 800x800
    ax_ = fig_.add_axes([0.06, 0.10, 0.48, 0.62])
    ax_.set_facecolor(CODE_)
    seq_ = med_((800,'sequencial',1))
    thr_sp_  = [seq_/med_((800,'threads',  p_)) for p_ in PAR_]
    prc_sp_  = [seq_/med_((800,'processos',p_)) for p_ in PAR_]
    ax_.plot(PAR_, PAR_,    ':',  color=DIM_, lw=1.5, label='Speedup ideal')
    ax_.plot(PAR_, thr_sp_, '-o', color=YEL_, lw=2.5, ms=8, label='Threads')
    ax_.plot(PAR_, prc_sp_, '-s', color=GREEN_, lw=2.5, ms=8, label='Processos')
    ax_.set_title('Speedup — 800×800', fontsize=13, color=FG_, fontweight='bold', pad=6)
    ax_.set_xlabel('T / P', fontsize=11, color=DIM_)
    ax_.set_ylabel('Speedup', fontsize=11, color=DIM_)
    ax_.set_xticks(PAR_)
    ax_.tick_params(colors=DIM_)
    ax_.legend(fontsize=10, facecolor=BG_, labelcolor=FG_, edgecolor=LINE_)
    ax_.grid(True, linestyle=':', alpha=0.3, color=DIM_)
    for spine_ in ax_.spines.values(): spine_.set_color(LINE_)

    # anotações
    ax_.annotate(f'{thr_sp_[-1]:.1f}×', xy=(16, thr_sp_[-1]),
                 xytext=(13.5, thr_sp_[-1]+1.2),
                 fontsize=11, color=YEL_, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=YEL_, lw=1.5))
    ax_.annotate(f'Ideal: 16×', xy=(16, 16), xytext=(12, 15),
                 fontsize=10, color=DIM_,
                 arrowprops=dict(arrowstyle='->', color=DIM_, lw=1))

    # painel explicativo direita
    ax_r_ = area_(fig_, 0.58, 0.10, 0.38, 0.62)

    blocos_exp_ = [
        (BLUE_,  'Por que não 16×?',
         ['Porção serial irredutível:', '  – leitura dos arquivos', '  – criação de workers',
          '  – escrita do resultado', '→ Lei de Amdahl limita o teto']),
        (YEL_,   'Threads · plateau T=8→T=16',
         ['Ganho de T=8→16 menor que T=4→8', '→ saturação dos núcleos físicos',
          '→ time-slicing sem ganho real']),
        (GREEN_, 'Processos · irregularidade',
         ['Overhead de fork() variável', '→ maior desvio padrão',
          '→ menos previsível que threads']),
    ]
    y_r_ = 0.92
    for cor_, titulo_b_, linhas_b_ in blocos_exp_:
        ax_r_.add_patch(plt.Rectangle((0.0, y_r_-0.005), 0.04, 0.05,
                        facecolor=cor_, transform=ax_r_.transAxes))
        ax_r_.text(0.07, y_r_+0.018, titulo_b_, va='center', fontsize=11,
                   fontweight='bold', color=FG_, transform=ax_r_.transAxes)
        y_r_ -= 0.055
        for linha_ in linhas_b_:
            ax_r_.text(0.07, y_r_, linha_, va='top', fontsize=9.5,
                       color=DIM_, fontfamily='monospace', transform=ax_r_.transAxes)
            y_r_ -= 0.075
        y_r_ -= 0.02

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 8: DISCUSSÃO — THREADS vs PROCESSOS ────────────────────────────
    fig_ = slide_('07 · Discussão — Threads vs. Processos')
    ax_ = area_(fig_)

    titulo_principal_(ax_, 'Threads vs. Processos — por que a diferença?')
    subtitulo_(ax_, 'Análise técnica das causas do comportamento observado', 0.80)

    # comparação lado a lado
    for col_, (titulo_c_, cor_, itens_) in enumerate([
        ('POSIX Threads (pthreads)', YEL_, [
            ('Memória compartilhada', 'M1 e M2 lidos 1× pelo processo pai\nThreads acessam diretamente — zero cópia'),
            ('Sem sincronização necessária', 'Cada thread escreve em faixas distintas\nde C → sem condição de corrida, sem mutex'),
            ('Criação leve', 'pthread_create() ~µs de overhead\nEscalonado pelo kernel no mesmo espaço'),
            ('Resultado', f'T=8: speedup {med_((800,"sequencial",1))/med_((800,"threads",8)):.1f}×\nT=16: speedup {med_((800,"sequencial",1))/med_((800,"threads",16)):.1f}×'),
        ]),
        ('Processos com fork()', GREEN_, [
            ('Copy-on-write', 'fork() não copia M1/M2 fisicamente\nSó copia páginas escritas (resultado C)'),
            ('Overhead de fork()', 'Criação de PCB, duplicação de descritores\n→ mais custoso que pthread_create()'),
            ('Isolamento total', 'Cada filho tem espaço de endereçamento próprio\n→ cache L1/L2 exclusivo (vantagem em CPUs NUMA)'),
            ('Resultado', f'P=8: speedup {med_((800,"sequencial",1))/med_((800,"processos",8)):.1f}×\nP=16: speedup {med_((800,"sequencial",1))/med_((800,"processos",16)):.1f}×'),
        ]),
    ]):
        x0_ = col_ * 0.51
        ax_.add_patch(FancyBboxPatch((x0_, -0.02), 0.48, 0.72,
                      boxstyle='round,pad=0.01', facecolor=CODE_,
                      edgecolor=cor_, linewidth=2, transform=ax_.transAxes))
        ax_.add_patch(FancyBboxPatch((x0_, 0.66), 0.48, 0.07,
                      boxstyle='round,pad=0.005', facecolor=cor_, alpha=0.2,
                      edgecolor=cor_, linewidth=2, transform=ax_.transAxes))
        ax_.text(x0_+0.24, 0.695, titulo_c_, ha='center', va='center',
                 fontsize=12, fontweight='bold', color=cor_, transform=ax_.transAxes)

        y_i_ = 0.60
        for subtit_, desc_ in itens_:
            ax_.text(x0_+0.02, y_i_, subtit_, va='top', fontsize=10,
                     fontweight='bold', color=FG_, transform=ax_.transAxes)
            y_i_ -= 0.045
            for linha_ in desc_.split('\n'):
                ax_.text(x0_+0.02, y_i_, linha_, va='top', fontsize=9,
                         color=DIM_, transform=ax_.transAxes)
                y_i_ -= 0.058
            y_i_ -= 0.025

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 9: T e P IDEAIS ────────────────────────────────────────────────
    fig_ = slide_('08 · Valor Ideal de T e P')
    ax_ = area_(fig_)

    titulo_principal_(ax_, 'Qual o valor ideal de T e P?')
    subtitulo_(ax_, 'Análise da relação speedup × eficiência × overhead', 0.80)

    # eficiência barras
    ax_bar_ = fig_.add_axes([0.06, 0.12, 0.50, 0.55])
    ax_bar_.set_facecolor(CODE_)

    seq_ = med_((800,'sequencial',1))
    x_ = np.arange(len(PAR_))
    w_ = 0.35
    ef_thr_  = [seq_/(med_((800,'threads',  p_))*p_)*100 for p_ in PAR_]
    ef_proc_ = [seq_/(med_((800,'processos',p_))*p_)*100 for p_ in PAR_]

    bars1_ = ax_bar_.bar(x_-w_/2, ef_thr_,  w_, color=YEL_,   alpha=0.85, label='Threads',   zorder=3)
    bars2_ = ax_bar_.bar(x_+w_/2, ef_proc_, w_, color=GREEN_,  alpha=0.85, label='Processos', zorder=3)
    ax_bar_.axhline(100, linestyle='--', color=DIM_, lw=1.5, label='Ideal 100%')

    for bar_, v_ in zip(list(bars1_)+list(bars2_), ef_thr_+ef_proc_):
        ax_bar_.text(bar_.get_x()+bar_.get_width()/2, v_+2,
                     f'{v_:.0f}%', ha='center', fontsize=9,
                     fontweight='bold', color=FG_)

    ax_bar_.set_title('Eficiência Paralela — 800×800', fontsize=12,
                      color=FG_, fontweight='bold', pad=6)
    ax_bar_.set_xticks(x_); ax_bar_.set_xticklabels([f'T/P={p_}' for p_ in PAR_])
    ax_bar_.set_ylabel('Eficiência (%)', color=DIM_)
    ax_bar_.set_ylim(0, 130)
    ax_bar_.tick_params(colors=DIM_)
    ax_bar_.legend(facecolor=BG_, labelcolor=FG_, edgecolor=LINE_)
    ax_bar_.grid(True, axis='y', linestyle=':', alpha=0.3, color=DIM_, zorder=0)
    for spine_ in ax_bar_.spines.values(): spine_.set_color(LINE_)

    # conclusões direita
    ax_c_ = area_(fig_, 0.60, 0.10, 0.36, 0.62)

    conclusoes_ = [
        (YEL_,   'T ideal = 8 (Threads)',
         'T=8: speedup %.1f× · eficiência %d%%\n'
         'T=16: speedup %.1f× · eficiência %d%%\n'
         '→ ganho marginal não justifica\n'
         '   o custo de workers extras' % (
            seq_/med_((800,'threads',8)),
            seq_/(med_((800,'threads',8))*8)*100,
            seq_/med_((800,'threads',16)),
            seq_/(med_((800,'threads',16))*16)*100)),
        (GREEN_, 'P ideal = 8 (Processos)',
         'P=8: speedup %.1f× · eficiência %d%%\n'
         'P=16: speedup %.1f× · eficiência %d%%\n'
         '→ overhead de fork() corrói\n'
         '   eficiência em P alto' % (
            seq_/med_((800,'processos',8)),
            seq_/(med_((800,'processos',8))*8)*100,
            seq_/med_((800,'processos',16)),
            seq_/(med_((800,'processos',16))*16)*100)),
        (BLUE_,  'Regra geral',
         'T = P ≈ nº de núcleos físicos da CPU\nAcima disso: time-slicing sem ganho\n'
         'Threads > Processos para dados\ncompartilhados em memória'),
    ]

    y_c_ = 0.96
    for cor_, tit_, desc_ in conclusoes_:
        ax_c_.add_patch(plt.Rectangle((0, y_c_-0.005), 0.03, 0.048,
                        facecolor=cor_, transform=ax_c_.transAxes))
        ax_c_.text(0.06, y_c_+0.018, tit_, va='center', fontsize=11,
                   fontweight='bold', color=cor_, transform=ax_c_.transAxes)
        y_c_ -= 0.055
        for linha_ in desc_.split('\n'):
            ax_c_.text(0.06, y_c_, linha_, va='top', fontsize=9,
                       color=DIM_, fontfamily='monospace', transform=ax_c_.transAxes)
            y_c_ -= 0.068
        y_c_ -= 0.025

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

    # ── SLIDE 10: CONCLUSÃO ──────────────────────────────────────────────────
    fig_ = slide_('09 · Conclusão')
    ax_ = area_(fig_)

    ax_.text(0.0, 0.95, '# conclusao', va='top', fontsize=11,
             color=DIM_, fontfamily='monospace', transform=ax_.transAxes)
    ax_.text(0.0, 0.87, 'O que aprendemos', va='top', fontsize=32,
             fontweight='bold', color=FG_, transform=ax_.transAxes)

    pontos_ = [
        (BLUE_,  'Paralelismo funciona',
         'Multiplicação de matrizes é paralelizável por Independência dos Dados.\n'
         'Redução de 84% no tempo para 800×800 com T=16 threads.'),
        (YEL_,   'Threads > Processos (dados compartilhados)',
         'Compartilhamento de memória elimina overhead de cópia.\n'
         'Processos competitivos só em matrizes muito grandes.'),
        (GREEN_, 'Lei de Amdahl sempre presente',
         'Speedup real (6.2×) <<  ideal (16×).\n'
         'Porção serial (I/O, criação de workers) define o teto.'),
        (RED_,   'T = P ≈ nº de núcleos físicos da máquina',
         'Acima do limite: time-slicing anula o ganho.\n'
         'Neste experimento: T=8 e P=8 = melhor custo-benefício.'),
    ]

    y_p_ = 0.70
    for cor_, tit_, desc_ in pontos_:
        ax_.add_patch(plt.Rectangle((0, y_p_+0.005), 0.006, 0.072,
                      facecolor=cor_, transform=ax_.transAxes))
        ax_.text(0.022, y_p_+0.052, tit_, va='top', fontsize=13,
                 fontweight='bold', color=cor_, transform=ax_.transAxes)
        for j_, linha_ in enumerate(desc_.split('\n')):
            ax_.text(0.022, y_p_+0.010-j_*0.042, linha_, va='top', fontsize=10.5,
                     color=DIM_, transform=ax_.transAxes)
        y_p_ -= 0.175

    # linha final
    ax_.add_patch(plt.Rectangle((0.0, 0.035), 1.0, 0.006, facecolor=LINE_, transform=ax_.transAxes))
    ax_.text(0.0, 0.028, 'Código completo:', va='top', fontsize=10, color=DIM_,
             transform=ax_.transAxes)
    ax_.text(0.22, 0.028, 'github.com/GabrielAirex', va='top', fontsize=10,
             color=BLUE_, fontfamily='monospace', transform=ax_.transAxes)

    pdf_.savefig(fig_, bbox_inches='tight'); plt.close(fig_)

print('slides_apresentacao.pdf gerado — 10 slides')
