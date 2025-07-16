import sqlite3

import state


class Db:
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(state.config['db'])
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise RuntimeError("Dati gioco non trovati") from e

    def get(self, query:str)->list:
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def getOne(self, query:str)->dict:
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def execute(self, query:str):
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()
