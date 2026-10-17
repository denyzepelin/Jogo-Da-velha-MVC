import sqlite3

# check_same_thread=False permite que o listener do teclado (pynput) salve dados sem erro de thread
conexao = sqlite3.connect("banco.db", check_same_thread=False)
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS game (
id INTEGER PRIMARY KEY AUTOINCREMENT,
vez_jogador INT NOT NULL,
jogador1 TEXT NOT NULL,
jogador2 TEXT NOT NULL,
game_finished BOOLEAN NOT NULL,
result TEXT,
tabuleiro TEXT NOT NULL)""")
conexao.commit()


def save_state(vez_jogador, jogador1, jogador2, game_finished, result, tabuleiro):
    cursor.execute(
        """INSERT INTO game (vez_jogador, jogador1, jogador2, game_finished, result, tabuleiro) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (vez_jogador, jogador1, jogador2, game_finished, result, str(tabuleiro))
    )
    conexao.commit()
    return cursor.lastrowid  # Retorna o ID do jogo recém-criado


def get_status():
    cursor.execute("SELECT * FROM game")
    return cursor.fetchall()


def game_not_finished():
    cursor.execute("SELECT * FROM game WHERE game_finished = 0")
    return cursor.fetchall()


def get_game_by_id(game_id):
    cursor.execute("SELECT * FROM game WHERE id = ?", (game_id,))
    return cursor.fetchone()


def update_game_status(game_id, vez_jogador, game_finished, result, tabuleiro):
    cursor.execute(
        """UPDATE game 
           SET vez_jogador = ?, game_finished = ?, result = ?, tabuleiro = ? 
           WHERE id = ?""",
        (vez_jogador, game_finished, result, str(tabuleiro), game_id)
    )
    conexao.commit()