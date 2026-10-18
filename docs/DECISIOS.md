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