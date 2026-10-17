from pynput import keyboard
import viewer
import database

def verificar_vitoria(tab_user):
    
    # Linhas da matriz
    
    for i in range(3):
        if tab_user[i] == [1, 1, 1] or tab_user[i] == [2, 2, 2]:
            return tab_user[i][0]

    # Colunas da matriz
    
    for i in range(3):
        var_de_verificacao = [tab_user[0][i], tab_user[1][i], tab_user[2][i]]
        if var_de_verificacao == [1, 1, 1] or var_de_verificacao == [2, 2, 2]:
            return var_de_verificacao[0]

    # Verifica diagonais
    
    diagonal1 = [tab_user[0][0], tab_user[1][1], tab_user[2][2]]
    diagonal2 = [tab_user[2][0], tab_user[1][1], tab_user[0][2]]
    if diagonal1 == [2, 2, 2] or diagonal1 == [1, 1, 1]:
        return diagonal1[1]
    if diagonal2 == [2, 2, 2] or diagonal2 == [1, 1, 1]:
        return diagonal2[1]

    # Verifica empate
    
    for x in range(3):
        for y in range(3):
            if tab_user[x][y] == 0:
                return 0
    return 3

def comecar_jogo(tabuleiro, tabuleiro_focus, LocTabFocus, jogo_terminou, x, jogadorX, JogadorO, game_id):
    jogador_atual = jogadorX if x[0] == 1 else JogadorO
    viewer.game_interface(tabuleiro, tabuleiro_focus, jogador_atual)

    def jogar(direcao):
        nonlocal jogo_terminou

        # Movimentação do cursor no tabuleiro
        if (not direcao[0] + LocTabFocus[0] == 3 and
            not direcao[1] + LocTabFocus[1] == 3 and
            not direcao[0] + LocTabFocus[0] == -1 and
            not direcao[1] + LocTabFocus[1] == -1 and
            not direcao == [10, 10]):
            tabuleiro_focus[LocTabFocus[0]][LocTabFocus[1]] = False
            LocTabFocus[0] += direcao[0]
            LocTabFocus[1] += direcao[1]
            tabuleiro_focus[LocTabFocus[0]][LocTabFocus[1]] = True

        # Jogada com Barra de Espaço
        if direcao == [10, 10]:
            if tabuleiro[LocTabFocus[0]][LocTabFocus[1]] == 0:
                tabuleiro[LocTabFocus[0]][LocTabFocus[1]] = x[0]
                ganhou = verificar_vitoria(tabuleiro)

                if ganhou == 1 or ganhou == 2:
                    vencedor = jogadorX if ganhou == 1 else JogadorO
                    viewer.game_interface(tabuleiro, tabuleiro_focus, vencedor)
                    jogo_terminou = True
                    database.update_game_status(game_id, x[0], True, f"Vitoria: {vencedor}", tabuleiro)
                    print(f"Jogador {vencedor} ganhou!")
                    return 0

                elif ganhou == 3:
                    viewer.game_interface(tabuleiro, tabuleiro_focus, jogadorX)
                    jogo_terminou = True
                    database.update_game_status(game_id, x[0], True, "Empate", tabuleiro)
                    print("O jogo empatou!")
                    return 0

                # Alterna a vez do jogador e salva o progresso no banco
                x[0] = 2 if x[0] == 1 else 1
                database.update_game_status(game_id, x[0], False, None, tabuleiro)

        element = jogadorX if x[0] == 1 else JogadorO
        viewer.game_interface(tabuleiro, tabuleiro_focus, element)

    def on_press(key, *args):
        pass

    def on_release(key, *args):
        try:
            if key == keyboard.Key.esc or (key.char is not None and key.char.lower() == "s"):
                database.update_game_status(game_id, x[0], False, None, tabuleiro)
                return False
        except AttributeError:
            if format(key) == "Key.up":
                jogar([-1, 0])
                return not jogo_terminou
            elif format(key) == "Key.left":
                jogar([0, -1])
                return not jogo_terminou
            elif format(key) == "Key.down":
                jogar([1, 0])
                return not jogo_terminou
            elif format(key) == "Key.right":
                jogar([0, 1])
                return not jogo_terminou
            elif format(key) == "Key.space":
                jogar([10, 10])
                return not jogo_terminou


    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    return True