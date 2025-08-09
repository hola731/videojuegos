import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Constantes
ANCHO, ALTO = 800, 600
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
FPS = 60

# Configuración de pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Prueba Pantalla Bonus')

# Fuente para texto
font_name = pygame.font.match_font('arial')

def dibujar_texto(surf, text, size, x, y, color=BLANCO):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def mostrar_pantalla_bonus():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¡NIVEL BONUS!", 72, ANCHO // 2, ALTO // 2 - 50, AMARILLO)
    dibujar_texto(pantalla, "¡3 vidas extra!", 48, ANCHO // 2, ALTO // 2 + 20, VERDE)
    pygame.display.flip()
    pygame.time.delay(3000)

# Reloj
clock = pygame.time.Clock()

# Mostrar pantalla de bonus
mostrar_pantalla_bonus()

# Bucle principal
ejecutando = True
while ejecutando:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

    # Mantener pantalla negra después del bonus
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "Presiona ESC para salir", 24, ANCHO // 2, ALTO // 2, BLANCO)
    pygame.display.flip()

pygame.quit()
sys.exit() 