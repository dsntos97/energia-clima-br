# %% [1] Conectar ao arquiv
from pathlib import Path 
import duckdb

print("pasta de trabalho: ", Path.cwd())

ARQUIVO = Path("../data/samples/CARGA_ENERGIA_2024.parquet")
con = duckdb.connect()
con.execute(f"CREATE OR REPLACE VIEW carga AS SELECT * FROM read_parquet('{ARQUIVO}')")
con.sql("SELECT * FROM carga LIMIT 5").df()

# %% [2] Qual periodo o arquivo cobre?
con.sql(""" SELECT min(din_instante)           AS primeiro_dia,
                   max(din_instante)           AS ultimo_dia,
                   count(DISTINCT din_instante) AS dias_distintos
                   FROM carga""").df()

# %%  [3] Cada Dia tem exatamente 4 Subsistemas ?
con.sql(""" SELECT n_subsistemas, count(*) AS dias
            FROM (
                SELECT din_instante, count (*) AS n_subsistemas
                FROM carga
                GROUP BY din_instante)
                GROUP BY n_subsistemas""").df()
            
            
# %% Ha valores faltantes? 

con.sql(""" SELECT count(*) AS linhas,
                    count(*) - count(din_instante) AS datas_nulas,
                    count(*) - count(id_subsistema) AS subsistemas_nulos,
                    count(*) - count(val_cargaenergiamwmed) AS cargas_nulas
                    FROM carga""").df()

# %% [5] Há linhas repetidas (mesmo dia e mesmo subsistema)?
con.sql("""
    SELECT din_instante, id_subsistema, count(*) AS repeticoes
    FROM carga
    GROUP BY din_instante, id_subsistema
    HAVING count(*) > 1
""").df()


# %% [6] Os valores fazem sentido? (por subsistema)
con.sql("""
    SELECT id_subsistema,
           nom_subsistema,
           round(min(val_cargaenergiamwmed)) AS minimo,
           round(avg(val_cargaenergiamwmed)) AS media,
           round(max(val_cargaenergiamwmed)) AS maximo
    FROM carga
    GROUP BY id_subsistema, nom_subsistema
    ORDER BY media DESC
""").df()


# %% [7] O que o dicionário oficial diz sobre as colunas?
import json

dicionario = json.loads(
    Path("../data/samples/DicionarioDados_Carga_Energia_Diaria.json").read_text()
)
print(json.dumps(dicionario, indent=2, ensure_ascii=False)[:3000])