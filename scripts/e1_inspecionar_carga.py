""" E1 / Tarefa 1.2: inspeciona o parquet de amostra de carga diaria do ONS """

from pathlib import Path
import duckdb

ARQUIVO = Path("data/samples/CARGA_ENERGIA_2024.parquet")

def titulo(texto: str) -> None:
    print(f"\n{'=' * 70}\n{texto}\n{'=' * 70}")

def main() -> None:
    if not ARQUIVO.exists():
        raise SystemExit(f"ARQUIVO NAO ENCONTRADO: {ARQUIVO}. REFACA O PASSO 1")
    
    con = duckdb.connect() # banco temporario em memoria, nao grava nada
    con.execute(f"CREATE VIEW carga AS SELECT * FROM read_parquet('{ARQUIVO}')")

    titulo("1. COLUNAS E TIPOS (o formulario da tabela)")
    colunas = con.execute("DESCRIBE carga").fetchall()
    for nome, tipo, *_ in colunas:
        print(f" {nome:<30} {tipo}")

    titulo("2. PRIMEIRAS 5 LINHSA (como sao os dados na pratica)")
    print(con.sql("SELECT * FROM carga LIMIT 5").df().to_string())

    titulo("3. TAMANHO")
    total = con.execute("SELECT count(*) FROM carga").fetchone()[0]
    print(f"LINHAS NO ARQUIVO: {total}")

    titulo("4. PERIODO COBERTO (colunas de data)")
    achou_data = False
    for nome, tipo, *_ in colunas:
        if tipo.startswith(("DATE", "TIMESTAMP")):
            achou_data = True
            mn, mx = con.execute(
                f'SELECT min("{nome}"), max("{nome}") FROM carga'
            ).fetchone()

            dias = con.execute(
                f'SELECT count(DISTINCT CAST ("{nome}" AS DATE))FROM carga'
            ).fetchone()[0]
            print(f"{nome}: de {mn} ate {mx} ({dias} dias distintos)")
        if not achou_data:
            print(" Nenhuma coluna de data de verdade: a data deve estar com texto.")

    
    titulo("5. COLUNAS DE TEXTO (candidatas a região/categoria)")
    for nome, tipo, *_ in colunas:
        if tipo == "VARCHAR":
            distintos = con.execute(
                f'SELECT count(DISTINCT "{nome}") FROM carga'
            ).fetchone()[0]
            print(f"  {nome}: {distintos} valores distintos")
            if distintos <= 20:
                valores = con.execute(
                    f'SELECT DISTINCT "{nome}" FROM carga ORDER BY 1'
                ).fetchall()
                print("     valores:", [v[0] for v in valores])

    titulo("6. QUALIDADE (mínimo, máximo e % de nulos por coluna)")
    resumo = con.sql("SUMMARIZE carga").df()
    cols = ["column_name", "column_type", "min", "max", "null_percentage"]
    print(resumo[cols].to_string(index=False))


if __name__ == "__main__":
    main()   
