# DECISIONS
| DATA | DECISAO | MOTIVO |
|---|---|---|
| 2026-10-15 | Python 3.12 gerenciado com uv | Ambiente reprodutível com lockfile |
| 2026-10-15 | Parquet (bronze) + DuckDB (silver/gold) | Sem servidor, ótimo para análise local |
| 2026-10-15 | dbt-duckdb para transformação | SQL versionado com testes |
| 2026-10-15 | Dagster para orquestração | Assets integram bem com dbt |
| 2026-10-15 | Granularidade diária por subsistema | Cabe em 30 dias e responde à pergunta |
| 2026-10-15 | data/ fora do git | Dados são reproduzíveis pelo pipeline |
