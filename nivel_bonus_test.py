import pygame
import random
import sys
import math

# Inicialización de Pygame
pygame.init()

# Constantes
ANCHO, ALTO = 800, 600
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CYAN = (0, 255, 255)
FPS = 60

# Configuración de pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Prueba Nivel Bonus')

# Fuente para texto
font_name = pygame.font.match_font('arial')

def dibujar_texto(surf, text, size, x, y, color=BLANCO):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def dibujar_vidas_jugador(surf, x, y, vidas, img):
    for i in range(vidas):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# Clases del juego
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.Surface((50, 10))
        self.image_orig.fill(BLANCO)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20
        self.vel_x = 7
        self.vidas = 6  # 3 vidas iniciales + 3 del bonus

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel_x
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.vel_x

class DisparoJugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect(centerx=x, bottom=y)

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

class Moneda(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 10)
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 8)
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 6)
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_y = 2
        self.vel_x = random.uniform(-1, 1)
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 5000

    def update(self):
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.vel_x *= -1
        if self.rect.top > ALTO or pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class Bola(pygame.sprite.Sprite):
    def __init__(self, color, radio=20):
        super().__init__()
        self.image = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radio, radio), radio)
        self.rect = self.image.get_rect()
        self.radio = radio
        self.destrucciones = 0
        self.color = color
        self.reaparecer()

    def reaparecer(self):
        self.rect.x = random.randint(self.radio, ANCHO - self.radio*2)
        self.rect.y = random.randint(50, 200)

    def on_hit(self):
        self.destrucciones += 1
        if self.destrucciones >= 5:
            # Crear monedas cuando la bola azul desaparece permanentemente
            for _ in range(random.randint(1, 3)):
                moneda = Moneda(self.rect.center)
                all_sprites.add(moneda)
                monedas.add(moneda)
            self.kill()
        else:
            # Crear moneda cuando la bola azul reaparece
            moneda = Moneda(self.rect.center)
            all_sprites.add(moneda)
            monedas.add(moneda)
            self.reaparecer()

    def update(self):
        pass

class BolaAzul(Bola):
    def __init__(self):
        super().__init__(AZUL)
        self.vel = 1.5
        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)

    def update(self):
        # Movimiento hacia el jugador
        try:
            if jugador:
                dx, dy = jugador.rect.centerx - self.rect.centerx, jugador.rect.centery - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist > 0:
                    self.rect.x += (dx / dist) * self.vel
                    self.rect.y += (dy / dist) * self.vel
        except (NameError, AttributeError):
            pass

def mostrar_pantalla_bonus():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¡NIVEL BONUS!", 72, ANCHO // 2, ALTO // 2 - 50, AMARILLO)
    dibujar_texto(pantalla, "¡3 vidas extra!", 48, ANCHO // 2, ALTO // 2 + 20, VERDE)
    dibujar_texto(pantalla, "Destruye las bolas azules para obtener monedas", 24, ANCHO // 2, ALTO // 2 + 80, BLANCO)
    pygame.display.flip()
    pygame.time.delay(3000)

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
disparos_jugador = pygame.sprite.Group()
monedas = pygame.sprite.Group()
puntos = 0

# Crear jugador
jugador = Jugador()
jugador_mini_img = pygame.transform.scale(jugador.image_orig, (25, 5))
jugador_mini_img.set_colorkey(NEGRO)
all_sprites.add(jugador)

# Crear 3 bolas azules para el nivel bonus
for _ in range(3):
    b = BolaAzul()
    all_sprites.add(b)
    enemigos.add(b)

# Mostrar pantalla de bonus
mostrar_pantalla_bonus()

# Reloj
clock = pygame.time.Clock()
ejecutando = True

while ejecutando:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Disparar
                disparo = DisparoJugador(jugador.rect.centerx, jugador.rect.top)
                all_sprites.add(disparo)
                disparos_jugador.add(disparo)

    all_sprites.update()

    # Colisión: Disparos del jugador vs enemigos
    golpeados = pygame.sprite.groupcollide(enemigos, disparos_jugador, False, True)
    for enemigo in golpeados:
        enemigo.on_hit()

    # Colisión: Jugador recolecta monedas
    monedas_recolectadas = pygame.sprite.spritecollide(jugador, monedas, True)
    for moneda in monedas_recolectadas:
        puntos += 10

    # Verificar victoria
    if len(enemigos) == 0:
        ejecutando = False

    # Dibujar todo
    pantalla.fill(NEGRO)
    all_sprites.draw(pantalla)
    
    # HUD
    dibujar_vidas_jugador(pantalla, ANCHO - 100, 10, jugador.vidas, jugador_mini_img)
    dibujar_texto(pantalla, f"Puntos: {puntos}", 22, 90, 10, AMARILLO)
    dibujar_texto(pantalla, "NIVEL BONUS", 24, ANCHO // 2, 10, CYAN)
    dibujar_texto(pantalla, "Presiona ESPACIO para disparar", 18, ANCHO // 2, ALTO - 30, BLANCO)
    
    pygame.display.flip()

# Pantalla de victoria
pantalla.fill(NEGRO)
dibujar_texto(pantalla, "¡VICTORIA!", 64, ANCHO // 2, ALTO // 2 - 50, VERDE)
dibujar_texto(pantalla, f"Puntos finales: {puntos}", 32, ANCHO // 2, ALTO // 2 + 20, BLANCO)
dibujar_texto(pantalla, "Presiona cualquier tecla para salir", 24, ANCHO // 2, ALTO // 2 + 80, BLANCO)
pygame.display.flip()

# Esperar input del usuario
esperando = True
while esperando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN:
            esperando = False

pygame.quit()
sys.exit() 