
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="GDE", layout="wide")
st.markdown(
    """
    <style>
    .main {background-color: #fefefe;}
    .stSidebar .sidebar-content {background-color: #0B3C5D; color: white;}
    .stButton>button {background-color: #1C6EA4; color: white;}
    .stMetricValue {color: #1C6EA4; font-weight:bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Gestão de entregas")

# Uploads
if 'expander_rel200' not in st.session_state:
    st.session_state.expander_rel200 = True
if 'expander_rel455' not in st.session_state:
    st.session_state.expander_rel455 = True

with st.expander("📘 Upload do Relatório 200 (xlsx)", expanded=st.session_state.expander_rel200):
    uploaded_rel200 = st.file_uploader("Escolha o arquivo Relatório 200 (xlsx)", type=["xlsx"], key="rel200")
if uploaded_rel200:
    st.session_state.expander_rel200 = False
    st.session_state.df_200 = pd.read_excel(uploaded_rel200, skiprows=1)

with st.expander("📘 Upload do Relatório 455 (xlsx)", expanded=st.session_state.expander_rel455):
    uploaded_rel455 = st.file_uploader("Escolha o arquivo Relatório 455 (xlsx)", type=["xlsx"], key="rel455")
if uploaded_rel455:
    st.session_state.expander_rel455 = False
    st.session_state.df_455 = pd.read_excel(uploaded_rel455, skiprows=1)


# Janela de datas
agora = datetime.now()
dia_semana = agora.weekday()
if dia_semana == 0:
    inicio = (agora - timedelta(days=3)).replace(hour=7, minute=0, second=0, microsecond=0)
else:
    inicio = (agora - timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0)
fim = agora.replace(hour=7, minute=0, second=0, microsecond=0)

if 'df_200' in st.session_state:
    df_200 = st.session_state.df_200.copy()
    if "SITUACAO" in df_200.columns:
        df_200 = df_200[~df_200["SITUACAO"].astype(str).str.contains("CANCELADO", case=False, na=False)]
    df_200["datahorasaida"] = pd.to_datetime(
        df_200.get("DIA_SAIDA_MANIF", "").astype(str) + " " + df_200.get("HORA_SAIDA_MANIF", "").astype(str),
        errors="coerce"
    )
    df_200 = df_200.dropna(subset=["datahorasaida"])
    df_200f = df_200[(df_200["datahorasaida"] >= inicio) & (df_200["datahorasaida"] < fim)].copy()
else:
    df_200 = pd.DataFrame()
    df_200f = pd.DataFrame()

inicio_dia = inicio.date()
fim_dia = fim.date()

if 'df_455' in st.session_state:
    df_455 = st.session_state.df_455.copy()

    
    for col in ["Data do Ultimo Manifesto", "Data do Ultimo Romaneio"]:
        if col in df_455.columns:
            df_455[col] = pd.to_datetime(df_455[col], errors="coerce").dt.date

    df_455 = df_455.dropna(subset=["Data do Ultimo Manifesto", "Data do Ultimo Romaneio"], how="all")

    condicao_m = (df_455.get("Data do Ultimo Manifesto") >= inicio_dia) & (df_455.get("Data do Ultimo Manifesto") < fim_dia)
    condicao_r = (df_455.get("Data do Ultimo Romaneio") >= inicio_dia) & (df_455.get("Data do Ultimo Romaneio") < fim_dia)
    df_455f = df_455[condicao_m | condicao_r].copy()

    
    if "Unidade da Ultima Ocorrencia" in df_455f.columns:
        df_455f = df_455f[df_455f["Unidade da Ultima Ocorrencia"] != "BTR - JK2"]
    if "Codigo da Ultima Ocorrencia" in df_455f.columns:
        df_455f = df_455f[df_455f["Codigo da Ultima Ocorrencia"] != 47]
    condicao_cwb = (df_455f.get("Unidade Destino do Ultimo Manifesto") == "CWB") & (df_455f.get("Ultimo Romaneio").isna())
    if not df_455f.empty:
        df_455f = df_455f[~condicao_cwb]
    if "Mercadoria" in df_455f.columns:
        df_455f = df_455f[~df_455f["Mercadoria"].isin(["  168-PALLETS", "  001-DIVERSOS"])]

    
    if "Ultimo Manifesto" in df_455f.columns:
        df_455f["Manifesto_Ajustado"] = df_455f["Ultimo Manifesto"].astype(str).str.replace(" ", "", regex=False)
    df_455f["Placa_Final"] = df_455f.get("Placa de Entrega", "")

    mask_sem_placa = df_455f["Placa_Final"].isna() | (df_455f["Placa_Final"] == "")
    if not df_200.empty and "NUM_MANIF" in df_200.columns and "PLACA_CAVALO" in df_200.columns:
        mapa_manifesto_placa = df_200.set_index("NUM_MANIF")["PLACA_CAVALO"]
        df_455f.loc[mask_sem_placa, "Placa_Final"] = df_455f.loc[mask_sem_placa, "Manifesto_Ajustado"].map(mapa_manifesto_placa)

    
    mapa_placa_motorista = {}
    if not df_200f.empty and "PLACA_CAVALO" in df_200f.columns and "MOTORISTA" in df_200f.columns:
        mapa_placa_motorista = df_200f.drop_duplicates(subset=["PLACA_CAVALO"]).set_index("PLACA_CAVALO")["MOTORISTA"].to_dict()

    
    if "Motorista" not in df_455f.columns:
        df_455f["Motorista"] = ""

    
    rename_map = {}
    if "Serie/Numero CTRC" in df_455f.columns:
        rename_map["Serie/Numero CTRC"] = "CT-e"
    if "Cliente Remetente" in df_455f.columns:
        rename_map["Cliente Remetente"] = "Cliente"
    if "Cliente Destinatario" in df_455f.columns:
        rename_map["Cliente Destinatario"] = "Destino"
    if "Cidade de Entrega" in df_455f.columns:
        rename_map["Cidade de Entrega"] = "Cidade"
    if "Mercadoria" in df_455f.columns:
        rename_map["Mercadoria"] = "Tipo"
    if "Notas Fiscais" in df_455f.columns:
        rename_map["Notas Fiscais"] = "NF"

    df_final = df_455f.rename(columns=rename_map)

    
    for c in ["CT-e", "Placa_Final", "Motorista", "Cliente", "Destino", "Cidade", "NF", "Tipo"]:
        if c not in df_final.columns:
            df_final[c] = ""

    df_final = df_final[["CT-e", "Placa_Final", "Motorista", "Cliente", "Destino", "Cidade", "NF", "Tipo"]].copy()

    
    df_final["Status"] = ""

  
    url_ship = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTm_mQYZvgTLu4C6Xpu1FvXw_IX0Eatl9MRMxkhH8BylxZO0POFN_oji0XxnGddkvaGN3PDJYYWD_Ed/pub?output=csv"

    try:
        df_sheet = pd.read_csv(url_ship, dtype=str)
        df_sheet.columns = df_sheet.columns.str.strip()
    except Exception as e:
        st.error(f"Erro ao carregar Google Sheets: {e}")
        df_sheet = pd.DataFrame()

    
    if not df_sheet.empty:
        
        if len(df_sheet.columns) >= 3:
            df_sheet = df_sheet.rename(columns={df_sheet.columns[0]: "CT-e", df_sheet.columns[2]: "Shipment"})
        else:
            
            df_sheet = df_sheet.rename(columns={df_sheet.columns[0]: "CT-e"})
            for col in df_sheet.columns:
                if "ship" in col.lower():
                    df_sheet = df_sheet.rename(columns={col: "Shipment"})
                    break

    df_sheet["Shipment"] = df_sheet.get("Shipment", "").fillna("")

    def ajustar_shipment(x):
        if x is None or str(x).strip() == "":
            return ""
        s = str(x).strip()
        s_digits = "".join(ch for ch in s if ch.isdigit())
        if len(s_digits) <= 3:
            return s_digits
        core = s_digits[1:-2] if len(s_digits) > 3 else ""
        if core == "":
            return ""
        return "700" + core

    if "Shipment" in df_sheet.columns:
        df_sheet["Shipment"] = df_sheet["Shipment"].apply(ajustar_shipment)
    else:
        df_sheet["Shipment"] = ""

   
    df_motoristas = pd.DataFrame(columns=["Placa", "Motorista_Sheet"])
    if not df_sheet.empty:
        if len(df_sheet.columns) >= 7:
            
            df_motoristas = df_sheet.rename(columns={
                df_sheet.columns[5]: "Placa",
                df_sheet.columns[6]: "Motorista_Sheet"
            })[["Placa", "Motorista_Sheet"]].copy()
        else:
            
            cols_low = [c.lower() for c in df_sheet.columns]
            placa_col = None
            motor_col = None
            for i, c in enumerate(cols_low):
                if "plac" in c:
                    placa_col = df_sheet.columns[i]
                if "motor" in c:
                    motor_col = df_sheet.columns[i]
            if placa_col and motor_col:
                df_motoristas = df_sheet[[placa_col, motor_col]].rename(columns={placa_col: "Placa", motor_col: "Motorista_Sheet"}).copy()
   
    if not df_motoristas.empty:
        df_motoristas["Placa"] = df_motoristas["Placa"].astype(str).str.strip()
        df_motoristas["Motorista_Sheet"] = df_motoristas["Motorista_Sheet"].astype(str).str.strip()
    else:
        df_motoristas = pd.DataFrame(columns=["Placa", "Motorista_Sheet"])

    
    if "CT-e" in df_sheet.columns:
        df_final = df_final.merge(df_sheet[["CT-e", "Shipment"]], on="CT-e", how="left")
    else:
        df_final = df_final.assign(Shipment="")

    
    if "Placa_Final" in df_final.columns:
        df_final["Motorista_200"] = df_final["Placa_Final"].map(mapa_placa_motorista) if mapa_placa_motorista else ""
    else:
        df_final["Motorista_200"] = ""

    
    df_final["Motorista"] = df_final.apply(
        lambda row: row["Motorista"] if pd.notna(row.get("Motorista")) and str(row.get("Motorista")).strip() != "" else (row.get("Motorista_200") if pd.notna(row.get("Motorista_200")) else ""),
        axis=1
    )

    
    if not df_motoristas.empty and "Placa_Final" in df_final.columns:
        df_final = df_final.merge(df_motoristas, left_on="Placa_Final", right_on="Placa", how="left")
        df_final["Motorista"] = df_final.apply(
            lambda row: row["Motorista"] if pd.notna(row.get("Motorista")) and str(row.get("Motorista")).strip() != "" else (row.get("Motorista_Sheet") if pd.notna(row.get("Motorista_Sheet")) else ""),
            axis=1
        )
        df_final = df_final.drop(columns=["Placa", "Motorista_Sheet"], errors="ignore")

   
    df_final = df_final.drop(columns=["Motorista_200"], errors="ignore")

    
    if "Placa_Final" in df_final.columns:
        df_final = df_final.rename(columns={"Placa_Final": "Placa"})
    if "Shipment" not in df_final.columns:
        df_final["Shipment"] = ""


    final_order = ["CT-e", "Status", "Placa", "Motorista", "Cliente", "Destino", "Cidade", "Shipment", "NF", "Tipo"]
    for col in final_order:
        if col not in df_final.columns:
            df_final[col] = ""
    df_final = df_final[final_order].copy()


    df_final = df_final.drop_duplicates(subset=["CT-e"], keep="first").copy()

   
    st.subheader("Relatório Consolidado")
    st.dataframe(df_final.set_index('CT-e'), use_container_width=True)

    # Preparar arquivo Excel para download
    df_final = df_final.sort_values(by="Motorista").reset_index(drop=True)
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False, sheet_name="Relatório")
        workbook = writer.book
        worksheet = writer.sheets["Relatório"]
        worksheet.hide_gridlines(2)
        worksheet.freeze_panes(1, 0)
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'align': 'center',
            'fg_color': '#D9E1F2',
            'border': 1
        })
        for col_num, value in enumerate(df_final.columns.values):
            worksheet.write(0, col_num, value, header_format)
            max_len = max(df_final[value].astype(str).map(len).max(), len(value)) + 2
            worksheet.set_column(col_num, col_num, max_len)

        center_format = workbook.add_format({'align': 'center'})
        try:
            ct_col_idx = df_final.columns.get_loc("CT-e")
            worksheet.set_column(ct_col_idx, ct_col_idx, 15, center_format)
        except Exception:
            pass

   
        placas = df_final["Placa"].fillna("").astype(str).tolist()
        paleta = ['#FFFFFF', '#F2F2F2']
        for row_num, placa in enumerate(placas, start=1):
            idx = abs(hash(placa)) % len(paleta)
            bg_color = paleta[idx]
            format_row = workbook.add_format({'bg_color': bg_color})
            worksheet.set_row(row_num, None, format_row)

    excel_buffer.seek(0)
    st.download_button(
        label="Baixar Relatório",
        data=excel_buffer,
        file_name=f"Relatorio_Ocorrencias_{datetime.now().strftime('%d-%m-%Y')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Faça upload dos relatórios 200 e 455 para gerar o relatório consolidado.")
