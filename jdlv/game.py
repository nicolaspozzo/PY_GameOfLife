

import pygame
import numpy as np
import time


pygame.init()

# Dimensiones de la pantalla
# width, height = 500, 500
width, height = 700, 500

screen = pygame.display.set_mode((width, height))

bg = 25, 25, 25

screen.fill(bg)
# Cantidad de pixels
# nxC, nyC = 25, 25
nxC, nyC = 50, 50
dimCW = width / nxC
dimCH = height / nyC

# Estados de las celdas: Vivas = 1, Mueratas = 0
gameState = np.zeros((nxC, nyC))

# Automata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Automoata movil
gameState[21 , 21] = 1
gameState[22 , 22] = 1
gameState[22 , 23] = 1
gameState[21 , 22] = 1
gameState[23 , 22] = 1

#  Control de la ejecucion del juego
pauseExect = False

# Bucle de ejecucion
while True:

    newGameState = np.copy(gameState)
    screen.fill(bg)

    time.sleep(0.1)

    # Registramos eventos del teclado y del mouse
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        
        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                # Calculamos el numero de vecinos cercanos
                n_neigh = gameState[(x - 1) % nxC , (y - 1) % nyC] + \
                        gameState[(x)     % nxC , (y - 1) % nyC] + \
                        gameState[(x + 1) % nxC , (y - 1) % nyC] + \
                        gameState[(x - 1) % nxC , (y)     % nyC] + \
                        gameState[(x + 1) % nxC , (y)     % nyC] + \
                        gameState[(x - 1) % nxC , (y + 1) % nyC] + \
                        gameState[(x)     % nxC , (y + 1) % nyC] + \
                        gameState[(x + 1) % nxC , (y + 1) % nyC]

                # Regla 1
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                # Regla 2
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0



            poly = [
                ((x)   * dimCW, y * dimCH),
                ((x+1) * dimCW, y * dimCH),
                ((x+1) * dimCW, (y+1) * dimCH),
                ((x)   * dimCW, (y+1) * dimCH)
            ]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen,(128,128,128), poly, 1)
            else:
                pygame.draw.polygon(screen,(255,255,255), poly, 0)

    # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)
    # Actualizamos la pantalla
    pygame.display.flip()
