# Dicionário de dados

## Fontes
| Fonte | Dataset | Licença/uso | Acesso |
|---|---|---|---|
| ONS | `carga-energia` (Carga de Energia Diária) | CC-BY: creditar o ONS | Parquet anual no S3 público do ONS |
| Open-Meteo | Archive API (ERA5) | Uso conforme termos do Open-Meteo: creditar a fonte | API HTTP sem chave |

Dado **real** em ambas as fontes. Nada simulado neste projeto.

## Bronze: carga (ONS, cru)
| Coluna | Tipo | Descrição oficial | Observações |
|---|---|---|---|
| id_subsistema | VARCHAR | [COPIAR DO DICIONÁRIO ONS] | Valores: N, NE, S, SE |
| nom_subsistema | VARCHAR | [COPIAR DO DICIONÁRIO ONS] | Nome por extenso |
| din_instante | TIMESTAMP | [COPIAR DO DICIONÁRIO ONS] | Diário, mas vem como TIMESTAMP; converter para DATE na silver |
| val_cargaenergiamwmed | DOUBLE | [COPIAR DO DICIONÁRIO ONS] | Unidade: [CONFIRMAR, esperado MWmed] |

## Bronze: clima (Open-Meteo, cru)
| Campo | Tipo | Descrição | Unidade |
|---|---|---|---|
| time | texto (AAAA-MM-DD) | Dia, no fuso America/Sao_Paulo | n/a |
| temperature_2m_mean | número | Temperatura média do dia a 2 m do solo | °C |
| temperature_2m_max | número | Temperatura máxima do dia | °C |
| temperature_2m_min | número | Temperatura mínima do dia | °C |

Não há coluna de região no retorno da API: nós a adicionamos ao baixar (id_subsistema, pela cidade-âncora).

## Gold: tabelas finais
### fato_carga_clima_diaria (1 linha = 1 dia x 1 subsistema)
| Coluna | Tipo | Chave | Origem | Regra |
|---|---|---|---|---|
| data | DATE | PK, FK | din_instante / time | Dentro da janela do projeto |
| id_subsistema | VARCHAR | PK, FK | id_subsistema | Um de N, NE, S, SE |
| carga_mwmed | DOUBLE | | val_cargaenergiamwmed | Maior que 0 |
| temp_media | DOUBLE | | temperature_2m_mean | Faixa plausível: -5 a 45 °C |
| temp_max | DOUBLE | | temperature_2m_max | Maior ou igual a temp_media |
| temp_min | DOUBLE | | temperature_2m_min | Menor ou igual a temp_media |

### dim_data
| Coluna | Tipo | Descrição |
|---|---|---|
| data | DATE (PK) | Dia do calendário |
| ano, mes | INT | Derivados da data |
| dia_da_semana | INT | 1 = segunda ... 7 = domingo (confirmar a convenção na E3) |
| eh_fim_de_semana | BOOLEAN | Sábado ou domingo |

### dim_regiao
| Coluna | Tipo | Descrição |
|---|---|---|
| id_subsistema | VARCHAR (PK) | N, NE, S, SE |
| nome_subsistema | VARCHAR | Nome por extenso (da fonte ONS) |
| cidade_ancora | VARCHAR | São Paulo, Porto Alegre, Salvador, Belém (SE, S, NE, N) |
| latitude, longitude | DOUBLE | Coordenadas usadas na API de clima |

## Limitações e notas
- Uma cidade-âncora por subsistema é uma simplificação do clima real.
- Clima é reanálise (ERA5), não estação meteorológica.
- A janela termina no último dia disponível nas duas fontes.