import pygame
import serial

pygame.init()  # Inicializa todos los módulos de Pygame

# Intentar conexión serial con Arduino
try:
    arduino = serial.Serial('COM5', 9600)
    usar_arduino = True
except Exception as e:
    print(f"⚠️ No se pudo conectar al Arduino en COM5: {e}")
    usar_arduino = False

# Configuración de pantalla
ANCHO, ALTO = 600, 400
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong Arcade")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROSA_PASTEL = (255, 182, 193)

# Tamaños
RAQUETA_ANCHO, RAQUETA_ALTO = 10, 60
PELOTA_RADIO = 7

# Cargar imagen del corazon
corazon = pygame.image.load("uwu.png").convert_alpha()
corazon = pygame.transform.scale(corazon, (PELOTA_RADIO * 2, PELOTA_RADIO * 2))

# Objetos
raqueta_izq = pygame.Rect(20, ALTO // 2 - RAQUETA_ALTO // 2, RAQUETA_ANCHO, RAQUETA_ALTO)
raqueta_der = pygame.Rect(ANCHO - 30, ALTO // 2 - RAQUETA_ALTO // 2, RAQUETA_ANCHO, RAQUETA_ALTO)
pelota = pygame.Rect(ANCHO // 2, ALTO // 2, PELOTA_RADIO * 2, PELOTA_RADIO * 2)

# Velocidades
VEL_RAQUETA = 5
VELOCIDAD_PELOTA = [3, 3]

# Puntuación
puntos_izq = 0
puntos_der = 0
fuente = pygame.font.SysFont("Arial", 30)

# Bucle de juego
ejecutando = True
while ejecutando:
    pygame.time.delay(20)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Leer datos de Arduino
    if usar_arduino and arduino.in_waiting > 0:
        comando = arduino.readline().decode().strip()
        if comando == "UP":
            raqueta_izq.y -= VEL_RAQUETA
        elif comando == "DOWN":
            raqueta_izq.y += VEL_RAQUETA

    # Movimiento raqueta derecha con teclado
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and raqueta_der.top > 0:
        raqueta_der.y -= VEL_RAQUETA
    if teclas[pygame.K_DOWN] and raqueta_der.bottom < ALTO:
        raqueta_der.y += VEL_RAQUETA

    # Movimiento pelota
    pelota.x += VELOCIDAD_PELOTA[0]
    pelota.y += VELOCIDAD_PELOTA[1]

    # Colisiones con bordes
    if pelota.top <= 0 or pelota.bottom >= ALTO:
        VELOCIDAD_PELOTA[1] *= -1

    # Colisiones con raquetas
    if pelota.colliderect(raqueta_izq) or pelota.colliderect(raqueta_der):
        VELOCIDAD_PELOTA[0] *= -1

    # Puntuación
    if pelota.left <= 0:
        puntos_der += 1
        pelota.x, pelota.y = ANCHO // 2, ALTO // 2
    elif pelota.right >= ANCHO:
        puntos_izq += 1
        pelota.x, pelota.y = ANCHO // 2, ALTO // 2

    # Dibujar todo
    VENTANA.fill(NEGRO)
    pygame.draw.rect(VENTANA, ROSA_PASTEL, raqueta_izq)
    pygame.draw.rect(VENTANA, ROSA_PASTEL, raqueta_der)
    VENTANA.blit(corazon, (pelota.x, pelota.y))

    # Mostrar puntuación
    texto = fuente.render(f"{puntos_izq}   {puntos_der}", True, BLANCO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 20))

    pygame.display.update()

pygame.quit()