import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import calendar
import math
import io
import base64
import requests
from pathlib import Path
from datetime import date, datetime, timedelta
from io import StringIO

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Painel Estratégico – GRLitoral",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── IMAGEM DE FUNDO ─────────────────────────────────────────────────────────
_fundo_css = ""
_fundo_path = Path(__file__).parent / "fundo.jpg"

if _fundo_path.exists():
    _b64 = base64.b64encode(_fundo_path.read_bytes()).decode()
    _fundo_css = f"""
    body::before {{
        content: '';
        position: fixed;
        inset: 0;
        background-image: url('data:image/jpeg;base64,{_b64}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        opacity: 0.60;
        z-index: -1;
        pointer-events: none;
    }}
    .stApp, [data-testid="stAppViewContainer"] {{
        background: transparent !important;
    }}
    [data-testid="stHeader"], header.stAppHeader {{
        background: transparent !important;
    }}
    """

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

{_fundo_css}

[data-testid="stMainBlockContainer"] {{
    padding: 1.5rem 1.5rem 2rem 1.5rem !important;
    max-width: 1400px !important;
    min-width: 1100px !important;
    width: 1400px !important;
}}

.header-banner {{
    background: linear-gradient(135deg, #0b3d91 0%, #0d5fa6 40%, #1a8a8a 100%);
    border-radius: 0 0 16px 16px;
    padding: 1.4rem 2rem 1.2rem 2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    flex-wrap: wrap;
    width: 100%;
    box-sizing: border-box;
}}
.header-logo {{ font-size: 2.97rem; }}
.header-title {{ color: #ffffff; font-size: 2.295rem; font-weight: 800; line-height: 1.15; margin: 0; }}
.header-sub {{ color: rgba(255,255,255,0.78); font-size: 1.107rem; margin-top: 0.2rem; }}
.header-date {{
    margin-left: auto;
    background: rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    color: #ffffff;
    font-size: 1.107rem;
    font-weight: 600;
    white-space: nowrap;
}}

.section-header {{
    background: linear-gradient(90deg, #0b3d91 0%, #1a8a8a 100%);
    color: #ffffff;
    font-size: 1.188rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.55rem 1rem;
    border-radius: 8px;
    margin: 1.1rem 0 0.7rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.kpi-card {{
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.10);
    border-left: 4px solid #0b3d91;
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.kpi-card.warn  {{ border-left-color: #e07b00; }}
.kpi-card.good  {{ border-left-color: #1a8a8a; }}
.kpi-card-label {{ font-size: 0.999rem; color: #5a6a7e; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }}
.kpi-card-value {{ font-size: 2.295rem; font-weight: 800; color: #0b3d91; line-height: 1.1; }}
.kpi-card-value.warn {{ color: #e07b00; }}
.kpi-card-value.good {{ color: #1a8a8a; }}
.kpi-card-sub   {{ font-size: 0.792rem; color: #8a9ab0; margin-top: 0.2rem; }}

.ind-card {{
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
}}
.ind-card-title {{
    font-size: 0.932rem;
    font-weight: 700;
    color: #0b3d91;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    line-height: 1.3;
    width: 100%;
}}
.ind-card-meta  {{ font-size: 0.68rem; color: #8a9ab0; }}
.ind-card-detail {{ font-size: 0.905rem; color: #5a6a7e; line-height: 1.5; width: 100%; }}

.acude-table-wrap {{
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
}}
.acude-table-title {{ font-size: 1.053rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; }}

.sit-card {{
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 0.75rem 0.75rem 0.75rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    box-sizing: border-box;
}}
.sit-card-title {{
    font-size: 1.053rem;
    font-weight: 700;
    color: #0b3d91;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
    text-align: center;
    width: 100%;
}}

.prog-card {{
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
    height: 100%;
}}
.prog-title {{ font-size: 1.053rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; }}
.prog-item {{
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid #f0f4fa;
    font-size: 0.88rem;
    color: #2d3a4a;
    line-height: 1.4;
}}
.prog-item:last-child {{ border-bottom: none; }}
.prog-dot {{ color: #1a8a8a; font-size: 0.81rem; margin-top: 0.3rem; flex-shrink: 0; }}

.fonte-badge {{
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: 0.5rem;
}}
.fonte-online {{ background: #d4edda; color: #155724; }}
.fonte-local  {{ background: #fff3cd; color: #856404; }}

.js-plotly-plot .plotly .modebar {{ display: none !important; }}

/* ---- Estilos do calendário (abaixo) ---- */
.cal-header {{
    background: linear-gradient(135deg, #0b3d91 0%, #1a8a8a 100%);
    color: white; 
    padding: 14px 18px; 
    border-radius: 8px 8px 0 0;
    display: flex; 
    justify-content: space-between; 
    align-items: center;
}}
.cal-title {{font-size:1.6rem; font-weight:800; letter-spacing:1px; margin:0;}}
.dia-semana-label {{text-align:center; font-weight:800; padding:6px; border-radius:6px;
                    margin-bottom:4px; font-size:0.8rem;}}
.day-card {{
    border:2px solid #ddd; border-radius:6px; padding:6px;
    height:170px; overflow-y:auto; box-sizing:border-box;
}}
.day-num {{font-weight:700; font-size:0.95rem; margin-bottom:4px;}}
.week-card {{
    border:1px solid #ccc; border-radius:0 0 6px 6px;
    padding:6px; box-sizing:border-box;
    height:420px; overflow-y:auto;
}}
.week-card-hoje {{ border:3px solid #F5A623; }}
.week-header {{
    text-align:center; padding:6px; border-radius:6px 6px 0 0;
    font-weight:800; color:white;
}}
.week-header .data-sub {{ font-size:0.75rem; font-weight:600; }}
.atividade-pill {{
    border-radius:5px; padding:4px 7px; margin-bottom:4px;
    font-size:0.72rem; line-height:1.3; color:white;
    word-wrap:break-word; overflow-wrap:break-word;
}}
.sem-atividade {{ font-size:0.72rem; color:#999; font-style:italic; }}
.mais-info {{ font-size:0.68rem; color:#888; }}

/* Estilo unificado para os botões do Streamlit */
div[data-testid="stButton"] > button {{
    background: linear-gradient(90deg, #0b3d91 0%, #1a8a8a 100%) !important;
    color: #ffffff !important;
    border: none !important;
    transition: transform 0.2s, box-shadow 0.2s;
}}

div[data-testid="stButton"] > button:hover {{
    background: linear-gradient(90deg, #1a8a8a 0%, #0b3d91 100%) !important;
    color: #ffffff !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(11,61,145,0.3) !important;
}}

div[data-testid="stButton"] > button p {{
    color: #ffffff !important;
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# ─── CONFIGURAÇÃO DA FONTE DE DADOS ──────────────────────────────────────────
SHEET_ID   = "1kte6Ys9vgzw7a0Z1PDXkxf6VOX9KHWlRCXp7P-7RSi4"
XLSX_LOCAL = Path(__file__).parent / "painel da grlitoral.xlsx"

SHEETS = {
    "metas":  f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=metas",
    "açudes": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=a%C3%A7udes",
    "prog":   f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=507430155",
}

def _safe_float(val, default=0.0):
    if val is None:
        return default
    try:
        f = float(str(val).replace(",", ".").strip())
        return default if math.isnan(f) else f
    except (ValueError, TypeError):
        return default

def _safe_str(val):
    s = str(val).strip() if val is not None else ""
    return "" if s.lower() in ("nan", "none", "") else s

@st.cache_data(ttl=300)
def load_data():
    try:
        dfs = {}
        for nome, url in SHEETS.items():
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            dfs[nome] = pd.read_csv(
                io.BytesIO(resp.content),
                encoding="utf-8-sig",
                header=None,
                dtype=str,
                keep_default_na=False,
            )
        return dfs["metas"], dfs["açudes"], dfs.get("prog", pd.DataFrame()), "online"
    except Exception:
        try:
            df_m = pd.read_excel(XLSX_LOCAL, sheet_name="metas",  header=None, dtype=str)
            df_a = pd.read_excel(XLSX_LOCAL, sheet_name="açudes", header=None, dtype=str)
            df_p = pd.read_excel(XLSX_LOCAL, sheet_name="prog",   header=None, dtype=str)
            return df_m, df_a, df_p, "local"
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            st.stop()

df_metas, df_acudes, df_prog, fonte_dados = load_data()

# ─── HELPERS DE LEITURA ───────────────────────────────────────────────────────
def cell(df, row, col, default=0.0):
    try:
        return _safe_float(df.iloc[row, col], default)
    except (IndexError, KeyError):
        return default

def cell_str(df, row, col):
    try:
        return _safe_str(df.iloc[row, col])
    except (IndexError, KeyError):
        return ""

# ─── PARSE DOS INDICADORES ────────────────────────────────────────────────────
gest = dict(
    cbh_ord_meta  = cell(df_metas,  2, 2),
    cbh_ord_real  = cell(df_metas,  2, 5),
    cbh_ext_meta  = cell(df_metas,  7, 2),
    cbh_ext_real  = cell(df_metas,  7, 5),
    cbh_for_meta  = cell(df_metas, 13, 2),
    cbh_for_real  = cell(df_metas, 13, 4),
    cap_meta      = cell(df_metas, 18, 2),
    cap_real      = cell(df_metas, 18, 4),
    aloc_meta     = cell(df_metas, 28, 2),
    aloc_real     = cell(df_metas, 28, 4),
    acomp_meta    = cell(df_metas, 38, 2),
    acomp_real    = cell(df_metas, 38, 4),
    aval_meta     = cell(df_metas, 48, 2),
    aval_real     = cell(df_metas, 48, 4),
    reuord        = cell(df_metas,  2, 4),
    reuex         = cell(df_metas,  7, 4),
)

oper = dict(
    anom_meta     = cell(df_metas, 61, 2),
    anom_real     = cell(df_metas, 61, 4),
    anom_r        = cell(df_metas, 62, 4),
    anom_a        = cell(df_metas, 63, 4),
    cob_meta      = cell(df_metas, 65, 2),
    cob_real      = cell(df_metas, 65, 4),
    cob_novos     = cell(df_metas, 66, 2),
    cob_novos_r   = cell(df_metas, 66, 4),
    cob_inad      = cell(df_metas, 67, 2),
    cob_inad_r    = cell(df_metas, 67, 4),
    fisc_meta     = cell(df_metas, 69, 2),
    fisc_real     = cell(df_metas, 69, 4),
    fisc_rv       = cell(df_metas, 70, 4),
    fisc_srv      = cell(df_metas, 71, 4),
    med_final     = cell(df_metas, 73, 4),
    med_man_meta  = cell(df_metas, 74, 2),
    med_man_real  = cell(df_metas, 74, 4),
    med_inst_meta = cell(df_metas, 75, 2),
    med_inst_real = cell(df_metas, 75, 4),
    med_med_meta  = cell(df_metas, 76, 2),
    med_med_real  = cell(df_metas, 76, 4),
    bati_meta     = cell(df_metas, 78, 2),
    bati_real     = cell(df_metas, 78, 4),
)

# ─── PARSE DOS AÇUDES ─────────────────────────────────────────────────────────
acudes = []
for i in range(99, 107):
    if i >= len(df_metas):
        break
    nome      = cell_str(df_metas, i, 0)
    municipio = cell_str(df_metas, i, 1)
    vol       = cell(df_metas, i, 2)
    pct_val   = cell(df_metas, i, 3)
    if not nome:
        continue
    acudes.append({"nome": nome, "municipio": municipio, "vol": vol, "pct": pct_val})

total_vol    = sum(a["vol"] for a in acudes)
total_acudes = len(acudes)
n_acima90    = sum(1 for a in acudes if a["pct"] >= 90)
n_80_90      = sum(1 for a in acudes if 80 <= a["pct"] < 90)
n_70_80      = sum(1 for a in acudes if 70 <= a["pct"] < 80)
n_abaixo70   = sum(1 for a in acudes if a["pct"] < 70)
n_entre10_90 = sum(1 for a in acudes if 10 <= a["pct"] < 90)
n_abaixo10   = sum(1 for a in acudes if a["pct"] < 10)

# ─── HELPERS DE VISUALIZAÇÃO ──────────────────────────────────────────────────
def pct(real, meta):
    if meta == 0:
        return 0
    return round(real / meta * 100, 1)

def svg_donut(real, meta, size=80):
    p = min(pct(real, meta), 100)
    color = "#1a8a8a" if p >= 100 else "#0b3d91"
    r = 30; cx = cy = size / 2; stroke_w = 12
    circumference = 2 * math.pi * r
    dash = circumference * p / 100
    gap  = circumference - dash
    return f"""
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e8f0fb" stroke-width="{stroke_w}"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke_w}"
          stroke-dasharray="{dash:.2f} {gap:.2f}" stroke-linecap="round"
          transform="rotate(-90 {cx} {cy})"/>
  <text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central"
        font-family="Inter,sans-serif" font-size="16.2" font-weight="800" fill="{color}">{p:.0f}%</text>
</svg>"""

# ─── NAVEGAÇÃO TEMPORAL (SESSÃO) ──────────────────────────────────────────────
if "prog_offset" not in st.session_state:
    st.session_state.prog_offset = 0

def navegar_dias(delta):
    st.session_state.prog_offset += delta

def voltar_hoje():
    st.session_state.prog_offset = 0

# ─── HEADER ───────────────────────────────────────────────────────────────────
today_str = date.today().strftime("%d/%m/%Y")
badge_cls = "fonte-online" if fonte_dados == "online" else "fonte-local"
badge_txt = "🟢 Online" if fonte_dados == "online" else "🟡 Local (cache)"

st.markdown(f"""
<div class="header-banner">
  <div class="header-logo">💧</div>
  <div>
    <div class="header-title">Painel Estratégico da Gerência do Litoral</div>
    <div class="header-sub">
      Monitoramento integrado dos indicadores de gestão e operação – GR Litoral / Itapipoca
      <span class="fonte-badge {badge_cls}">{badge_txt}</span>
    </div>
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
      <div class="kpi-card-sub">{n_acima90/max(total_acudes,1)*100:.1f}% do total</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-card-label">〰️ Entre 70% e 90%</div>
      <div class="kpi-card-value">{n_80_90 + n_70_80}</div>
      <div class="kpi-card-sub">{n_entre10_90/max(total_acudes,1)*100:.1f}% do total</div>
    </div>""", unsafe_allow_html=True)
with col5:
    cls = "warn" if n_abaixo10 > 0 else ""
    st.markdown(f"""
    <div class="kpi-card {cls}">
      <div class="kpi-card-label">⚠️ Abaixo de 70%</div>
      <div class="kpi-card-value {cls}">{n_abaixo70}</div>
      <div class="kpi-card-sub">{n_abaixo10/max(total_acudes,1)*100:.1f}% do total</div>
    </div>""", unsafe_allow_html=True)

# ─── NÚCLEO DE GESTÃO ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📋 NÚCLEO DE GESTÃO</div>', unsafe_allow_html=True)

gest_items = [
    ("🫗 Alocações",      gest["aloc_real"],    gest["aloc_meta"],    f"{int(gest['aloc_real'])}/{int(gest['aloc_meta'])} reuniões"),
    ("📈 Acompanhar",     gest["acomp_real"],   gest["acomp_meta"],   f"{int(gest['acomp_real'])}/{int(gest['acomp_meta'])} reuniões"),
    ("📊 Avaliação",      gest["aval_real"],    gest["aval_meta"],    f"{int(gest['aval_real'])}/{int(gest['aval_meta'])} reuniões"),
    ("👥 CBH Ordinária", gest["cbh_ord_real"], gest["cbh_ord_meta"], f"{int(gest['cbh_ord_real'])}/{int(gest['cbh_ord_meta'])} partic. - ({int(gest['reuord'])} / 4)"),
    ("👥 CBH Extraord.", gest["cbh_ext_real"], gest["cbh_ext_meta"], f"{int(gest['cbh_ext_real'])}/{int(gest['cbh_ext_meta'])} partic. - ({int(gest['reuex'])} / 4)"),
    ("👥 CBH Fórum",      gest["cbh_for_real"], gest["cbh_for_meta"], f"{int(gest['cbh_for_real'])}/{int(gest['cbh_for_meta'])} reuniões"),
    ("👩‍🏫 Capacitações",  gest["cap_real"],     gest["cap_meta"],     f"{int(gest['cap_real'])}/{int(gest['cap_meta'])} capacit."),
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

oper_items = [
    ("👨‍🔧 Cor. Anomalias",  oper["anom_real"],  oper["anom_meta"],
     f"Regional: R {int(oper['anom_r'])}/A {int(oper['anom_a'])}<br>Corrigidas: {int(oper['anom_real'])}/{int(oper['anom_meta'])}"),
    ("🪙 Reg. Cobrança",   oper["cob_real"],   oper["cob_meta"],
     f"Novos: {int(oper['cob_novos_r'])} | Inad.: {int(oper['cob_inad_r'])}<br>Real: {int(oper['cob_real'])}/{int(oper['cob_meta'])}"),
    ("🔎 Fiscalização",    oper["fisc_real"],  oper["fisc_meta"],
     f"Com RV: {int(oper['fisc_rv'])} | Sem RV: {int(oper['fisc_srv'])}<br>Real: {int(oper['fisc_real'])}/{int(oper['fisc_meta'])}"),
    ("⏲️ Medidores",        oper["med_final"],  100,
     f"Manut.: {int(oper['med_man_real'])}/{int(oper['med_man_meta'])} | Inst.: {int(oper['med_inst_real'])}/{int(oper['med_inst_meta'])}<br>"
     f"Med.: {int(oper['med_med_real'])}/{int(oper['med_med_meta'])}"),
    ("🚢 Batimetria",      oper["bati_real"],  oper["bati_meta"],
     f"Batimetrias<br>Realizadas: {int(oper['bati_real'])}/{int(oper['bati_meta'])}"),
]

cols_o = st.columns(5)
for col, (label, real, meta, detail) in zip(cols_o, oper_items):
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
            bar_color, dot = "#0b3d91", "🔵"
        elif pct_val >= 70:
            bar_color, dot = "#1a8a8a", "🟢"
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
              <div style="flex:1;background:#e8f0fb;border-radius:3px;height:10px;overflow:hidden">
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

# Donut situação
with col_sit:
    fig_sit = go.Figure(
        go.Pie(
            labels=["Acima de 90%", "80% – 90%", "70% – 80%", "Abaixo de 70%"],
            values=[max(n_acima90,0), max(n_80_90,0), max(n_70_80,0), max(n_abaixo70,0)],
            hole=0.50,
            marker_colors=["#0b3d91", "#1a8a8a", "#f5c842", "#e07b00"],
            textinfo="none",
            hovertemplate="%{label}<br>%{value} açude(s)<extra></extra>",
            sort=False,
        )
    )
    fig_sit.add_annotation(
        text=f"<b>{total_acudes}</b><br><span style='font-size:9px'>açudes</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=24, color="#0b3d91", family="Inter"),
    )
    fig_sit.update_layout(
        margin=dict(l=8, r=8, t=8, b=8),
        showlegend=True,
        legend=dict(orientation="v", x=0.5, xanchor="right", y=-0.18,
                    font=dict(size=10, family="Inter"), itemsizing="constant"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=310,
    )
    st.markdown('<div class="sit-card"><div class="sit-card-title">📊 Situação dos Açudes</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_sit, use_container_width=True, config={"displayModeBar": False}, key="donut_sit")
    st.markdown("</div>", unsafe_allow_html=True)

# ─── PROGRAMAÇÃO COM NAVEGAÇÃO TEMPORAL ──────────────────────────────────────
with col_prog:
    data_alvo     = date.today() + timedelta(days=st.session_state.prog_offset)
    data_alvo_str = data_alvo.strftime("%d/%m/%Y")
    # Dia da semana em PT-BR, sem depender de locale do sistema (weekday(): 0=segunda ... 6=domingo)
    DIAS_SEMANA_EXT = ["Segunda-feira", "Terça-feira", "Quarta-feira",
                        "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_semana_str = DIAS_SEMANA_EXT[data_alvo.weekday()]
    # Coluna A = data, Coluna E (índice 4) = texto da atividade
    COL_ATIVIDADE = 4
    prog_do_dia = []
    if not df_prog.empty:
        for _, row in df_prog.iterrows():
            try:
                row_data = _safe_str(row.iloc[0])
                row_ativ = _safe_str(row.iloc[COL_ATIVIDADE])
                if data_alvo_str in row_data or data_alvo.strftime("%Y-%m-%d") in row_data:
                    if row_ativ:
                        prog_do_dia.append(row_ativ)
            except Exception:
                pass
    if prog_do_dia:
        items_html = "".join(
            f'<div class="prog-item"><span class="prog-dot">●</span><span>{t}</span></div>'
            for t in prog_do_dia
        )
    else:
        items_html = f'<div class="prog-item"><span style="color:#8a9ab0">Nenhuma programação para {data_alvo_str}.</span></div>'
    st.markdown(f"""
    <div class="prog-card">
      <div class="prog-title">📅 Programação — {data_alvo_str} - {dia_semana_str}</div>
      {items_html}
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
    c_prev, c_hoje, c_next = st.columns(3)
    with c_prev:
        st.button("⬅️ Anterior", on_click=navegar_dias, args=(-1,), use_container_width=True)
    with c_hoje:
        st.button("📅 Hoje", on_click=voltar_hoje, use_container_width=True,
                  disabled=(st.session_state.prog_offset == 0))
    with c_next:
        st.button("Próximo ➡️", on_click=navegar_dias, args=(1,), use_container_width=True)

# ─── FOOTER DO PAINEL ────────────────────────────────────────────────────────
fonte_label = "Google Sheets (online)" if fonte_dados == "online" else "arquivo local (xlsx)"
st.markdown(f"""
<div style="text-align:center;margin-top:1.5rem;color:#8a9ab0;font-size:0.72rem">
  COGERH – Companhia de Gestão dos Recursos Hídricos &nbsp;|&nbsp; GR Litoral / Itapipoca &nbsp;|&nbsp;
  Fonte: {fonte_label} &nbsp;|&nbsp; Cache: 5 min
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# CALENDÁRIO DE ATIVIDADES (abaixo do painel)
# ══════════════════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:2.5rem'></div>", unsafe_allow_html=True)

CAL_SHEET_ID = SHEET_ID
CAL_GID = "507430155"
CAL_CSV_URL = f"https://docs.google.com/spreadsheets/d/{CAL_SHEET_ID}/export?format=csv&gid={CAL_GID}"

DIAS_SEMANA_CAL = ["DOMINGO", "SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO"]
MESES_PT = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
MAX_ATIVIDADES_DIA = 10

CATEGORIAS = [
    ("Reunião",          ["reunião", "reuniao", "encontro"],                        "#4A90D9"),
    ("Mobilização",      ["mobilização", "mobilizacao"],                            "#E67E22"),
    ("Publicação/Story", ["publicar", "publicação", "publicacao", "story", "post", "reels", "matéria", "materia", "Parabenizar", "parabenizar"], "#9B59B6"),
    ("Gravação",         ["gravação", "gravacao", "vídeo", "video"],                "#1ABC9C"),
    ("Faturamento",      ["faturamento", "leitura", "hidrômetro", "hidrometro"],    "#27AE60"),
    ("Instrumentação",   ["instrumentação", "instrumentacao", "piezômetro", "piezometro", "percolação", "percolacao"], "#16A085"),
    ("Monitoramento",    ["monitoramento", "captação", "captacao", "perenização", "perenizacao", "sigerh"], "#2980B9"),
    ("Vistoria/Fiscaliz.", ["vistoria", "fiscalização", "fiscalizacao", "inspeção", "inspecao"], "#F4A460"),
    ("Coleta/Água",      ["coleta", "análise qualitativa", "analise qualitativa", "sonda"], "#3498DB"),
    ("Diárias/Admin.",   ["diária", "diaria", "protheus", "estoque", "frota", "almoxarifado", "combustível", "combustivel", "logistico","logístico"], "#20B2AA"),
    ("Relatório/Ata",    ["relatório", "relatorio", "ata", "parecer", "diagnóstico", "diagnostico"], "#8E44AD"),
    ("Capacitação",      ["capacitação", "capacitacao", "curso", "treinamento", "oficina"], "#D35400"),
    ("Feriado/Data",     ["feriado", "ponto facultativo", "data magna", "carnaval", "sexta-feira santa"], "#C0392B"),
]
COR_PADRAO = "#95A5A6"


def categorizar(texto: str):
    if not isinstance(texto, str) or not texto.strip():
        return "Outros", COR_PADRAO
    t = texto.lower()
    for nome, palavras, cor in CATEGORIAS:
        if any(p in t for p in palavras):
            return nome, cor
    return "Outros", COR_PADRAO


@st.cache_data(ttl=600)
def carregar_dados_calendario():
    resp = requests.get(CAL_CSV_URL, timeout=15)
    resp.raise_for_status()
    df_raw = pd.read_csv(
        io.BytesIO(resp.content),
        encoding="utf-8-sig",
        header=None
    )

    df = df_raw.iloc[6:, [0, 4]].copy()
    df.columns = ["data_raw", "atividade"]
    df = df.dropna(subset=["data_raw"])

    df["data"] = pd.to_datetime(df["data_raw"], format="%d/%m/%Y", errors="coerce")
    df = df.dropna(subset=["data"])
    df["data"] = df["data"].dt.date
    df["atividade"] = df["atividade"].fillna("").astype(str).str.strip()
    df = df[df["atividade"] != ""]

    cat_cor = df["atividade"].apply(categorizar)
    df["categoria"] = cat_cor.apply(lambda x: x[0])
    df["cor"] = cat_cor.apply(lambda x: x[1])

    return df.sort_values("data").reset_index(drop=True)


def gerar_observacoes_key(dia: date) -> str:
    return f"obs_{dia.isoformat()}"


hoje = date.today()
if "cal_ano" not in st.session_state:
    st.session_state.cal_ano = hoje.year
if "cal_mes" not in st.session_state:
    st.session_state.cal_mes = hoje.month
if "cal_view" not in st.session_state:
    st.session_state.cal_view = "mes"
if "cal_semana_ref" not in st.session_state:
    st.session_state.cal_semana_ref = hoje
if "cal_observacoes" not in st.session_state:
    st.session_state.cal_observacoes = {}

try:
    df_cal = carregar_dados_calendario()
except Exception as e:
    st.error(f"Erro ao carregar a planilha do calendário: {e}")
    df_cal = pd.DataFrame(columns=["data", "atividade", "categoria", "cor"])


def atividades_do_dia(dia: date):
    return df_cal[df_cal["data"] == dia].to_dict("records")


def render_mes_calendario():
    ano, mes = st.session_state.cal_ano, st.session_state.cal_mes

    st.markdown(f"""
    <div class="cal-header">
        <div class="cal-title">📅 MINHA SEMANA / MÊS</div>
        <div style="font-size:20px; font-weight:700; background:#F5A623; padding:6px 18px; border-radius:6px;">
            {MESES_PT[mes].upper()} / {ano}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([1, 1, 4, 1, 1])
    with c1:
        if st.button("◀ Ano", key="cal_btn_ano_prev"):
            st.session_state.cal_ano -= 1
            st.rerun()
    with c2:
        if st.button("◀ Mês", key="cal_btn_mes_prev"):
            if mes == 1:
                st.session_state.cal_mes, st.session_state.cal_ano = 12, ano - 1
            else:
                st.session_state.cal_mes -= 1
            st.rerun()
    with c4:
        if st.button("Mês ▶", key="cal_btn_mes_next"):
            if mes == 12:
                st.session_state.cal_mes, st.session_state.cal_ano = 1, ano + 1
            else:
                st.session_state.cal_mes += 1
            st.rerun()
    with c5:
        if st.button("Ano ▶", key="cal_btn_ano_next"):
            st.session_state.cal_ano += 1
            st.rerun()

    cores_semana = ["#EC7063", "#F4D03F", "#5DADE2", "#F0B27A", "#52BE80", "#5DADE2", "#A569BD"]
    cols = st.columns(7)
    for i, dia_nome in enumerate(DIAS_SEMANA_CAL):
        cols[i].markdown(
            f'<div class="dia-semana-label" style="background:{cores_semana[i]};color:white;">{dia_nome}</div>',
            unsafe_allow_html=True)

    cal_obj = calendar.Calendar(firstweekday=6)
    semanas = cal_obj.monthdatescalendar(ano, mes)

    for semana in semanas:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            with cols[i]:
                no_mes = dia.month == mes
                ativs = atividades_do_dia(dia)
                borda = "#F5A623" if dia == hoje else "#ddd"
                opacidade = "1" if no_mes else "0.35"

                pills_html = ""
                for a in ativs[:MAX_ATIVIDADES_DIA]:
                    texto = a["atividade"][:60] + ("…" if len(a["atividade"]) > 60 else "")
                    pills_html += f'<div class="atividade-pill" style="background:{a["cor"]};">{texto}</div>'
                if len(ativs) > MAX_ATIVIDADES_DIA:
                    pills_html += f'<div class="mais-info">+{len(ativs)-MAX_ATIVIDADES_DIA} mais</div>'

                card_html = (
                    f'<div class="day-card" style="border-color:{borda}; opacity:{opacidade};">'
                    f'<div class="day-num">{dia.day}</div>'
                    f'{pills_html}'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                label_btn = "Abrir ›" if ativs else "·"
                if st.button(label_btn, key=f"cal_btn_{dia.isoformat()}", use_container_width=True):
                    st.session_state.cal_semana_ref = dia
                    st.session_state.cal_view = "semana"
                    st.rerun()

    with st.expander("🎨 Legenda de categorias"):
        leg_cols = st.columns(4)
        for idx, (nome, _, cor) in enumerate(CATEGORIAS):
            with leg_cols[idx % 4]:
                st.markdown(
                    f'<span style="background:{cor};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{nome}</span>',
                    unsafe_allow_html=True)


def render_semana_calendario():
    ref = st.session_state.cal_semana_ref
    dias_desde_domingo = (ref.weekday() + 1) % 7
    inicio_semana = ref - timedelta(days=dias_desde_domingo)
    dias = [inicio_semana + timedelta(days=i) for i in range(7)]

    c1, c2, c3 = st.columns([1, 5, 1])
    with c1:
        if st.button("◀ Voltar ao mês", key="cal_btn_voltar_mes"):
            st.session_state.cal_view = "mes"
            st.rerun()
    with c2:
        st.markdown(
            f"<h2 style='text-align:center;'>MINHA SEMANA — {inicio_semana.strftime('%d/%m')} a {dias[-1].strftime('%d/%m/%Y')}</h2>",
            unsafe_allow_html=True)
    with c3:
        nav1, nav2 = st.columns(2)
        with nav1:
            if st.button("◀", key="cal_btn_sem_prev"):
                st.session_state.cal_semana_ref = ref - timedelta(days=7)
                st.rerun()
        with nav2:
            if st.button("▶", key="cal_btn_sem_next"):
                st.session_state.cal_semana_ref = ref + timedelta(days=7)
                st.rerun()

    cores_semana = ["#EC7063", "#F4D03F", "#5DADE2", "#F0B27A", "#52BE80", "#5DADE2", "#A569BD"]
    cols = st.columns(7)

    for i, dia in enumerate(dias):
        with cols[i]:
            classe_extra = " week-card-hoje" if dia == hoje else ""

            ativs = atividades_do_dia(dia)
            pills_html = ""
            if not ativs:
                pills_html = '<div class="sem-atividade">Sem atividades</div>'
            else:
                for a in ativs[:MAX_ATIVIDADES_DIA]:
                    pills_html += f'<div class="atividade-pill" style="background:{a["cor"]};">{a["atividade"]}</div>'
                if len(ativs) > MAX_ATIVIDADES_DIA:
                    pills_html += f'<div class="mais-info">+{len(ativs)-MAX_ATIVIDADES_DIA} atividades não exibidas</div>'

            bloco_html = (
                f'<div class="week-header" style="background:{cores_semana[i]};">'
                f'{DIAS_SEMANA_CAL[i]}<br><span class="data-sub">{dia.strftime("%d/%m")}</span>'
                f'</div>'
                f'<div class="week-card{classe_extra}">{pills_html}</div>'
            )
            st.markdown(bloco_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📝 Observações da semana")
    chave = gerar_observacoes_key(inicio_semana)
    valor_atual = st.session_state.cal_observacoes.get(chave, "")
    novo_valor = st.text_area("Anotações, lembretes ou pendências desta semana:",
                               value=valor_atual, height=120, key=f"cal_ta_{chave}")
    st.session_state.cal_observacoes[chave] = novo_valor
    st.caption("⚠️ Observações ficam salvas apenas durante esta sessão do navegador.")


if st.session_state.cal_view == "mes":
    render_mes_calendario()
else:
    render_semana_calendario()
