import sqlite3

conexao = sqlite3.connect('pescaria.db')

cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS estoque_peixes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL
)
''')

peixes = [
    ('Pacu', 150),
    ('Pintado', 85),
    ('Dourado', 40),
    ('Cachara', 60),
    ('Curimbatá', 200),
    ('Piapara', 120),
    ('Piau', 180),
    ('Traíra', 90),
    ('Barbado', 35),
    ('Jaú', 15)
]


cursor.execute('DELETE FROM estoque_peixes')

cursor.executemany('''
INSERT INTO estoque_peixes (nome, quantidade) VALUES (?, ?)
''', peixes)

conexao.commit()
conexao.close()

print("Banco de dados 'pescaria.db' criado e populado com sucesso!")