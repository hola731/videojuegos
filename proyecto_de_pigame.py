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
MAGENTA = (255, 0, 255)
FPS = 60

# Configuración de pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Destruye las bolas')

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

# --- Clases del Juego ---

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
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.vidas = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.powerup_level = 0
        self.powerup_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = ANCHO // 2
            self.rect.bottom = ALTO - 20

        if not self.hidden:
            # Ciclo de poderes
            if pygame.time.get_ticks() - self.powerup_timer > 5000:
                self.powerup_timer = pygame.time.get_ticks()
                self.powerup_level = (self.powerup_level % 3) + 1

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.vel_x
            if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
                self.rect.x += self.vel_x
            if teclas[pygame.K_SPACE]:
                self.disparar()

    def disparar(self):
        if not self.hidden:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                if self.powerup_level == 1:  # Doble disparo
                    disparo1 = DisparoJugador(self.rect.left + 10, self.rect.top)
                    disparo2 = DisparoJugador(self.rect.right - 10, self.rect.top)
                    all_sprites.add(disparo1, disparo2)
                    disparos_jugador.add(disparo1, disparo2)
                elif self.powerup_level == 3:  # Triple disparo
                    disparo1 = DisparoJugador(self.rect.left + 5, self.rect.top)
                    disparo2 = DisparoJugador(self.rect.centerx, self.rect.top)
                    disparo3 = DisparoJugador(self.rect.right - 5, self.rect.top)
                    all_sprites.add(disparo1, disparo2, disparo3)
                    disparos_jugador.add(disparo1, disparo2, disparo3)
                else:  # Disparo normal (y para doble daño)
                    disparo = DisparoJugador(self.rect.centerx, self.rect.top)
                    all_sprites.add(disparo)
                    disparos_jugador.add(disparo)

    def hide(self):
        self.vidas -= 1
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (ANCHO / 2, ALTO + 200)

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

class DisparoEnemigo(pygame.sprite.Sprite):
    def __init__(self, center_pos, target_pos, color=(255, 100, 0), speed=5):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=center_pos)
        dx, dy = target_pos[0] - center_pos[0], target_pos[1] - center_pos[1]
        dist = math.hypot(dx, dy)
        self.vel_x, self.vel_y = (dx / dist) * speed if dist else 0, (dy / dist) * speed if dist else speed

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if not pantalla.get_rect().colliderect(self.rect):
            self.kill()

class Particula(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_x, self.vel_y = random.uniform(-4, 4), random.uniform(-4, 4)
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = random.randint(300, 700)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class DisparoExplosivo(DisparoEnemigo):
    def __init__(self, center_pos, target_pos):
        super().__init__(center_pos, target_pos, color=NEGRO, speed=3)
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLANCO, (7, 7), 7)
        pygame.draw.circle(self.image, ROJO, (7, 7), 4)
        self.rect = self.image.get_rect(center=center_pos)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if not pantalla.get_rect().colliderect(self.rect):
            self.explotar()

    def explotar(self):
        for _ in range(random.randint(10, 15)):
            all_sprites.add(Particula(self.rect.center))
        self.kill()

class RayoLaser(pygame.sprite.Sprite):
    def __init__(self, center_pos, target_pos, color=CYAN, speed=8):
        super().__init__()
        # Calcular la dirección del láser
        dx, dy = target_pos[0] - center_pos[0], target_pos[1] - center_pos[1]
        dist = math.hypot(dx, dy)
        
        # Crear una superficie para el láser
        self.image = pygame.Surface((4, dist), pygame.SRCALPHA)
        
        # Dibujar el láser con gradiente
        for i in range(int(dist)):
            alpha = 255 - (i * 100 // int(dist))  # Fade out effect
            color_with_alpha = (*color, alpha)
            pygame.draw.line(self.image, color_with_alpha, (2, i), (2, i+1), 4)
        
        # Rotar la imagen para que apunte hacia el objetivo
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image, angle)
        
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_x, self.vel_y = (dx / dist) * speed if dist else 0, (dy / dist) * speed if dist else speed
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 2000  # 2 segundos

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Eliminar si sale de pantalla o expira
        if not pantalla.get_rect().colliderect(self.rect) or pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class Semicirculo(pygame.sprite.Sprite):
    def __init__(self, center_pos, color=AMARILLO, radio=30):
        super().__init__()
        self.image = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
        # Dibujar semicírculo (mitad inferior)
        pygame.draw.arc(self.image, color, (0, 0, radio*2, radio*2), 0, math.pi, 3)
        # Rellenar el semicírculo
        pygame.draw.polygon(self.image, color, [(radio, radio), (0, radio), (0, radio*2), (radio*2, radio*2), (radio*2, radio)])
        
        self.rect = self.image.get_rect(center=center_pos)
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 1000  # 1 segundo
        self.vel_y = -2  # Se mueve hacia arriba

    def update(self):
        self.rect.y += self.vel_y
        
        # Fade out effect
        alpha = max(0, 255 - ((pygame.time.get_ticks() - self.creation_time) * 255 // self.lifespan))
        if alpha <= 0:
            self.kill()
        else:
            # Crear una nueva superficie con transparencia
            temp_surface = self.image.copy()
            temp_surface.set_alpha(alpha)
            self.image = temp_surface

class Bola(pygame.sprite.Sprite):
    def __init__(self, color, radio=20):
        super().__init__()
        self.image = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radio, radio), radio)
        self.rect = self.image.get_rect()
        self.radio = radio
        self.destrucciones = 0
        self.reaparecer()

    def reaparecer(self):
        self.rect.x = random.randint(self.radio, ANCHO - self.radio*2)
        self.rect.y = random.randint(50, 200)

    def on_hit(self):
        self.destrucciones += 1
        if self.destrucciones >= 5:
            # Crear semicírculo cuando la bola desaparece
            semicirculo = Semicirculo(self.rect.center)
            all_sprites.add(semicirculo)
            self.kill()
        else:
            self.reaparecer()

    def update(self):
        pass

class BolaVerde(Bola):
    def __init__(self):
        super().__init__(VERDE)

class BolaAzul(Bola):
    def __init__(self):
        super().__init__(AZUL)
        self.vel = 1.5
        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)

    def on_hit(self):
        self.destrucciones += 1
        if self.destrucciones >= 5:
            # Crear semicírculo cuando la bola desaparece
            semicirculo = Semicirculo(self.rect.center, color=CYAN)
            all_sprites.add(semicirculo)
            self.kill()
        else:
            self.reaparecer()

    def update(self):
        if not jugador.hidden:
            dx, dy = jugador.rect.centerx - self.rect.centerx, jugador.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.rect.x += (dx / dist) * self.vel
                self.rect.y += (dy / dist) * self.vel

    def disparar(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and not jugador.hidden:
            self.last_shot = now
            disparo = RayoLaser(self.rect.center, jugador.rect.center, color=CYAN)
            all_sprites.add(disparo)
            disparos_enemigos.add(disparo)

class BolaRoja(Bola):
    def __init__(self):
        super().__init__(ROJO)
        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)

    def on_hit(self):
        self.destrucciones += 1
        if self.destrucciones >= 5:
            # Crear semicírculo cuando la bola desaparece
            semicirculo = Semicirculo(self.rect.center, color=MAGENTA)
            all_sprites.add(semicirculo)
            self.kill()
        else:
            self.reaparecer()

    def disparar(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and not jugador.hidden:
            self.last_shot = now
            disparo = RayoLaser(self.rect.center, jugador.rect.center, color=ROJO)
            all_sprites.add(disparo)
            disparos_enemigos.add(disparo)

    def update(self):
        self.disparar()

class BolaNegra(Bola):
    def __init__(self):
        super().__init__(BLANCO, radio=22) # Color cambiado a blanco
        self.vidas = 4
        self.shoot_delay = 2000
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)
        self.vel_x = 2

    def on_hit(self):
        damage = 1
        if jugador.powerup_level == 2: # Doble Daño
            damage = 2
        self.vidas -= damage
        if self.vidas <= 0:
            self.destrucciones += 1
            if self.destrucciones >= 5:
                # Crear semicírculo cuando la bola desaparece
                semicirculo = Semicirculo(self.rect.center, color=AMARILLO)
                all_sprites.add(semicirculo)
                self.kill()
            else:
                self.reaparecer()
                self.vidas = 4

    def disparar(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and not jugador.hidden:
            self.last_shot = now
            disparo = RayoLaser(self.rect.center, jugador.rect.center, color=BLANCO)
            all_sprites.add(disparo)
            disparos_enemigos.add(disparo)

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right > ANCHO or self.rect.left < 0:
            self.vel_x *= -1
        self.disparar()

def show_game_over_screen():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "GAME OVER", 64, ANCHO / 2, ALTO / 4, ROJO)
    
    # Botón de "Volver a Jugar"
    button_rect = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 - 25, 200, 50)
    pygame.draw.rect(pantalla, VERDE, button_rect)
    dibujar_texto(pantalla, "Volver a Jugar", 24, ANCHO / 2, ALTO / 2 - 15, NEGRO)

    pygame.display.flip()
    esperando = True
    while esperando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False  # Indica que quiere salir
            if evento.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(evento.pos):
                    return True  # Indica que quiere volver a jugar
    return False

# --- Grupos de Sprites e Instanciación ---
all_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
bolas_azules = pygame.sprite.Group()
disparos_jugador = pygame.sprite.Group()
disparos_enemigos = pygame.sprite.Group()

jugador = Jugador()
jugador_mini_img = pygame.transform.scale(jugador.image_orig, (25, 5))
jugador_mini_img.set_colorkey(NEGRO)
all_sprites.add(jugador)

for _ in range(3):
    b = BolaVerde()
    all_sprites.add(b)
    enemigos.add(b)
for _ in range(2):
    b = BolaRoja()
    all_sprites.add(b)
    enemigos.add(b)
for _ in range(2):
    b = BolaNegra()
    all_sprites.add(b)
    enemigos.add(b)
bola_azul = BolaAzul()
all_sprites.add(bola_azul)
enemigos.add(bola_azul)
bolas_azules.add(bola_azul)

# Reloj y Bucle principal
clock = pygame.time.Clock()
ejecutando_juego = True
while ejecutando_juego:
    # --- Reset / Setup del juego ---
    all_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    bolas_azules = pygame.sprite.Group()
    disparos_jugador = pygame.sprite.Group()
    disparos_enemigos = pygame.sprite.Group()

    jugador = Jugador()
    jugador_mini_img = pygame.transform.scale(jugador.image_orig, (25, 5))
    jugador_mini_img.set_colorkey(NEGRO)
    all_sprites.add(jugador)

    for _ in range(3):
        b = BolaVerde()
        all_sprites.add(b)
        enemigos.add(b)
    for _ in range(2):
        b = BolaRoja()
        all_sprites.add(b)
        enemigos.add(b)
    for _ in range(2):
        b = BolaNegra()
        all_sprites.add(b)
        enemigos.add(b)
    bola_azul = BolaAzul()
    all_sprites.add(bola_azul)
    enemigos.add(bola_azul)
    bolas_azules.add(bola_azul)

    game_over = False
    partida_en_curso = True
    while partida_en_curso:
        if game_over:
            if show_game_over_screen():
                partida_en_curso = False # Para salir al bucle exterior y reiniciar
            else:
                partida_en_curso = False
                ejecutando_juego = False
        else:
            clock.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    partida_en_curso = False
                    ejecutando_juego = False

            all_sprites.update()

            # Colisión: Disparos del jugador vs enemigos
            golpeados = pygame.sprite.groupcollide(enemigos, disparos_jugador, False, True)
            for enemigo in golpeados:
                enemigo.on_hit()

            # Colisión: Enemigos o sus disparos vs jugador
            if not jugador.hidden:
                # Disparos enemigos vs jugador
                impactos_disparos = pygame.sprite.spritecollide(jugador, disparos_enemigos, False)
                for impacto in impactos_disparos:
                    if hasattr(impacto, 'explotar'): impacto.explotar()
                    else: impacto.kill()
                    jugador.hide()
                
                # Bola azul vs jugador
                colisiones_bola_azul = pygame.sprite.spritecollide(jugador, bolas_azules, False)
                if colisiones_bola_azul:
                    jugador.hide()
                    for bola in colisiones_bola_azul:
                        bola.on_hit()

            if jugador.vidas == 0 and not jugador.hidden:
                game_over = True

            # Dibujar todo
            pantalla.fill(NEGRO)
            all_sprites.draw(pantalla)
            dibujar_vidas_jugador(pantalla, ANCHO - 100, 10, jugador.vidas, jugador_mini_img)
            powerup_text = "Poder: Ninguno"
            if jugador.powerup_level == 1:
                powerup_text = "Poder: Doble Disparo"
            elif jugador.powerup_level == 2:
                powerup_text = "Poder: Doble Daño"
            elif jugador.powerup_level == 3:
                powerup_text = "Poder: Triple Disparo"
            dibujar_texto(pantalla, powerup_text, 18, ANCHO / 2, 10)
            pygame.display.flip()

pygame.quit()
sys.exit()
 