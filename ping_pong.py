import pygame

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 600, 400
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong Arcade")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Configuración de raquetas y pelota
RAQUETA_ANCHO, RAQUETA_ALTO = 10, 60
PELOTA_RADIO = 7
VELOCIDAD_PELOTA = [3, 3]

# Posiciones iniciales
raqueta_izq = pygame.Rect(20, ALTO // 2 - RAQUETA_ALTO // 2, RAQUETA_ANCHO, RAQUETA_ALTO)
raqueta_der = pygame.Rect(ANCHO - 30, ALTO // 2 - RAQUETA_ALTO // 2, RAQUETA_ANCHO, RAQUETA_ALTO)
pelota = pygame.Rect(ANCHO // 2, ALTO // 2, PELOTA_RADIO * 2, PELOTA_RADIO * 2)

# Velocidad de las raquetas
VEL_RAQUETA = 5

# Bucle de juego
ejecutando = True
while ejecutando:
    pygame.time.delay(20)

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Movimiento de raquetas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and raqueta_der.top > 0:
        raqueta_der.y -= VEL_RAQUETA
    if teclas[pygame.K_DOWN] and raqueta_der.bottom < ALTO:
        raqueta_der.y += VEL_RAQUETA
    if teclas[pygame.K_w] and raqueta_izq.top > 0:
        raqueta_izq.y -= VEL_RAQUETA
    if teclas[pygame.K_s] and raqueta_izq.bottom < ALTO:
        raqueta_izq.y += VEL_RAQUETA

    # Movimiento de la pelota
    pelota.x += VELOCIDAD_PELOTA[0]
    pelota.y += VELOCIDAD_PELOTA[1]

    # Colisión con bordes
    if pelota.top <= 0 or pelota.bottom >= ALTO:
        VELOCIDAD_PELOTA[1] *= -1

    # Colisión con raquetas
    if pelota.colliderect(raqueta_izq) or pelota.colliderect(raqueta_der):
        VELOCIDAD_PELOTA[0] *= -1

    # Reinicio si la pelota sale de la pantalla
    if pelota.left <= 0 or pelota.right >= ANCHO:
        pelota.x, pelota.y = ANCHO // 2, ALTO // 2
        VELOCIDAD_PELOTA = [3, 3]

    # Dibujar elementos
    VENTANA.fill(NEGRO)
    pygame.draw.rect(VENTANA, BLANCO, raqueta_izq)
    pygame.draw.rect(VENTANA, BLANCO, raqueta_der)
    pygame.draw.ellipse(VENTANA, BLANCO, pelota)

    pygame.display.update()

pygame.quit()
