#STATE 
**Etapa atual** E1 Contrato e dados

## Pronto
- E0 concluída (repo, uv, ruff, pytest, CI verde)
- E1/1.1: dataset `carga-energia` (ONS), 1 Parquet por ano (2000 a 2026; 2026 parcial)
- E1/1.2 (parcial): 2024 tem 1464 linhas = 366 dias x 4 subsistemas.
  Colunas: id_subsistema, nom_subsistema, din_instante (TIMESTAMP), val_cargaenergiamwmed (DOUBLE)
  - E1/1.2 concluída (2024): [N] linhas, [N] dias distintos, 4 subsistemas por dia.
  Nulos: [N]. Duplicatas: [N]. Unidade da carga: [conforme dicionário].
  Média por subsistema: SE [x], NE [x], S [x], N [x].
  - E1/1.3: validar a API Open-Meteo



## Proximo passo exato 
E1/1.4: modelo estrela e janela de anos

## Bloqueios 
- nenhum
