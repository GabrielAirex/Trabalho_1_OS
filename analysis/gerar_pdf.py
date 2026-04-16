#!/usr/bin/env python3
# Gera o relatorio completo em PDF usando matplotlib PdfPages;
# Neste caso, cada pagina e construida como uma figura matplotlib;

import csv, io
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# ── Dados ────────────────────────────────────────────────────────────────────
dados_ = defaultdict(list)
with open("resultados.csv") as f_:
    for row_ in csv.DictReader(f_):
        chave_ = (int(row_["tamanho"]), row_["tipo"], int(row_["param"]))
        dados_[chave_].append(int(row_["tempo_us"]))

def med_(k_):
    v_ = dados_.get(k_, [])
    return sum(v_)/len(v_) if v_ else 0

def dp_(k_):
    v_ = dados_.get(k_, [])
    if len(v_) < 2: return 0
    m_ = sum(v_)/len(v_)
    return (sum((x_-m_)**2 for x_ in v_)/(len(v_)-1))**.5

TAM_   = [100, 200, 400, 800]
PAR_   = [2, 4, 8, 16]
CSEQ_  = '#1a56db'
CTHR_  = '#e3a008'
CPROC_ = '#057a55'
CBKG_  = '#1e3a5f'

# ── Helpers ──────────────────────────────────────────────────────────────────
def nova_pagina_(pdf_, titulo_sec_=None):
    fig_ = plt.figure(figsize=(8.27, 11.69))  # A4
    fig_.patch.set_facecolor('white')
    # topo colorido fino
    ax_top_ = fig_.add_axes([0, 0.965, 1, 0.035])
    ax_top_.set_facecolor(CBKG_)
    ax_top_.axis('off')
    ax_top_.text(0.02, 0.5, 'UFRN · IMD · Sistemas Operacionais · Trabalho 1 – Processos e Threads',
                 va='center', ha='left', color='white', fontsize=7,
                 transform=ax_top_.transAxes)
    ax_top_.text(0.98, 0.5, 'Gabriel Afonso Freitas Aires · 20240078874',
                 va='center', ha='right', color='#bfdbfe', fontsize=7,
                 transform=ax_top_.transAxes)
    # rodape
    ax_bot_ = fig_.add_axes([0, 0, 1, 0.025])
    ax_bot_.set_facecolor('#f1f5f9')
    ax_bot_.axis('off')
    ax_bot_.text(0.5, 0.5, 'Engenharia de Computação / CT – Natal – Bacharelado · github.com/GabrielAirex',
                 va='center', ha='center', color='#64748b', fontsize=6.5,
                 transform=ax_bot_.transAxes)
    return fig_

def salvar_(fig_, pdf_):
    pdf_.savefig(fig_, bbox_inches='tight')
    plt.close(fig_)

# ════════════════════════════════════════════════════════════════════════════
with PdfPages('relatorio.pdf') as pdf_:

    # ── PÁGINA 1: CAPA ───────────────────────────────────────────────────────
    fig_ = plt.figure(figsize=(8.27, 11.69))
    fig_.patch.set_facecolor(CBKG_)

    # gradiente simulado com retangulos num eixo auxiliar
    ax_grad_ = fig_.add_axes([0, 0, 1, 1])
    ax_grad_.axis('off')
    ax_grad_.set_zorder(0)
    for i_, alpha_ in enumerate(np.linspace(0.0, 0.35, 40)):
        ax_grad_.add_patch(plt.Rectangle((0, i_/40), 1, 1/40,
                           transform=ax_grad_.transAxes, color='#06b6d4', alpha=alpha_))

    # logos
    for x_, txt_ in [(0.32, 'UFRN'), (0.68, 'IMD')]:
        fig_.text(x_, 0.80, txt_, ha='center', va='center',
                  fontsize=26, fontweight='bold', color='white',
                  bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.15, edgecolor='white'))

    fig_.text(0.5, 0.70, 'Trabalho Prático – Unidade 1', ha='center', va='center',
              fontsize=22, fontweight='bold', color='white')
    fig_.text(0.5, 0.645, 'Processos e Threads', ha='center', va='center',
              fontsize=17, color='#bfdbfe')
    fig_.text(0.5, 0.595, 'Multiplicação de Matrizes Paralela em C++', ha='center', va='center',
              fontsize=13, color='#e0f2fe', style='italic')

    # linha separadora
    ax_grad_.add_patch(plt.Rectangle((0.1, 0.568), 0.8, 0.003,
                       transform=ax_grad_.transAxes, color='white', alpha=0.4))

    # infos
    infos_ = [
        ('Disciplina',  'IMD0036 – Sistemas Operacionais'),
        ('Aluno',       'Gabriel Afonso Freitas Aires'),
        ('Matrícula',   '20240078874'),
        ('Curso',       'Engenharia de Computação / CT – Natal – Bacharelado'),
        ('GitHub',      'github.com/GabrielAirex'),
        ('Data',        'Abril de 2026'),
    ]
    y0_ = 0.520
    for label_, val_ in infos_:
        fig_.text(0.22, y0_, label_ + ':', ha='right', va='center',
                  fontsize=11, color='#bfdbfe', fontweight='bold')
        fig_.text(0.24, y0_, val_, ha='left', va='center',
                  fontsize=11, color='white')
        y0_ -= 0.052

    fig_.text(0.5, 0.10, 'Universidade Federal do Rio Grande do Norte\nInstituto Metrópole Digital',
              ha='center', va='center', fontsize=9, color='#94a3b8', linespacing=1.7)

    pdf_.savefig(fig_, bbox_inches='tight')
    plt.close(fig_)

    # ── PÁGINA 2: INTRODUÇÃO + ETAPA 1 ──────────────────────────────────────
    fig_ = nova_pagina_(pdf_)
    ax_ = fig_.add_axes([0.07, 0.04, 0.86, 0.90])
    ax_.axis('off')

    y_ = 0.98
    def titulo_(t_, y_, cor_=CBKG_, size_=13):
        ax_.add_patch(FancyBboxPatch((0, y_-0.018), 1, 0.035,
                      boxstyle='round,pad=0.005', facecolor=cor_, edgecolor='none',
                      transform=ax_.transAxes))
        ax_.text(0.012, y_, t_, va='center', ha='left', fontsize=size_,
                 fontweight='bold', color='white', transform=ax_.transAxes)
        return y_ - 0.055

    def corpo_(linhas_, y_, size_=8.5, cor_='#1e293b', indent_=0.012):
        for l_ in linhas_:
            ax_.text(indent_, y_, l_, va='top', ha='left', fontsize=size_,
                     color=cor_, transform=ax_.transAxes, wrap=True)
            y_ -= 0.028
        return y_

    def caixa_(linhas_, y_, facecolor_='#eff6ff', edgecolor_=CSEQ_, size_=8):
        h_ = len(linhas_) * 0.028 + 0.016
        ax_.add_patch(FancyBboxPatch((0.01, y_-h_+0.006), 0.985, h_,
                      boxstyle='round,pad=0.005', facecolor=facecolor_,
                      edgecolor=edgecolor_, linewidth=1.5, transform=ax_.transAxes))
        for i_, l_ in enumerate(linhas_):
            ax_.text(0.025, y_ - i_*0.028, l_, va='top', ha='left', fontsize=size_,
                     color='#1e293b', transform=ax_.transAxes)
        return y_ - h_ - 0.01

    y_ = titulo_('1. Introdução', y_)
    y_ = corpo_([
        'Este trabalho implementa a multiplicação de matrizes com paralelismo usando threads POSIX e processos Unix.',
        'A multiplicação de matrizes é O(n³) e cada elemento c_ij pode ser calculado independentemente',
        '(Independência dos Dados), tornando-a ideal para paralelização.',
    ], y_)
    y_ -= 0.01

    y_ = titulo_('2. Programas Implementados (Etapa 1)', y_)

    progs_ = [
        ('auxiliar',            CSEQ_,  'Recebe n1,m1,n2,m2 via args. Gera M1 e M2 aleatórias e salva em matrix1.txt / matrix2.txt.'),
        ('sequencial',          CTHR_,  'Lê M1 e M2, executa multiplicação com 3 loops aninhados O(n³), salva resultado + tempo.'),
        ('paralelo_threads',    CPROC_, 'Lê matrizes ANTES de criar T threads. Cada thread calcula N1/T linhas. Gera T arquivos.'),
        ('paralelo_processos',  '#6d28d9','Lê matrizes ANTES do fork(). Cria P processos filho via fork(). Cada filho gera 1 arquivo.'),
    ]
    for nome_, cor_, desc_ in progs_:
        ax_.add_patch(FancyBboxPatch((0.01, y_-0.038), 0.985, 0.042,
                      boxstyle='round,pad=0.005', facecolor=cor_, edgecolor='none',
                      transform=ax_.transAxes, alpha=0.9))
        ax_.text(0.025, y_-0.005, nome_, va='top', fontsize=9, fontweight='bold',
                 color='white', transform=ax_.transAxes)
        ax_.text(0.025, y_-0.022, desc_, va='top', fontsize=7.8,
                 color='#f8fafc', transform=ax_.transAxes)
        y_ -= 0.050

    y_ -= 0.01
    y_ = titulo_('Formato dos Arquivos', y_, cor_='#334155', size_=11)
    y_ = corpo_(['Entrada (matrix1.txt / matrix2.txt): linha 1 = "N M", linhas seguintes = valores da matriz.'], y_)
    y_ = caixa_(['Resultado: linha 1 = dimensões  |  linhas seguintes = "cIJ valor"  |  última linha = tempo em microssegundos'], y_)

    y_ -= 0.01
    y_ = titulo_('Estratégia de Paralelização', y_, cor_='#334155', size_=11)
    y_ = caixa_([
        'Threads: matrizes lidas antes da criação → threads compartilham M1 e M2 (read-only) sem mutex.',
        '         Cada thread escreve em faixas distintas de C → sem condição de corrida.',
        'Processos: matrizes lidas antes do fork() → filhos herdam dados via copy-on-write.',
        '           Cada filho calcula sua faixa e salva em arquivo próprio, depois exit(0).',
    ], y_, facecolor_='#f0fdf4', edgecolor_=CPROC_)

    y_ = corpo_([
        'Distribuição de linhas: linhas_por_worker = N÷T; resto = N%T distribuído às primeiras workers.',
    ], y_)

    salvar_(fig_, pdf_)

    # ── PÁGINA 3: METODOLOGIA + TABELA RESULTADOS ────────────────────────────
    fig_ = nova_pagina_(pdf_)
    ax_ = fig_.add_axes([0.05, 0.04, 0.90, 0.90])
    ax_.axis('off')

    y_ = 0.98
    y_ = titulo_('3. Etapa 2 – Resultados dos Experimentos', y_)

    y_ = caixa_([
        'Metodologia: 10 execuções por configuração · 4 tamanhos (100², 200², 400², 800²)',
        'Para paralelas: tempo = maior tempo entre as workers (gargalo real do sistema).',
        'Speedup = tempo_sequencial / tempo_paralelo',
    ], y_, facecolor_='#fffbeb', edgecolor_='#d97706')

    y_ -= 0.012

    # Tabela
    col_labels_ = ['Matriz', 'Config.', 'Tempo Médio', 'Desv. Pad.', 'Speedup']
    col_x_      = [0.00, 0.14, 0.40, 0.60, 0.80]
    col_w_      = [0.14, 0.26, 0.20, 0.20, 0.18]

    # header
    for cx_, cw_, cl_ in zip(col_x_, col_w_, col_labels_):
        ax_.add_patch(plt.Rectangle((cx_, y_-0.022), cw_-0.003, 0.025,
                      facecolor=CBKG_, edgecolor='none', transform=ax_.transAxes))
        ax_.text(cx_+cw_/2-0.002, y_-0.008, cl_, va='center', ha='center',
                 fontsize=7.5, fontweight='bold', color='white', transform=ax_.transAxes)
    y_ -= 0.030

    row_alt_ = False
    for tam_ in TAM_:
        seq_us_ = med_((tam_, 'sequencial', 1))
        rows_ = [('sequencial', 1, CSEQ_)] + \
                [(f'threads T={p_}', p_, CTHR_) for p_ in PAR_] + \
                [(f'processos P={p_}', p_, CPROC_) for p_ in PAR_]

        for label_, param_, cor_ in rows_:
            tipo_ = label_.split()[0]
            us_   = med_((tam_, tipo_, param_))
            dpv_  = dp_((tam_, tipo_, param_))
            sp_   = seq_us_ / us_ if us_ > 0 else 1.0
            ms_   = us_ / 1000
            dms_  = dpv_ / 1000

            bg_ = '#f8fafc' if row_alt_ else 'white'
            ax_.add_patch(plt.Rectangle((0, y_-0.018), 1, 0.022,
                          facecolor=bg_, edgecolor='none', transform=ax_.transAxes))
            # barra colorida na esquerda indicando tipo
            ax_.add_patch(plt.Rectangle((0, y_-0.018), 0.004, 0.022,
                          facecolor=cor_, edgecolor='none', transform=ax_.transAxes))

            vals_ = [f'{tam_}×{tam_}', label_, f'{ms_:.2f} ms', f'±{dms_:.2f} ms', f'{sp_:.2f}×']
            for cx_, cw_, val_ in zip(col_x_, col_w_, vals_):
                ha_ = 'center' if cx_ > 0.10 else 'left'
                xv_ = cx_+cw_/2-0.002 if ha_=='center' else cx_+0.012
                fw_ = 'bold' if tipo_=='sequencial' else 'normal'
                ax_.text(xv_, y_-0.006, val_, va='center', ha=ha_,
                         fontsize=7, color='#1e293b', fontweight=fw_,
                         transform=ax_.transAxes)
            row_alt_ = not row_alt_
            y_ -= 0.022
            if y_ < 0.04:
                break
        if y_ < 0.04:
            break

    salvar_(fig_, pdf_)

    # ── PÁGINAS 4-7: UM GRÁFICO DE TEMPO POR PÁGINA ─────────────────────────
    for tam_ in TAM_:
        fig_ = nova_pagina_(pdf_)

        ax_title_ = fig_.add_axes([0.07, 0.87, 0.86, 0.07])
        ax_title_.axis('off')
        ax_title_.add_patch(FancyBboxPatch((0, 0.1), 1, 0.8,
                            boxstyle='round,pad=0.02', facecolor=CBKG_,
                            edgecolor='none', transform=ax_title_.transAxes))
        ax_title_.text(0.5, 0.55, f'Gráfico de Tempo Médio de Execução – Matriz {tam_}×{tam_}',
                       ha='center', va='center', fontsize=13, fontweight='bold',
                       color='white', transform=ax_title_.transAxes)

        ax_ = fig_.add_axes([0.10, 0.46, 0.85, 0.38])
        seq_s_  = med_((tam_,'sequencial',1)) / 1e6
        thr_s_  = [med_((tam_,'threads',  p_)) / 1e6 for p_ in PAR_]
        proc_s_ = [med_((tam_,'processos',p_)) / 1e6 for p_ in PAR_]

        ax_.plot(PAR_, [seq_s_]*4, '--o', color=CSEQ_,  label='Sequencial', lw=2.5, ms=8, zorder=3)
        ax_.plot(PAR_, thr_s_,     '-s',  color=CTHR_,  label='Threads',    lw=2.5, ms=9, zorder=3)
        ax_.plot(PAR_, proc_s_,    '-^',  color=CPROC_, label='Processos',  lw=2.5, ms=9, zorder=3)
        ax_.fill_between(PAR_, thr_s_,  alpha=0.10, color=CTHR_)
        ax_.fill_between(PAR_, proc_s_, alpha=0.10, color=CPROC_)
        ax_.set_xlabel('Número de Threads / Processos', fontsize=11)
        ax_.set_ylabel('Tempo (segundos)', fontsize=11)
        ax_.set_xticks(PAR_)
        ax_.legend(fontsize=10, loc='upper right')
        ax_.grid(True, linestyle='--', alpha=0.4)
        ax_.set_facecolor('#fafafa')
        for spine_ in ax_.spines.values(): spine_.set_color('#e2e8f0')

        # speedup subplot
        ax2_ = fig_.add_axes([0.10, 0.06, 0.85, 0.32])
        seq_us_ = med_((tam_,'sequencial',1))
        thr_sp_  = [seq_us_/med_((tam_,'threads',  p_)) for p_ in PAR_]
        proc_sp_ = [seq_us_/med_((tam_,'processos',p_)) for p_ in PAR_]

        ax2_.plot(PAR_, PAR_,     '--', color='#9ca3af', label='Ideal',    lw=1.5)
        ax2_.plot(PAR_, thr_sp_,  '-s', color=CTHR_,    label='Threads',   lw=2.2, ms=7)
        ax2_.plot(PAR_, proc_sp_, '-^', color=CPROC_,   label='Processos', lw=2.2, ms=7)
        ax2_.set_xlabel('Número de Threads / Processos', fontsize=10)
        ax2_.set_ylabel('Speedup', fontsize=10)
        ax2_.set_xticks(PAR_)
        ax2_.legend(fontsize=9, loc='upper left')
        ax2_.grid(True, linestyle='--', alpha=0.4)
        ax2_.set_facecolor('#fafafa')
        ax2_.set_title(f'Speedup – {tam_}×{tam_}', fontsize=10, fontweight='bold', pad=6)
        for spine_ in ax2_.spines.values(): spine_.set_color('#e2e8f0')

        salvar_(fig_, pdf_)

    # ── PÁGINA 8: HEATMAP SPEEDUP + EFICIÊNCIA ───────────────────────────────
    fig_ = nova_pagina_(pdf_)

    ax_title_ = fig_.add_axes([0.07, 0.87, 0.86, 0.06])
    ax_title_.axis('off')
    ax_title_.add_patch(FancyBboxPatch((0,0.05),1,0.9, boxstyle='round,pad=0.02',
                        facecolor=CBKG_, edgecolor='none', transform=ax_title_.transAxes))
    ax_title_.text(0.5, 0.55, 'Análise de Speedup e Eficiência Paralela',
                   ha='center', va='center', fontsize=13, fontweight='bold',
                   color='white', transform=ax_title_.transAxes)

    # Heatmaps
    for idx_, (tipo_, label_, col_) in enumerate([('threads','Threads',CTHR_),('processos','Processos',CPROC_)]):
        ax_ = fig_.add_axes([0.07 + idx_*0.48, 0.53, 0.42, 0.30])
        mat_ = np.array([[round(med_((t_,'sequencial',1))/med_((t_,tipo_,p_)),2)
                          for p_ in PAR_] for t_ in TAM_])
        im_ = ax_.imshow(mat_, cmap='YlOrRd', aspect='auto', vmin=1, vmax=10)
        ax_.set_xticks(range(4)); ax_.set_xticklabels([f'T={p_}' for p_ in PAR_], fontsize=8)
        ax_.set_yticks(range(4)); ax_.set_yticklabels([f'{t_}²' for t_ in TAM_], fontsize=8)
        ax_.set_title(f'Speedup – {label_}', fontsize=10, fontweight='bold')
        for i_ in range(4):
            for j_ in range(4):
                ax_.text(j_, i_, f'{mat_[i_,j_]:.1f}×', ha='center', va='center',
                         fontsize=9, fontweight='bold',
                         color='black' if mat_[i_,j_] < 5 else 'white')
        plt.colorbar(im_, ax=ax_, shrink=0.85)

    # Eficiência barras
    for idx_, (tipo_, label_, cor_) in enumerate([('threads','Threads',CTHR_),('processos','Processos',CPROC_)]):
        ax_ = fig_.add_axes([0.07 + idx_*0.48, 0.08, 0.42, 0.38])
        seq_ = med_((800,'sequencial',1))
        ef_  = [seq_/(med_((800,tipo_,p_))*p_)*100 for p_ in PAR_]
        bars_ = ax_.bar(PAR_, ef_, color=cor_, alpha=0.85, width=1.5, zorder=3)
        ax_.axhline(100, linestyle='--', color='#9ca3af', lw=1.5, label='Ideal 100%')
        for bar_, v_ in zip(bars_, ef_):
            ax_.text(bar_.get_x()+bar_.get_width()/2, v_+2,
                     f'{v_:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax_.set_title(f'Eficiência – {label_} (800×800)', fontsize=10, fontweight='bold')
        ax_.set_xlabel('Número de workers', fontsize=9)
        ax_.set_ylabel('Eficiência (%)', fontsize=9)
        ax_.set_xticks(PAR_)
        ax_.set_ylim(0, 130)
        ax_.legend(fontsize=8)
        ax_.grid(True, linestyle='--', alpha=0.3, axis='y', zorder=0)
        ax_.set_facecolor('#fafafa')

    salvar_(fig_, pdf_)

    # ── PÁGINA 9: DISCUSSÃO ──────────────────────────────────────────────────
    fig_ = nova_pagina_(pdf_)
    ax_ = fig_.add_axes([0.07, 0.04, 0.86, 0.90])
    ax_.axis('off')

    y_ = 0.98
    y_ = titulo_('5. Etapa 3 – Discussões', y_)

    y_ = titulo_('a) Por que os resultados? Houve diferença entre serial, threads e processos?', y_,
                 cor_='#334155', size_=10)

    blocos_ = [
        ('#eff6ff', CSEQ_, 'Sequencial vs. Paralelo',
         ['Todas as versões paralelas superaram a sequencial. Para 800×800, threads T=16',
          'alcançaram speedup ≈6,2× e processos P=16 speedup ≈6,1×. O ganho cresce com',
          'o tamanho da matriz, pois o custo de criação de workers é amortizado.']),
        ('#fffbeb', '#d97706', 'Threads vs. Processos',
         ['Threads superaram processos em matrizes médias (200×200, 400×400) por',
          'compartilharem memória — sem cópia de dados. Processos têm overhead de fork()',
          'e I/O separado. Em 800×800 com P=16, processos equipararam-se às threads,',
          'pois o overhead foi amortizado e o isolamento de memória favoreceu o cache.']),
        ('#f0fdf4', CPROC_, 'Plateau de T=8 para T=16 (Lei de Amdahl)',
         ['O ganho de T=8→T=16 foi menor que T=4→T=8. Isso confirma a Lei de Amdahl:',
          'a porção serial (leitura de arquivo, criação de threads, escrita de resultados)',
          'limita o speedup máximo. Acima do número de núcleos físicos da CPU, threads',
          'extras disputam os mesmos núcleos por time-slicing sem ganho real.']),
        ('#fef2f2', '#dc2626', 'Matrizes pequenas (100×100)',
         ['O overhead de criar e sincronizar workers (~312 µs sequencial) é comparável ao',
          'cálculo. Ainda houve ganho por eficiência de cache e baixa contenção. Em CPUs',
          'monocore o resultado poderia ser negativo (overhead > ganho).']),
    ]

    for facecolor_, edgecolor_, titulo_bloco_, linhas_ in blocos_:
        h_ = len(linhas_)*0.027 + 0.042
        ax_.add_patch(FancyBboxPatch((0.01, y_-h_), 0.985, h_,
                      boxstyle='round,pad=0.006', facecolor=facecolor_,
                      edgecolor=edgecolor_, linewidth=1.5, transform=ax_.transAxes))
        ax_.text(0.025, y_-0.012, titulo_bloco_, va='top', fontsize=9, fontweight='bold',
                 color='#1e293b', transform=ax_.transAxes)
        for i_, l_ in enumerate(linhas_):
            ax_.text(0.025, y_-0.030-i_*0.027, l_, va='top', fontsize=8,
                     color='#334155', transform=ax_.transAxes)
        y_ -= h_ + 0.015

    y_ -= 0.01
    y_ = titulo_('b) Qual o valor ideal de T e P?', y_, cor_='#334155', size_=10)

    for facecolor_, edgecolor_, titulo_b_, linhas_b_ in [
        ('#eff6ff', CSEQ_, 'Threads — T ideal: T = 8',
         ['Para matrizes ≥400×400, T=8 apresenta a melhor relação speedup/eficiência.',
          'T=16 traz ganho marginal com eficiência ~44%, indicando contenção de núcleos.',
          'Recomendação: T = número de núcleos lógicos da CPU.']),
        ('#f0fdf4', CPROC_, 'Processos — P ideal: P = 8',
         ['Overhead de fork() maior que threads; para matrizes médias P=8 é mais eficiente.',
          'Para matrizes grandes, P=16 equipara-se a threads. Recomendação: P = núcleos físicos.']),
    ]:
        h_ = len(linhas_b_)*0.027 + 0.042
        ax_.add_patch(FancyBboxPatch((0.01, y_-h_), 0.985, h_,
                      boxstyle='round,pad=0.006', facecolor=facecolor_,
                      edgecolor=edgecolor_, linewidth=1.5, transform=ax_.transAxes))
        ax_.text(0.025, y_-0.012, titulo_b_, va='top', fontsize=9, fontweight='bold',
                 color='#1e293b', transform=ax_.transAxes)
        for i_, l_ in enumerate(linhas_b_):
            ax_.text(0.025, y_-0.030-i_*0.027, l_, va='top', fontsize=8,
                     color='#334155', transform=ax_.transAxes)
        y_ -= h_ + 0.015

    salvar_(fig_, pdf_)

    # ── PÁGINA 10: CONCLUSÃO ─────────────────────────────────────────────────
    fig_ = nova_pagina_(pdf_)
    ax_ = fig_.add_axes([0.07, 0.04, 0.86, 0.90])
    ax_.axis('off')

    y_ = 0.98
    y_ = titulo_('6. Conclusão', y_)

    pontos_ = [
        'A paralelização traz ganhos reais, especialmente em problemas de maior dimensão, onde o custo\n'
        '   de criação dos workers é amortizado pelo volume de cálculo.',
        'Threads são mais eficientes que processos para computação intensiva com dados compartilhados,\n'
        '   pois evitam overhead de cópia de memória.',
        'O ganho nunca é linear (Lei de Amdahl) pois sempre há uma porção serial irredutível.',
        'O valor ótimo de T e P está relacionado ao número de núcleos de CPU disponíveis.',
        'Para problemas com independência de dados (como multiplicação de matrizes), a programação\n'
        '   paralela é altamente recomendada.',
    ]
    for i_, p_ in enumerate(pontos_):
        ax_.add_patch(plt.Circle((0.028, y_-0.012), 0.012, color=CSEQ_, transform=ax_.transAxes))
        ax_.text(0.04, y_-0.012, str(i_+1), va='center', ha='center', fontsize=7,
                 fontweight='bold', color='white', transform=ax_.transAxes)
        ax_.text(0.06, y_-0.006, p_, va='top', fontsize=8.5, color='#1e293b',
                 transform=ax_.transAxes)
        lines_ = p_.count('\n') + 1
        y_ -= 0.040 + (lines_-1)*0.020

    y_ -= 0.02

    # Destaque final
    h_dest_ = 0.10
    ax_.add_patch(FancyBboxPatch((0.01, y_-h_dest_), 0.985, h_dest_,
                  boxstyle='round,pad=0.01', facecolor='#f0fdf4',
                  edgecolor=CPROC_, linewidth=2, transform=ax_.transAxes))
    ax_.text(0.5, y_-0.025, 'Resultado Principal', ha='center', va='top',
             fontsize=11, fontweight='bold', color=CPROC_, transform=ax_.transAxes)
    ax_.text(0.5, y_-0.052,
             'Para a matriz 800×800, threads T=16 alcançaram speedup de 6,2×',
             ha='center', va='top', fontsize=10, color='#1e293b', transform=ax_.transAxes)
    ax_.text(0.5, y_-0.075,
             'reduzindo o tempo de 354 ms para 57 ms  —  redução de 84% no tempo de execução.',
             ha='center', va='top', fontsize=10, color='#1e293b', transform=ax_.transAxes)

    y_ -= h_dest_ + 0.04

    # Observações adicionais
    y_ = titulo_('Observações Adicionais', y_, cor_='#334155', size_=10)
    obs_ = [
        '• Localidade de cache: workers operam em linhas contíguas → menos cache misses.',
        '• Copy-on-write: fork() não copia fisicamente M1 e M2, apenas as páginas escritas → mitiga overhead.',
        '• Variabilidade: processos têm maior desvio padrão em matrizes pequenas (overhead variável do fork()).',
        '• Escalabilidade: o algoritmo escala bem até o limite do hardware (número de núcleos físicos).',
    ]
    for o_ in obs_:
        ax_.text(0.02, y_, o_, va='top', fontsize=8.5, color='#334155',
                 transform=ax_.transAxes)
        y_ -= 0.032

    salvar_(fig_, pdf_)

print("relatorio.pdf gerado com sucesso!")
