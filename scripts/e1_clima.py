#%% [1] Cidades ancoras (uma por subsistema)
import httpx
import pandas as pd

CIDADES = pd.DataFrame(
    [
        ("SE", "Sao Paulo", -23.55, -46.63),
        ("S", "Porto Alegre", -30.03, -52.23),
        ("NE", "Salvador", -12.97, -38.51),
        ("N", "Belem", -1.46, -48.50),

    ],
    columns=["id_subsistema", "cidade", "latitude", "longitude"],
    
)
CIDADES
# %%
# %% [2] Primeiro pedido: uma cidade, um ano
URL = "https://archive-api.open-meteo.com/v1/archive"

cid = CIDADES.loc[CIDADES["id_subsistema"] == "SE"].iloc[0]
params = {
    "latitude": cid["latitude"],
    "longitude": cid["longitude"],
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "daily": "temperature_2m_mean,temperature_2m_max,temperature_2m_min",
    "timezone": "America/Sao_Paulo",
}

resp = httpx.get(URL, params=params, timeout=30)
print("Status HTTP:", resp.status_code)  # esperado: 200

dados = resp.json()
print("Campos da resposta:", list(dados.keys()))
print("Coordenada usada pela API:", dados["latitude"], dados["longitude"])
print("Unidades:", dados["daily_units"])
# %% [3] Resposta -> tabela
clima_se = pd.DataFrame(dados["daily"]).rename(
    columns={
        "time": "data",
        "temperature_2m_mean": "temp_media",
        "temperature_2m_max": "temp_max",
        "temperature_2m_min": "temp_min",
    }
)
clima_se["data"] = pd.to_datetime(clima_se["data"])

print("Linhas x colunas:", clima_se.shape)
print("Nulos por coluna:")
print(clima_se.isna().sum())
clima_se.describe()

# %%
# %% [4] Clima + carga do SE: o join fecha?
import duckdb

carga_se = duckdb.sql("""
    SELECT CAST(din_instante AS DATE) AS data,
           id_subsistema,
           val_cargaenergiamwmed      AS carga_mwmed
    FROM read_parquet('data/samples/CARGA_ENERGIA_2024.parquet')
    WHERE id_subsistema = 'SE'
""").df()
carga_se["data"] = pd.to_datetime(carga_se["data"])

junta = carga_se.merge(clima_se, on="data", how="outer", indicator=True)
print(junta["_merge"].value_counts())  # both = achou par; left_only/right_only = sobrou

junta[["carga_mwmed", "temp_media"]].corr()

#%% os 4 substemas de uma vez
import time

PARAMS_BASE = {
    "start_date":"2024-01-01",
    "end_date":"2024-12-31",
    "daily":"temperature_2m_mean,temperature_2m_max,temperature_2m_min",
    "timezone":"America/Sao_Paulo",
}
RENOMEAR = {
    "time":"data",
    "temperature_2m_mean":"temp_media",
    "temperature_2m_max":"temp_max",
    "temperature_2m_min":"temp_min",
}

pedacos = []
for _, c in CIDADES.iterrows():
    params = {**PARAMS_BASE, "latitude": c["latitude"], "longitude":c["longitude"]}
    r = httpx.get(URL, params=params, timeout=30)
    r.raise_for_status() #mostra o erro se houver

    df = pd.DataFrame(r.json()["daily"]).rename(columns=RENOMEAR)
    df["id_subsistema"] = c["id_subsistema"]
    pedacos.append(df)
    
    print(f"{c["cidade"]:<14} status={r.status_code} linhas={len(df)}")
    time.sleep(1) # pausa de 1seg entre requisicoes

clima = pd.concat(pedacos, ignore_index=True)
clima["data"] = pd.to_datetime(clima["data"])

print("\n TOTAL DE LINHAS: ", len(clima))
print("NULOS: ", int(clima.isna().sum().sum()))
clima.groupby("id_subsistema").size()

# %% [6] Join completo: 4 subsistemas x 366 dias
import duckdb
carga = duckdb.sql("""
                    SELECT CAST(din_instante AS DATE) AS data,
                    id_subsistema,
                    val_cargaenergiamwmed AS carga_mwmed
                    FROM read_parquet('data/samples/CARGA_ENERGIA_2024.parquet')""").df()

carga["data"] = pd.to_datetime(carga["data"])
junta = carga.merge(
                    clima,
                    on=["data","id_subsistema"],
                    how="outer",
                    indicator=True,
                    validate="one_to_one", #erro se houver duplicata em qualquer lado
)

print("linhas: ", len(junta))
print(junta["_merge"].value_counts())

print("\n correlacao carga x temperatura media por subsistema: ")
for sub, g in junta.groupby("id_subsistema"):
    print(f" {sub:<3} {g["carga_mwmed"].corr(g["temp_media"]):.2f}")

    #%% [7] ate que dia vai o arquivo de 2026
    import duckdb

    duckdb.sql("""
                SELECT min(CAST(din_instante AS DATE)) AS primeiro_dia,
                        max(CAST(din_instate AS DATE)) AS ultimo_dia,
                        count(DISTINCT CAST(din_instante AS DATE)) AS dias,
                        count(*)                                AS linhas
                        FROM read_parquet('data/samples/CARGA_ENERGIA_2024.parquet')""").df()