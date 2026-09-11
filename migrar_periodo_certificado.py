
import sqlite3
import sys

CAMINHO_BANCO = "cvauto.db"


def coluna_permite_nulo(cursor, tabela, coluna):
    cursor.execute(f"PRAGMA table_info({tabela})")
    for row in cursor.fetchall():
        # row: (cid, name, type, notnull, dflt_value, pk)
        if row[1] == coluna:
            return row[3] == 0
    raise RuntimeError(f"coluna '{coluna}' nao encontrada na tabela '{tabela}'")


def main():
    con = sqlite3.connect(CAMINHO_BANCO)
    cur = con.cursor()

    if coluna_permite_nulo(cur, "certificados", "periodo"):
        print("Nada a fazer: a coluna 'periodo' ja aceita valor nulo.")
        con.close()
        return

    print("Migrando tabela 'certificados' (periodo -> aceita nulo)...")

    cur.execute("PRAGMA foreign_keys=off")
    cur.execute("BEGIN TRANSACTION")
    cur.execute("ALTER TABLE certificados RENAME TO certificados_old")
    cur.execute(
        """
        CREATE TABLE certificados (
            id INTEGER NOT NULL,
            nome VARCHAR NOT NULL,
            instituicao VARCHAR NOT NULL,
            carga_horaria INTEGER,
            situacao VARCHAR(12) NOT NULL,
            periodo VARCHAR,
            arquivo_path VARCHAR,
            curriculo_id INTEGER NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(curriculo_id) REFERENCES curriculos (id)
        )
        """
    )
    cur.execute("INSERT INTO certificados SELECT * FROM certificados_old")
    cur.execute("DROP TABLE certificados_old")
    con.commit()
    cur.execute("PRAGMA foreign_keys=on")

    cur.execute("SELECT COUNT(*) FROM certificados")
    total = cur.fetchone()[0]
    con.close()

    print(f"Migracao concluida com sucesso. {total} certificado(s) preservado(s).")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERRO na migracao: {exc}", file=sys.stderr)
        sys.exit(1)
