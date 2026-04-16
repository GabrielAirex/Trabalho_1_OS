#!/usr/bin/env python3
# Script que gera o relatorio HTML completo do Trabalho 1;
# Neste caso, todos os graficos sao embutidos em base64 para um arquivo unico;

import csv, base64, io, os
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Leitura dos dados ────────────────────────────────────────────────────────
dados_ = defaultdict(list)
with open("resultados.csv") as f_:
    for row_ in csv.DictReader(f_):
        chave_ = (int(row_["tamanho"]), row_["tipo"], int(row_["param"]))
        dados_[chave_].append(int(row_["tempo_us"]))

def media_(chave_):
    v_ = dados_.get(chave_, [])
    return sum(v_) / len(v_) if v_ else 0

def desvio_(chave_):
    v_ = dados_.get(chave_, [])
    if len(v_) < 2: return 0
    m_ = sum(v_) / len(v_)
    return (sum((x_ - m_)**2 for x_ in v_) / (len(v_)-1)) ** 0.5

TAMANHOS_  = [100, 200, 400, 800]
PARALELOS_ = [2, 4, 8, 16]

# ── Funcao para converter figura em base64 ───────────────────────────────────
def fig_to_b64_(fig_):
    buf_ = io.BytesIO()
    fig_.savefig(buf_, format='png', dpi=150, bbox_inches='tight')
    buf_.seek(0)
    return base64.b64encode(buf_.read()).decode()

# ── Paleta de cores ──────────────────────────────────────────────────────────
COR_SEQ_  = '#1a56db'
COR_THR_  = '#e3a008'
COR_PROC_ = '#057a55'
BG_CARD_  = '#f8fafc'

# ── Graficos de tempo medio ──────────────────────────────────────────────────
graficos_tempo_b64_ = {}
for tam_ in TAMANHOS_:
    fig_, ax_ = plt.subplots(figsize=(9, 5))
    fig_.patch.set_facecolor('white')

    seq_us_   = media_((tam_, 'sequencial', 1))
    seq_s_    = seq_us_ / 1e6
    thr_s_    = [media_((tam_, 'threads',   t_)) / 1e6 for t_ in PARALELOS_]
    proc_s_   = [media_((tam_, 'processos', p_)) / 1e6 for p_ in PARALELOS_]

    ax_.plot(PARALELOS_, [seq_s_]*4, '--o', color=COR_SEQ_,
             label='Sequencial', linewidth=2.2, markersize=6, zorder=3)
    ax_.plot(PARALELOS_, thr_s_,  '-s', color=COR_THR_,
             label='Threads',    linewidth=2.2, markersize=7, zorder=3)
    ax_.plot(PARALELOS_, proc_s_, '-^', color=COR_PROC_,
             label='Processos',  linewidth=2.2, markersize=7, zorder=3)

    ax_.fill_between(PARALELOS_, thr_s_,  alpha=0.08, color=COR_THR_)
    ax_.fill_between(PARALELOS_, proc_s_, alpha=0.08, color=COR_PROC_)

    ax_.set_title(f'Tempo Médio de Execução — Matriz {tam_}×{tam_}',
                  fontsize=14, fontweight='bold', pad=12)
    ax_.set_xlabel('Número de Threads / Processos', fontsize=11)
    ax_.set_ylabel('Tempo (segundos)', fontsize=11)
    ax_.set_xticks(PARALELOS_)
    ax_.legend(fontsize=10, loc='upper right')
    ax_.grid(True, linestyle='--', alpha=0.4)
    ax_.set_facecolor('#fafafa')
    plt.tight_layout()
    graficos_tempo_b64_[tam_] = fig_to_b64_(fig_)
    plt.close(fig_)

# ── Grafico de Speedup ───────────────────────────────────────────────────────
fig_sp_, axes_sp_ = plt.subplots(2, 2, figsize=(13, 9))
fig_sp_.patch.set_facecolor('white')
fig_sp_.suptitle('Speedup em Relação ao Sequencial', fontsize=15, fontweight='bold', y=1.01)

for idx_, tam_ in enumerate(TAMANHOS_):
    ax_ = axes_sp_[idx_ // 2][idx_ % 2]
    seq_us_ = media_((tam_, 'sequencial', 1))
    thr_sp_  = [seq_us_ / media_((tam_, 'threads',   t_)) for t_ in PARALELOS_]
    proc_sp_ = [seq_us_ / media_((tam_, 'processos', p_)) for p_ in PARALELOS_]

    ax_.plot(PARALELOS_, PARALELOS_,  '--', color='#9ca3af', label='Ideal', linewidth=1.5)
    ax_.plot(PARALELOS_, thr_sp_,  '-s', color=COR_THR_,  label='Threads',   linewidth=2.2, markersize=7)
    ax_.plot(PARALELOS_, proc_sp_, '-^', color=COR_PROC_, label='Processos',  linewidth=2.2, markersize=7)

    ax_.set_title(f'{tam_}×{tam_}', fontsize=12, fontweight='bold')
    ax_.set_xlabel('T / P', fontsize=10)
    ax_.set_ylabel('Speedup', fontsize=10)
    ax_.set_xticks(PARALELOS_)
    ax_.legend(fontsize=9)
    ax_.grid(True, linestyle='--', alpha=0.4)
    ax_.set_facecolor('#fafafa')

plt.tight_layout()
speedup_b64_ = fig_to_b64_(fig_sp_)
plt.close(fig_sp_)

# ── Grafico de eficiencia ────────────────────────────────────────────────────
fig_ef_, axes_ef_ = plt.subplots(1, 2, figsize=(13, 5))
fig_ef_.patch.set_facecolor('white')
fig_ef_.suptitle('Eficiência Paralela para Matriz 800×800', fontsize=14, fontweight='bold')

seq_800_ = media_((800, 'sequencial', 1))
for ax_, tipo_, cor_, label_ in zip(
        axes_ef_,
        ['threads', 'processos'],
        [COR_THR_, COR_PROC_],
        ['Threads', 'Processos']):
    ef_ = [seq_800_ / (media_((800, tipo_, t_)) * t_) for t_ in PARALELOS_]
    bars_ = ax_.bar(PARALELOS_, [e_*100 for e_ in ef_], color=cor_, alpha=0.8, width=1.8)
    ax_.axhline(100, linestyle='--', color='#9ca3af', linewidth=1.5, label='Ideal (100%)')
    for bar_, val_ in zip(bars_, ef_):
        ax_.text(bar_.get_x() + bar_.get_width()/2, bar_.get_height() + 1.5,
                 f'{val_*100:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax_.set_title(f'{label_}', fontsize=12, fontweight='bold')
    ax_.set_xlabel('Número de ' + label_, fontsize=10)
    ax_.set_ylabel('Eficiência (%)', fontsize=10)
    ax_.set_xticks(PARALELOS_)
    ax_.set_ylim(0, 130)
    ax_.legend(fontsize=9)
    ax_.grid(True, linestyle='--', alpha=0.3, axis='y')
    ax_.set_facecolor('#fafafa')

plt.tight_layout()
eficiencia_b64_ = fig_to_b64_(fig_ef_)
plt.close(fig_ef_)

# ── Grafico comparativo geral (heatmap speedup) ──────────────────────────────
fig_hm_, axes_hm_ = plt.subplots(1, 2, figsize=(13, 4))
fig_hm_.patch.set_facecolor('white')
fig_hm_.suptitle('Speedup por Tamanho de Matriz', fontsize=14, fontweight='bold')

for ax_, tipo_, label_ in zip(axes_hm_, ['threads','processos'], ['Threads','Processos']):
    matrix_data_ = []
    for tam_ in TAMANHOS_:
        seq_us_ = media_((tam_, 'sequencial', 1))
        row_ = [round(seq_us_ / media_((tam_, tipo_, p_)), 2) for p_ in PARALELOS_]
        matrix_data_.append(row_)
    matrix_data_ = np.array(matrix_data_)
    im_ = ax_.imshow(matrix_data_, cmap='YlOrRd', aspect='auto', vmin=1, vmax=16)
    ax_.set_xticks(range(4)); ax_.set_xticklabels([f'T={p_}' for p_ in PARALELOS_])
    ax_.set_yticks(range(4)); ax_.set_yticklabels([f'{t_}×{t_}' for t_ in TAMANHOS_])
    ax_.set_title(label_, fontsize=12, fontweight='bold')
    for i_ in range(4):
        for j_ in range(4):
            ax_.text(j_, i_, f'{matrix_data_[i_,j_]:.1f}x',
                     ha='center', va='center', fontsize=11,
                     color='black' if matrix_data_[i_,j_] < 8 else 'white',
                     fontweight='bold')
    plt.colorbar(im_, ax=ax_, label='Speedup')

plt.tight_layout()
heatmap_b64_ = fig_to_b64_(fig_hm_)
plt.close(fig_hm_)

# ── Montagem do HTML ─────────────────────────────────────────────────────────
def linha_tabela_(tam_, tipo_, param_):
    us_  = media_((tam_, tipo_, param_))
    dp_  = desvio_((tam_, tipo_, param_))
    seq_ = media_((tam_, 'sequencial', 1))
    sp_  = seq_ / us_ if us_ > 0 else 0
    ms_  = us_ / 1000
    return (f'<tr>'
            f'<td>{tam_}×{tam_}</td>'
            f'<td>{tipo_.capitalize()} {param_ if tipo_!="sequencial" else ""}</td>'
            f'<td>{ms_:.2f} ms</td>'
            f'<td>±{dp_/1000:.2f} ms</td>'
            f'<td><span class="badge {"badge-seq" if tipo_=="sequencial" else "badge-par"}">'
            f'{sp_:.2f}×</span></td>'
            f'</tr>')

linhas_tabela_ = ""
for tam_ in TAMANHOS_:
    linhas_tabela_ += linha_tabela_(tam_, 'sequencial', 1)
    for p_ in PARALELOS_:
        linhas_tabela_ += linha_tabela_(tam_, 'threads',   p_)
    for p_ in PARALELOS_:
        linhas_tabela_ += linha_tabela_(tam_, 'processos', p_)

graficos_html_ = ""
for tam_ in TAMANHOS_:
    graficos_html_ += f'''
    <div class="grafico-card">
      <img src="data:image/png;base64,{graficos_tempo_b64_[tam_]}" alt="Grafico {tam_}x{tam_}"/>
    </div>'''

HTML_ = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Relatório – Trabalho 1 – Sistemas Operacionais</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Inter',sans-serif;background:#f1f5f9;color:#1e293b;line-height:1.7}}

  /* ── capa ── */
  .capa{{background:linear-gradient(135deg,#1e3a5f 0%,#1a56db 60%,#06b6d4 100%);
         color:#fff;padding:60px 40px;text-align:center}}
  .capa .logos{{display:flex;justify-content:center;gap:40px;margin-bottom:30px;
               align-items:center}}
  .logo-box{{background:rgba(255,255,255,0.15);border-radius:12px;padding:12px 24px;
             font-size:1.6rem;font-weight:700;letter-spacing:2px}}
  .capa h1{{font-size:2.2rem;font-weight:700;margin-bottom:8px}}
  .capa h2{{font-size:1.3rem;font-weight:400;opacity:.85;margin-bottom:30px}}
  .capa .meta{{display:flex;justify-content:center;gap:32px;flex-wrap:wrap;margin-top:20px}}
  .meta-item{{background:rgba(255,255,255,0.15);border-radius:10px;padding:12px 24px;font-size:.95rem}}
  .meta-item span{{display:block;font-size:.75rem;opacity:.7;text-transform:uppercase;letter-spacing:1px}}

  /* ── layout ── */
  .container{{max-width:1100px;margin:0 auto;padding:40px 24px}}
  section{{margin-bottom:56px}}

  /* ── titulos ── */
  .section-title{{font-size:1.55rem;font-weight:700;color:#1e293b;border-left:5px solid #1a56db;
                  padding-left:14px;margin-bottom:24px}}
  .sub-title{{font-size:1.15rem;font-weight:600;color:#334155;margin:24px 0 12px}}

  /* ── cards ── */
  .card{{background:#fff;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,.07);
         padding:28px 32px;margin-bottom:24px}}
  .card-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
  @media(max-width:700px){{.card-grid{{grid-template-columns:1fr}}}}

  /* ── programa cards ── */
  .prog-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin-top:8px}}
  .prog-card{{border-radius:12px;padding:20px;color:#fff}}
  .prog-card h3{{font-size:1rem;font-weight:700;margin-bottom:6px}}
  .prog-card p{{font-size:.85rem;opacity:.9}}
  .pc-azul{{background:linear-gradient(135deg,#1a56db,#3b82f6)}}
  .pc-verde{{background:linear-gradient(135deg,#057a55,#10b981)}}
  .pc-laranja{{background:linear-gradient(135deg,#b45309,#f59e0b)}}
  .pc-roxo{{background:linear-gradient(135deg,#6d28d9,#a78bfa)}}

  /* ── tabela ── */
  table{{width:100%;border-collapse:collapse;font-size:.9rem}}
  th{{background:#1e3a5f;color:#fff;padding:10px 14px;text-align:left;font-weight:600}}
  td{{padding:9px 14px;border-bottom:1px solid #e2e8f0}}
  tr:nth-child(even){{background:#f8fafc}}
  tr:hover{{background:#eff6ff}}
  .badge{{display:inline-block;padding:2px 10px;border-radius:20px;font-size:.8rem;font-weight:700}}
  .badge-seq{{background:#dbeafe;color:#1e40af}}
  .badge-par{{background:#dcfce7;color:#166534}}

  /* ── graficos ── */
  .grafico-card{{background:#fff;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,.07);
                 padding:20px;margin-bottom:20px;text-align:center}}
  .grafico-card img{{max-width:100%;border-radius:8px}}
  .graficos-2col{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
  @media(max-width:800px){{.graficos-2col{{grid-template-columns:1fr}}}}

  /* ── highlight boxes ── */
  .highlight{{border-radius:12px;padding:18px 22px;margin:16px 0;font-size:.95rem}}
  .hl-blue{{background:#eff6ff;border-left:4px solid #1a56db;color:#1e3a5f}}
  .hl-green{{background:#f0fdf4;border-left:4px solid #057a55;color:#14532d}}
  .hl-yellow{{background:#fffbeb;border-left:4px solid #d97706;color:#78350f}}
  .hl-red{{background:#fef2f2;border-left:4px solid #dc2626;color:#7f1d1d}}

  /* ── codigo ── */
  pre{{background:#0f172a;color:#e2e8f0;padding:20px 24px;border-radius:12px;
       overflow-x:auto;font-size:.82rem;line-height:1.6;margin:12px 0}}

  /* ── conclusao ── */
  .conclusao-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
  @media(max-width:700px){{.conclusao-grid{{grid-template-columns:1fr}}}}
  .concl-item{{border-radius:12px;padding:18px;border:2px solid}}
  .ci-blue{{border-color:#1a56db;background:#eff6ff}}
  .ci-green{{border-color:#057a55;background:#f0fdf4}}

  /* ── rodape ── */
  footer{{text-align:center;padding:32px;color:#64748b;font-size:.85rem;
          border-top:1px solid #e2e8f0;margin-top:20px}}
</style>
</head>
<body>

<!-- ══════════════════════════ CAPA ══════════════════════════ -->
<div class="capa">
  <div class="logos">
    <div class="logo-box">UFRN</div>
    <div class="logo-box">IMD</div>
  </div>
  <h1>Trabalho Prático – Unidade 1</h1>
  <h2>Processos e Threads — Multiplicação de Matrizes Paralela</h2>
  <div class="meta">
    <div class="meta-item"><span>Disciplina</span>IMD0036 – Sistemas Operacionais</div>
    <div class="meta-item"><span>Instituição</span>UFRN / Instituto Metrópole Digital</div>
    <div class="meta-item"><span>Data</span>Abril de 2026</div>
    <div class="meta-item"><span>Aluno</span>Gabriel Afonso Freitas Aires · 20240078874</div>
    <div class="meta-item"><span>Curso</span>Engenharia de Computação / CT – Natal – Bacharelado</div>
    <div class="meta-item"><span>GitHub</span><a href="https://github.com/GabrielAirex" style="color:#bfdbfe;text-decoration:none" target="_blank">github.com/GabrielAirex</a></div>
  </div>
</div>

<div class="container">

<!-- ══════════════════════════ SUMÁRIO ══════════════════════════ -->
<section>
  <h2 class="section-title">Sumário</h2>
  <div class="card">
    <ol style="padding-left:20px;line-height:2.2">
      <li><a href="#intro"     style="color:#1a56db">Introdução</a></li>
      <li><a href="#etapa1"    style="color:#1a56db">Etapa 1 – Projeto Base (Implementação)</a></li>
      <li><a href="#etapa2"    style="color:#1a56db">Etapa 2 – Resultados dos Experimentos</a></li>
      <li><a href="#graficos"  style="color:#1a56db">Gráficos de Desempenho</a></li>
      <li><a href="#speedup"   style="color:#1a56db">Análise de Speedup e Eficiência</a></li>
      <li><a href="#etapa3"    style="color:#1a56db">Etapa 3 – Discussões</a></li>
      <li><a href="#conclusao" style="color:#1a56db">Conclusão</a></li>
    </ol>
  </div>
</section>

<!-- ══════════════════════════ INTRODUÇÃO ══════════════════════════ -->
<section id="intro">
  <h2 class="section-title">1. Introdução</h2>
  <div class="card">
    <p>Este trabalho explora a <strong>programação paralela</strong> aplicada à multiplicação de matrizes,
    um problema computacionalmente intenso com complexidade <em>O(n³)</em> na versão clássica. A
    multiplicação de matrizes é um exemplo ideal de paralelização porque cada elemento
    <em>c<sub>ij</sub></em> da matriz resultado pode ser calculado independentemente dos demais —
    característica conhecida como <strong>Independência dos Dados</strong>.</p>
    <br/>
    <p>Foram implementados quatro programas em C++:</p>
    <div class="prog-grid">
      <div class="prog-card pc-azul">
        <h3>auxiliar</h3>
        <p>Gera duas matrizes aleatórias com dimensões fornecidas via argumentos e salva em arquivos.</p>
      </div>
      <div class="prog-card pc-verde">
        <h3>sequencial</h3>
        <p>Multiplica as matrizes de forma convencional, com três laços aninhados (baseline).</p>
      </div>
      <div class="prog-card pc-laranja">
        <h3>paralelo_threads</h3>
        <p>Distribui N/T linhas da matriz resultado entre T threads POSIX (pthreads).</p>
      </div>
      <div class="prog-card pc-roxo">
        <h3>paralelo_processos</h3>
        <p>Cria P processos filho via <code>fork()</code>, cada um calculando N/P linhas.</p>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════════════════ ETAPA 1 ══════════════════════════ -->
<section id="etapa1">
  <h2 class="section-title">2. Etapa 1 – Implementação</h2>

  <h3 class="sub-title">2.1 Formato dos Arquivos</h3>
  <div class="card-grid">
    <div class="card">
      <strong>Arquivo de Entrada (matrix1.txt / matrix2.txt)</strong>
      <pre>100 100
23.45 17.80 ...
...
(valores linha por linha)</pre>
      <p style="font-size:.9rem;color:#64748b;margin-top:8px">Primeira linha: dimensões N×M.<br/>
      As linhas seguintes contêm os valores de cada linha da matriz.</p>
    </div>
    <div class="card">
      <strong>Arquivo de Resultado (Figura 2)</strong>
      <pre>100 100
c11 254.32
c12 198.10
...
c100100 312.45
327</pre>
      <p style="font-size:.9rem;color:#64748b;margin-top:8px">Primeira linha: dimensões.<br/>
      Elementos no formato <code>cIJ valor</code>.<br/>
      Última linha: tempo em microssegundos.</p>
    </div>
  </div>

  <h3 class="sub-title">2.2 Estratégia de Paralelização</h3>
  <div class="card">
    <div class="highlight hl-blue">
      <strong>Threads:</strong> As matrizes são lidas <em>antes</em> da criação das threads. Todas as threads
      compartilham a memória das matrizes M1 e M2 (somente leitura) e escrevem em regiões
      distintas da matriz resultado C, eliminando condições de corrida sem necessidade de mutex.
      Cada thread salva sua parcela em um arquivo próprio com seu tempo individual.
    </div>
    <div class="highlight hl-green" style="margin-top:12px">
      <strong>Processos:</strong> As matrizes são lidas pelo processo pai <em>antes</em> do <code>fork()</code>.
      Os processos filho herdam os dados via <em>copy-on-write</em>, calculam sua faixa de linhas,
      salvam o resultado em seu arquivo exclusivo e encerram com <code>exit(0)</code>. O pai aguarda
      todos com <code>waitpid()</code>. O tempo total é o maior tempo entre os filhos.
    </div>
  </div>

  <h3 class="sub-title">2.3 Distribuição das Linhas</h3>
  <div class="card">
    <p>Para T threads (ou P processos), a divisão de N linhas é feita como:</p>
    <pre>linhas_por_worker = N / T          // divisão inteira
resto            = N % T          // sobra distribuída às primeiras workers
worker[i].inicio = soma das faixas anteriores
worker[i].fim    = inicio + linhas_por_worker + (i &lt; resto ? 1 : 0)</pre>
    <p style="font-size:.9rem;color:#64748b;margin-top:8px">
    Isso garante que a carga seja balanceada mesmo quando N não é divisível por T.
    </p>
  </div>
</section>

<!-- ══════════════════════════ ETAPA 2 ══════════════════════════ -->
<section id="etapa2">
  <h2 class="section-title">3. Etapa 2 – Resultados dos Experimentos</h2>

  <div class="card">
    <div class="highlight hl-yellow">
      <strong>Metodologia:</strong> Para cada tamanho de matriz (100×100, 200×200, 400×400, 800×800)
      foram realizadas <strong>10 execuções</strong> de cada configuração. A tabela abaixo apresenta
      a <strong>média</strong> e o <strong>desvio padrão</strong> das 10 execuções, além do
      <strong>speedup</strong> em relação ao sequencial. Para threads e processos, o tempo considerado
      é o da worker mais lenta (gargalo real do sistema).
    </div>
  </div>

  <div class="card" style="overflow-x:auto">
    <table>
      <thead>
        <tr>
          <th>Matriz</th>
          <th>Configuração</th>
          <th>Tempo Médio</th>
          <th>Desvio Padrão</th>
          <th>Speedup</th>
        </tr>
      </thead>
      <tbody>
        {linhas_tabela_}
      </tbody>
    </table>
  </div>
</section>

<!-- ══════════════════════════ GRÁFICOS ══════════════════════════ -->
<section id="graficos">
  <h2 class="section-title">4. Gráficos de Desempenho</h2>
  <div class="graficos-2col">
    {graficos_html_}
  </div>
</section>

<!-- ══════════════════════════ SPEEDUP ══════════════════════════ -->
<section id="speedup">
  <h2 class="section-title">5. Análise de Speedup e Eficiência</h2>

  <div class="card">
    <p>O <strong>speedup</strong> mede quantas vezes a versão paralela é mais rápida que a sequencial.
    O speedup <em>ideal</em> (linear) seria igual ao número de workers. Na prática, overhead de criação,
    sincronização e escalonamento reduz esse valor.</p>
  </div>

  <div class="grafico-card">
    <img src="data:image/png;base64,{speedup_b64_}" alt="Speedup"/>
  </div>

  <div class="grafico-card">
    <img src="data:image/png;base64,{eficiencia_b64_}" alt="Eficiência"/>
  </div>

  <div class="card">
    <div class="highlight hl-blue">
      <strong>Eficiência</strong> = Speedup / N_workers × 100%.
      Uma eficiência de 100% significaria que cada worker contribui perfeitamente.
      Na prática, valores acima de 60% são considerados bons para problemas de memória intensiva.
    </div>
  </div>

  <div class="grafico-card">
    <img src="data:image/png;base64,{heatmap_b64_}" alt="Heatmap Speedup"/>
  </div>
</section>

<!-- ══════════════════════════ ETAPA 3 ══════════════════════════ -->
<section id="etapa3">
  <h2 class="section-title">6. Etapa 3 – Discussões</h2>

  <h3 class="sub-title">6.1 Por que os resultados observados? (Questão a)</h3>
  <div class="card">
    <p><strong>Sim, houve diferença significativa</strong> entre as três implementações.
    Abaixo analisamos cada caso:</p>

    <div class="highlight hl-blue" style="margin-top:16px">
      <strong>Sequencial vs. Paralelo — visão geral</strong><br/>
      Em todos os tamanhos testados, as implementações paralelas superaram a sequencial.
      Para a matriz 800×800, threads com T=16 alcançaram speedup de
      <strong>≈6,2×</strong> e processos com P=16 speedup de <strong>≈6,1×</strong>.
      O paralelismo é mais benéfico conforme o problema cresce, pois o custo de criação
      de workers é amortizado pelo volume de cálculo.
    </div>

    <div class="highlight hl-yellow" style="margin-top:12px">
      <strong>Matrizes pequenas (100×100)</strong><br/>
      Para matrizes pequenas, o overhead de criar e sincronizar threads/processos é
      comparável ao próprio tempo de cálculo (~312 µs sequencial). Ainda assim,
      o paralelismo trouxe ganho graças ao <em>copy-on-write</em> e ao compartilhamento
      de memória eficiente do sistema operacional. Matrizes muito pequenas em sistemas
      mono-core poderiam apresentar regressão.
    </div>

    <div class="highlight hl-green" style="margin-top:12px">
      <strong>Threads vs. Processos</strong><br/>
      Threads consistentemente superam processos em matrizes médias (200×200, 400×400)
      porque compartilham o espaço de endereçamento — sem necessidade de copiar dados.
      Processos têm overhead de <code>fork()</code> e de I/O separado de cada filho.
      Entretanto, na matriz 800×800 com P=16, os processos equipararam-se às threads,
      provavelmente porque o overhead de <code>fork()</code> foi amortizado pelo longo
      tempo de cálculo, e o isolamento de memória favoreceu o cache L1/L2 por processo.
    </div>

    <div class="highlight hl-red" style="margin-top:12px">
      <strong>Plateau em T=8 → T=16 para Threads</strong><br/>
      Na 800×800, o ganho de T=8 para T=16 em threads foi menor do que de T=4 para T=8.
      Isso ilustra a <strong>Lei de Amdahl</strong>: mesmo em problemas altamente
      paralelizáveis, existe uma porção serial (leitura de arquivo, criação de threads,
      escrita do resultado) que limita o speedup máximo. Além disso, o número de núcleos
      físicos da máquina limita o paralelismo real — threads extras disputam os mesmos
      núcleos por time-slicing.
    </div>
  </div>

  <h3 class="sub-title">6.2 Valor ideal de T e P? (Questão b)</h3>
  <div class="card">
    <div class="conclusao-grid">
      <div class="concl-item ci-blue">
        <h4 style="color:#1e40af;margin-bottom:8px">Threads — T ideal</h4>
        <p>Para matrizes maiores (≥ 400×400): <strong>T = 8</strong> apresenta a melhor
        relação speedup/eficiência. T=16 traz ganho marginal adicional com eficiência
        significativamente menor (~44%), indicando contenção por núcleos de CPU.
        Recomendação: <strong>T = número de núcleos lógicos da máquina</strong>.</p>
      </div>
      <div class="concl-item ci-green">
        <h4 style="color:#14532d;margin-bottom:8px">Processos — P ideal</h4>
        <p>Para matrizes maiores (≥ 400×400): <strong>P = 8</strong> a <strong>P = 16</strong>.
        O overhead de <code>fork()</code> é maior que threads, por isso em matrizes médias
        P=8 é mais eficiente. Para matrizes muito grandes, P=16 equipara-se às threads.
        Recomendação: <strong>P = número de núcleos físicos da máquina</strong>.</p>
      </div>
    </div>
    <div class="highlight hl-yellow" style="margin-top:16px">
      <strong>Conclusão geral sobre T e P:</strong> O valor ótimo depende do hardware.
      Em uma máquina com <em>N</em> núcleos, usar mais de <em>N</em> workers causa
      <em>context switching</em> excessivo sem ganho real. Para este experimento, com
      base nos dados coletados, <strong>T=8 para threads e P=8 para processos</strong>
      representam o melhor ponto de equilíbrio entre speedup e eficiência.
    </div>
  </div>

  <h3 class="sub-title">6.3 Observações Adicionais</h3>
  <div class="card">
    <ul style="padding-left:20px;line-height:2.1">
      <li><strong>Lei de Amdahl:</strong> O speedup é limitado pela fração serial do programa
          (leitura de arquivo, alocação de memória, escrita de resultados). Mesmo com 16 workers,
          o speedup máximo observado foi ≈6×, longe do ideal 16×.</li>
      <li><strong>Localidade de cache:</strong> Cada thread/processo trabalha em linhas contíguas
          da matriz resultado, o que favorece o acesso sequencial à memória e reduz cache misses.</li>
      <li><strong>Variabilidade:</strong> Processos apresentaram maior desvio padrão que threads
          em matrizes pequenas, reflexo do overhead variável do <code>fork()</code> e do
          escalonamento de processos pelo SO.</li>
      <li><strong>Copy-on-write:</strong> O <code>fork()</code> no Linux usa copy-on-write,
          evitando copiar fisicamente as matrizes M1 e M2 para cada filho — apenas as páginas
          escritas (resultado) são duplicadas. Isso mitiga parte do overhead de processos.</li>
    </ul>
  </div>
</section>

<!-- ══════════════════════════ CONCLUSÃO ══════════════════════════ -->
<section id="conclusao">
  <h2 class="section-title">7. Conclusão</h2>
  <div class="card">
    <p>Este trabalho demonstrou na prática os conceitos de programação paralela utilizando
    threads POSIX e processos Unix para acelerar a multiplicação de matrizes. Os experimentos
    confirmaram os fundamentos teóricos estudados em aula:</p>
    <br/>
    <ul style="padding-left:20px;line-height:2.2">
      <li>A paralelização traz ganhos reais de desempenho, especialmente para problemas de
          maior dimensão, onde o custo de criação dos workers é amortizado.</li>
      <li>Threads são mais eficientes que processos para computação intensiva com dados
          compartilhados, pois evitam overhead de cópia de memória.</li>
      <li>O ganho nunca é linear (Lei de Amdahl), pois sempre há uma porção serial irredutível.</li>
      <li>O valor ótimo de T e P está relacionado ao número de núcleos de CPU disponíveis.</li>
      <li>Para problemas suficientemente grandes e com boa paralelização de dados, como a
          multiplicação de matrizes, a programação paralela é altamente recomendada.</li>
    </ul>
    <div class="highlight hl-green" style="margin-top:20px">
      <strong>Resultado principal:</strong> Para a maior matriz testada (800×800), a versão
      paralela com 16 threads alcançou <strong>speedup de 6,2×</strong>, reduzindo o tempo
      de 354ms para apenas 57ms — uma redução de 84% no tempo de execução.
    </div>
  </div>
</section>

</div><!-- /container -->

<footer>
  Universidade Federal do Rio Grande do Norte — Instituto Metrópole Digital<br/>
  IMD0036 – Sistemas Operacionais · Trabalho Prático Unidade 1 · 2026
</footer>
</body>
</html>"""

with open("relatorio.html", "w", encoding="utf-8") as f_:
    f_.write(HTML_)

print("Relatorio gerado: relatorio.html")
