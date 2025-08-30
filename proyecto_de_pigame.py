import pygame
import random
import sys
import math
import json
import os





# Inicialización de Pygame
pygame.init()
bolas_celestes = pygame.sprite.Group()

# Clase BolaCeleste (debe ir después de inicializar pygame)
class BolaCeleste(pygame.sprite.Sprite):
    """Bola celeste especial que otorga un poder aleatorio al jugador"""
    def __init__(self, center_pos):
        super().__init__()
        # Crear una superficie circular para la bola celeste
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, CYAN, (14, 14), 14)
        pygame.draw.circle(self.image, BLANCO, (14, 14), 9)
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_y = 2  # Velocidad de caída
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 6000  # Duración de vida en milisegundos

    def update(self):
        """Actualizar la posición y verificar si debe eliminarse"""
        self.rect.y += self.vel_y
        if self.rect.top > ALTO or pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

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

# Variables globales para controles
CONTROLES = {
    'izquierda': pygame.K_LEFT,
    'derecha': pygame.K_RIGHT,
    'disparo': pygame.K_SPACE
}

# Variables globales para el juego
jugador = None
jugador_mini_img = None
all_sprites = None
enemigos = None
bolas_azules = None
disparos_jugador = None
disparos_enemigos = None
monedas = None
puntos = 0
horda_actual = 1
TOTAL_HORDAS = 30
clock = pygame.time.Clock()

# Variables globales para mejoras activas
ESCUDO_TEMPORAL_TIMER = 0

# Configuración de pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Destruye las bolas')

# Cargar imágenes de personajes
try:
    imagen_alien_verde = pygame.image.load('image/alien.webp').convert_alpha()
    imagen_alien_rojo = pygame.image.load('image/alienrojo2.png').convert_alpha()
    imagen_nave = pygame.image.load('image/nave.png').convert_alpha()
    imagen_alien_blanco = pygame.image.load('image/alienblanco.jpg').convert_alpha()
    imagen_alien_azul = pygame.image.load('image/alienazul.png').convert_alpha()
    imagen_alien_naranja = pygame.image.load('image/aliennaranja2.png').convert_alpha()
    imagen_alien_morado = pygame.image.load('image/alienmorado2.png').convert_alpha()
    imagen_calavera = pygame.image.load('image/calavera2.png').convert_alpha()
    
    # Redimensionar imágenes para que se ajusten al juego
    imagen_alien_verde = pygame.transform.scale(imagen_alien_verde, (60, 60))  # Aumentado de 40x40 a 60x60
    imagen_alien_rojo = pygame.transform.scale(imagen_alien_rojo, (60, 60))   # Aumentado de 40x40 a 60x60
    imagen_nave = pygame.transform.scale(imagen_nave, (70, 15))  # Aumentado de 50x10 a 70x15
    imagen_alien_blanco = pygame.transform.scale(imagen_alien_blanco, (64, 64))  # Aumentado de 44x44 a 64x64
    imagen_alien_azul = pygame.transform.scale(imagen_alien_azul, (60, 60))    # Aumentado de 40x40 a 60x60
    imagen_alien_naranja = pygame.transform.scale(imagen_alien_naranja, (60, 60))
    imagen_alien_morado = pygame.transform.scale(imagen_alien_morado, (60, 60))
    imagen_calavera = pygame.transform.scale(imagen_calavera, (60, 60))
except:
    # Si no se pueden cargar las imágenes, usar formas geométricas por defecto
    imagen_alien_verde = None
    imagen_alien_rojo = None
    imagen_nave = None
    imagen_alien_blanco = None
    imagen_alien_azul = None
    imagen_alien_naranja = None
    imagen_alien_morado = None
    imagen_calavera = None
    print("No se pudieron cargar las imágenes. Usando formas geométricas por defecto.")

# Fuente para texto
font_name = pygame.font.match_font('arial')

def dibujar_texto(surf, text, size, x, y, color=BLANCO):
    """Dibuja texto en la superficie especificada"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)

def dibujar_boton(surf, rect, color, texto, color_texto=BLANCO, tamaño_texto=24):
    """Dibuja un botón con texto centrado"""
    pygame.draw.rect(surf, color, rect)
    pygame.draw.rect(surf, BLANCO, rect, 2)  # Borde blanco
    dibujar_texto(surf, texto, tamaño_texto, rect.centerx, rect.centery, color_texto)

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
        if imagen_nave:
            self.image_orig = imagen_nave
        else:
            self.image_orig = pygame.Surface((70, 15))  # Aumentado de 50x10 a 70x15
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
        self.escudo = False  # Nuevo atributo: escudo
        self.escudo_timer = 0  # Temporizador del escudo

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = ANCHO // 2
            self.rect.bottom = ALTO - 20
            self.escudo = True  # Activar escudo SOLO al reaparecer
            self.escudo_timer = pygame.time.get_ticks()

        # Desactivar escudo tras 2 segundos
        if self.escudo and pygame.time.get_ticks() - self.escudo_timer > 2000:
            self.escudo = False

        if not self.hidden:
            teclas = pygame.key.get_pressed()
            if teclas[CONTROLES['izquierda']] and self.rect.left > 0:
                self.rect.x -= self.vel_x
            if teclas[CONTROLES['derecha']] and self.rect.right < ANCHO:
                self.rect.x += self.vel_x
            if teclas[CONTROLES['disparo']]:
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
        if not self.hidden:
            self.vidas -= 1
            self.hidden = True
            self.hide_timer = pygame.time.get_ticks()
            self.rect.center = (ANCHO / 2, ALTO + 200)
        # El escudo se activa al reaparecer, no aquí

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
        if target_pos is not None:
            dx, dy = target_pos[0] - center_pos[0], target_pos[1] - center_pos[1]
            dist = math.hypot(dx, dy)
            self.vel_x, self.vel_y = (dx / dist) * speed if dist else 0, (dy / dist) * speed if dist else speed
        else:
            self.vel_x, self.vel_y = 0, speed  # Movimiento vertical por defecto

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if not pantalla.get_rect().colliderect(self.rect):
            self.kill()

class Particula(pygame.sprite.Sprite):
    def __init__(self, center_pos, color=None):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        if color is None:
            # Colores aleatorios para las partículas
            colors = [ROJO, VERDE, AZUL, AMARILLO, CYAN, MAGENTA, BLANCO]
            color = random.choice(colors)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_x, self.vel_y = random.uniform(-6, 6), random.uniform(-6, 6)
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = random.randint(500, 1000)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # Añadir gravedad
        self.vel_y += 0.2
        if pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    """Efecto de explosión cuando se destruye una bola"""
    def __init__(self, center_pos, color=None):
        super().__init__()
        self.center_pos = center_pos
        self.color = color if color else random.choice([ROJO, VERDE, AZUL, AMARILLO, CYAN, MAGENTA])
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 1000  # 1 segundo
        self.particles_created = False
        
    def create_particles(self):
        """Crea las partículas de la explosión"""
        if not self.particles_created:
            self.particles_created = True
            # Crear múltiples partículas con el color de la explosión
            for _ in range(random.randint(15, 25)):
                particle = Particula(self.center_pos, self.color)
                all_sprites.add(particle)
    
    def update(self):
        if not self.particles_created:
            self.create_particles()
        
        if pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class DisparoExplosivo(DisparoEnemigo):
    def __init__(self, center_pos, target_pos, color=ROJO):
        super().__init__(center_pos, target_pos, color=NEGRO, speed=3)
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        # Dibujar el proyectil explosivo con el color especificado
        pygame.draw.circle(self.image, color, (7, 7), 7)
        pygame.draw.circle(self.image, BLANCO, (7, 7), 4)
        pygame.draw.circle(self.image, color, (7, 7), 2)
        self.rect = self.image.get_rect(center=center_pos)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # Verificar si sale de pantalla
        if not pantalla.get_rect().colliderect(self.rect):
            self.explotar()

    def explotar(self):
        # Crear más partículas para un efecto más espectacular
        for _ in range(random.randint(15, 25)):
            # La partícula se añadirá al grupo cuando se llame a generar_horda
            pass
        self.kill()

class RayoLaser(pygame.sprite.Sprite):
    def __init__(self, center_pos, target_pos, color=CYAN, speed=8):
        super().__init__()
        # Crear un rayo láser vertical que va hacia abajo
        self.image = pygame.Surface((4, ALTO), pygame.SRCALPHA)
        
        # Dibujar el láser vertical con gradiente
        for i in range(ALTO):
            alpha = 255 - (i * 100 // ALTO)  # Fade out effect
            color_with_alpha = (*color, alpha)
            pygame.draw.line(self.image, color_with_alpha, (2, i), (2, i+1), 4)
        
        self.rect = self.image.get_rect(centerx=center_pos[0], top=center_pos[1])
        self.vel_y = speed  # Solo movimiento vertical hacia abajo
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 2000  # 2 segundos

    def update(self):
        self.rect.y += self.vel_y
        
        # Eliminar si sale de pantalla o expira
        if self.rect.top > ALTO or pygame.time.get_ticks() - self.creation_time > self.lifespan:
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
        self.original_image = self.image.copy()

    def update(self):
        self.rect.y += self.vel_y
        
        # Fade out effect
        alpha = max(0, 255 - ((pygame.time.get_ticks() - self.creation_time) * 255 // self.lifespan))
        if alpha <= 0:
            self.kill()
        else:
            # Crear una nueva superficie con transparencia
            self.image = self.original_image.copy()
            self.image.set_alpha(alpha)

class Moneda(pygame.sprite.Sprite):
    """Monedas que sueltan las bolas verdes"""
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Dibujar moneda dorada
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 10)  # Dorado
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 8)   # Amarillo brillante
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 6)   # Centro dorado
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_y = 2  # Cae hacia abajo
        self.vel_x = random.uniform(-1, 1)  # Movimiento horizontal aleatorio
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 5000  # 5 segundos

    def update(self):
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        
        # Rebotar en los bordes de la pantalla
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.vel_x *= -1
        
        # Eliminar si sale de pantalla o expira
        if self.rect.top > ALTO or pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class Bola(pygame.sprite.Sprite):
    def __init__(self, color, radio=30):  # Aumentado de 20 a 30
        super().__init__()
        self.image = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radio, radio), radio)
        self.rect = self.image.get_rect()
        self.radio = radio
        self.destrucciones = 0
        self.color = color
        self.imagen_personalizada = None  # Para preservar imágenes personalizadas
        self.reaparecer()

    def reaparecer(self):
        self.rect.x = random.randint(self.radio, ANCHO - self.radio*2)
        self.rect.y = random.randint(50, 200)
        # Restaurar imagen personalizada si existe
        if self.imagen_personalizada:
            self.image = self.imagen_personalizada
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(self.radio, ANCHO - self.radio*2)
            self.rect.y = random.randint(50, 200)

    def on_hit(self):
        self.destrucciones += 1
        # En dificultad difícil, los enemigos soportan más golpes
        destrucciones_necesarias = 5
        if hasattr(self, 'destrucciones_extra'):
            destrucciones_necesarias += self.destrucciones_extra
        if self.destrucciones >= destrucciones_necesarias:
            # 50% de probabilidad de soltar bola celeste SOLO al ser destruida
            if random.random() < 0.5:
                bola_celeste = BolaCeleste(self.rect.center)
                all_sprites.add(bola_celeste)
                bolas_celestes.add(bola_celeste)
            self.kill()
        else:
            self.reaparecer()

    def update(self):
        pass

class BolaVerde(Bola):
    def __init__(self):
        super().__init__(VERDE)
        # Usar imagen del alien verde si está disponible
        if imagen_alien_verde:
            self.image = imagen_alien_verde
            self.rect = self.image.get_rect()
            self.imagen_personalizada = imagen_alien_verde
        self.shoot_delay = 3000  # 3 segundos
        self.last_shot = pygame.time.get_ticks() + random.randint(-1000, 1000)

    def on_hit(self):
        super().on_hit()
        if self.destrucciones >= 5:
            # Suelta 3 monedas al ser destruida
            for _ in range(3):
                moneda = Moneda(self.rect.center)
                añadir_sprite_seguro(moneda, all_sprites, monedas)
        else:
            # Suelta 1 moneda al ser golpeada
            moneda = Moneda(self.rect.center)
            añadir_sprite_seguro(moneda, all_sprites, monedas)

    def disparar(self):
        # Verificar si jugador existe y no está oculto
        try:
            if jugador and not jugador.hidden:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    # Crear rayo láser que va hacia abajo
                    rayo = RayoLaser(self.rect.center, None, color=VERDE)
                    all_sprites.add(rayo)
                    disparos_enemigos.add(rayo)
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

    def update(self):
        self.disparar()

class BolaAzul(Bola):
    def __init__(self):
        super().__init__(AZUL)
        # Usar imagen del alien azul si está disponible
        if imagen_alien_azul:
            self.image = imagen_alien_azul
            self.rect = self.image.get_rect()
            self.imagen_personalizada = imagen_alien_azul
        self.vel = 1.5
        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)

    def on_hit(self):
        super().on_hit()
        if self.destrucciones >= 5:
            # Suelta 2 monedas al ser destruida
            for _ in range(2):
                moneda = Moneda(self.rect.center)
                añadir_sprite_seguro(moneda, all_sprites, monedas)
        else:
            # Suelta 1 moneda al ser golpeada
            moneda = Moneda(self.rect.center)
            añadir_sprite_seguro(moneda, all_sprites, monedas)

    def disparar(self):
        # Verificar si jugador existe y no está oculto
        try:
            if jugador and not jugador.hidden:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    disparo = DisparoExplosivo(self.rect.center, jugador.rect.center, color=CYAN)
                    all_sprites.add(disparo)
                    disparos_enemigos.add(disparo)
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

    def update(self):
        # Verificar si jugador existe y no está oculto
        try:
            if jugador and not jugador.hidden:
                dx, dy = jugador.rect.centerx - self.rect.centerx, jugador.rect.centery - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist > 0:
                    self.rect.x += (dx / dist) * self.vel
                    self.rect.y += (dy / dist) * self.vel
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

class BolaRoja(Bola):
    def __init__(self):
        super().__init__(ROJO)
        # Usar imagen del alien rojo si está disponible
        if imagen_alien_rojo:
            self.image = imagen_alien_rojo
            self.rect = self.image.get_rect()
            self.imagen_personalizada = imagen_alien_rojo
        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)

    def on_hit(self):
        super().on_hit()

    def disparar(self):
        # Verificar si jugador existe y no está oculto
        try:
            if jugador and not jugador.hidden:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    disparo = DisparoExplosivo(self.rect.center, jugador.rect.center, color=ROJO)
                    all_sprites.add(disparo)
                    disparos_enemigos.add(disparo)
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

    def update(self):
        self.disparar()

class BolaNegra(Bola):
    def __init__(self):
        super().__init__(BLANCO, radio=32) # Aumentado de 22 a 32
        # Usar imagen del alien blanco si está disponible
        if imagen_alien_blanco:
            self.image = imagen_alien_blanco
            self.rect = self.image.get_rect()
            self.imagen_personalizada = imagen_alien_blanco
        self.vidas = 4
        self.shoot_delay = 2000
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)
        self.vel_x = 2

    def on_hit(self):
        # Verificar si jugador existe
        try:
            if jugador:
                damage = 1
                if jugador.powerup_level == 2: # Doble Daño
                    damage = 2
                self.vidas -= damage
                if self.vidas <= 0:
                    super().on_hit()
                    if self.destrucciones < 5:
                        self.vidas = 4
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

    def disparar(self):
        # Verificar si jugador existe y no está oculto
        try:
            if jugador and not jugador.hidden:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    disparo = DisparoExplosivo(self.rect.center, jugador.rect.center, color=BLANCO)
                    all_sprites.add(disparo)
                    disparos_enemigos.add(disparo)
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right > ANCHO or self.rect.left < 0:
            self.vel_x *= -1
        self.disparar()

class BolaMorada(Bola):
    def __init__(self):
        super().__init__(MAGENTA, radio=30)  # Color morado/rosa
        if imagen_alien_morado:
            self.image = imagen_alien_morado
            self.rect = self.image.get_rect()
            self.imagen_personalizada = imagen_alien_morado
        self.shoot_delay = 2500
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)
        self.teleport_delay = 4000  # Teletransporte cada 4 segundos
        self.last_teleport = pygame.time.get_ticks()

    def on_hit(self):
        super().on_hit()

    def teletransportar(self):
        """Teletransporta la bola a una nueva posición aleatoria"""
        self.rect.x = random.randint(self.radio, ANCHO - self.radio*2)
        self.rect.y = random.randint(50, 200)

    def disparar(self):
        # Verificar si jugador existe y no está oculto
        try:
            if jugador and not jugador.hidden:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    # Disparo izquierdo
                    disparo_izq = DisparoEnemigo(self.rect.center, (jugador.rect.centerx - 40, jugador.rect.centery), color=MAGENTA)
                    # Disparo derecho
                    disparo_der = DisparoEnemigo(self.rect.center, (jugador.rect.centerx + 40, jugador.rect.centery), color=MAGENTA)
                    # Rayo láser central
                    rayo = RayoLaser(self.rect.center, None, color=MAGENTA)
                    all_sprites.add(disparo_izq, disparo_der, rayo)
                    disparos_enemigos.add(disparo_izq, disparo_der, rayo)
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

    def update(self):
        # Teletransporte automático
        now = pygame.time.get_ticks()
        if now - self.last_teleport > self.teleport_delay:
            self.teletransportar()
            self.last_teleport = now
        
        self.disparar()

class BolaNaranja(Bola):
    def __init__(self):
        super().__init__((255, 165, 0), radio=30)  # Color naranja
        if imagen_alien_naranja:
            self.image = imagen_alien_naranja
            self.rect = self.image.get_rect()
            self.imagen_personalizada = imagen_alien_naranja
        self.shoot_delay = 3000
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)
        self.disparando = False
        self.disparo_timer = 0
        self.rayos_disparados = 0
        self.vel_x = 2  # Velocidad de movimiento horizontal
        self.teleport_delay = 5000  # Teletransporte cada 5 segundos si no es destruida
        self.last_teleport = pygame.time.get_ticks()

    def on_hit(self):
        super().on_hit()

    def teletransportar(self):
        """Teletransporta la bola a una nueva posición aleatoria"""
        self.rect.x = random.randint(self.radio, ANCHO - self.radio*2)
        self.rect.y = random.randint(50, 200)

    def disparar_tres_rayos(self):
        """Dispara tres rayos láser grandes y largos hacia abajo"""
        if self.rayos_disparados < 3:
            # Todos los rayos van hacia abajo, pero con desplazamiento horizontal
            desplazamientos = [-30, 0, 30]  # Izquierda, centro, derecha
            for i, dx in enumerate(desplazamientos):
                if self.rayos_disparados == i:
                    vel_x = 0
                    vel_y = 8  # Más rápido y siempre hacia abajo
                    # Posición inicial desplazada
                    pos = (self.rect.centerx + dx, self.rect.bottom)
                    rayo = RayoLaserPequeno(pos, (vel_x, vel_y), color=(255, 165, 0), ancho=16, alto=60)
                    all_sprites.add(rayo)
                    disparos_enemigos.add(rayo)
                    self.rayos_disparados += 1
                    break

    def disparar(self):
        # Verificar si jugador existe y no está oculto
        try:
            if jugador and not jugador.hidden:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    if not self.disparando:
                        self.disparando = True
                        self.disparo_timer = now
                        self.rayos_disparados = 0
                        self.vel_x_guardada = self.vel_x  # Guardar velocidad
                        self.vel_x = 0  # Detener movimiento
                    # Disparar los tres rayos consecutivamente con delay entre ellos
                    if self.disparando and now - self.disparo_timer > 300:  # 300ms entre rayos
                        self.disparar_tres_rayos()
                        if self.rayos_disparados >= 3:
                            self.disparando = False
                            self.last_shot = now
                            self.vel_x = getattr(self, 'vel_x_guardada', 2)  # Restaurar velocidad
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

    def update(self):
        # Movimiento horizontal de izquierda a derecha
        self.rect.x += self.vel_x
        
        # Rebotar en los bordes
        if self.rect.right > ANCHO or self.rect.left < 0:
            self.vel_x *= -1
        
        # Teletransporte automático si no es destruida
        now = pygame.time.get_ticks()
        if now - self.last_teleport > self.teleport_delay:
            self.teletransportar()
            self.last_teleport = now
        
        # Disparar
        self.disparar()

class Bomba(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (139, 69, 19), (10, 10), 10)  # Color marrón
        pygame.draw.circle(self.image, (255, 0, 0), (10, 10), 8)     # Color rojo
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 4)   # Color amarillo (mecha)
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.lifespan = 10000  # 10 segundos
        self.creation_time = pygame.time.get_ticks()
    
    def on_hit(self):
        self.kill()  # La bomba se destruye al tocar al jugador
    
    def update(self):
        # Movimiento con rebote
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Rebotar en los bordes de la pantalla
        if self.rect.right > ANCHO or self.rect.left < 0:
            self.vel_x *= -1
        if self.rect.bottom > ALTO - 100 or self.rect.top < 50:
            self.vel_y *= -1
        
        # Verificar tiempo de vida
        if pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class BolaGris(Bola):
    def __init__(self):
        super().__init__((128, 128, 128), radio=30)
        if imagen_calavera:
            self.image = imagen_calavera
            self.rect = self.image.get_rect()
            self.imagen_personalizada = imagen_calavera
        self.vel_x = 1.5
        self.shoot_delay = 2000  # Dispara cada 2 segundos
        self.last_shot = pygame.time.get_ticks() + random.randint(-500, 500)

    def on_hit(self):
        self.destrucciones += 1
        if self.destrucciones >= 5:
            # 50% de probabilidad de soltar bola celeste SOLO al ser destruida
            if random.random() < 0.5:
                bola_celeste = BolaCeleste(self.rect.center)
                all_sprites.add(bola_celeste)
                bolas_celestes.add(bola_celeste)
            # Soltar 3 bolas pequeñas al morir
            for _ in range(3):
                bola_pequena = BolaPequena(self.rect.center)
                all_sprites.add(bola_pequena)
                enemigos.add(bola_pequena)
            self.kill()
        else:
            # Soltar 1 bola pequeña al ser golpeada
            bola_pequena = BolaPequena(self.rect.center)
            all_sprites.add(bola_pequena)
            enemigos.add(bola_pequena)
            self.reaparecer()

    def disparar(self):
        # Verificar si jugador existe y no está oculto
        try:
            if jugador and not jugador.hidden:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    # Dispara un proyectil dirigido al jugador
                    disparo = DisparoEnemigo(self.rect.center, jugador.rect.center, color=(128, 128, 128))
                    all_sprites.add(disparo)
                    disparos_enemigos.add(disparo)
        except (NameError, AttributeError):
            pass  # El jugador aún no existe

    def update(self):
        self.rect.x += self.vel_x
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x *= -1
        elif self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.vel_x *= -1
        
        self.disparar()

class ProyectilRebotador(pygame.sprite.Sprite):
    """Proyectil especial que rebota en las paredes y debe ser destruido por el jugador"""
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((18, 18), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (180, 180, 180), (9, 9), 9)
        pygame.draw.circle(self.image, (255, 0, 0), (9, 9), 4, 2)  # Borde rojo
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_x = random.uniform(-4, 4)
        self.vel_y = random.uniform(-4, 4)
        self.lifespan = 12000  # 12 segundos de vida
        self.creation_time = pygame.time.get_ticks()
        self.salud = 1  # El jugador debe destruirlos
        self.shoot_delay = 2000
        self.last_shot = pygame.time.get_ticks()

    def on_hit(self):
        self.salud -= 1
        if self.salud <= 0:
            self.kill()
    
    def disparar(self):  # DisparoExplosivo
        try:
            if jugador and not jugador.hidden:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    disparo = DisparoExplosivo(self.rect.center, jugador.rect.center, color=(128, 128, 128))
                    all_sprites.add(disparo)
                    disparos_enemigos.add(disparo)
        except (NameError, AttributeError):
            pass
    
    def update(self):  # Movimiento diagonal, rebote, disparo
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # Rebote horizontal
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x *= -1
        elif self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.vel_x *= -1
        # Rebote vertical
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y *= -1
        elif self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
            self.vel_y *= -1
        
        # Desaparecer tras cierto tiempo
        if pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()
            
        self.disparar()

class BolaPequena(Bola):
    """Bolas pequeñas que crea la BolaGris"""
    def __init__(self, center_pos):
        super().__init__((100, 100, 100), radio=15)  # Color gris más oscuro, tamaño pequeño
        self.rect.center = center_pos
        self.vel = 1.8  # Velocidad de persecución
        self.lifespan = 8000  # 8 segundos de vida
        self.creation_time = pygame.time.get_ticks()

    def on_hit(self):
        self.kill()  # Las bolas pequeñas mueren con un solo golpe

    def update(self):
        # Perseguir al jugador
        try:
            if jugador and not jugador.hidden:
                dx, dy = jugador.rect.centerx - self.rect.centerx, jugador.rect.centery - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist > 0:
                    self.rect.x += (dx / dist) * self.vel
                    self.rect.y += (dy / dist) * self.vel
        except (NameError, AttributeError):
            pass  # El jugador aún no existe
        
        # Verificar tiempo de vida
        if pygame.time.get_ticks() - self.creation_time > self.lifespan:
            self.kill()

class RayoLaserPequeno(pygame.sprite.Sprite):
    """Rayo láser pequeño para la BolaNaranja"""
    def __init__(self, center_pos, velocidad, color=(255, 165, 0), ancho=16, alto=60):
        super().__init__()
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, ancho, alto))
        self.rect = self.image.get_rect(center=center_pos)
        self.vel_x, self.vel_y = velocidad
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 1500  # 1.5 segundos

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Eliminar si sale de pantalla o expira
        if (self.rect.right < 0 or self.rect.left > ANCHO or 
            self.rect.bottom < 0 or self.rect.top > ALTO or
            pygame.time.get_ticks() - self.creation_time > self.lifespan):
            self.kill()

def show_game_over_screen():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "GAME OVER", 64, ANCHO / 2, ALTO / 4, ROJO)
    # Botón de "Tienda"
    button_tienda_rect = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 - 70, 200, 50)
    pygame.draw.rect(pantalla, CYAN, button_tienda_rect)
    dibujar_texto(pantalla, "Tienda", 24, ANCHO / 2, ALTO / 2 - 60, NEGRO)
    # Botón de "Volver a Jugar"
    button_reiniciar_rect = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 - 5, 200, 50)
    pygame.draw.rect(pantalla, VERDE, button_reiniciar_rect)
    dibujar_texto(pantalla, "Volver a Jugar", 24, ANCHO / 2, ALTO / 2 + 10, NEGRO)
    # Botón de "Volver al Menú"
    button_menu_rect = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 + 60, 200, 50)
    pygame.draw.rect(pantalla, AMARILLO, button_menu_rect)
    dibujar_texto(pantalla, "Volver al Menú", 24, ANCHO / 2, ALTO / 2 + 70, NEGRO)
    pygame.display.flip()
    esperando = True
    while esperando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONUP:
                if button_tienda_rect.collidepoint(evento.pos):
                    return "tienda"
                elif button_reiniciar_rect.collidepoint(evento.pos):
                    return "reiniciar"  # Volver a jugar el mismo nivel
                elif button_menu_rect.collidepoint(evento.pos):
                    return "menu"  # Volver al menú
    return "salir"

def show_victory_screen():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¡VICTORIA!", 64, ANCHO / 2, ALTO / 4, VERDE)
    dibujar_texto(pantalla, "¡Has destruido todas las bolas!", 32, ANCHO / 2, ALTO / 2 - 50, BLANCO)
    
    # Botón de "Volver al Menú"
    button_rect = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 + 25, 200, 50)
    pygame.draw.rect(pantalla, VERDE, button_rect)
    dibujar_texto(pantalla, "Volver al Menú", 24, ANCHO / 2, ALTO / 2 + 40, NEGRO)

    pygame.display.flip()
    esperando = True
    while esperando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
            if evento.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(evento.pos):
                    esperando = False

def mostrar_pantalla_niveles():
    """Muestra una pantalla con todos los niveles y sus bolas asignadas"""
    scroll = 0
    max_scroll = 0
    niveles_totales = 30
    ancho_boton = 300
    alto_boton = 50
    espacio_entre_botones = 15
    alto_area = niveles_totales * (alto_boton + espacio_entre_botones)
    alto_visible = ALTO - 250  # Espacio visible para los niveles
    max_scroll = max(0, alto_area - alto_visible)

    esperando = True
    resultado = False
    while esperando:
        pantalla.fill(NEGRO)
        # Título
        dibujar_texto(pantalla, "NIVELES DEL JUEGO", 48, ANCHO // 2, 50, VERDE)
        # Información de las bolas
        y_pos = 120 - scroll
        y_pos += 40  # Mantener el espaciado para que los botones no se desplacen
        y_pos += 20
        dibujar_texto(pantalla, "SELECCIONA UN NIVEL:", 24, ANCHO // 2, y_pos, VERDE)
        y_pos += 40
        botones_niveles = []
        for nivel in range(1, niveles_totales + 1):
            x = ANCHO // 2 - ancho_boton // 2
            y = y_pos + (nivel - 1) * (alto_boton + espacio_entre_botones)
            boton = pygame.Rect(x, y, ancho_boton, alto_boton)
            if 100 < y < ALTO - 100:
                pygame.draw.rect(pantalla, VERDE, boton)
                dibujar_texto(pantalla, f"Nivel {nivel}  |  Round {nivel}", 22, x + ancho_boton // 2, y + alto_boton // 2, NEGRO)
            botones_niveles.append((nivel, boton))
        # Botón para volver al menú en la esquina superior izquierda
        boton_volver = pygame.Rect(20, 20, 120, 40)
        pygame.draw.rect(pantalla, ROJO, boton_volver)
        dibujar_texto(pantalla, "MENU", 24, 80, 40, BLANCO)
        # Flechas de scroll
        flecha_arriba = pygame.Rect(ANCHO - 60, ALTO - 120, 50, 50)
        flecha_abajo = pygame.Rect(ANCHO - 60, ALTO - 60, 50, 50)
        pygame.draw.rect(pantalla, AZUL, flecha_arriba)
        pygame.draw.rect(pantalla, BLANCO, flecha_arriba, 2)
        dibujar_texto(pantalla, "↑", 30, ANCHO - 35, ALTO - 110, BLANCO)
        pygame.draw.rect(pantalla, AZUL, flecha_abajo)
        pygame.draw.rect(pantalla, BLANCO, flecha_abajo, 2)
        dibujar_texto(pantalla, "↓", 30, ANCHO - 35, ALTO - 50, BLANCO)
        pygame.display.flip()
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
                resultado = False
            elif evento.type == pygame.MOUSEBUTTONUP:
                if flecha_arriba.collidepoint(evento.pos):
                    scroll = max(0, scroll - (alto_boton + espacio_entre_botones) * 2)
                elif flecha_abajo.collidepoint(evento.pos):
                    scroll = min(max_scroll, scroll + (alto_boton + espacio_entre_botones) * 2)
                elif boton_volver.collidepoint(evento.pos):
                    esperando = False
                    resultado = "volver"
                else:
                    for nivel, boton in botones_niveles:
                        if boton.collidepoint(evento.pos):
                            esperando = False
                            resultado = nivel
                            break
    return resultado

def mostrar_pantalla_horda(numero_horda):
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, f"Round {numero_horda}", 72, ANCHO // 2, ALTO // 2 - 50, CYAN)
    pygame.display.flip()
    pygame.time.delay(2000)  # Espera 2 segundos

def mostrar_vida_extra():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¡Vida extra!", 60, ANCHO // 2, ALTO // 2 - 30, VERDE)
    pygame.display.flip()
    pygame.time.delay(1200)

def mostrar_pantalla_bonus():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¡ROUND BONUS!", 72, ANCHO // 2, ALTO // 2 - 50, AMARILLO)
    dibujar_texto(pantalla, "¡3 vidas extra!", 48, ANCHO // 2, ALTO // 2 + 20, VERDE)
    dibujar_texto(pantalla, "Destruye las bolas azules para obtener monedas", 24, ANCHO // 2, ALTO // 2 + 80, BLANCO)
    pygame.display.flip()
    pygame.time.delay(3000)

def mostrar_pantalla_inicio():
    """Pantalla de inicio con 4 opciones"""
    while True:
        pantalla.fill(NEGRO)
        
        # Título del juego
        dibujar_texto(pantalla, "DESTRUYE LOS CÍRCULOS", 64, ANCHO // 2, ALTO // 6, CYAN)
        
        # Botones principales (centro)
        boton_iniciar = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 90, 200, 50)
        boton_infinito = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 30, 200, 50)
        
        # Botones inferiores
        boton_config = pygame.Rect(20, ALTO - 80, 150, 50)  # Esquina inferior izquierda
        boton_tienda = pygame.Rect(ANCHO // 2 - 75, ALTO - 80, 150, 50)  # Centro inferior
        boton_salir = pygame.Rect(ANCHO - 170, ALTO - 80, 150, 50)  # Esquina inferior derecha
        
        # Dibujar botones principales
        pygame.draw.rect(pantalla, VERDE, boton_iniciar)
        pygame.draw.rect(pantalla, MAGENTA, boton_infinito)
        
        # Dibujar botones inferiores
        pygame.draw.rect(pantalla, AMARILLO, boton_config)
        pygame.draw.rect(pantalla, CYAN, boton_tienda)
        pygame.draw.rect(pantalla, ROJO, boton_salir)
        
        # Texto de los botones principales
        dibujar_texto(pantalla, "NIVELES", 24, ANCHO // 2, ALTO // 2 - 80, NEGRO)
        dibujar_texto(pantalla, "NIVELES INFINITOS", 20, ANCHO // 2, ALTO // 2 - 20, NEGRO)
        
        # Texto de los botones inferiores
        dibujar_texto(pantalla, "CONFIGURACIÓN", 20, 95, ALTO - 70, NEGRO)
        dibujar_texto(pantalla, "TIENDA", 24, ANCHO // 2, ALTO - 70, NEGRO)
        dibujar_texto(pantalla, "SALIR", 24, ANCHO - 95, ALTO - 70, NEGRO)
        
        pygame.display.flip()
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if boton_iniciar.collidepoint(evento.pos):
                    return "iniciar"
                elif boton_infinito.collidepoint(evento.pos):
                    return "infinito"
                elif boton_config.collidepoint(evento.pos):
                    return "configuracion"
                elif boton_tienda.collidepoint(evento.pos):
                    return "tienda"
                elif boton_salir.collidepoint(evento.pos):
                    return "salir"
        
        clock.tick(FPS)

def mostrar_pantalla_configuracion():
    """Pantalla de configuración principal con opciones de controles"""
    global CONTROLES
    
    while True:
        pantalla.fill(NEGRO)
        
        dibujar_texto(pantalla, "CONFIGURACIÓN", 48, ANCHO // 2, ALTO // 4, AMARILLO)
        
        # Mostrar controles actuales
        dibujar_texto(pantalla, "Controles actuales:", 24, ANCHO // 2, ALTO // 2 - 80, BLANCO)
        dibujar_texto(pantalla, f"Izquierda: {pygame.key.name(CONTROLES['izquierda']).upper()}", 20, ANCHO // 2, ALTO // 2 - 50, VERDE)
        dibujar_texto(pantalla, f"Derecha: {pygame.key.name(CONTROLES['derecha']).upper()}", 20, ANCHO // 2, ALTO // 2 - 20, VERDE)
        dibujar_texto(pantalla, f"Disparo: {pygame.key.name(CONTROLES['disparo']).upper()}", 20, ANCHO // 2, ALTO // 2 + 10, VERDE)
        
        # Botones de controles
        boton_flechas = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 50, 140, 40)
        boton_wasd = pygame.Rect(ANCHO // 2 + 10, ALTO // 2 + 50, 140, 40)
        
        # Botón de dificultad con flecha
        boton_dificultad = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 120, 200, 50)
        
        boton_volver = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 180, 200, 50)
        
        # Dibujar botones de controles
        pygame.draw.rect(pantalla, CYAN, boton_flechas)
        pygame.draw.rect(pantalla, CYAN, boton_wasd)
        
        # Dibujar botón de dificultad
        pygame.draw.rect(pantalla, AMARILLO, boton_dificultad)
        
        pygame.draw.rect(pantalla, VERDE, boton_volver)
        
        # Texto de los botones de controles
        dibujar_texto(pantalla, "FLECHAS", 18, ANCHO // 2 - 80, ALTO // 2 + 60, NEGRO)
        dibujar_texto(pantalla, "WASD", 18, ANCHO // 2 + 80, ALTO // 2 + 60, NEGRO)
        
        # Texto del botón de dificultad con flecha
        dibujar_texto(pantalla, "DIFICULTAD →", 20, ANCHO // 2, ALTO // 2 + 130, NEGRO)
        
        dibujar_texto(pantalla, "VOLVER", 24, ANCHO // 2, ALTO // 2 + 190, NEGRO)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if boton_flechas.collidepoint(evento.pos):
                    # Cambiar a controles de flechas
                    CONTROLES = {
                        'izquierda': pygame.K_LEFT,
                        'derecha': pygame.K_RIGHT,
                        'disparo': pygame.K_SPACE
                    }
                elif boton_wasd.collidepoint(evento.pos):
                    # Cambiar a controles WASD
                    CONTROLES = {
                        'izquierda': pygame.K_a,
                        'derecha': pygame.K_d,
                        'disparo': pygame.K_SPACE
                    }
                elif boton_dificultad.collidepoint(evento.pos):
                    # Ir a la pantalla de dificultad
                    opcion_dificultad = mostrar_pantalla_dificultad()
                    if opcion_dificultad == "salir":
                        return "salir"
                elif boton_volver.collidepoint(evento.pos):
                    return "volver"
        
        clock.tick(FPS)

def mostrar_pantalla_dificultad():
    """Pantalla de configuración de dificultad del juego"""
    global DIFICULTAD_JUEGO
    
    while True:
        pantalla.fill(NEGRO)
        
        dibujar_texto(pantalla, "DIFICULTAD", 48, ANCHO // 2, ALTO // 4, AMARILLO)
        
        # Mostrar dificultad actual
        dibujar_texto(pantalla, f"Dificultad actual: {DIFICULTAD_JUEGO.upper()}", 24, ANCHO // 2, ALTO // 2 - 60, BLANCO)
        
        # Descripción de cada dificultad
        dibujar_texto(pantalla, "FÁCIL: Para principiantes", 18, ANCHO // 2, ALTO // 2 - 20, VERDE)
        dibujar_texto(pantalla, "NORMAL: Dificultad estándar", 18, ANCHO // 2, ALTO // 2 + 10, AMARILLO)
        dibujar_texto(pantalla, "DIFÍCIL: Para jugadores experimentados", 18, ANCHO // 2, ALTO // 2 + 40, ROJO)
        
        # Botones de dificultad
        boton_facil = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 80, 140, 40)
        boton_normal = pygame.Rect(ANCHO // 2 + 10, ALTO // 2 + 80, 140, 40)
        boton_dificil = pygame.Rect(ANCHO // 2 - 70, ALTO // 2 + 130, 140, 40)
        
        boton_volver = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 180, 200, 50)
        
        # Dibujar botones de dificultad
        pygame.draw.rect(pantalla, VERDE, boton_facil)
        pygame.draw.rect(pantalla, AMARILLO, boton_normal)
        pygame.draw.rect(pantalla, ROJO, boton_dificil)
        
        pygame.draw.rect(pantalla, VERDE, boton_volver)
        
        # Texto de los botones de dificultad
        dibujar_texto(pantalla, "FÁCIL", 18, ANCHO // 2 - 80, ALTO // 2 + 90, NEGRO)
        dibujar_texto(pantalla, "NORMAL", 18, ANCHO // 2 + 80, ALTO // 2 + 90, NEGRO)
        dibujar_texto(pantalla, "DIFÍCIL", 18, ANCHO // 2, ALTO // 2 + 150, NEGRO)  # Centrado en el botón
        
        dibujar_texto(pantalla, "VOLVER", 24, ANCHO // 2, ALTO // 2 + 190, NEGRO)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if boton_facil.collidepoint(evento.pos):
                    DIFICULTAD_JUEGO = "facil"
                elif boton_normal.collidepoint(evento.pos):
                    DIFICULTAD_JUEGO = "normal"
                elif boton_dificil.collidepoint(evento.pos):
                    DIFICULTAD_JUEGO = "dificil"
                elif boton_volver.collidepoint(evento.pos):
                    return "volver"
        
        clock.tick(FPS)

# Variables globales para guardado
ARCHIVO_GUARDADO = "guardado_infinito.json"
ARCHIVO_MONEDAS = "monedas_globales.json"
ARCHIVO_INVENTARIO = "inventario.json"

# Sistema de inventario
def cargar_inventario():
    """Carga el inventario del jugador desde el archivo"""
    if os.path.exists(ARCHIVO_INVENTARIO):
        try:
            with open(ARCHIVO_INVENTARIO, 'r') as f:
                return json.load()
        except:
            return []
    return []

def guardar_inventario(inventario):
    """Guarda el inventario del jugador en el archivo"""
    try:
        with open(ARCHIVO_INVENTARIO, 'w') as f:
            json.dump(inventario, f)
    except:
        pass

def añadir_a_inventario(tipo_item):
    """Añade un item al inventario"""
    inventario = cargar_inventario()
    inventario.append(tipo_item)
    guardar_inventario(inventario)

# Sistema de monedas globales
def cargar_monedas():
    """Carga las monedas del jugador desde el archivo"""
    try:
        with open(ARCHIVO_MONEDAS, 'r') as f:
            data = json.load(f)
            return data.get('monedas', 0)
    except:
        return 0

def guardar_monedas(monedas):
    """Guarda las monedas del jugador en el archivo"""
    try:
        with open(ARCHIVO_MONEDAS, 'w') as f:
            json.dump({'monedas': monedas, 'dificultad': 'facil'}, f)
    except:
        pass

# Función auxiliar para añadir sprites a los grupos de forma segura
def añadir_sprite_seguro(sprite, *grupos):
    """Añade un sprite a los grupos especificados de forma segura"""
    try:
        for grupo in grupos:
            if grupo is not None:
                grupo.add(sprite)
    except (NameError, AttributeError):
        pass  # Los grupos aún no existen

# Variables globales para la tienda
MONEDAS_JUGADOR = cargar_monedas()

# Variable global para la dificultad del juego
DIFICULTAD_JUEGO = "normal"

# Diccionario para nombres de poderes
PODER_NOMBRES = {
    'vida_extra': '¡Vida Extra!',
    'escudo_temporal': '¡Escudo Temporal!',
    'doble_disparo': '¡Doble Disparo!',
    'triple_disparo': '¡Triple Disparo!',
    'velocidad_disparo': '¡Disparo Rápido!',
    'doble_daño': '¡Doble Daño!'
}

# Variables para mejoras activas
DOBLE_PUNTOS_ACTIVO = False
DOBLE_PUNTOS_TIMER = 0
ESCUDO_TEMPORAL_TIMER = 0

# Objetos disponibles en la tienda - Separados por categorías
PODERES_TIENDA = {
    'doble_disparo': {
        'nombre': 'Doble Disparo',
        'precio': 20,
        'descripcion': 'Dispara dos balas simultáneamente',
        'tipo': 'doble_disparo'
    },
    'triple_disparo': {
        'nombre': 'Triple Disparo',
        'precio': 50,
        'descripcion': 'Dispara tres balas simultáneamente',
        'tipo': 'triple_disparo'
    },
    'velocidad_disparo': {
        'nombre': 'Velocidad de Disparo',
        'precio': 35,
        'descripcion': 'Aumenta la velocidad de disparo',
        'tipo': 'velocidad_disparo'
    },
}

OBJETOS_TIENDA = {
    'vida_extra': {
        'nombre': 'Vida Extra',
        'precio': 10,
        'descripcion': 'Añade una vida extra al jugador',
        'tipo': 'vida'
    },
    'escudo_temporal': {
        'nombre': 'Escudo Temporal',
        'precio': 25,
        'descripcion': 'Escudo que protege por 10 segundos',
        'tipo': 'escudo'
    }
}

def aplicar_mejora(jugador, tipo_mejora):
    """Aplica la mejora comprada al jugador"""
    global ESCUDO_TEMPORAL_TIMER
    if tipo_mejora == 'vida_extra':
        jugador.vidas += 1
    elif tipo_mejora == 'escudo_temporal':
        jugador.escudo = True
        ESCUDO_TEMPORAL_TIMER = pygame.time.get_ticks()
    elif tipo_mejora == 'doble_disparo':
        jugador.powerup_level = max(jugador.powerup_level, 1)
        jugador.powerup_timer = pygame.time.get_ticks()
    elif tipo_mejora == 'triple_disparo':
        jugador.powerup_level = max(jugador.powerup_level, 3)
        jugador.powerup_timer = pygame.time.get_ticks()
    elif tipo_mejora == 'velocidad_disparo':
        jugador.shoot_delay = max(100, jugador.shoot_delay - 50)
    elif tipo_mejora == 'doble_daño':
        jugador.powerup_level = max(jugador.powerup_level, 2)
        jugador.powerup_timer = pygame.time.get_ticks()


def mostrar_pantalla_tienda():
    """Pantalla de tienda del juego con objetos y mejoras comprables separados por categorías"""
    global MONEDAS_JUGADOR, pantalla

    # Asegurar que la pantalla está inicializada
    if pantalla is None:
        pantalla = pygame.display.set_mode((ANCHO, ALTO))

    # Recargar monedas del jugador
    try:
        MONEDAS_JUGADOR = cargar_monedas()
    except Exception as e:
        MONEDAS_JUGADOR = 0

    # Variables para la interfaz
    scroll_y = 0
    total_items = len(OBJETOS_TIENDA) + len(PODERES_TIENDA)
    # Ajuste: sumar 50 por el espacio del título de poderes
    max_scroll = max(0, total_items * 80 + 50 - ALTO + 200)
    
    while True:
        pantalla.fill(NEGRO)

        # Título de la tienda (se mueve con el scroll)
        dibujar_texto(pantalla, "TIENDA", 64, ANCHO // 2, 50 - scroll_y, AMARILLO)

        # Mostrar monedas del jugador (esquina superior derecha, fijo)
        dibujar_texto(pantalla, f"Monedas: {MONEDAS_JUGADOR}", 24, ANCHO - 20, 20, (255, 215, 0))

        # Título de la sección de objetos (se mueve con el scroll)
        dibujar_texto(pantalla, "OBJETOS", 28, ANCHO // 2, 170 - scroll_y, CYAN)

        # Dibujar objetos de la tienda
        y_pos = 200 - scroll_y
        for item_id, item in OBJETOS_TIENDA.items():
            if y_pos > ALTO:
                break
            if y_pos < -100:
                y_pos += 80
                continue
            # Fondo del objeto (más pequeño)
            item_rect = pygame.Rect(100, y_pos, ANCHO - 200, 70)
            color_fondo = VERDE if MONEDAS_JUGADOR >= item['precio'] else (128, 128, 128)  # Verde si puede comprar, gris si no
            pygame.draw.rect(pantalla, color_fondo, item_rect)
            pygame.draw.rect(pantalla, BLANCO, item_rect, 2)
            # Información del objeto (centrada)
            dibujar_texto(pantalla, item['nombre'], 22, ANCHO // 2, y_pos + 5, NEGRO)
            dibujar_texto(pantalla, item['descripcion'], 16, ANCHO // 2, y_pos + 25, NEGRO)
            dibujar_texto(pantalla, f"Precio: {item['precio']} monedas", 18, ANCHO // 2, y_pos + 45, NEGRO)
            # Botón de compra
            if MONEDAS_JUGADOR >= item['precio']:
                boton_comprar = pygame.Rect(ANCHO - 180, y_pos + 20, 100, 40)
                pygame.draw.rect(pantalla, AZUL, boton_comprar)
                pygame.draw.rect(pantalla, BLANCO, boton_comprar, 2)
                dibujar_texto(pantalla, "COMPRAR", 16, ANCHO - 130, y_pos + 30, BLANCO)
            y_pos += 80

        # Título de la sección de poderes
        dibujar_texto(pantalla, "PODERES", 28, ANCHO // 2, y_pos + 10, MAGENTA)
        y_pos += 50

        # Dibujar poderes de la tienda
        for item_id, item in PODERES_TIENDA.items():
            if y_pos > ALTO:
                break
            if y_pos < -100:
                y_pos += 80
                continue
            # Fondo del poder (más pequeño)
            item_rect = pygame.Rect(100, y_pos, ANCHO - 200, 70)
            color_fondo = VERDE if MONEDAS_JUGADOR >= item['precio'] else (128, 128, 128)  # Verde si puede comprar, gris si no
            pygame.draw.rect(pantalla, color_fondo, item_rect)
            pygame.draw.rect(pantalla, BLANCO, item_rect, 2)
            # Información del poder (centrada)
            dibujar_texto(pantalla, item['nombre'], 22, ANCHO // 2, y_pos + 5, NEGRO)
            dibujar_texto(pantalla, item['descripcion'], 16, ANCHO // 2, y_pos + 25, NEGRO)
            dibujar_texto(pantalla, f"Precio: {item['precio']} monedas", 18, ANCHO // 2, y_pos + 45, NEGRO)
            # Botón de compra
            if MONEDAS_JUGADOR >= item['precio']:
                boton_comprar = pygame.Rect(ANCHO - 180, y_pos + 20, 100, 40)
                pygame.draw.rect(pantalla, AZUL, boton_comprar)
                pygame.draw.rect(pantalla, BLANCO, boton_comprar, 2)
                dibujar_texto(pantalla, "COMPRAR", 16, ANCHO - 130, y_pos + 30, BLANCO)
            y_pos += 80

        # Botones de navegación
        if max_scroll > 0:
            # Botón subir
            if scroll_y > 0:
                boton_subir = pygame.Rect(ANCHO - 50, ALTO - 150, 40, 40)
                pygame.draw.rect(pantalla, AZUL, boton_subir)
                pygame.draw.rect(pantalla, BLANCO, boton_subir, 2)
                dibujar_texto(pantalla, "↑", 24, ANCHO - 30, ALTO - 145, BLANCO)
            # Botón bajar
            if scroll_y < max_scroll:
                boton_bajar = pygame.Rect(ANCHO - 50, ALTO - 100, 40, 40)
                pygame.draw.rect(pantalla, AZUL, boton_bajar)
                pygame.draw.rect(pantalla, BLANCO, boton_bajar, 2)
                dibujar_texto(pantalla, "↓", 24, ANCHO - 30, ALTO - 95, BLANCO)

        # Botón para volver al menú principal (esquina superior izquierda)
        boton_volver = pygame.Rect(20, 20, 150, 40)
        pygame.draw.rect(pantalla, VERDE, boton_volver)
        dibujar_texto(pantalla, "VOLVER", 22, 95, 30, NEGRO)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                mouse_pos = evento.pos
                # Verificar clic en botón volver
                if boton_volver.collidepoint(mouse_pos):
                    return "volver"
                # Verificar clic en botones de navegación
                if max_scroll > 0:
                    if scroll_y > 0 and pygame.Rect(ANCHO - 50, ALTO - 150, 40, 40).collidepoint(mouse_pos):
                        scroll_y = max(0, scroll_y - 80)
                    elif scroll_y < max_scroll and pygame.Rect(ANCHO - 50, ALTO - 100, 40, 40).collidepoint(mouse_pos):
                        scroll_y = min(max_scroll, scroll_y + 80)
                # Verificar clic en botones de compra
                y_pos = 200 - scroll_y
                # Verificar objetos
                for item_id, item in OBJETOS_TIENDA.items():
                    if y_pos > ALTO:
                        break
                    if y_pos < -100:
                        y_pos += 80
                        continue
                    if MONEDAS_JUGADOR >= item['precio']:
                        boton_comprar = pygame.Rect(ANCHO - 180, y_pos + 20, 100, 40)
                        if boton_comprar.collidepoint(mouse_pos):
                            # Procesar compra
                            MONEDAS_JUGADOR -= item['precio']
                            guardar_monedas(MONEDAS_JUGADOR)
                            # Añadir al inventario para ser usado en el próximo juego
                            añadir_a_inventario(item['tipo'])
                            # Mostrar mensaje de confirmación
                            mostrar_mensaje_compra(item['nombre'])
                    y_pos += 80
                # Título de poderes
                y_pos += 50
                # Verificar poderes
                for item_id, item in PODERES_TIENDA.items():
                    if y_pos > ALTO:
                        break
                    if y_pos < -100:
                        y_pos += 80
                        continue
                    if MONEDAS_JUGADOR >= item['precio']:
                        boton_comprar = pygame.Rect(ANCHO - 180, y_pos + 20, 100, 40)
                        if boton_comprar.collidepoint(mouse_pos):
                            # Procesar compra
                            MONEDAS_JUGADOR -= item['precio']
                            guardar_monedas(MONEDAS_JUGADOR)
                            # Añadir al inventario para ser usado en el próximo juego
                            añadir_a_inventario(item['tipo'])
                            # Mostrar mensaje de confirmación
                            mostrar_mensaje_compra(item['nombre'])
                    y_pos += 80
            elif evento.type == pygame.MOUSEWHEEL:
                # Scroll con rueda del mouse
                scroll_y = max(0, min(max_scroll, scroll_y - evento.y * 40))
            elif evento.type == pygame.KEYDOWN:
                # Scroll con flechas del teclado
                if evento.key == pygame.K_DOWN:
                    scroll_y = min(max_scroll, scroll_y + 80)
                elif evento.key == pygame.K_UP:
                    scroll_y = max(0, scroll_y - 80)

        clock.tick(FPS)

def mostrar_mensaje_compra(nombre_item):
    """Muestra un mensaje de confirmación de compra"""
    tiempo_inicio = pygame.time.get_ticks()
    duracion = 2000  # 2 segundos
    
    while pygame.time.get_ticks() - tiempo_inicio < duracion:
        pantalla.fill(NEGRO)
        
        # Mensaje de compra exitosa
        dibujar_texto(pantalla, "¡Compra Exitosa!", 48, ANCHO // 2, ALTO // 2 - 50, VERDE)
        dibujar_texto(pantalla, f"Has comprado: {nombre_item}", 32, ANCHO // 2, ALTO // 2, BLANCO)
        dibujar_texto(pantalla, "Presiona cualquier tecla para continuar...", 24, ANCHO // 2, ALTO // 2 + 50, CYAN)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONUP:
                return
        
        clock.tick(FPS)

def serializar_enemigos():
    """Convierte el estado actual de los enemigos a formato JSON"""
    enemigos_data = []
    for enemigo in enemigos:
        enemigo_info = {
            'tipo': enemigo.__class__.__name__,
            'posicion': [enemigo.rect.x, enemigo.rect.y],
            'destrucciones': enemigo.destrucciones if hasattr(enemigo, 'destrucciones') else 0,
            'radio': enemigo.radio if hasattr(enemigo, 'radio') else 20
        }
        # Para BolaNegra, guardar también las vidas
        if hasattr(enemigo, 'vidas'):
            enemigo_info['vidas'] = enemigo.vidas
        # Para bolas azules, guardar velocidad
        if hasattr(enemigo, 'vel'):
            enemigo_info['vel'] = enemigo.vel
        # Para bolas negras, guardar velocidad horizontal
        if hasattr(enemigo, 'vel_x'):
            enemigo_info['vel_x'] = enemigo.vel_x
        # Guardar timers de disparo
        if hasattr(enemigo, 'last_shot'):
            enemigo_info['last_shot'] = enemigo.last_shot
        if hasattr(enemigo, 'shoot_delay'):
            enemigo_info['shoot_delay'] = enemigo.shoot_delay
        
        enemigos_data.append(enemigo_info)
    return enemigos_data

def recrear_enemigos(enemigos_data):
    """Recrea los enemigos desde los datos guardados"""
    global all_sprites, enemigos, bolas_azules
    
    for enemigo_info in enemigos_data:
        # Crear el enemigo según su tipo
        if enemigo_info['tipo'] == 'BolaVerde':
            enemigo = BolaVerde()
        elif enemigo_info['tipo'] == 'BolaAzul':
            enemigo = BolaAzul()
            bolas_azules.add(enemigo)
        elif enemigo_info['tipo'] == 'BolaRoja':
            enemigo = BolaRoja()
        elif enemigo_info['tipo'] == 'BolaNegra':
            enemigo = BolaNegra()
        elif enemigo_info['tipo'] == 'BolaMorada':
            enemigo = BolaMorada()
        elif enemigo_info['tipo'] == 'BolaNaranja':
            enemigo = BolaNaranja()
        elif enemigo_info['tipo'] == 'BolaGris':
            enemigo = BolaGris()
        elif enemigo_info['tipo'] == 'BolaPequena':
            enemigo = BolaPequena(enemigo_info['posicion'])
        elif enemigo_info['tipo'] == 'Bomba':
            enemigo = Bomba(enemigo_info['posicion'])
        else:
            continue  # Tipo desconocido, saltar
        
        # Restaurar posición
        enemigo.rect.x = enemigo_info['posicion'][0]
        enemigo.rect.y = enemigo_info['posicion'][1]
        
        # Restaurar destrucciones
        enemigo.destrucciones = enemigo_info['destrucciones']
        
        # Restaurar atributos específicos
        if 'vidas' in enemigo_info and hasattr(enemigo, 'vidas'):
            enemigo.vidas = enemigo_info['vidas']
        if 'vel' in enemigo_info and hasattr(enemigo, 'vel'):
            enemigo.vel = enemigo_info['vel']
        if 'vel_x' in enemigo_info and hasattr(enemigo, 'vel_x'):
            enemigo.vel_x = enemigo_info['vel_x']
        if 'last_shot' in enemigo_info and hasattr(enemigo, 'last_shot'):
            enemigo.last_shot = enemigo_info['last_shot']
        if 'shoot_delay' in enemigo_info and hasattr(enemigo, 'shoot_delay'):
            enemigo.shoot_delay = enemigo_info['shoot_delay']
        
        # Agregar a los grupos
        all_sprites.add(enemigo)
        enemigos.add(enemigo)

def guardar_progreso_infinito(horda, puntos, vidas):
    """Guarda el progreso del modo infinito"""
    datos = {
        'horda': horda,
        'puntos': puntos,
        'vidas': vidas,
        'enemigos': serializar_enemigos(),
        'timestamp': pygame.time.get_ticks()
    }
    try:
        with open(ARCHIVO_GUARDADO, 'w') as f:
            json.dump(datos, f)
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

def cargar_progreso_infinito():
    """Carga el progreso guardado del modo infinito"""
    if os.path.exists(ARCHIVO_GUARDADO):
        try:
            with open(ARCHIVO_GUARDADO, 'r') as f:
                datos = json.load(f)
            return datos
        except Exception as e:
            print(f"Error al cargar: {e}")
            return None
    return None

def mostrar_pantalla_guardado_infinito():
    """Pantalla para elegir entre nuevo juego o continuar"""
    progreso = cargar_progreso_infinito()
    
    while True:
        pantalla.fill(NEGRO)
        
        dibujar_texto(pantalla, "NIVELES INFINITOS", 48, ANCHO // 2, ALTO // 4, MAGENTA)
        
        if progreso:
            dibujar_texto(pantalla, f"Progreso guardado: Horda {progreso['horda']}, {progreso['puntos']} puntos", 20, ANCHO // 2, ALTO // 2 - 60, CYAN)
        
        # Botones
        boton_nuevo = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 20, 200, 50)
        pygame.draw.rect(pantalla, VERDE, boton_nuevo)
        dibujar_texto(pantalla, "NUEVO JUEGO", 24, ANCHO // 2, ALTO // 2 - 10, NEGRO)
        
        if progreso:
            boton_continuar = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 40, 200, 50)
            pygame.draw.rect(pantalla, AMARILLO, boton_continuar)
            dibujar_texto(pantalla, "CONTINUAR", 24, ANCHO // 2, ALTO // 2 + 50, NEGRO)
        
        boton_volver = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 100, 200, 50)
        pygame.draw.rect(pantalla, ROJO, boton_volver)
        dibujar_texto(pantalla, "VOLVER", 24, ANCHO // 2, ALTO // 2 + 110, NEGRO)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            elif evento.type == pygame.MOUSEBUTTONUP:
                if boton_nuevo.collidepoint(evento.pos):
                    return "nuevo"
                elif progreso and boton_continuar.collidepoint(evento.pos):
                    return "continuar"
                elif boton_volver.collidepoint(evento.pos):
                    return "volver"
        
        clock.tick(FPS)

def mostrar_pantalla_guardar():
    """Pantalla para guardar progreso"""
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¿Guardar progreso?", 36, ANCHO // 2, ALTO // 2 - 50, AMARILLO)
    
    # Botones
    boton_si = pygame.Rect(ANCHO // 2 - 120, ALTO // 2, 100, 40)
    boton_no = pygame.Rect(ANCHO // 2 + 20, ALTO // 2, 100, 40)
    
    pygame.draw.rect(pantalla, VERDE, boton_si)
    pygame.draw.rect(pantalla, ROJO, boton_no)
    
    dibujar_texto(pantalla, "SÍ", 20, ANCHO // 2 - 70, ALTO // 2 + 10, NEGRO)
    dibujar_texto(pantalla, "NO", 20, ANCHO // 2 + 70, ALTO // 2 + 10, NEGRO)
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if boton_si.collidepoint(evento.pos):
                    return True
                elif boton_no.collidepoint(evento.pos):
                    return False
        clock.tick(FPS)

# --- Grupos de Sprites e Instanciación ---
all_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
bolas_azules = pygame.sprite.Group()
disparos_jugador = pygame.sprite.Group()
disparos_enemigos = pygame.sprite.Group()
monedas = pygame.sprite.Group()  # Nuevo grupo para monedas
puntos = 0  # Contador de puntos por monedas

horda_actual = 1
TOTAL_HORDAS = 30

# Mapeo de nombres de clases de bolas para la generación de hordas
BOLA_CLASES = {
    'BolaVerde': BolaVerde,
    'BolaAzul': BolaAzul,
    'BolaRoja': BolaRoja,
    'BolaNegra': BolaNegra,
    'BolaMorada': BolaMorada,
    'BolaNaranja': BolaNaranja,
    'BolaGris': BolaGris,
}

# Configuración de hordas para cada nivel
HORDAS_CONFIG = {
    1: {'BolaNegra': 4},
    2: {'BolaRoja': 4},
    3: {'BolaAzul': 4},
    4: {'BolaVerde': 4},
    5: {'BolaNegra': 3, 'BolaRoja': 3},
    6: {'BolaAzul': 3, 'BolaVerde': 3},
    7: {'BolaMorada': 3},
    8: {'BolaNaranja': 3},
    9: {'BolaGris': 3},
    10: {'BolaNegra': 4, 'BolaRoja': 4, 'BolaAzul': 3},
    11: {'BolaVerde': 5, 'BolaMorada': 2},
    12: {'BolaNaranja': 3, 'BolaGris': 2},
    13: {'BolaNegra': 6},
    14: {'BolaRoja': 6},
    15: {'BolaAzul': 6},
    16: {'BolaVerde': 6},
    17: {'BolaMorada': 4},
    18: {'BolaNaranja': 4},
    19: {'BolaGris': 4},
    20: {'BolaNegra': 3, 'BolaRoja': 3, 'BolaAzul': 3, 'BolaVerde': 3},
    21: {'BolaMorada': 3, 'BolaNaranja': 3},
    22: {'BolaGris': 3, 'BolaNegra': 4},
    23: {'BolaRoja': 5, 'BolaAzul': 4},
    24: {'BolaVerde': 5, 'BolaMorada': 3},
    25: {'BolaNaranja': 3, 'BolaGris': 3, 'BolaNegra': 2},
    26: {'BolaMorada': 5},
    27: {'BolaNaranja': 5},
    28: {'BolaGris': 5},
    29: {'BolaNegra': 4, 'BolaMorada': 3, 'BolaGris': 2},
    30: {'BolaVerde': 4, 'BolaAzul': 4, 'BolaRoja': 4, 'BolaNegra': 4},
}

def calcular_monedas_totales_nivel(nivel):
    """Calcula el número total de monedas en un nivel específico."""
    config_horda = HORDAS_CONFIG.get(nivel, {})
    total_monedas = 0
    
    # Monedas por tipo de bola
    monedas_por_bola = {
        'BolaVerde': 7,  # 4 golpes (1 moneda c/u) + 3 por destrucción
        'BolaAzul': 6    # 4 golpes (1 moneda c/u) + 2 por destrucción
    }
    
    for nombre_clase, cantidad in config_horda.items():
        if nombre_clase in monedas_por_bola:
            total_monedas += cantidad * monedas_por_bola[nombre_clase]
            
    return total_monedas

def generar_horda(horda):
    """Genera la horda de enemigos para el nivel especificado."""
    mostrar_pantalla_horda(horda)
    
    # Obtener la configuración de la horda para el nivel actual
    config_horda = HORDAS_CONFIG.get(horda)
    
    # Si no hay configuración para el nivel, generar una horda por defecto
    if not config_horda:
        # Por defecto, generar 3 bolas negras
        config_horda = {'BolaNegra': 3}
        
    # Generar los enemigos según la configuración
    for nombre_clase, cantidad in config_horda.items():
        clase_bola = BOLA_CLASES.get(nombre_clase)
        if clase_bola:
            for _ in range(cantidad):
                enemigo = clase_bola()
                aplicar_dificultad_enemigo(enemigo)
                all_sprites.add(enemigo)
                enemigos.add(enemigo)
                # Si es una BolaAzul, añadirla al grupo correspondiente
                if isinstance(enemigo, BolaAzul):
                    bolas_azules.add(enemigo)

def aplicar_dificultad_enemigo(enemigo):
    """Aplica la dificultad seleccionada a los enemigos"""
    global DIFICULTAD_JUEGO
    
    if DIFICULTAD_JUEGO == "dificil":
        # En dificultad difícil, los enemigos soportan más golpes
        if hasattr(enemigo, 'destrucciones'):
            enemigo.destrucciones = 0  # Resetear contador para aplicar nueva lógica
        # Aumentar resistencia: soportan 1-2 golpes extra
        if hasattr(enemigo, 'vidas'):
            enemigo.vidas += 2  # BolaNegra: de 4 a 6 vidas
        else:
            # Para otras bolas, aumentar el número de destrucciones necesarias
            enemigo.destrucciones_extra = 2  # Necesitan 2 golpes extra
        # Disparar más rápido (reducir delay en 0.5 segundos = 500ms)
        if hasattr(enemigo, 'shoot_delay'):
            enemigo.shoot_delay = max(200, enemigo.shoot_delay - 500)  # Mínimo 200ms
    elif DIFICULTAD_JUEGO == "facil":
        # En dificultad fácil, los enemigos disparan más lento (aumentar delay en 1 segundo = 1000ms)
        if hasattr(enemigo, 'shoot_delay'):
            enemigo.shoot_delay += 1000

def generar_horda_infinita(horda):
    """Genera bolas para niveles infinitos con dificultad creciente"""
    if horda > 1:
        mostrar_pantalla_horda(horda)
    
    # Dificultad creciente: más bolas según el número de horda
    num_bolas_verdes = min(3 + (horda // 3), 8)  # Máximo 8 bolas verdes
    num_bolas_rojas = min(2 + (horda // 2), 6)    # Máximo 6 bolas rojas
    num_bolas_negras = min(2 + (horda // 4), 5)   # Máximo 5 bolas negras
    num_bolas_azules = min(1 + (horda // 5), 4)   # Máximo 4 bolas azules
    num_bolas_moradas = min(1 + (horda // 6), 3)  # Máximo 3 bolas moradas
    num_bolas_naranjas = min(1 + (horda // 7), 3) # Máximo 3 bolas naranjas
    num_bolas_grises = min(1 + (horda // 8), 3)   # Máximo 3 bolas grises
    
    # Ajuste para dificultad fácil: reducir en 1 las bolas verde, azul y roja (mínimo 1)
    if DIFICULTAD_JUEGO == "facil":
        num_bolas_verdes = max(1, num_bolas_verdes - 1)
        num_bolas_rojas = max(1, num_bolas_rojas - 1)
        num_bolas_azules = max(1, num_bolas_azules - 1)
    
    # Generar las bolas verdes
    for _ in range(num_bolas_verdes):
        enemigo = BolaVerde()
        aplicar_dificultad_enemigo(enemigo)
        all_sprites.add(enemigo)
        enemigos.add(enemigo)
    
    # Generar las bolas rojas
    for _ in range(num_bolas_rojas):
        enemigo = BolaRoja()
        aplicar_dificultad_enemigo(enemigo)
        all_sprites.add(enemigo)
        enemigos.add(enemigo)
    
    # Generar las bolas negras
    for _ in range(num_bolas_negras):
        enemigo = BolaNegra()
        aplicar_dificultad_enemigo(enemigo)
        all_sprites.add(enemigo)
        enemigos.add(enemigo)
    
    # Generar las bolas azules
    for _ in range(num_bolas_azules):
        enemigo = BolaAzul()
        aplicar_dificultad_enemigo(enemigo)
        all_sprites.add(enemigo)
        enemigos.add(enemigo)
        bolas_azules.add(enemigo)  # Añadir al grupo especial de bolas azules
    
    # Generar las bolas moradas
    for _ in range(num_bolas_moradas):
        enemigo = BolaMorada()
        aplicar_dificultad_enemigo(enemigo)
        all_sprites.add(enemigo)
        enemigos.add(enemigo)
    
    # Generar las bolas naranjas
    for _ in range(num_bolas_naranjas):
        enemigo = BolaNaranja()
        aplicar_dificultad_enemigo(enemigo)
        all_sprites.add(enemigo)
        enemigos.add(enemigo)
    
    # Generar las bolas grises
    for _ in range(num_bolas_grises):
        enemigo = BolaGris()
        aplicar_dificultad_enemigo(enemigo)
        all_sprites.add(enemigo)
        enemigos.add(enemigo)
        
def game_loop(modo_infinito=False, nivel_inicial=1):
    global jugador, jugador_mini_img, all_sprites, enemigos, bolas_azules, disparos_jugador, disparos_enemigos, monedas, puntos, horda_actual, ESCUDO_TEMPORAL_TIMER, MONEDAS_JUGADOR

    # Variables para el texto de poder
    poder_texto = ""
    poder_texto_timer = 0

    # Inicialización de grupos y variables del juego
    all_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    bolas_azules = pygame.sprite.Group()
    disparos_jugador = pygame.sprite.Group()
    disparos_enemigos = pygame.sprite.Group()
    monedas = pygame.sprite.Group()
    
    jugador = Jugador()
    all_sprites.add(jugador)

    # Aplicar mejoras del inventario
    inventario = cargar_inventario()
    if inventario:
        for tipo_mejora in inventario:
            aplicar_mejora(jugador, tipo_mejora)
        # Limpiar inventario después de aplicarlo
        guardar_inventario([])
    
    puntos = 0
    horda_actual = nivel_inicial
    
    # Variables para el contador de monedas del nivel
    monedas_recolectadas_nivel = 0
    if not modo_infinito:
        monedas_nivel_total = calcular_monedas_totales_nivel(horda_actual)
    else:
        # En modo infinito no hay un total fijo, se podría calcular por horda si se quisiera
        monedas_nivel_total = 0

    if modo_infinito:
        progreso = cargar_progreso_infinito()
        if progreso:
            horda_actual = progreso['horda']
            puntos = progreso['puntos']
            jugador.vidas = progreso['vidas']
            recrear_enemigos(progreso['enemigos'])
        else:
            generar_horda_infinita(horda_actual)
    else:
        generar_horda(horda_actual)

    jugando = True
    while jugando:
        clock.tick(FPS)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if modo_infinito:
                        if mostrar_pantalla_guardar():
                            guardar_progreso_infinito(horda_actual, puntos, jugador.vidas)
                    jugando = False
            elif evento.type == pygame.MOUSEBUTTONUP and modo_infinito:
                # Manejar clics en botones solo en modo infinito
                boton_guardar = pygame.Rect(ANCHO - 200, ALTO - 60, 80, 40)
                boton_salir = pygame.Rect(ANCHO - 100, ALTO - 60, 80, 40)
                
                if boton_guardar.collidepoint(evento.pos):
                    # Guardar progreso y mostrar confirmación
                    guardar_progreso_infinito(horda_actual, puntos, jugador.vidas)
                    # Mostrar mensaje de confirmación temporal
                    poder_texto = "¡Progreso guardado!"
                    poder_texto_timer = pygame.time.get_ticks()
                elif boton_salir.collidepoint(evento.pos):
                    # Preguntar si guardar antes de salir
                    if mostrar_pantalla_guardar():
                        guardar_progreso_infinito(horda_actual, puntos, jugador.vidas)
                    jugando = False

        all_sprites.update()

        # Colisiones
        # Disparos del jugador con enemigos
        colisiones = pygame.sprite.groupcollide(enemigos, disparos_jugador, False, True)
        for enemigo in colisiones:
            enemigo.on_hit()
            puntos += 10

        # Disparos de enemigos con el jugador
        if not jugador.hidden:
            colisiones = pygame.sprite.spritecollide(jugador, disparos_enemigos, True)
            if colisiones and not jugador.escudo:
                jugador.hide()

        # Colisión de enemigos con el jugador
        if not jugador.hidden:
            colisiones = pygame.sprite.spritecollide(jugador, enemigos, False)
            if colisiones and not jugador.escudo:
                jugador.hide()

        # Monedas con el jugador
        colisiones = pygame.sprite.spritecollide(jugador, monedas, True)
        for _ in colisiones:
            MONEDAS_JUGADOR += 1
            monedas_recolectadas_nivel += 1  # Incrementar contador del nivel
            guardar_monedas(MONEDAS_JUGADOR)

        # Bolas celestes con el jugador
        colisiones = pygame.sprite.spritecollide(jugador, bolas_celestes, True)
        for _ in colisiones:
            # Aplicar poder aleatorio
            poder = random.choice(['vida_extra', 'escudo_temporal', 'doble_daño'])
            aplicar_mejora(jugador, poder)
            # Mostrar texto del poder
            poder_texto = PODER_NOMBRES[poder]
            poder_texto_timer = pygame.time.get_ticks()


        if len(enemigos) == 0:
            if modo_infinito:
                horda_actual += 1
                generar_horda_infinita(horda_actual)
            else:
                # Nivel completado, mostrar pantalla de victoria y salir del bucle
                show_victory_screen()
                jugando = False

        if jugador.vidas == 0 and not jugador.hidden:
            opcion = show_game_over_screen()
            if opcion == "reiniciar":
                game_loop(modo_infinito, nivel_inicial)
                return
            elif opcion == "tienda":
                mostrar_pantalla_tienda()
                jugando = False # Go back to main menu
            else: # Covers "menu" and "salir"
                jugando = False


        # Dibujar / renderizar
        pantalla.fill(NEGRO)
        all_sprites.draw(pantalla)
        dibujar_vidas_jugador(pantalla, 5, 5, jugador.vidas, jugador.image)

        # Dibujar contador de monedas del nivel
        if not modo_infinito:
            texto_monedas = f"Monedas: {monedas_recolectadas_nivel} / {monedas_nivel_total}"
            dibujar_texto(pantalla, texto_monedas, 22, ANCHO - 120, 10)
        else:
            # En modo infinito, solo mostrar las recolectadas en la horda
            texto_monedas = f"Monedas horda: {monedas_recolectadas_nivel}"
            dibujar_texto(pantalla, texto_monedas, 22, ANCHO - 120, 10)
            
            # Dibujar botones de Guardar y Salir en modo infinito
            boton_guardar = pygame.Rect(ANCHO - 200, ALTO - 60, 80, 40)
            boton_salir = pygame.Rect(ANCHO - 100, ALTO - 60, 80, 40)
            
            dibujar_boton(pantalla, boton_guardar, VERDE, "GUARDAR", NEGRO, 18)
            dibujar_boton(pantalla, boton_salir, ROJO, "SALIR", BLANCO, 18)

        # Dibujar texto del poder
        if poder_texto and pygame.time.get_ticks() - poder_texto_timer < 2000:  # 2 segundos
            dibujar_texto(pantalla, poder_texto, 36, ANCHO // 2, 20, AMARILLO)
        else:
            poder_texto = ""

        pygame.display.flip()

if __name__ == "__main__":
    while True:
        opcion = mostrar_pantalla_inicio()
        if opcion == "iniciar":
            nivel_seleccionado = mostrar_pantalla_niveles()
            if nivel_seleccionado and nivel_seleccionado != "volver":
                game_loop(modo_infinito=False, nivel_inicial=nivel_seleccionado)
        elif opcion == "infinito":
            opcion_infinito = mostrar_pantalla_guardado_infinito()
            if opcion_infinito != "volver":
                game_loop(modo_infinito=True)
        elif opcion == "configuracion":
            mostrar_pantalla_configuracion()
        elif opcion == "tienda":
            mostrar_pantalla_tienda()
        elif opcion == "salir":
            break
    pygame.quit()
    sys.exit()
