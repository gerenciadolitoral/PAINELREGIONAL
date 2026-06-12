import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
from pathlib import Path
from datetime import date

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Estratégico – GR Litoral",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container {
    padding: 0 1.5rem 2rem 1.5rem !important;
    max-width: 100% !important;
}

/* Header */
.header-banner {
    background: linear-gradient(135deg, #0b3d91 0%, #0d5fa6 40%, #1a8a8a 100%);
    border-radius: 0 0 16px 16px;
    padding: 1.4rem 2rem 1.2rem 2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    flex-wrap: wrap;
}
.header-logo { font-size: 3.3rem; }
.header-title { color: #ffffff; font-size: 2.55rem; font-weight: 800; line-height: 1.15; margin: 0; }
.header-sub { color: rgba(255,255,255,0.78); font-size: 1.23rem; margin-top: 0.2rem; }
.header-date {
    margin-left: auto;
    background: rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    color: #ffffff;
    font-size: 1.23rem;
    font-weight: 600;
    white-space: nowrap;
}

/* Section headers */
.section-header {
    background: linear-gradient(90deg, #0b3d91 0%, #1a8a8a 100%);
    color: #ffffff;
    font-size: 1.32rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.55rem 1rem;
    border-radius: 8px;
    margin: 1.1rem 0 0.7rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* KPI top row */
.kpi-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.10);
    border-left: 4px solid #0b3d91;
    min-height: 135px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-card.warn  { border-left-color: #e07b00; }
.kpi-card.good  { border-left-color: #1a8a8a; }
.kpi-card-label { font-size: 1.11rem; color: #5a6a7e; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.kpi-card-value { font-size: 2.55rem; font-weight: 800; color: #0b3d91; line-height: 1.1; }
.kpi-card-value.warn { color: #e07b00; }
.kpi-card-value.good { color: #1a8a8a; }
.kpi-card-sub   { font-size: 1.08rem; color: #8a9ab0; margin-top: 0.2rem; }

/* Indicator cards — SELF-CONTAINED, no plotly inside */
.ind-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 0.8rem 0.75rem 0.75rem 0.75rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
    height: 100%;
    box-sizing: border-box;
}
.ind-card-title {
    font-size: 1.04rem;
    font-weight: 700;
    color: #0b3d91;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    line-height: 1.3;
    width: 100%;
}
.ind-card-meta  { font-size: 1.02rem; color: #8a9ab0; }
.ind-card-detail { font-size: 1.01rem; color: #5a6a7e; line-height: 1.5; width: 100%; }

/* SVG donut inside card */
.donut-wrap { width: 120px; height: 120px; flex-shrink: 0; }

/* Açudes table */
.acude-table-wrap {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
}
.acude-table-title { font-size: 1.17rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; }

/* Programação */
.prog-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
    height: 100%;
}
.prog-title { font-size: 1.17rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; }
.prog-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid #f0f4fa;
    font-size: 1.2rem;
    color: #2d3a4a;
    line-height: 1.4;
}
.prog-item:last-child { border-bottom: none; }
.prog-dot { color: #1a8a8a; font-size: 0.9rem; margin-top: 0.3rem; flex-shrink: 0; }

.js-plotly-plot .plotly .modebar { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─── DATA ─────────────────────────────────────────────────────────────────────
XLSX = Path(__file__).parent / "painel da grlitoral.xlsx"

@st.cache_data(ttl=300)
def load_data():
    df_m = pd.read_excel(XLSX, sheet_name="metas",  header=None)
    df_a = pd.read_excel(XLSX, sheet_name="açudes", header=None)
    return df_m, df_a

df_metas, df_acudes = load_data()

gest = dict(
    cbh_ord_meta=160, cbh_ord_real=34,
    cbh_ext_meta=160, cbh_ext_real=28,
    cbh_for_meta=4,   cbh_for_real=1,
    cap_meta=8,       cap_real=2,
    aloc_meta=8,      aloc_real=0,
    acomp_meta=8,     acomp_real=0,
    aval_meta=8,      aval_real=10,
)

oper = dict(
    anom_meta=23,     anom_real=15,
    cob_meta=37,      cob_real=28,
    fisc_meta=105,    fisc_real=51,
    med_man_meta=18,  med_man_real=4,
    med_inst_meta=10, med_inst_real=3,
    med_med_meta=56,  med_med_real=11,
    bati_meta=2,      bati_real=1,
)

acudes = [
    {"nome": str(df_acudes.iloc[i, 0]).strip(),
     "municipio": str(df_acudes.iloc[i, 1]).strip(),
     "vol": float(df_acudes.iloc[i, 8]),
     "pct": float(df_acudes.iloc[i, 9])}
    for i in range(len(df_acudes))
    if pd.notna(df_acudes.iloc[i, 0])
]
total_vol    = sum(a["vol"] for a in acudes)
n_acima90    = sum(1 for a in acudes if a["pct"] >= 90)
n_entre10_90 = sum(1 for a in acudes if 10 <= a["pct"] < 90)
n_abaixo10   = sum(1 for a in acudes if a["pct"] < 10)
total_acudes = len(acudes)

prog_hoje = [
    "Solicitar apoio logístico para Erandir - reunião do FCCBH (PROCOMITÊ)",
    "Publicação de aniversário de Raimundo Ribeiro Sales",
    "Mobilização para 75ª Reunião Ordinária (Morrinhos/Santana do Acaraú/Amontada)",
    "Providenciar atividades programadas para o mês de julho",
    "Inspeção de Segurança e Medição de Vazão (Patos e Santo Antonio de Aracatiaçu)",
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def pct(real, meta):
    if meta == 0: return 0
    return round(real / meta * 100, 1)

def svg_donut(real, meta, size=80):
    """Gera um mini donut SVG completamente autocontido — sem Plotly."""
    p = min(pct(real, meta), 100)
    color = "#1a8a8a" if p >= 100 else "#0b3d91"
    r = 30
    cx = cy = size / 2
    stroke_w = 9
    circumference = 2 * math.pi * r
    dash = circumference * p / 100
    gap  = circumference - dash
    # Começa no topo: rotate -90
    return f"""
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e8f0fb" stroke-width="{stroke_w}"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke_w}"
          stroke-dasharray="{dash:.2f} {gap:.2f}"
          stroke-linecap="round"
          transform="rotate(-90 {cx} {cy})"/>
  <text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central"
        font-family="Inter,sans-serif" font-size="12" font-weight="800" fill="{color}">{p:.0f}%</text>
</svg>"""

# ─── HEADER ───────────────────────────────────────────────────────────────────
today_str = date.today().strftime("%d/%m/%Y")
st.markdown(f"""
<div class="header-banner">
  <div class="header-logo">💧</div>
  <div>
    <div class="header-title">Dashboard Estratégico da Gerência Regional</div>
    <div class="header-sub">Monitoramento integrado dos indicadores de gestão e operação – GR Litoral / Itapipoca</div>
  </div>
  <div class="header-date">📅 {today_str} &nbsp;|&nbsp; COGERH</div>
</div>
""", unsafe_allow_html=True)

# ─── KPI TOP ROW ──────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""
    <div class="kpi-card good">
      <div class="kpi-card-label">🏛️ Açudes Monitorados</div>
      <div class="kpi-card-value good">{total_acudes}</div>
      <div class="kpi-card-sub">GR Litoral / Itapipoca</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-card-label">💧 Volume Total (hm³)</div>
      <div class="kpi-card-value">{total_vol:.2f}</div>
      <div class="kpi-card-sub">Volume atual armazenado</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="kpi-card good">
      <div class="kpi-card-label">✅ Acima de 90%</div>
      <div class="kpi-card-value good">{n_acima90}</div>
      <div class="kpi-card-sub">{n_acima90/total_acudes*100:.1f}% do total</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-card-label">〰️ Entre 10% e 90%</div>
      <div class="kpi-card-value">{n_entre10_90}</div>
      <div class="kpi-card-sub">{n_entre10_90/total_acudes*100:.1f}% do total</div>
    </div>""", unsafe_allow_html=True)
with col5:
    cls = "warn" if n_abaixo10 > 0 else ""
    st.markdown(f"""
    <div class="kpi-card {cls}">
      <div class="kpi-card-label">⚠️ Abaixo de 10%</div>
      <div class="kpi-card-value {cls}">{n_abaixo10}</div>
      <div class="kpi-card-sub">{n_abaixo10/total_acudes*100:.1f}% do total</div>
    </div>""", unsafe_allow_html=True)

# ─── NÚCLEO DE GESTÃO ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">👥 NÚCLEO DE GESTÃO</div>', unsafe_allow_html=True)

gest_items = [
    ("Alocações",       gest["aloc_real"],    gest["aloc_meta"],    f"{gest['aloc_real']}/{gest['aloc_meta']} reuniões"),
    ("Acompanhamento",  gest["acomp_real"],   gest["acomp_meta"],   f"{gest['acomp_real']}/{gest['acomp_meta']} reuniões"),
    ("Avaliação",       gest["aval_real"],    gest["aval_meta"],    f"{gest['aval_real']}/{gest['aval_meta']} reuniões"),
    ("CBH Ordinária",   gest["cbh_ord_real"], gest["cbh_ord_meta"], f"{gest['cbh_ord_real']}/{gest['cbh_ord_meta']} partic."),
    ("CBH Extraord.",   gest["cbh_ext_real"], gest["cbh_ext_meta"], f"{gest['cbh_ext_real']}/{gest['cbh_ext_meta']} partic."),
    ("CBH Fórum",       gest["cbh_for_real"], gest["cbh_for_meta"], f"{gest['cbh_for_real']}/{gest['cbh_for_meta']} reuniões"),
    ("Capacitações",    gest["cap_real"],     gest["cap_meta"],     f"{gest['cap_real']}/{gest['cap_meta']} capacit."),
]

cols_g = st.columns(7)
for col, (label, real, meta, detail) in zip(cols_g, gest_items):
    donut = svg_donut(real, meta)
    with col:
        st.markdown(f"""
        <div class="ind-card">
          <div class="ind-card-title">{label}</div>
          {donut}
          <div class="ind-card-detail">{detail}</div>
        </div>""", unsafe_allow_html=True)

# ─── NÚCLEO DE OPERAÇÃO ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">⚙️ NÚCLEO DE OPERAÇÃO</div>', unsafe_allow_html=True)

# Medidores: média das 3 metas
avg_med_pct = (pct(oper["med_man_real"], oper["med_man_meta"]) +
               pct(oper["med_inst_real"], oper["med_inst_meta"]) +
               pct(oper["med_med_real"],  oper["med_med_meta"])) / 3

oper_items = [
    ("🛡️ Anomalias",     oper["anom_real"],  oper["anom_meta"],
     f"Regional: {oper['anom_real']}/{oper['anom_meta']}<br>Corrigidas: {oper['anom_real']}"),
    ("📃 Reg. Cobrança", oper["cob_real"],   oper["cob_meta"],
     f"Novos: 12 | Inad.: 16<br>Real: {oper['cob_real']}/{oper['cob_meta']}"),
    ("🔎 Fiscalização",  oper["fisc_real"],  oper["fisc_meta"],
     f"Com RV: 13 | Sem RV: 38<br>Real: {oper['fisc_real']}/{oper['fisc_meta']}"),
    ("📡 Medidores",     avg_med_pct,        100,
     f"Manut.: {oper['med_man_real']}/{oper['med_man_meta']}<br>"
     f"Inst.: {oper['med_inst_real']}/{oper['med_inst_meta']}<br>"
     f"Med.: {oper['med_med_real']}/{oper['med_med_meta']}"),
    ("🚢 Batimetria",    oper["bati_real"],   oper["bati_meta"],
     f"Realizadas: {oper['bati_real']}/{oper['bati_meta']}"),
]

cols_o = st.columns(5)
for col, (label, real, meta, detail) in zip(cols_o, oper_items):
    # Para medidores o real já é pct, passamos diretamente
    if label == "📡 Medidores":
        donut = svg_donut(real, meta)  # real=avg_pct, meta=100
    else:
        donut = svg_donut(real, meta)
    with col:
        st.markdown(f"""
        <div class="ind-card">
          <div class="ind-card-title">{label}</div>
          {donut}
          <div class="ind-card-detail">{detail}</div>
        </div>""", unsafe_allow_html=True)

# ─── BOTTOM ROW ───────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
col_ac, col_sit, col_prog = st.columns([2.2, 1.0, 1.8])

# Tabela de açudes
with col_ac:
    rows_html = ""
    for a in acudes:
        pct_val = a["pct"]
        if pct_val >= 90:
            bar_color, dot = "#1a8a8a", "🟢"
        elif pct_val >= 10:
            bar_color, dot = "#0b3d91", "🔵"
        else:
            bar_color, dot = "#e07b00", "🟠"
        w = min(pct_val, 100)
        rows_html += f"""
        <tr style="border-bottom:1px solid #f0f4fa;">
          <td style="padding:0.35rem 0.5rem;font-size:0.78rem;font-weight:600;color:#0d1b2a">{dot} {a['nome']}</td>
          <td style="padding:0.35rem 0.5rem;font-size:0.75rem;color:#5a6a7e">{a['municipio']}</td>
          <td style="padding:0.35rem 0.5rem;font-size:0.78rem;font-weight:600;color:#0b3d91;text-align:right">{a['vol']:.2f}</td>
          <td style="padding:0.35rem 0.5rem;width:120px">
            <div style="display:flex;align-items:center;gap:0.4rem">
              <div style="flex:1;background:#e8f0fb;border-radius:3px;height:7px;overflow:hidden">
                <div style="width:{w}%;height:100%;background:{bar_color};border-radius:3px"></div>
              </div>
              <span style="font-size:0.75rem;font-weight:700;color:{bar_color};white-space:nowrap">{pct_val:.1f}%</span>
            </div>
          </td>
        </tr>"""
    st.markdown(f"""
    <div class="acude-table-wrap">
      <div class="acude-table-title">🏛️ Situação dos Açudes (hm³ / % capacidade)</div>
      <table style="width:100%;border-collapse:collapse">
        <thead>
          <tr style="background:#f5f8ff">
            <th style="padding:0.3rem 0.5rem;font-size:0.7rem;text-align:left;color:#5a6a7e;font-weight:700">AÇUDE</th>
            <th style="padding:0.3rem 0.5rem;font-size:0.7rem;text-align:left;color:#5a6a7e;font-weight:700">MUNICÍPIO</th>
            <th style="padding:0.3rem 0.5rem;font-size:0.7rem;text-align:right;color:#5a6a7e;font-weight:700">hm³</th>
            <th style="padding:0.3rem 0.5rem;font-size:0.7rem;color:#5a6a7e;font-weight:700">% CAP.</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)

# Donut de situação — Plotly correto: dentro de um único st.plotly_chart
with col_sit:
    fig_sit = go.Figure(go.Pie(
        labels=["Acima de 90%", "Entre 10–90%", "Abaixo de 10%"],
        values=[n_acima90, n_entre10_90, n_abaixo10],
        hole=0.60,
        marker_colors=["#1a8a8a", "#0b3d91", "#e07b00"],
        textinfo="none",
        hovertemplate="%{label}<br>%{value} açudes<extra></extra>",
    ))
    fig_sit.add_annotation(
        text=f"<b>{total_acudes}</b><br><span style='font-size:9px'>açudes</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="#0b3d91", family="Inter"),
    )
    fig_sit.update_layout(
        margin=dict(l=8, r=8, t=36, b=8),
        showlegend=True,
        legend=dict(
            orientation="v",
            x=0.5, xanchor="center",
            y=-0.12,
            font=dict(size=10, family="Inter"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(
            text="Situação dos Açudes",
            font=dict(size=11, color="#0b3d91", family="Inter"),
            x=0.5,
        ),
        height=300,
    )
    st.markdown('<div class="acude-table-wrap" style="padding-bottom:0.5rem">', unsafe_allow_html=True)
    st.plotly_chart(fig_sit, use_container_width=True, config={"displayModeBar": False}, key="donut_sit")
    st.markdown('</div>', unsafe_allow_html=True)

# Programação
with col_prog:
    items_html = "".join(
        f'<div class="prog-item"><span class="prog-dot">●</span><span>{t}</span></div>'
        for t in prog_hoje
    )
    st.markdown(f"""
    <div class="prog-card">
      <div class="prog-title">📅 Programação — {today_str}</div>
      {items_html}
    </div>""", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:1.5rem;color:#8a9ab0;font-size:0.72rem">
  COGERH – Companhia de Gestão dos Recursos Hídricos &nbsp;|&nbsp; GR Litoral / Itapipoca &nbsp;|&nbsp;
  Dados: painel_da_grlitoral.xlsx
</div>""", unsafe_allow_html=True)
