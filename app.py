import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
import io
import requests
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
    padding: 1.5rem 1.5rem 2rem 1.5rem !important;
    max-width: 1400px !important;
    min-width: 1100px !important;
    width: 1400px !important;
}

.header-banner {
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
}
.header-logo { font-size: 2.97rem; }
.header-title { color: #ffffff; font-size: 2.295rem; font-weight: 800; line-height: 1.15; margin: 0; }
.header-sub { color: rgba(255,255,255,0.78); font-size: 1.107rem; margin-top: 0.2rem; }
.header-date {
    margin-left: auto;
    background: rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    color: #ffffff;
    font-size: 1.107rem;
    font-weight: 600;
    white-space: nowrap;
}

.section-header {
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
}

.kpi-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.10);
    border-left: 4px solid #0b3d91;
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-card.warn  { border-left-color: #e07b00; }
.kpi-card.good  { border-left-color: #1a8a8a; }
.kpi-card-label { font-size: 0.999rem; color: #5a6a7e; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.kpi-card-value { font-size: 2.295rem; font-weight: 800; color: #0b3d91; line-height: 1.1; }
.kpi-card-value.warn { color: #e07b00; }
.kpi-card-value.good { color: #1a8a8a; }
.kpi-card-sub   { font-size: 0.792rem; color: #8a9ab0; margin-top: 0.2rem; }

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
    font-size: 0.932rem;
    font-weight: 700;
    color: #0b3d91;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    line-height: 1.3;
    width: 100%;
}
.ind-card-meta  { font-size: 0.68rem; color: #8a9ab0; }
.ind-card-detail { font-size: 0.905rem; color: #5a6a7e; line-height: 1.5; width: 100%; }

.acude-table-wrap {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
}
.acude-table-title { font-size: 1.053rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; }

.sit-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 0.75rem 0.75rem 0.75rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    box-sizing: border-box;
}
.sit-card-title {
    font-size: 1.053rem;
    font-weight: 700;
    color: #0b3d91;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
    text-align: center;
    width: 100%;
}

.prog-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 8px rgba(11,61,145,0.09);
    height: 100%;
}
.prog-title { font-size: 1.053rem; font-weight: 700; color: #0b3d91; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.7rem; }
.prog-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid #f0f4fa;
    font-size: 0.88rem;
    color: #2d3a4a;
    line-height: 1.4;
}
.prog-item:last-child { border-bottom: none; }
.prog-dot { color: #1a8a8a; font-size: 0.81rem; margin-top: 0.3rem; flex-shrink: 0; }

.fonte-badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: 0.5rem;
}
.fonte-online { background: #d4edda; color: #155724; }
.fonte-local  { background: #fff3cd; color: #856404; }

.js-plotly-plot .plotly .modebar { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─── CONFIGURAÇÃO DA FONTE DE DADOS ──────────────────────────────────────────
SHEET_ID  = "1kte6Ys9vgzw7a0Z1PDXkxf6VOX9KHWlRCXp7P-7RSi4"
XLSX_LOCAL = Path(__file__).parent / "painel da grlitoral.xlsx"

SHEETS = {
    "metas":  f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=metas",
    "açudes": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=a%C3%A7udes",
    "prog":   f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=prog",
}

# Intervalo dos açudes na planilha: A100:A107 → índices 99–106 (0-based)
ACUDE_START = 99
ACUDE_END   = 107  # exclusive

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
    """
    Tenta carregar dados do Google Sheets online.
    Se falhar, usa o xlsx local como fallback.
    Retorna (df_metas, df_acudes, df_prog, fonte).
    """
    try:
        dfs = {}
        for nome, url in SHEETS.items():
            resp = requests.get(url, timeout=15)
            resp.encoding = "utf-8"          # ← CORRIGIDO: força encoding antes de resp.text
            resp.raise_for_status()
            dfs[nome] = pd.read_csv(
                io.StringIO(resp.text),
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
    cbh_ord_real  = cell(df_metas,  3, 4),
    cbh_ext_meta  = cell(df_metas,  7, 2),
    cbh_ext_real  = cell(df_metas,  8, 4),
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
)

oper = dict(
    anom_meta     = cell(df_metas, 61, 2),
    anom_real     = cell(df_metas, 61, 4),
    anom_r     = cell(df_metas, 62, 4),
    anom_a     = cell(df_metas, 63, 4),
    
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

# Programação de hoje (linhas 85–94, col A)
prog_hoje = []
for i in range(85, 95):
    s = cell_str(df_metas, i, 0)
    if s and s.upper() not in ("PROGRAMAÇÃO DE HOJE",):
        prog_hoje.append(s)
    if len(prog_hoje) >= 8:
        break

# ─── PARSE DOS AÇUDES ─────────────────────────────────────────────────────────
# Intervalo correto: linhas 100–107 da planilha = índices 99–106 (0-based)
acudes = []
for i in range(ACUDE_START, min(ACUDE_END, len(df_acudes))):
    nome = cell_str(df_acudes, i, 0)
    if not nome:
        continue
    vol     = _safe_float(df_acudes.iloc[i, 8] if df_acudes.shape[1] > 8 else None)
    pct_val = _safe_float(df_acudes.iloc[i, 9] if df_acudes.shape[1] > 9 else None)
    municipio = cell_str(df_acudes, i, 1)
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
    if meta == 0: return 0
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

# ─── HEADER ───────────────────────────────────────────────────────────────────
today_str = date.today().strftime("%d/%m/%Y")
badge_cls = "fonte-online" if fonte_dados == "online" else "fonte-local"
badge_txt = "🟢 Online" if fonte_dados == "online" else "🟡 Local (cache)"

st.markdown(f"""
<div class="header-banner">
  <div class="header-logo">💧</div>
  <div>
    <div class="header-title">Dashboard Estratégico da Gerência Regional</div>
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
      <div class="kpi-card-label">〰️ Entre 10% e 90%</div>
      <div class="kpi-card-value">{n_entre10_90}</div>
      <div class="kpi-card-sub">{n_entre10_90/max(total_acudes,1)*100:.1f}% do total</div>
    </div>""", unsafe_allow_html=True)
with col5:
    cls = "warn" if n_abaixo10 > 0 else ""
    st.markdown(f"""
    <div class="kpi-card {cls}">
      <div class="kpi-card-label">⚠️ Abaixo de 10%</div>
      <div class="kpi-card-value {cls}">{n_abaixo10}</div>
      <div class="kpi-card-sub">{n_abaixo10/max(total_acudes,1)*100:.1f}% do total</div>
    </div>""", unsafe_allow_html=True)

# ─── NÚCLEO DE GESTÃO ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📋 NÚCLEO DE GESTÃO</div>', unsafe_allow_html=True)

gest_items = [
    ("🫗 Alocações",     gest["aloc_real"],    gest["aloc_meta"],    f"{int(gest['aloc_real'])}/{int(gest['aloc_meta'])} reuniões"),
    ("📈 Acompanhar",    gest["acomp_real"],   gest["acomp_meta"],   f"{int(gest['acomp_real'])}/{int(gest['acomp_meta'])} reuniões"),
    ("📊 Avaliação",     gest["aval_real"],    gest["aval_meta"],    f"{int(gest['aval_real'])}/{int(gest['aval_meta'])} reuniões"),
    ("👥 CBH Ordinária", gest["cbh_ord_real"], gest["cbh_ord_meta"], f"{int(gest['cbh_ord_real'])}/{int(gest['cbh_ord_meta'])} partic."),
    ("👥 CBH Extraord.", gest["cbh_ext_real"], gest["cbh_ext_meta"], f"{int(gest['cbh_ext_real'])}/{int(gest['cbh_ext_meta'])} partic."),
    ("👥 CBH Fórum",     gest["cbh_for_real"], gest["cbh_for_meta"], f"{int(gest['cbh_for_real'])}/{int(gest['cbh_for_meta'])} reuniões"),
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

avg_med_pct = oper["med_final"]
  

oper_items = [
    ("👨‍🔧 Cor. Anomalias",  oper["anom_real"],  oper["anom_meta"],
     f"Regional: R {int(oper['anom_r'])}/A {int(oper['anom_a'])}<br>Corrigidas: {int(oper['anom_real'])}/{int(oper['anom_meta'])}"),
    ("🪙 Reg. Cobrança",   oper["cob_real"],   oper["cob_meta"],
     f"Novos: {int(oper['cob_novos_r'])} | Inad.: {int(oper['cob_inad_r'])}<br>Real: {int(oper['cob_real'])}/{int(oper['cob_meta'])}"),
    ("🔎 Fiscalização",    oper["fisc_real"],  oper["fisc_meta"],
     f"Com RV: {int(oper['fisc_rv'])} | Sem RV: {int(oper['fisc_srv'])}<br>Real: {int(oper['fisc_real'])}/{int(oper['fisc_meta'])}"),
     ("⏲️ Medidores",       avg_med_pct,        100,
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

# Donut situação
with col_sit:
    fig_sit = go.Figure(go.Pie(
        labels=["Abaixo de 70%", "70% – 80%", "80% – 90%", "Acima de 90%"],
        values=[max(n_abaixo70, 0), max(n_70_80, 0), max(n_80_90, 0), max(n_acima90, 0)],
        hole=0.50,
        marker_colors=["#e07b00", "#f5c842", "#0b3d91", "#1a8a8a"],
        textinfo="none",
        hovertemplate="%{label}<br>%{value} açude(s)<extra></extra>",
    ))
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
    st.markdown('</div>', unsafe_allow_html=True)

# Programação
with col_prog:
    items_html = "".join(
        f'<div class="prog-item"><span class="prog-dot">●</span><span>{t}</span></div>'
        for t in prog_hoje
    ) or '<div class="prog-item"><span style="color:#8a9ab0">Nenhuma programação registrada para hoje.</span></div>'
    st.markdown(f"""
    <div class="prog-card">
      <div class="prog-title">📅 Programação — {today_str}</div>
      {items_html}
    </div>""", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
fonte_label = "Google Sheets (online)" if fonte_dados == "online" else "arquivo local (xlsx)"
st.markdown(f"""
<div style="text-align:center;margin-top:1.5rem;color:#8a9ab0;font-size:0.72rem">
  COGERH – Companhia de Gestão dos Recursos Hídricos &nbsp;|&nbsp; GR Litoral / Itapipoca &nbsp;|&nbsp;
  Fonte: {fonte_label} &nbsp;|&nbsp; Cache: 5 min
</div>""", unsafe_allow_html=True)
