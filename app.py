import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import date
import base64

# ─── 1. PAGE CONFIG ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Estratégico – GR Litoral",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── 2. FUNÇÃO PARA CARREGAR O PNG ──────────────────────────────────────────
@st.cache_data
def carregar_imagem(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    img_base64 = carregar_imagem("template.png")
except:
    img_base64 = "" # Prevenção de erro caso a imagem não esteja no diretório

# ─── 3. CSS GLOBAL E CSS DO TEMPLATE PNG ────────────────────────────────────
st.markdown("""
<style>
/* Reset & Globals do seu app original */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding: 0 1.5rem 2rem 1.5rem !important; max-width: 100% !important; }

/* CSS Mágico para o Fundo PNG e os Cards Absolutos */
.wrap-kpi { position: relative; width: 100%; max-width: 1500px; margin: 0 auto 2rem auto; }
.bg-template { width: 100%; display: block; border-radius: 10px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); }
.slot { 
    position: absolute; display: flex; align-items: center; justify-content: center;
    font-family: 'Inter', sans-serif; font-weight: 800; color: #0b3d91; 
}
.kpi-valor { font-size: 2.8vw; } /* Tamanho responsivo baseado na tela */

/* Seus estilos de cards para a parte debaixo */
.card { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 100%; }
.prog-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #333; margin-bottom: 6px; }
.prog-dot { color: #0b3d91; font-size: 10px; }
</style>
""", unsafe_allow_html=True)

# ─── 4. CARREGAMENTO E PROCESSAMENTO DE DADOS (SEU MOTOR) ───────────────────
XLSX = Path(__file__).parent / "painel da grlitoral.xlsx"

@st.cache_data(ttl=300)
def load_data():
    # Carregando as abas conforme seu código original
    df_m = pd.read_excel(XLSX, sheet_name="metas", header=None)
    df_a = pd.read_excel(XLSX, sheet_name="açudes", header=None)
    return df_m, df_a

try:
    df_metas, df_acudes = load_data()
    
    # Processamento de Açudes
    acudes = []
    for i in range(len(df_acudes)):
        if pd.notna(df_acudes.iloc[i, 0]):
            acudes.append({
                "nome": str(df_acudes.iloc[i, 0]).strip(),
                "municipio": str(df_acudes.iloc[i, 1]),
                "vol": float(df_acudes.iloc[i, 8]),
                "pct": float(df_acudes.iloc[i, 9])
            })
            
    total_acudes = len(acudes)
    total_vol = sum(a["vol"] for a in acudes)
    n_acima90 = sum(1 for a in acudes if a["pct"] >= 90)
    n_entre10_90 = sum(1 for a in acudes if 10 <= a["pct"] < 90)
    n_abaixo10 = sum(1 for a in acudes if a["pct"] < 10)
    
    # Simulação da "Programação de hoje" (do seu código)
    prog_hoje = ["Reunião de alocação negociada do açude Patos", 
                 "Publicação de matéria sobre o açude Santo Antônio",
                 "Monitoramento dos Poços e Medição de Vazão"]

except Exception as e:
    st.error(f"Erro ao carregar a planilha: {e}")
    st.stop()


# ─── 5. HEADER COM O PNG E KPIs ALOCADOS (O CASAMENTO PERFEITO) ─────────────
# Aqui pegamos as suas 5 métricas principais e jogamos cirurgicamente no PNG
# NOTA EXPLORADORA: Ajuste as porcentagens de 'left' e 'top' para alinhar milimetricamente 
# com os buracos desenhados na sua imagem 'template.png'.

html_header = f'''
<div class="wrap-kpi">
    <img class="bg-template" src="data:image/png;base64,{img_base64}">
    
    <div class="slot kpi-valor" style="left: 6%; top: 40%; width: 14%; height: 30%;">{total_acudes}</div>
    
    <div class="slot kpi-valor" style="left: 24%; top: 40%; width: 14%; height: 30%;">{total_vol:.2f}</div>
    
    <div class="slot kpi-valor" style="left: 42.5%; top: 40%; width: 14%; height: 30%;">{n_acima90}</div>
    
    <div class="slot kpi-valor" style="left: 61%; top: 40%; width: 14%; height: 30%;">{n_entre10_90}</div>
    
    <div class="slot kpi-valor" style="left: 79.5%; top: 40%; width: 14%; height: 30%;">{n_abaixo10}</div>
</div>
'''
st.markdown(html_header, unsafe_allow_html=True)


# ─── 6. O RESTO DO SEU DASHBOARD ORIGINAL LOGO ABAIXO DO PNG ────────────────
st.markdown("<br>", unsafe_allow_html=True)

# Linha do Meio: Gestão e Operação
col_g, col_o = st.columns(2)

with col_g:
    st.markdown("### 🟢 NÚCLEO DE GESTÃO PARTICIPATIVA")
    st.info("Aqui entram os indicadores extraídos da aba 'gest.csv' do seu motor original. (Reuniões, CBH, etc)")

with col_o:
    st.markdown("### 🟡 NÚCLEO DE OPERAÇÃO")
    st.warning("Aqui entram os indicadores da aba 'oper.csv' (Fiscalização, Instalação e Manutenção).")

st.markdown("<hr style='margin: 1rem 0; border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)

# Linha de Baixo: Açudes, Gráfico Plotly e Programação
col_t, col_p, col_prog = st.columns([2, 1.2, 1.2])

with col_t:
    st.markdown("#### 📋 Situação dos Açudes")
    df_exibicao = pd.DataFrame(acudes)
    # Formatação rápida para exibição
    if not df_exibicao.empty:
        df_exibicao.columns = ['Açude', 'Município', 'Vol (hm³)', 'Vol (%)']
        st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

with col_p:
    st.markdown("#### 🍩 Distribuição")
    # O seu gráfico Plotly Donut Chart recriado!
    fig_sit = go.Figure(go.Pie(
        labels=["< 10%", "10% a 90%", "> 90%"],
        values=[n_abaixo10, n_entre10_90, n_acima90],
        hole=0.6,
        marker_colors=["#e74c3c", "#f1c40f", "#2ecc71"],
        textinfo="none"
    ))
    fig_sit.add_annotation(
        text=f"<b>{total_acudes}</b><br><span style='font-size:10px'>açudes</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color="#0b3d91", family="Inter")
    )
    fig_sit.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=True,
        legend=dict(orientation="h", x=0, y=-0.2, font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=280
    )
    st.plotly_chart(fig_sit, use_container_width=True, config={"displayModeBar": False})

with col_prog:
    st.markdown("#### 📅 Programação de Hoje")
    items_html = "".join(f'<div class="prog-item"><span class="prog-dot">●</span><span>{t}</span></div>' for t in prog_hoje)
    st.markdown(f'<div class="card">{items_html}</div>', unsafe_allow_html=True)
