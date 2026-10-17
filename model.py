import database
import viewer
import controller
import ast
import time
import sys
import termios

# Ordem dos processos
# 1 dar boas vindas
# 2 perguntar se quer jogar algum jogo passado
# 3 input da decisão do usuário
# 4 jogar de acordo com o processo 3
# 5 jogar o jogo
# 6 terminar o jogo, caso o usuário queira continuar volta para o processo 2
# 7 fim

while True:
    tab = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    focus = [[False, False, False], [False, True, False], [False, False, False]]
    position = [1, 1]
    jogo_acabou = False
    vezJogador = [1]
    jogadorX = ""
    jogadorO = ""
    game_id = None

    jogo_da_database = viewer.inicar_jogo()

    if jogo_da_database:
        jogos_nao_terminados = database.game_not_finished()

        if len(jogos_nao_terminados) == 0:
            print("Nenhum jogo encontrado")
            for ponto in [".", "..", "..."]:
                time.sleep(0.75)
                print(ponto)

            jogadores = viewer.adicionar_dados()
            jogadorX = jogadores[0]
            jogadorO = jogadores[1]
            game_id = database.save_state(vezJogador[0], jogadorX, jogadorO, False, None, tab)
        else:
            ids_validos = [jogo[0] for jogo in jogos_nao_terminados]

            while True:
                for x in jogos_nao_terminados:
                    print(f"id:{x[0]} | jogador1:{x[2]} | jogador2:{x[3]}")

                try:
                    id_escolhido = int(input("\nSelecione um id válido: "))
                    if id_escolhido in ids_validos:
                        jogo_salvo = database.get_game_by_id(id_escolhido)
                        game_id = jogo_salvo[0]
                        vezJogador = [jogo_salvo[1]]
                        jogadorX = jogo_salvo[2]
                        jogadorO = jogo_salvo[3]
                        tab = ast.literal_eval(jogo_salvo[6])  # Converte texto salvo de volta para matriz
                        break
                    else:
                        print("ID não pertence à lista de jogos em aberto. Tente novamente.\n")
                except ValueError:
                    print("Digite um número inteiro válido.\n")
    else:
        jogadores = viewer.adicionar_dados()
        jogadorX = jogadores[0]
        jogadorO = jogadores[1]
        game_id = database.save_state(vezJogador[0], jogadorX, jogadorO, False, None, tab)

    jogo_acabou = controller.comecar_jogo(
        tab, focus, position, jogo_acabou, vezJogador, jogadorX, jogadorO, game_id
    )

    if jogo_acabou:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        kill = False
        while True:
            print("Quer parar de jogar?[S,n]")
            resposta = input().strip()
            if resposta.lower() == 's':
                kill = True
                break
            elif resposta.lower() == 'n':
                break
            else:
                print(f'Comando "{resposta}" não encontrado ')

        if kill:
            break

database.conexao.close()