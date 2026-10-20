# DECISIONS
| DATA | DECISAO | MOTIVO |
|---|---|---|
| 2026-10-15 | Python 3.12 gerenciado com uv | Ambiente reprodutível com lockfile |
| 2026-10-15 | Parquet (bronze) + DuckDB (silver/gold) | Sem servidor, ótimo para análise local |
| 2026-10-15 | dbt-duckdb para transformação | SQL versionado com testes |
| 2026-10-15 | Dagster para orquestração | Assets integram bem com dbt |
| 2026-10-15 | Granularidade diária por subsistema | Cabe em 30 dias e responde à pergunta |
| 2026-10-15 | data/ fora do git | Dados são reproduzíveis pelo pipeline |
| 2026-10-18 | Clima via Open-Meteo Archive (ERA5), sem chave | Gratuito, histórico longo, diário |
| 2026-10-18 | 1 cidade-âncora por subsistema (SP, POA, SSA, BEL) | Simplificação v1; v2.0 pode usar média ponderada |
| 2026-10-18 | Chave de integração: (data, id_subsistema) | Carga e clima encaixam 1:1 por dia e subsistema |
| 2026-10-18 | Janela 2021-01-01 até o último dia comum às duas fontes | 5 anos completos; 2020 distorcido pela pandemia |
| 2026-10-18 | 2026 parcial reservado para teste incremental (E4) e teste final do modelo (E6) | Dado que o modelo nunca viu |
| 2026-10-18 | Modelo estrela: dim_data, dim_regiao, fato_carga_clima_diaria | Perguntas analíticas viram joins simples |