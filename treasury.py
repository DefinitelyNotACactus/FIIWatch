import pandas as pd
import numpy as np

def parse_sheet(table, sheet):
    df = table.parse(sheet)
    df.columns = df.iloc[0].values

    df = df.iloc[1:]
    df.index = pd.to_datetime(df['Dia'], format='%d/%m/%Y')
    df.drop(columns=['Dia'], inplace=True)
    
    return df

# IPCA + (Juros Semestrais)
NTNB = pd.ExcelFile('https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2022/NTN-B_2022.xls')
NTNB_DICT = {name[-2:]: parse_sheet(NTNB, name) for name in NTNB.sheet_names}
NTNB_LAST_UPDATE = str(NTNB_DICT[NTNB.sheet_names[0][-2:]].index[-1]).split(' ')[0]
# IPCA +
#NTNB_PRINCIPAL = pd.ExcelFile('https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2022/NTN-B_Principal_2022.xls')
# IGPM +
#NTNC = pd.ExcelFile('https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2022/NTN-C_2022.xls')
# Pré-fixado (Juros Semestrais)
NTNF = pd.ExcelFile('https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2022/NTN-F_2022.xls')
NTNF_DICT = {name[-2:]: parse_sheet(NTNF, name) for name in NTNF.sheet_names}
NTNF_LAST_UPDATE = str(NTNF_DICT[NTNF.sheet_names[0][-2:]].index[-1]).split(' ')[0]
# Tesouro SELIC
LFT = pd.ExcelFile('https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2022/LFT_2022.xls')
LFT_DICT = {name[-2:]: parse_sheet(LFT, name) for name in LFT.sheet_names}
LFT_LAST_UPDATE = str(LFT_DICT[LFT.sheet_names[0][-2:]].index[-1]).split(' ')[0]
# Pré-fixado
#LTN = pd.ExcelFile('https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2022/LTN_2022.xls')
