#!/usr/bin/env python3
# Gera os 7 slides da apresentação em PNG (1920x1080, 16:9);

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe
import numpy as np
from collections import defaultdict
import csv, os

# ── Paleta ───────────────────────────────────────────────────────────────────
DARK_   = '#0f172a'
BLUE_   = '#1a56db'
LIGHT_  = '#e0f2fe'
ACCENT_ = '#06b6d4'
WHITE_  = '#ffffff'
GRAY_   = '#94a3b8'
THR_    = '#e3a008'
PROC_   = '#057a55'
W, H    = 16, 9   # proporção A (figsize em polegadas * 120dpi = 1920x1080)

os.makedirs('slides', exist_ok=True)

def salvar_(fig_, nome_):
    fig_.savefig(f'slides/{nome_}', dpi=120, bbox_inches='tight',
                 facecolor=fig_.get_facecolor())
    plt.close(fig_)
    print(f'  Slide salvo: slides/{nome_}')

def nova_fig_():
    fig_ = plt.figure(figsize=(W, H))
    fig_.patch.set_facecolor(DARK_)
    return fig_

def barra_topo_(fig_, texto_esq_='', texto_dir_='Gabriel Aires · 20240078874'):
    ax_ = fig_.add_axes([0, 0.93, 1, 0.07])
    ax_.set_facecolor(BLUE_)
    ax_.axis('off')
    ax_.text(0.015, 0.5, texto_esq_, va='center', ha='left', color=WHITE_,
             fontsize=12, fontweight='bold', transform=ax_.transAxes)
    ax_.text(0.985, 0.5, texto_dir_, va='center', ha='right', color=LIGHT_,
             fontsize=11, transform=ax_.transAxes)
    return ax_

def barra_base_(fig_, texto_='IMD0036 – Sistemas Operacionais  ·  UFRN / IMD  ·  github.com/GabrielAirex'):
    ax_ = fig_.add_axes([0, 0, 1, 0.05])
    ax_.set_facecolor('#1e293b')
    ax_.axis('off')
    ax_.text(0.5, 0.5, texto_, va='center', ha='center', color=GRAY_,
             fontsize=10, transform=ax_.transAxes)

def numero_slide_(fig_, n_, total_=7):
    ax_ = fig_.add_axes([0.93, 0, 0.07, 0.05])
    ax_.set_facecolor('#1e293b')
    ax_.axis('off')
    ax_.text(0.5, 0.5, f'{n_}/{total_}', va='center', ha='center',
             color=GRAY_, fontsize=10, transform=ax_.transAxes)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 1 – CAPA
# ════════════════════════════════════════════════════════════════════════════
print('Gerando Slide 1 – Capa...')
fig_ = nova_fig_()

# fundo gradiente
ax_bg_ = fig_.add_axes([0, 0, 1, 1])
ax_bg_.set_facecolor(DARK_)
ax_bg_.axis('off')
for i_, a_ in enumerate(np.linspace(0, 0.4, 50)):
    ax_bg_.add_patch(plt.Rectangle((0, i_/50), 1, 1/50,
                     transform=ax_bg_.transAxes, color=ACCENT_, alpha=a_))

# linha decorativa
ax_bg_.add_patch(plt.Rectangle((0.08, 0.44), 0.84, 0.004,
                 transform=ax_bg_.transAxes, color=ACCENT_, alpha=0.6))

# logos
for x_, txt_ in [(0.30, 'UFRN'), (0.70, 'IMD')]:
    ax_bg_.text(x_, 0.82, txt_, ha='center', va='center', fontsize=52,
                fontweight='bold', color=WHITE_,
                path_effects=[pe.withStroke(linewidth=3, foreground=BLUE_)],
                transform=ax_bg_.transAxes)

ax_bg_.text(0.5, 0.70, 'Trabalho Prático – Unidade 1',
            ha='center', va='center', fontsize=36, fontweight='bold',
            color=WHITE_, transform=ax_bg_.transAxes)
ax_bg_.text(0.5, 0.61, 'Processos e Threads',
            ha='center', va='center', fontsize=28, color=LIGHT_,
            transform=ax_bg_.transAxes)
ax_bg_.text(0.5, 0.53, 'Multiplicação de Matrizes Paralela em C++',
            ha='center', va='center', fontsize=18, color=ACCENT_, style='italic',
            transform=ax_bg_.transAxes)

infos_ = [
    ('Aluno',      'Gabriel Afonso Freitas Aires'),
    ('Matrícula',  '20240078874'),
    ('Curso',      'Engenharia de Computação / CT – Natal – Bacharelado'),
    ('Disciplina', 'IMD0036 – Sistemas Operacionais · Abril 2026'),
    ('GitHub',     'github.com/GabrielAirex'),
]
y0_ = 0.38
for label_, val_ in infos_:
    ax_bg_.text(0.35, y0_, label_ + ':', ha='right', va='center',
                fontsize=14, color=ACCENT_, fontweight='bold',
                transform=ax_bg_.transAxes)
    ax_bg_.text(0.37, y0_, val_, ha='left', va='center',
                fontsize=14, color=WHITE_, transform=ax_bg_.transAxes)
    y0_ -= 0.068

salvar_(fig_, '01_capa.png')

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 2 – O QUE FOI IMPLEMENTADO
# ════════════════════════════════════════════════════════════════════════════
print('Gerando Slide 2 – Implementação...')
fig_ = nova_fig_()
barra_topo_(fig_, 'O que foi implementado')
barra_base_(fig_)
numero_slide_(fig_, 2)

ax_ = fig_.add_axes([0.04, 0.07, 0.92, 0.83])
ax_.set_facecolor(DARK_)
ax_.axis('off')

ax_.text(0.5, 0.95, 'Quatro programas implementados em C++',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=WHITE_, transform=ax_.transAxes)

progs_ = [
    ('01', 'auxiliar',           BLUE_,   '#1e40af',
     'Recebe n1, m1, n2, m2 pela linha de comando\n'
     'Gera M1 (n1×m1) e M2 (n2×m2) aleatórias\n'
     'Salva em matrix1.txt e matrix2.txt'),
    ('02', 'sequencial',         '#7c3aed','#4c1d95',
     'Lê M1 e M2 dos arquivos\n'
     'Multiplicação clássica com 3 loops aninhados O(n³)\n'
     'Salva resultado + tempo no arquivo de saída (baseline)'),
    ('03', 'paralelo_threads',   THR_,    '#78350f',
     'Matrizes lidas ANTES de criar as threads\n'
     'Cada thread calcula N/T linhas da matriz C\n'
     'Gera T arquivos de resultado com tempo individual'),
    ('04', 'paralelo_processos', PROC_,   '#14532d',
     'Matrizes lidas ANTES do fork()\n'
     'P processos filho via fork(), cada um com N/P linhas\n'
     'Cada filho salva 1 arquivo; pai espera com waitpid()'),
]

xs_ = [0.01, 0.26, 0.51, 0.76]
for (num_, nome_, cor_, escuro_, desc_), x_ in zip(progs_, xs_):
    # card
    ax_.add_patch(FancyBboxPatch((x_, 0.05), 0.235, 0.80,
                  boxstyle='round,pad=0.02', facecolor=cor_, edgecolor='none',
                  alpha=0.18, transform=ax_.transAxes))
    ax_.add_patch(FancyBboxPatch((x_, 0.73), 0.235, 0.12,
                  boxstyle='round,pad=0.02', facecolor=cor_,
                  edgecolor='none', transform=ax_.transAxes))
    ax_.text(x_+0.118, 0.795, num_, ha='center', va='center',
             fontsize=28, fontweight='bold', color=WHITE_,
             transform=ax_.transAxes, alpha=0.3)
    ax_.text(x_+0.118, 0.795, nome_, ha='center', va='center',
             fontsize=14, fontweight='bold', color=WHITE_,
             transform=ax_.transAxes)
    for i_, linha_ in enumerate(desc_.split('\n')):
        ax_.text(x_+0.015, 0.67 - i_*0.14, '▸  ' + linha_,
                 va='top', ha='left', fontsize=10.5, color=WHITE_,
                 transform=ax_.transAxes, alpha=0.9, wrap=True)

salvar_(fig_, '02_implementacao.png')

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3 – ESTRATÉGIA DE PARALELIZAÇÃO
# ════════════════════════════════════════════════════════════════════════════
print('Gerando Slide 3 – Estratégia...')
fig_ = nova_fig_()
barra_topo_(fig_, 'Estratégia de Paralelização')
barra_base_(fig_)
numero_slide_(fig_, 3)

ax_ = fig_.add_axes([0.04, 0.07, 0.92, 0.83])
ax_.set_facecolor(DARK_)
ax_.axis('off')

ax_.text(0.5, 0.95, 'Como o trabalho é dividido entre os workers',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=WHITE_, transform=ax_.transAxes)

# Diagrama de divisão de linhas
n_linhas_ = 8
cores_w_  = [BLUE_, THR_, PROC_, '#7c3aed']
for i_ in range(n_linhas_):
    cor_ = cores_w_[i_ // 2] if i_ < 8 else GRAY_
    ax_.add_patch(FancyBboxPatch((0.05, 0.55 + i_*0.038), 0.38, 0.032,
                  boxstyle='round,pad=0.003', facecolor=cor_, alpha=0.85,
                  edgecolor='none', transform=ax_.transAxes))
    label_ = f'Linha {i_+1}'
    ax_.text(0.24, 0.566 + i_*0.038, label_, ha='center', va='center',
             fontsize=10, color=WHITE_, fontweight='bold',
             transform=ax_.transAxes)

ax_.text(0.24, 0.88, 'Matriz Resultado C (N linhas)', ha='center',
         fontsize=13, fontweight='bold', color=WHITE_, transform=ax_.transAxes)

for i_, (label_, cor_) in enumerate([('Worker 0\n(T=4)', BLUE_), ('Worker 1', THR_),
                                       ('Worker 2', PROC_), ('Worker 3', '#7c3aed')]):
    y_w_ = 0.56 + i_*0.076
    ax_.annotate('', xy=(0.54, y_w_+0.025), xytext=(0.43, y_w_+0.025),
                 xycoords='axes fraction', textcoords='axes fraction',
                 arrowprops=dict(arrowstyle='->', color=cor_, lw=2.5))
    ax_.add_patch(FancyBboxPatch((0.55, y_w_), 0.18, 0.055,
                  boxstyle='round,pad=0.01', facecolor=cor_, alpha=0.85,
                  edgecolor='none', transform=ax_.transAxes))
    ax_.text(0.64, y_w_+0.027, label_, ha='center', va='center',
             fontsize=11, fontweight='bold', color=WHITE_,
             transform=ax_.transAxes)
    ax_.text(0.78, y_w_+0.027, 'N/T linhas', ha='left', va='center',
             fontsize=10, color=LIGHT_, transform=ax_.transAxes)

# bullets explicativos
bullets_ = [
    (BLUE_,  'Independência dos Dados: c_ij depende só da linha i de M1 e coluna j de M2'),
    (THR_,   'Threads: compartilham M1 e M2 na memória — sem mutex, sem cópia'),
    (PROC_,  'Processos: fork() com copy-on-write — dados só copiados se escritos'),
    (ACCENT_,'Distribuição: linhas_por_worker = N÷T  |  resto distribuído às primeiras workers'),
]
for i_, (cor_, txt_) in enumerate(bullets_):
    y_b_ = 0.40 - i_*0.095
    ax_.add_patch(plt.Circle((0.04, y_b_+0.014), 0.012, color=cor_,
                  transform=ax_.transAxes, zorder=3))
    ax_.text(0.065, y_b_+0.014, txt_, va='center', ha='left',
             fontsize=12, color=WHITE_, transform=ax_.transAxes)

salvar_(fig_, '03_estrategia.png')

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4 – RESULTADOS (gráfico 800x800)
# ════════════════════════════════════════════════════════════════════════════
print('Gerando Slide 4 – Resultados...')

dados_ = defaultdict(list)
with open('resultados.csv') as f_:
    for row_ in csv.DictReader(f_):
        k_ = (int(row_['tamanho']), row_['tipo'], int(row_['param']))
        dados_[k_].append(int(row_['tempo_us']))
def med_(k_): v_=dados_.get(k_,[]); return sum(v_)/len(v_) if v_ else 0

TAM_ = [100,200,400,800]; PAR_ = [2,4,8,16]

fig_ = nova_fig_()
barra_topo_(fig_, 'Resultados dos Experimentos')
barra_base_(fig_)
numero_slide_(fig_, 4)

ax_info_ = fig_.add_axes([0.04, 0.75, 0.92, 0.15])
ax_info_.set_facecolor(DARK_)
ax_info_.axis('off')
ax_info_.text(0.5, 0.8, '10 execuções por configuração  ·  Matrizes: 100×100 até 800×800',
              ha='center', va='center', fontsize=14, color=LIGHT_,
              transform=ax_info_.transAxes)

# grafico principal 800x800
ax_ = fig_.add_axes([0.07, 0.10, 0.55, 0.62])
ax_.set_facecolor('#1e293b')
seq_s_ = med_((800,'sequencial',1))/1e3
thr_s_ = [med_((800,'threads',p_))/1e3 for p_ in PAR_]
prc_s_ = [med_((800,'processos',p_))/1e3 for p_ in PAR_]

ax_.plot(PAR_,[seq_s_]*4,'--o',color=BLUE_, label='Sequencial',lw=2.5,ms=9,zorder=3)
ax_.plot(PAR_,thr_s_,'-s',color=THR_,label='Threads',lw=2.5,ms=10,zorder=3)
ax_.plot(PAR_,prc_s_,'-^',color=PROC_,label='Processos',lw=2.5,ms=10,zorder=3)
ax_.fill_between(PAR_,thr_s_,alpha=0.12,color=THR_)
ax_.fill_between(PAR_,prc_s_,alpha=0.12,color=PROC_)
ax_.set_title('Tempo Médio – Matriz 800×800', fontsize=14, fontweight='bold',
              color=WHITE_, pad=10)
ax_.set_xlabel('Número de Threads / Processos', fontsize=12, color=LIGHT_)
ax_.set_ylabel('Tempo (milissegundos)', fontsize=12, color=LIGHT_)
ax_.set_xticks(PAR_)
ax_.tick_params(colors=LIGHT_)
ax_.legend(fontsize=11, facecolor='#334155', labelcolor=WHITE_)
ax_.grid(True,linestyle='--',alpha=0.3,color=GRAY_)
for spine_ in ax_.spines.values(): spine_.set_color('#334155')

# tabela de destaques
ax_t_ = fig_.add_axes([0.64, 0.10, 0.33, 0.62])
ax_t_.set_facecolor(DARK_)
ax_t_.axis('off')
ax_t_.text(0.5, 0.97, 'Destaques — 800×800', ha='center', va='top',
           fontsize=14, fontweight='bold', color=WHITE_, transform=ax_t_.transAxes)

linhas_tab_ = [
    ('Sequencial',    f'{seq_s_:.1f} ms',   '1,0×',  BLUE_),
    ('Threads T=2',   f'{thr_s_[0]:.1f} ms', f'{seq_s_/thr_s_[0]:.1f}×', THR_),
    ('Threads T=4',   f'{thr_s_[1]:.1f} ms', f'{seq_s_/thr_s_[1]:.1f}×', THR_),
    ('Threads T=8',   f'{thr_s_[2]:.1f} ms', f'{seq_s_/thr_s_[2]:.1f}×', THR_),
    ('Threads T=16',  f'{thr_s_[3]:.1f} ms', f'{seq_s_/thr_s_[3]:.1f}×', THR_),
    ('Processos P=2', f'{prc_s_[0]:.1f} ms', f'{seq_s_/prc_s_[0]:.1f}×', PROC_),
    ('Processos P=8', f'{prc_s_[2]:.1f} ms', f'{seq_s_/prc_s_[2]:.1f}×', PROC_),
    ('Processos P=16',f'{prc_s_[3]:.1f} ms', f'{seq_s_/prc_s_[3]:.1f}×', PROC_),
]
for i_, (cfg_, t_, sp_, cor_) in enumerate(linhas_tab_):
    y_r_ = 0.87 - i_*0.108
    bg_  = '#1e293b' if i_%2==0 else '#0f172a'
    ax_t_.add_patch(plt.Rectangle((0, y_r_-0.07), 1, 0.10,
                    facecolor=bg_, edgecolor='none', transform=ax_t_.transAxes))
    ax_t_.add_patch(plt.Rectangle((0, y_r_-0.07), 0.03, 0.10,
                    facecolor=cor_, edgecolor='none', transform=ax_t_.transAxes))
    ax_t_.text(0.06, y_r_-0.012, cfg_, va='center', fontsize=10,
               color=WHITE_, transform=ax_t_.transAxes)
    ax_t_.text(0.68, y_r_-0.012, t_, va='center', ha='center', fontsize=10,
               color=LIGHT_, transform=ax_t_.transAxes)
    ax_t_.text(0.93, y_r_-0.012, sp_, va='center', ha='center', fontsize=11,
               color=cor_, fontweight='bold', transform=ax_t_.transAxes)

salvar_(fig_, '04_resultados.png')

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 5 – SPEEDUP COMPARATIVO (todos os tamanhos)
# ════════════════════════════════════════════════════════════════════════════
print('Gerando Slide 5 – Speedup...')
fig_ = nova_fig_()
barra_topo_(fig_, 'Análise de Speedup')
barra_base_(fig_)
numero_slide_(fig_, 5)

for idx_, tam_ in enumerate(TAM_):
    col_ = idx_ % 2
    row_ = idx_ // 2
    ax_ = fig_.add_axes([0.06 + col_*0.49, 0.10 + (1-row_)*0.40, 0.43, 0.33])
    ax_.set_facecolor('#1e293b')
    seq_ = med_((tam_,'sequencial',1))
    thr_sp_  = [seq_/med_((tam_,'threads',  p_)) for p_ in PAR_]
    prc_sp_  = [seq_/med_((tam_,'processos',p_)) for p_ in PAR_]
    ax_.plot(PAR_,PAR_,'--',color=GRAY_,label='Ideal',lw=1.5)
    ax_.plot(PAR_,thr_sp_,'-s',color=THR_, label='Threads',  lw=2.2,ms=7)
    ax_.plot(PAR_,prc_sp_,'-^',color=PROC_,label='Processos',lw=2.2,ms=7)
    ax_.set_title(f'Speedup – {tam_}×{tam_}', fontsize=12, fontweight='bold', color=WHITE_, pad=6)
    ax_.set_xlabel('T / P', fontsize=10, color=LIGHT_)
    ax_.set_ylabel('Speedup', fontsize=10, color=LIGHT_)
    ax_.set_xticks(PAR_)
    ax_.tick_params(colors=LIGHT_, labelsize=9)
    ax_.legend(fontsize=9, facecolor='#334155', labelcolor=WHITE_)
    ax_.grid(True,linestyle='--',alpha=0.3,color=GRAY_)
    for spine_ in ax_.spines.values(): spine_.set_color('#334155')

ax_tit_ = fig_.add_axes([0.04, 0.76, 0.92, 0.14])
ax_tit_.axis('off')
ax_tit_.set_facecolor(DARK_)
ax_tit_.text(0.5, 0.6, 'Speedup nunca linear — confirma a Lei de Amdahl',
             ha='center', va='center', fontsize=18, fontweight='bold',
             color=WHITE_, transform=ax_tit_.transAxes)
ax_tit_.text(0.5, 0.15,
             'Porção serial (leitura/escrita de arquivos) limita o ganho máximo  ·  '
             'Acima do nº de núcleos, workers disputam CPU por time-slicing',
             ha='center', va='center', fontsize=12, color=LIGHT_,
             transform=ax_tit_.transAxes)

salvar_(fig_, '05_speedup.png')

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 6 – DISCUSSÃO
# ════════════════════════════════════════════════════════════════════════════
print('Gerando Slide 6 – Discussão...')
fig_ = nova_fig_()
barra_topo_(fig_, 'Discussão dos Resultados')
barra_base_(fig_)
numero_slide_(fig_, 6)

ax_ = fig_.add_axes([0.04, 0.07, 0.92, 0.83])
ax_.set_facecolor(DARK_)
ax_.axis('off')

ax_.text(0.5, 0.96, 'Por que esses resultados? Qual o T e P ideais?',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color=WHITE_, transform=ax_.transAxes)

blocos_ = [
    (BLUE_,   '0:00',  'Threads > Processos em matrizes médias',
     'Threads compartilham memória — sem cópia de dados, sem overhead de fork().\n'
     'Em 800×800 com 16 workers, ambos se equiparam (overhead amortizado).'),
    (THR_,    '⚠',     'Speedup não linear — Lei de Amdahl',
     'Porção serial irredutível (I/O, criação de workers) limita o ganho.\n'
     'Speedup máximo observado: 6,2× com 16 threads  vs.  ideal de 16×.'),
    (PROC_,   '✓',     'T ideal = 8 para Threads',
     'Melhor relação speedup/eficiência. T=16 traz apenas ganho marginal\n'
     'com eficiência ~44%  →  workers extras disputam os mesmos núcleos.'),
    (ACCENT_, '✓',     'P ideal = 8 para Processos',
     'Overhead do fork() maior que threads. P=8 mais estável.\n'
     'P=16 equipara-se a threads só em matrizes grandes (overhead amortizado).'),
]

for i_, (cor_, icon_, titulo_, desc_) in enumerate(blocos_):
    y_b_ = 0.75 - i_*0.205
    ax_.add_patch(FancyBboxPatch((0.01, y_b_-0.12), 0.97, 0.155,
                  boxstyle='round,pad=0.015', facecolor=cor_, alpha=0.15,
                  edgecolor=cor_, linewidth=2, transform=ax_.transAxes))
    ax_.add_patch(FancyBboxPatch((0.01, y_b_+0.02), 0.03, 0.115,
                  boxstyle='round,pad=0.005', facecolor=cor_, edgecolor='none',
                  transform=ax_.transAxes))
    ax_.text(0.025, y_b_+0.077, icon_, ha='center', va='center',
             fontsize=16, color=WHITE_, fontweight='bold', transform=ax_.transAxes)
    ax_.text(0.06, y_b_+0.09, titulo_, va='top', ha='left', fontsize=14,
             fontweight='bold', color=WHITE_, transform=ax_.transAxes)
    for j_, linha_ in enumerate(desc_.split('\n')):
        ax_.text(0.06, y_b_+0.055-j_*0.045, linha_, va='top', ha='left',
                 fontsize=11.5, color=LIGHT_, transform=ax_.transAxes)

salvar_(fig_, '06_discussao.png')

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 7 – CONCLUSÃO + ENCERRAMENTO
# ════════════════════════════════════════════════════════════════════════════
print('Gerando Slide 7 – Conclusão...')
fig_ = nova_fig_()
barra_topo_(fig_, 'Conclusão')
barra_base_(fig_)
numero_slide_(fig_, 7)

ax_ = fig_.add_axes([0.04, 0.07, 0.92, 0.83])
ax_.set_facecolor(DARK_)
ax_.axis('off')

ax_.text(0.5, 0.97, 'Conclusões Principais', ha='center', va='top',
         fontsize=22, fontweight='bold', color=WHITE_, transform=ax_.transAxes)

pontos_ = [
    (BLUE_,  'Paralelismo traz ganhos reais para problemas com\nIndependência dos Dados (como multiplicação de matrizes)'),
    (THR_,   'Threads mais eficientes que processos para\ndados compartilhados — sem overhead de cópia'),
    (PROC_,  'Ganho nunca linear — Lei de Amdahl sempre presente\n(porção serial limita speedup máximo)'),
    (ACCENT_,'Valor ideal: T = P ≈ número de núcleos lógicos da CPU\n(neste experimento: T=8, P=8 melhor equilíbrio)'),
]
for i_, (cor_, txt_) in enumerate(pontos_):
    y_p_ = 0.80 - i_*0.175
    ax_.add_patch(plt.Circle((0.035, y_p_+0.015), 0.022,
                  color=cor_, transform=ax_.transAxes, zorder=3))
    ax_.text(0.035, y_p_+0.015, str(i_+1), ha='center', va='center',
             fontsize=13, fontweight='bold', color=WHITE_, transform=ax_.transAxes)
    for j_, linha_ in enumerate(txt_.split('\n')):
        ax_.text(0.075, y_p_+0.02-j_*0.06, linha_, va='top', ha='left',
                 fontsize=13.5, color=WHITE_ if j_==0 else LIGHT_,
                 fontweight='bold' if j_==0 else 'normal',
                 transform=ax_.transAxes)

# Destaque resultado principal
ax_.add_patch(FancyBboxPatch((0.05, 0.04), 0.90, 0.115,
              boxstyle='round,pad=0.015', facecolor=PROC_, alpha=0.2,
              edgecolor=PROC_, linewidth=2.5, transform=ax_.transAxes))
seq_800_ = med_((800,'sequencial',1))/1e3
thr_800_ = med_((800,'threads',16))/1e3
reducao_ = (1 - thr_800_/seq_800_)*100
ax_.text(0.5, 0.115, f'Resultado Principal — Matriz 800×800  ·  Threads T=16',
         ha='center', va='center', fontsize=13, fontweight='bold',
         color=WHITE_, transform=ax_.transAxes)
ax_.text(0.5, 0.068,
         f'{seq_800_:.0f} ms  →  {thr_800_:.0f} ms   '
         f'|   Speedup: {seq_800_/thr_800_:.1f}×   '
         f'|   Redução de {reducao_:.0f}% no tempo de execução',
         ha='center', va='center', fontsize=13, color=LIGHT_,
         transform=ax_.transAxes)

salvar_(fig_, '07_conclusao.png')

print('\nTodos os slides gerados em ./slides/')
print('Ordem para o vídeo:')
for f_ in sorted(os.listdir('slides')):
    print(f'  {f_}')
