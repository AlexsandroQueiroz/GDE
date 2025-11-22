
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="Dashboard Dinâmico - 073 (Reescrito)", layout="wide")
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

st.image("data:image/png;base64,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",width=150)
st.title("Gestão de entregas (Reescrito)")

# --- dicionario_placas (mantive seu mapeamento original)
dicionario_placas = { 
    "AUU2168": "JEAN CARLO FILUS",
    "ARK2319": "GILMAR BONETE",
    "BCP0A55": "SERGIO MARKOWICZ",
    "MHV4747": "GILSON BONETE",
    "MIK5D90": "URBANO CARACHO",
    "BAF1554": "CARLOS FELIPE",
    "NZL5D30": "EDIR JEZ",
    "ATD5C29": "GETER ZACARIAS",
    "AOQ4182": "EDILSON MAURILIO CORREA",
    "AYA2D69": "ROBERTO MAURILIO CORREIA",
    "AVY2D92": "MAURILIO PINHEIRO",
    "ATC2B88": "EDUARDO JOSE DA SILVA",
    "AWC4B38": "PEDRO CEZAR TROMBACO",
    "AZN3A28": "ANTONIO MARCOS",
    "DRI2F93": "ELISANDRA MUFATO",
    "AYY9490": "ALEX FABIANO FAGUNDES DOS SANTOS",
    "MDS0F24": "CLEBERSON FURLAN",
    "DVS1B60": "FABIANO ANTONIO DA ROCHA",
    "MLN9J58": "DOUGLAS IAN FRANCO",
    "MAY1F93": "JONATHAN GREGORIO DA SILVA",
    "AVP9B09": "JOSUE LUIS DE SOUZA",
    "FGU4I29": "LOURIVAL ROEPER",
    "AZU0D80": "LUIZ FELIPE DA PAZ VELLOSO",
    "AXY3B00": "MAIKON EIDT GONCALVES",
    "AVI0896": "JADIR APARECIDO DOS SANTOS",
    "AOX1J30": "DIEGO RAMOS FRANCISCO DA SILVA",
    "EVO9E70": "REINALDO KERSCHER DA ROCHA",
    "CUA0F83": "ROGERIO ATNER",
    "AUT3H70": "RONALDO COSTA",
    "JCN4E40": "WAGNER VELOSO DE OLIVEIRA",
    "PUJ4F40": "CELSO APARECIDO DA ROCHA",
    "AXX1C73": "REGINALDO LEMOS",
    "FCE1F91": "DIEGO VALDOMIRO",
    "ATU3532": "HEVERTON ROSA DOS SANTOS",
    "AUB8I31": "OTONIEL MAXIMIANO DA SILVA",
    "JAS2E67": "AGUINALDO MORAIS TEIXEIRA",
    "JBC2B51": "EDSON PEREIRA DA SILVA",
    "ATO8908": "JOSE APARECIDO DE JESUS",
    "JAS2E48": "NIVALDO SANTOS SOUZA",
    "AQH2023": "ANSELMO APARECIDO RODRIGUES",
    "NEC1362": "EDIVANDO DEFAVERI",
    "ETU4F95": "MARCIO DE OLIVEIRA JORGE",
    "OYT0H45": "EMERSON FERREIRA DE ANDRADE",
    "MGV0679": "SILVIO TOLARDO",
    "MFT7941": "EDSON JOSE COUTINHO",
    "MMF0820": "JULIO CEZAR",
    "IPA4J50": "LUIZ PROSDOCIMO",
    "ARE9E25": "WIWILLIAM CANDIDO CAETANOLLIAN",
    "ARV2769": "EMERSON GONCALVES APOLINARIO",
    "OLS4C44": "JOSÉ GENARIO LEAL",
    "EFU0H78": "MAURICIO CESAR MYSZKA",
    "RHN3D74": "JUAREZ DOS SANTOS",
    "JBS3I12": "ADRIANO PORFIRIO",
    "AQM2782": "ODAIR ANTONIO FEDRIGO",
    "RJX9B77": "JHONATA SERGIO DUTKEVICZ DO NASCIMENTO",
    "AUE0B95": "JOSE ADMIR",
    "AYM4313": "WILLIAN CORTES CARDOSO",
    "AAM6A01": "WILLIAN CORTES CARDOSO",
    "ATZ1H55": "JOSÉ GENARIO LEAL",
    "AGW0057": "THIAGO ALDAMIR MARQUES LEITH",
    "TAX3I90": "FRANCISCO RICARDO SARAIVA DE ARAUJO",
    "DVT9J76": "JOAO ANDRADE PIRES",
    "FME5E96": "AURELIO ROBERTO MORAIS SOARES",
    "PGR6B00": "MURILO HENRIQUE DOS SANTOS",
    "APQ0I85": "EVERSON MARCELO ALVES CARDOSO",
    "AYH0C58": "GERSON MARCELO SKRYPEC BUENO",
    "EGR9E16": "APARECIDO RODRIGUES DA SILVA",
    "MHW2734": "MARIA DO SOCORRO",
    "BDA4J25": "ALVARO LUIZ SANDRI",
    "IRU6B73": "WAGNER GONCALVES DA SILVA",
    "APW1789": "DHONATA ROVERSO MUSSO",
    "NMR2D71": "CLAUDINEI APARECIDO DE JESUS",
    "BAM5D71": "MARCIO JOSE GOMES",
    "ATJ8452": "JULIO CESAR KNOPF"
}

# Uploads
if 'expander_rel200' not in st.session_state:
    st.session_state.expander_rel200 = True
if 'expander_rel455' not in st.session_state:
    st.session_state.expander_rel455 = True

with st.expander("📘 Upload do Relatório 200", expanded=st.session_state.expander_rel200):
    uploaded_rel200 = st.file_uploader("Escolha o arquivo Relatório 200 (xlsx)", type=["xlsx"], key="rel200")
if uploaded_rel200:
    st.session_state.expander_rel200 = False
    st.session_state.df_200 = pd.read_excel(uploaded_rel200, skiprows=1)

with st.expander("📘 Upload do Relatório 455", expanded=st.session_state.expander_rel455):
    uploaded_rel455 = st.file_uploader("Escolha o arquivo Relatório 455 (xlsx)", type=["xlsx"], key="rel455")
if uploaded_rel455:
    st.session_state.expander_rel455 = False
    st.session_state.df_455 = pd.read_excel(uploaded_rel455, skiprows=1)

# Date window logic (same as original)
agora = datetime.now()
dia_semana = agora.weekday()
if dia_semana == 0:
    inicio = (agora - timedelta(days=3)).replace(hour=7, minute=0, second=0, microsecond=0)
else:
    inicio = (agora - timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0)
fim = agora.replace(hour=7, minute=0, second=0, microsecond=0)

if 'df_200' in st.session_state:
    df_200 = st.session_state.df_200
    # keep original filters
    if "SITUACAO" in df_200.columns:
        df_200 = df_200[~df_200["SITUACAO"].astype(str).str.contains("CANCELADO", case=False, na=False)]
    df_200["datahorasaida"] = pd.to_datetime(
        df_200.get("DIA_SAIDA_MANIF", "").astype(str) + " " + df_200.get("HORA_SAIDA_MANIF", "").astype(str),
        errors="coerce"
    )
    df_200 = df_200.dropna(subset=["datahorasaida"])
    df_200f = df_200[(df_200["datahorasaida"] >= inicio) & (df_200["datahorasaida"] < fim)]
else:
    df_200 = pd.DataFrame()
    df_200f = pd.DataFrame()

inicio_dia = inicio.date()
fim_dia = fim.date()

if 'df_455' in st.session_state:
    df_455 = st.session_state.df_455.copy()
    # normalize date columns
    for col in ["Data do Ultimo Manifesto", "Data do Ultimo Romaneio"]:
        if col in df_455.columns:
            df_455[col] = pd.to_datetime(df_455[col], errors="coerce").dt.date

    df_455 = df_455.dropna(subset=["Data do Ultimo Manifesto", "Data do Ultimo Romaneio"], how="all")
    condicao_m = (df_455.get("Data do Ultimo Manifesto") >= inicio_dia) & (df_455.get("Data do Ultimo Manifesto") < fim_dia)
    condicao_r = (df_455.get("Data do Ultimo Romaneio") >= inicio_dia) & (df_455.get("Data do Ultimo Romaneio") < fim_dia)
    df_455f = df_455[condicao_m | condicao_r].copy()

    # filters from original code
    if "Unidade da Ultima Ocorrencia" in df_455f.columns:
        df_455f = df_455f[df_455f["Unidade da Ultima Ocorrencia"] != "BTR - JK2"]
    if "Codigo da Ultima Ocorrencia" in df_455f.columns:
        df_455f = df_455f[df_455f["Codigo da Ultima Ocorrencia"] != 47]
    condicao_cwb = (df_455f.get("Unidade Destino do Ultimo Manifesto") == "CWB") & (df_455f.get("Ultimo Romaneio").isna())
    if not df_455f.empty:
        df_455f = df_455f[~condicao_cwb]
    if "Mercadoria" in df_455f.columns:
        df_455f = df_455f[~df_455f["Mercadoria"].isin(["  168-PALLETS", "  001-DIVERSOS"])]

    # Ajustes e mapeamentos
    if "Ultimo Manifesto" in df_455f.columns:
        df_455f["Manifesto_Ajustado"] = df_455f["Ultimo Manifesto"].astype(str).str.replace(" ", "", regex=False)
    df_455f["Placa_Final"] = df_455f.get("Placa de Entrega")

    mask_sem_placa = df_455f["Placa_Final"].isna() | (df_455f["Placa_Final"] == "")
    if not df_200.empty and "NUM_MANIF" in df_200.columns and "PLACA_CAVALO" in df_200.columns:
        mapa_manifesto_placa = df_200.set_index("NUM_MANIF")["PLACA_CAVALO"]
        df_455f.loc[mask_sem_placa, "Placa_Final"] = df_455f.loc[mask_sem_placa, "Manifesto_Ajustado"].map(mapa_manifesto_placa)

    mapa_placa_motorista = {}
    if not df_200f.empty and "PLACA_CAVALO" in df_200f.columns and "MOTORISTA" in df_200f.columns:
        mapa_placa_motorista = df_200f.drop_duplicates(subset=["PLACA_CAVALO"]).set_index("PLACA_CAVALO")["MOTORISTA"].to_dict()

    df_455f["Motorista"] = df_455f["Placa_Final"].map(mapa_placa_motorista)
    df_455f["Motorista"] = df_455f.apply(lambda row: dicionario_placas.get(row["Placa_Final"], row["Motorista"]), axis=1)

    # Montar tabela final (colunas base)
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
        rename_map["Notas Fiscais"] = "NF's"

    df_final = df_455f.rename(columns=rename_map)

    # ensure required columns exist before selecting
    for c in ["CT-e", "Placa_Final", "Motorista", "Cliente", "Destino", "Cidade", "NF's", "Tipo"]:
        if c not in df_final.columns:
            df_final[c] = ""

    df_final = df_final[["CT-e", "Placa_Final", "Motorista", "Cliente", "Destino", "Cidade", "NF's", "Tipo"]].copy()

    # cria Status e renomeia NF's mantendo conteúdo
    df_final["Status"] = ""

    # renomeia NF's para NF e mantém o conteúdo original
    if "NF's" in df_final.columns:
        df_final = df_final.rename(columns={"NF's": "NF"})
    else:
        df_final["NF"] = ""


    # --- Importação automática da base Shipment (Google Sheets CSV) ---
    url_ship = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTm_mQYZvgTLu4C6Xpu1FvXw_IX0Eatl9MRMxkhH8BylxZO0POFN_oji0XxnGddkvaGN3PDJYYWD_Ed/pub?output=csv"

    try:
        df_ship = pd.read_csv(url_ship)
        df_ship.columns = df_ship.columns.str.strip()
        # assume A = CT-e, C = Shipment (as requested)
        if len(df_ship.columns) >= 3:
            df_ship = df_ship.rename(columns={df_ship.columns[0]: "CT-e", df_ship.columns[2]: "Shipment"})
        else:
            # fallback: try common names
            df_ship = df_ship.rename(columns={df_ship.columns[0]: "CT-e"})
            if "Shipment" not in df_ship.columns:
                # try to find a column containing 'Shipment' in its name
                for col in df_ship.columns:
                    if "ship" in col.lower():
                        df_ship = df_ship.rename(columns={col: "Shipment"})
                        break
    except Exception as e:
        st.error(f"Não foi possível carregar a base Shipment: {e}")
        df_ship = pd.DataFrame(columns=["CT-e", "Shipment"])

    # Ajuste da Shipment conforme regra: remove 1º dígito (esperado 8), remove últimos 2 dígitos (esperado 12), prefixa 700
    def ajustar_shipment(x):
        if pd.isna(x) or str(x).strip() == "":
            return ""
        s = str(x).strip()
        # keep only digits
        s_digits = "".join(ch for ch in s if ch.isdigit())
        if len(s_digits) <= 3:
            return s_digits
        # remove first char and last two chars safely
        core = s_digits[1:-2] if len(s_digits) > 3 else ""
        if core == "":
            return ""
        return "700" + core

    if "Shipment" in df_ship.columns:
        df_ship["Shipment"] = df_ship["Shipment"].apply(ajustar_shipment)
    else:
        df_ship["Shipment"] = ""

    # Merge shipments
    if "CT-e" not in df_ship.columns:
        st.warning("A base Shipment não possui coluna CT-e reconhecida; a coluna Shipment ficará vazia.")
        df_ship["CT-e"] = ""

    df_final = df_final.merge(df_ship[["CT-e", "Shipment"]], on="CT-e", how="left")

    # Rename Placa_Final to Placa to match requested output
    df_final = df_final.rename(columns={"Placa_Final": "Placa"})

    # Reorder columns exactly as requested
    final_order = ["CT-e", "Status", "Placa", "Motorista", "Cliente", "Destino", "Cidade", "NF", "Shipment", "Tipo"]
    for col in final_order:
        if col not in df_final.columns:
            df_final[col] = ""
    df_final = df_final[final_order].copy()

    # Display and download
    st.subheader("Relatório Consolidado")
    st.dataframe(df_final.set_index('CT-e'), use_container_width=True)

    # Prepare excel file
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

        # alternating colors by motorista
        motoristas = df_final["Motorista"].fillna("").astype(str).tolist()
        colors = ['#FFFFFF', '#F2F2F2']
        for row_num, motorista in enumerate(motoristas, start=1):
            bg_color = colors[hash(motorista) % 2]
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
