import os
import sqlite3

class Database:

    def __init__(self):

        self.conn = sqlite3.connect("Data/automacao.db")

        self.cursor = self.conn.cursor()

        self.criar_tabela()

    def criar_tabela(self):

        self.cursor.execute("""

            CREATE TABLE IF NOT EXISTS chamados (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                id_chamado TEXT UNIQUE,

                categoria TEXT,

                perguntas_feitas INTEGER,

                respostas_recebidas INTEGER,

                aprovacao INTEGER,

                status TEXT,

                erro TEXT

            )

        """)

        self.conn.commit()

    def salvar_chamado(self, id_chamado):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO chamados (
                id_chamado
            )
            VALUES (?)
        """, (id_chamado,))

        self.conn.commit()

        print(f"[DB] Chamado salvo: {id_chamado}")

    def atualizar_categoria(self, id_chamado, categoria):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE chamados
            SET categoria = ?
            WHERE REPLACE(id_chamado, ' ', '') = ?
        """, (categoria, id_chamado))

        self.conn.commit()

    def atualizar_validacoes(
        self,
        id_chamado,
        perguntas,
        aprovacao
    ):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE chamados
            SET
                perguntas_feitas = ?,
                aprovacao = ?
            WHERE id_chamado = ?
        """, (
            int(perguntas),
            int(aprovacao),
            id_chamado
        ))

        self.conn.commit()

        print(f"[DB] Validações atualizadas: {id_chamado}")