import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import date

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Estratégico – GR Litoral",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS (mantido, mas com pequenos ajustes para garantir o fluxo) ─────────
st.markdown("""
<style>
/* ── Reset & globals ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container {
    padding: 0 1.5rem 2rem 1.5rem !important;
    max-width: 100% !important;
}

/* ── Header banner ── */
.header-banner {
    background: linear-gradient(135deg, #0b3d91 0%, #0d5fa6 40%, #1a8a8a 100%);
    background-image: linear-gradient(135deg, #0b3d91 0%, #0d5fa6 40%, #1a8a8a 100%),
                      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='120'%3E%3Cpath d='M0 60 Q200 20 400 60 Q600 100 800 60' stroke='rgba(255,255,255,0.08)' stroke-width='3' fill='none'/%3E%3Cpath d='M0 80 Q200 40 400 80 Q600 120 800 80' stroke='rgba(255,255,255,0.05)' stroke-width='2' fill='none'/%3E%3C/svg%3E");
    background-blend-mode: overlay;
    border-radius: 0 0 16px 16px;
    padding: 1.4rem 2rem 1.2rem 2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    flex-wrap: wrap;
}
.header-logo { font-size: 2.2rem; }
.header-title { color: #ffffff; font-size: 1.7rem; font-weight: 800; line-height: 1.15; margin: 0; }
.header-sub { color: rgba(255,255,255,0.78); font-size: 0.82rem; margin-top: 0.2rem; }
.header-date {
    margin-left: auto;
    background: rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    color: #ffffff;
    font-size: 0.82rem;
    font-weight: 600;
    white-space: nowrap;
}

/* ── Section headers ── */
.section-header {
    background: linear-gradient(90deg, #0b3d91 0%, #1a8a8a 100%);
    color: #ffffff;
    font-size: 0.88rem;
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

/* ── KPI cards – top row ── */
.kpi-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.10);
    border-left: 4px solid #0b3d91;
    height: 100%;
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-card.warn  { border-left-color: #e07b00; }
.kpi-card.good  { border-left-color: #1a8a8a; }
.kpi-card-label { font-size: 0.74rem; color: #5a6a7e; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.kpi-card-value { font-size: 1.7rem; font-weight: 800; color: #0b3d91; line-height: 1.1; }
.kpi-card-value.warn { color: #e07b00; }
.kpi-card-value.good { color: #1a8a8a; }
.kpi-card-sub   { font-size: 0.72rem; color: #8a9ab0; margin-top: 0.2rem; }

/* ── Indicator cards (gestão/operação) ── */
.ind-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 0.9rem 1rem 0.85rem 1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
    text-align: center;
    height: 100%;
}
.ind-card-title { font-size: 0.72rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.5rem; }
.ind-card-pct   { font-size: 1.55rem; font-weight: 800; color: #0b3d91; line-height: 1.1; }
.ind-card-pct.over { color: #1a8a8a; }
.ind-card-meta  { font-size: 0.7rem; color: #8a9ab0; margin-top: 0.2rem; }
.ind-card-detail { font-size: 0.68rem; color: #5a6a7e; margin-top: 0.35rem; line-height: 1.5; }
.ind-card-count { font-size: 1.8rem; font-weight: 800; color: #0b3d91; }
.progress-bar-outer {
    background: #e8f0fb;
    border-radius: 4px;
    height: 6px;
    margin: 0.45rem 0 0.25rem 0;
    overflow: hidden;
}
.progress-bar-inner {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #0b3d91, #1a8a8a);
}
.progress-bar-inner.over { background: linear-gradient(90deg, #1a8a8a, #0bd4a0); }

/* ── Açudes table ── */
.acude-table-wrap {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
}
.acude-table-title { font-size: 0.78rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; }

/* ── Programação ── */
.prog-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
    height: 100%;
}
.prog-title { font-size: 0.78rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; }
.prog-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid #f0f4fa;
    font-size: 0.8rem;
    color: #2d3a4a;
    line-height: 1.4;
}
.prog-item:last-child { border-bottom: none; }
.prog-dot { color: #1a8a8a; font-size: 0.6rem; margin-top: 0.3rem; flex-shrink: 0; }

/* ── Plotly overrides ── */
.js-plotly-plot .plotly .modebar { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
XLSX = Path(__file__).parent / "painel da grlitoral.xlsx"

@st.cache_data(ttl=300)
def load_data():
    df_m = pd.read_excel(XLSX, sheet_name="metas",   header=None)
    df_a = pd.read_excel(XLSX, sheet_name="açudes",  header=None)
    return df_m, df_a

df_metas, df_acudes = load_data()

# ── Indicadores de Gestão ────
gest = dict(
    cbh_ord_meta=160,   cbh_ord_real=34,
    cbh_ext_meta=160,   cbh_ext_real=28,
    cbh_for_meta=4,     cbh_for_real=1,
    cap_meta=8,         cap_real=2,
    aloc_meta=8,        aloc_real=0,
    acomp_meta=8,       acomp_real=0,
    aval_meta=8,        aval_real=10,
)

# ── Indicadores de Operação ──
oper = dict(
    anom_meta=23,   anom_real=15,
    cob_meta=37,    cob_real=28,
    fisc_meta=105,  fisc_real=51,
    med_man_meta=18,  med_man_real=4,
    med_inst_meta=10, med_inst_real=3,
    med_med_meta=56,  med_med_real=11,
    bati_meta=2,    bati_real=1,
)

# ── Açudes ───────────────────
acudes = [
    {"nome": str(df_acudes.iloc[i, 0]).strip(),
     "municipio": str(df_acudes.iloc[i, 1]).strip(),
     "vol": float(df_acudes.iloc[i, 8]),
     "pct": float(df_acudes.iloc[i, 9])}
    for i in range(len(df_acudes))
    if pd.notna(df_acudes.iloc[i, 0])
]
total_vol   = sum(a["vol"] for a in acudes)
n_acima90   = sum(1 for a in acudes if a["pct"] >= 90)
n_entre10_90 = sum(1 for a in acudes if 10 <= a["pct"] < 90)
n_abaixo10  = sum(1 for a in acudes if a["pct"] < 10)
total_acudes = len(acudes)

# ── Programação de Hoje (do arquivo original) ──
prog_hoje = [
    "Solicitar apoio logístico para Erandir - reunião do FCCBH (PROCOMITÊ)",
    "Publicação de aniversário de Raimundo Ribeiro Sales",
    "Mobilização para 75ª Reunião Ordinária (Morrinhos/Santana do Acaraú/Amontada)",
    "Providenciar atividades programadas para o mês de julho",
    "Inspeção de Segurança e Medição de Vazão (Patos e Santo Antonio de Aracatiaçu)",
]

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def pct(real, meta):
    if meta == 0: return 0
    return round(real / meta * 100, 1)

def pbar(real, meta, w=120, h=80):
    p = min(pct(real, meta), 100)
    color_arc = "#1a8a8a" if p >= 100 else "#0b3d91"
    fig = go.Figure(go.Pie(
        values=[p, 100-p],
        hole=0.72,
        direction="clockwise",
        rotation=90,
        sort=False,
        marker_colors=[color_arc, "#e8f0fb"],
        textinfo="none",
        hoverinfo="skip",
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        width=w, height=h,
        annotations=[dict(
            text=f"<b>{p:.0f}%</b>",
            x=0.5, y=0.5,
            font=dict(size=14, color=color_arc, family="Inter"),
            showarrow=False,
        )],
    )
    return fig

def inline_bar(real, meta):
    p = min(pct(real, meta), 100)
    color = "over" if p >= 100 else ""
    return f"""
    <div class="progress-bar-outer">
      <div class="progress-bar-inner {color}" style="width:{p}%"></div>
    </div>"""

# ─── HEADER ──────────────────────────────────────────────────────────────────
today_str = date.today().strftime("%d/%m/%Y")
st.markdown(f"""
<div class="header-banner">
  <div class="header-logo">💧</div>
  <div>
    <div class="header-title">Dashboard Estratégico da Gerência Regional</div>
    <div class="header-sub">Monitoramento integrado dos indicadores de gestão e operação dos recursos hídricos – GR Litoral / Itapipoca</div>
  </div>
  <div class="header-date">📅 {today_str} &nbsp;|&nbsp; COGERH</div>
</div>
""", unsafe_allow_html=True)

# ─── KPI TOP ROW (Layout reestruturado) ─────────────────────────────────────
# Usamos um container para garantir que os cards se ajustem bem
with st.container():
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
          <div class="kpi-card-label">✅ Acima de 90% cap.</div>
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

# ─── NÚCLEO DE GESTÃO (Layout reestruturado) ─────────────────────────────────
st.markdown('<div class="section-header">👥 NÚCLEO DE GESTÃO</div>', unsafe_allow_html=True)

# Agrupamos os dados para facilitar a iteração
gest_items = [
    ("Alocações de Água", gest["aloc_real"], gest["aloc_meta"], f"Meta: {gest['aloc_meta']} reuniões", "reuniões", False),
    ("Acompanhamento", gest["acomp_real"], gest["acomp_meta"], f"Meta: {gest['acomp_meta']} reuniões", "reuniões", False),
    ("Avaliação", gest["aval_real"], gest["aval_meta"], f"Meta: {gest['aval_meta']} reuniões", "reuniões", False),
    ("CBH Ordinária", gest["cbh_ord_real"], gest["cbh_ord_meta"], f"Meta: {gest['cbh_ord_meta']} participantes", "partic.", False),
    ("CBH Extraordinária", gest["cbh_ext_real"], gest["cbh_ext_meta"], f"Meta: {gest['cbh_ext_meta']} participantes", "partic.", False),
    ("CBH Fórum", gest["cbh_for_real"], gest["cbh_for_meta"], f"Meta: {gest['cbh_for_meta']} reuniões", "reuniões", False),
    ("Capacitações", gest["cap_real"], gest["cap_meta"], f"Meta: {gest['cap_meta']} capacitações", None, True),
]
icons = ["🚰", "🔍", "📋", "👥", "👥", "🎓", "🎓"]

# Usamos um container e dividimos em 7 colunas para maior responsividade
with st.container():
    cols_g = st.columns(7)
    for col, (label, real, meta, meta_txt, unit, is_count), icon in zip(cols_g, gest_items, icons):
        with col:
            if is_count:
                st.markdown(f"""
                <div class="ind-card">
                  <div class="ind-card-title">{icon} {label}</div>
                  <div class="ind-card-count">{real}</div>
                  {inline_bar(real, meta)}
                  <div class="ind-card-meta">{meta_txt}</div>
                </div>""", unsafe_allow_html=True)
            else:
                fig = pbar(real, meta)
                st.markdown(f'<div class="ind-card"><div class="ind-card-title">{icon} {label}</div>', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False}, key=f"gest_{label}")
                st.markdown(f'<div class="ind-card-meta">{real} {unit if unit else ""} / {meta_txt}</div></div>', unsafe_allow_html=True)

# ─── NÚCLEO DE OPERAÇÃO (Layout reestruturado) ───────────────────────────────
st.markdown('<div class="section-header">⚙️ NÚCLEO DE OPERAÇÃO</div>', unsafe_allow_html=True)

# Organizamos os cards em 5 colunas
with st.container():
    cols_o = st.columns(5)
    
    # Anomalias
    with cols_o[0]:
        p = pct(oper["anom_real"], oper["anom_meta"])
        fig = pbar(oper["anom_real"], oper["anom_meta"], w=130, h=88)
        st.markdown('<div class="ind-card"><div class="ind-card-title">🛡️ Anomalias</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False}, key="oper_anom")
        st.markdown(f"""
        <div class="ind-card-detail">
          Regional: {oper['anom_real']} / {oper['anom_meta']} meta<br>
          Corrigidas: {oper['anom_real']}
        </div></div>""", unsafe_allow_html=True)
    
    # Regularização de Cobrança
    with cols_o[1]:
        fig = pbar(oper["cob_real"], oper["cob_meta"], w=130, h=88)
        st.markdown('<div class="ind-card"><div class="ind-card-title">📃 Reg. Cobrança</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False}, key="oper_cob")
        st.markdown(f"""
        <div class="ind-card-detail">
          Novos: {12} | Inad.: {16}<br>
          Real: {oper['cob_real']} / Meta: {oper['cob_meta']}
        </div></div>""", unsafe_allow_html=True)
    
    # Fiscalização
    with cols_o[2]:
        fig = pbar(oper["fisc_real"], oper["fisc_meta"], w=130, h=88)
        st.markdown('<div class="ind-card"><div class="ind-card-title">🔎 Fiscalização</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False}, key="oper_fisc")
        st.markdown(f"""
        <div class="ind-card-detail">
          Com RV: 13 | Sem RV: 38<br>
          Real: {oper['fisc_real']} / Meta: {oper['fisc_meta']}
        </div></div>""", unsafe_allow_html=True)
    
    # Medidores
    with cols_o[3]:
        avg_med = (pct(oper["med_man_real"], oper["med_man_meta"]) +
                   pct(oper["med_inst_real"], oper["med_inst_meta"]) +
                   pct(oper["med_med_real"], oper["med_med_meta"])) / 3
        fig = pbar(avg_med, 100, w=130, h=88)
        st.markdown('<div class="ind-card"><div class="ind-card-title">📡 Medidores</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False}, key="oper_med")
        st.markdown(f"""
        <div class="ind-card-detail">
          Manutenções: {oper['med_man_real']}/{oper['med_man_meta']}<br>
          Instalações: {oper['med_inst_real']}/{oper['med_inst_meta']}<br>
          Medições: {oper['med_med_real']}/{oper['med_med_meta']}
        </div></div>""", unsafe_allow_html=True)
    
    # Batimetria
    with cols_o[4]:
        fig = pbar(oper["bati_real"], oper["bati_meta"], w=130, h=88)
        st.markdown('<div class="ind-card"><div class="ind-card-title">🚢 Batimetria</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False}, key="oper_bati")
        st.markdown(f"""
        <div class="ind-card-detail">
          Realizadas: {oper['bati_real']} de {oper['bati_meta']}<br>
          Meta: {oper['bati_meta']} batimetrias
        </div></div>""", unsafe_allow_html=True)

# ─── BOTTOM ROW: Açudes + Situação + Programação (Layout reestruturado) ─────
st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
# Agora usamos um layout de 3 colunas, mas com proporções ajustadas para não quebrar
col_ac, col_sit, col_prog = st.columns([2.2, 1.0, 1.8])

# ── Açudes table (dentro do primeiro container) ──
with col_ac:
    rows_html = ""
    for a in acudes:
        pct_val = a["pct"]
        if pct_val >= 90:
            bar_color = "#1a8a8a"
            dot = "🟢"
        elif pct_val >= 10:
            bar_color = "#0b3d91"
            dot = "🔵"
        else:
            bar_color = "#e07b00"
            dot = "🟠"
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

# ── Situação donut ──
with col_sit:
    fig_sit = go.Figure(go.Pie(
        labels=["Acima de 90%", "Entre 10-90%", "Abaixo de 10%"],
        values=[n_acima90, n_entre10_90, n_abaixo10],
        hole=0.60,
        marker_colors=["#1a8a8a", "#0b3d91", "#e07b00"],
        textinfo="none",
        hovertemplate="%{label}<br>%{value} açudes<extra></extra>",
    ))
    fig_sit.add_annotation(
        text=f"<b>{total_acudes}</b><br><span style='font-size:10px'>açudes</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color="#0b3d91", family="Inter"),
    )
    fig_sit.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=True,
        legend=dict(orientation="v", x=0, y=0, font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text="Situação dos Açudes", font=dict(size=11, color="#0b3d91", family="Inter"), x=0.5),
        height=280,
    )
    st.markdown('<div class="acude-table-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_sit, use_container_width=True, config={"displayModeBar": False}, key="donut_sit")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Programação de Hoje ──
with col_prog:
    items_html = "".join(
        f'<div class="prog-item"><span class="prog-dot">●</span><span>{t}</span></div>'
        for t in prog_hoje
    )
    st.markdown(f"""
    <div class="prog-card">
      <div class="prog-title">📅 Programação de Hoje — {today_str}</div>
      {items_html}
    </div>""", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:1.5rem;color:#8a9ab0;font-size:0.72rem">
  COGERH – Companhia de Gestão dos Recursos Hídricos &nbsp;|&nbsp; GR Litoral / Itapipoca &nbsp;|&nbsp;
  Dados: painel_da_grlitoral.xlsx
</div>""", unsafe_allow_html=True)
