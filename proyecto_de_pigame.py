import pygame
import random
import sys
import math
import json
import os

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

# Cargar imágenes de personajes
try:
    imagen_alien_verde = pygame.image.load('image/alien.webp').convert_alpha()
    imagen_alien_rojo = pygame.image.load('image/alienrojo.png').convert_alpha()
    imagen_nave = pygame.image.load('image/nave.png').convert_alpha()
    imagen_alien_blanco = pygame.image.load('image/alienblanco.jpg').convert_alpha()
    imagen_alien_azul = pygame.image.load('image/alienazul.png').convert_alpha()
    
    # Redimensionar imágenes para que se ajusten al juego
    imagen_alien_verde = pygame.transform.scale(imagen_alien_verde, (40, 40))
    imagen_alien_rojo = pygame.transform.scale(imagen_alien_rojo, (40, 40))
    imagen_nave = pygame.transform.scale(imagen_nave, (50, 10))
    imagen_alien_blanco = pygame.transform.scale(imagen_alien_blanco, (44, 44))
    imagen_alien_azul = pygame.transform.scale(imagen_alien_azul, (40, 40))
except:
    # Si no se pueden cargar las imágenes, usar formas geométricas por defecto
    imagen_alien_verde = None
    imagen_alien_rojo = None
    imagen_nave = None
    imagen_alien_blanco = None
    imagen_alien_azul = None
    print("No se pudieron cargar las imágenes. Usando formas geométricas por defecto.")

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
        if imagen_nave:
            self.image_orig = imagen_nave
        else:
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
        self.escudo = False  # Nuevo atributo: escudo
        self.escudo_timer = 0  # Temporizador del escudo

    def update(self):
        reaparecido = False
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = ANCHO // 2
            self.rect.bottom = ALTO - 20
            self.escudo = True  # Activar escudo al reaparecer
            self.escudo_timer = pygame.time.get_ticks()
            reaparecido = True

        # Desactivar escudo tras 2 segundos
        if self.escudo and pygame.time.get_ticks() - self.escudo_timer > 2000:
            self.escudo = False

        if not self.hidden:
            # Ciclo de poderes
            if pygame.time.get_ticks() - self.powerup_timer > 5000:
                self.powerup_timer = pygame.time.get_ticks()
                self.powerup_level = (self.powerup_level % 3) + 1

            teclas = pygame.key.get_pressed()
            if teclas[CONTROLES['izquierda']] and self.rect.left > 0:
                self.rect.x -= self.vel_x
            if teclas[CONTROLES['derecha']] and self.rect.right < ANCHO:
                self.rect.x += self.vel_x
            if teclas[CONTROLES['disparo']]:
                self.disparar()

        # Si acaba de reaparecer, forzar el escudo activo antes de colisiones
        if reaparecido:
            self.escudo = True
            self.escudo_timer = pygame.time.get_ticks()

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
            all_sprites.add(Particula(self.rect.center))
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
        # --- Añadir la moneda al grupo de monedas si no está ---
        if self not in monedas:
            monedas.add(self)

class Bola(pygame.sprite.Sprite):
    def __init__(self, color, radio=20):
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
        if self.destrucciones >= 5:
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
        self.destrucciones += 1
        if self.destrucciones >= 5:
            # Crear monedas cuando la bola desaparece permanentemente
            for _ in range(random.randint(2, 4)):
                moneda = Moneda(self.rect.center)
                all_sprites.add(moneda)
            self.kill()
        else:
            # Crear moneda cuando la bola reaparece
            moneda = Moneda(self.rect.center)
            all_sprites.add(moneda)
            self.reaparecer()

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
        self.destrucciones += 1
        if self.destrucciones >= 5:
            # Crear monedas cuando la bola azul desaparece permanentemente
            for _ in range(random.randint(1, 3)):
                moneda = Moneda(self.rect.center)
                all_sprites.add(moneda)
            self.kill()
        else:
            # Crear moneda cuando la bola azul reaparece
            moneda = Moneda(self.rect.center)
            all_sprites.add(moneda)
            self.reaparecer()

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
        self.destrucciones += 1
        if self.destrucciones >= 5:
            self.kill()
        else:
            self.reaparecer()

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
        super().__init__(BLANCO, radio=22) # Color cambiado a blanco
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
                    self.destrucciones += 1
                    if self.destrucciones >= 5:
                        self.kill()
                    else:
                        self.reaparecer()
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

def show_game_over_screen():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "GAME OVER", 64, ANCHO / 2, ALTO / 4, ROJO)
    
    # Botón de "Volver a Jugar"
    button_rect = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 - 25, 200, 50)
    pygame.draw.rect(pantalla, VERDE, button_rect)
    dibujar_texto(pantalla, "Volver a Jugar", 24, ANCHO / 2, ALTO / 2 - 15, NEGRO)
    
    # Botón de "Volver al Menú"
    button_menu_rect = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 + 40, 200, 50)
    pygame.draw.rect(pantalla, AMARILLO, button_menu_rect)
    dibujar_texto(pantalla, "Volver al Menú", 24, ANCHO / 2, ALTO / 2 + 50, NEGRO)

    pygame.display.flip()
    esperando = True
    while esperando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(evento.pos):
                    return "jugar"  # Volver a jugar
                elif button_menu_rect.collidepoint(evento.pos):
                    return "menu"  # Volver al menú
    return "salir"

def show_victory_screen():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¡VICTORIA!", 64, ANCHO / 2, ALTO / 4, VERDE)
    dibujar_texto(pantalla, "¡Has destruido todas las bolas!", 32, ANCHO / 2, ALTO / 2 - 50, BLANCO)
    
    # Botón de "Volver a Jugar"
    button_rect = pygame.Rect(ANCHO / 2 - 100, ALTO / 2 + 25, 200, 50)
    pygame.draw.rect(pantalla, VERDE, button_rect)
    dibujar_texto(pantalla, "Volver a Jugar", 24, ANCHO / 2, ALTO / 2 + 40, NEGRO)

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

def mostrar_pantalla_horda(numero_horda):
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, f"Horda {numero_horda}", 72, ANCHO // 2, ALTO // 2 - 50, CYAN)
    pygame.display.flip()
    pygame.time.delay(2000)  # Espera 2 segundos

def mostrar_vida_extra():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¡Vida extra!", 60, ANCHO // 2, ALTO // 2 - 30, VERDE)
    pygame.display.flip()
    pygame.time.delay(1200)

def mostrar_pantalla_bonus():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "¡NIVEL BONUS!", 72, ANCHO // 2, ALTO // 2 - 50, AMARILLO)
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
        dibujar_texto(pantalla, "INICIAR JUEGO", 24, ANCHO // 2, ALTO // 2 - 80, NEGRO)
        dibujar_texto(pantalla, "NIVELES INFINITOS", 20, ANCHO // 2, ALTO // 2 - 20, NEGRO)
        
        # Texto de los botones inferiores
        dibujar_texto(pantalla, "CONFIGURACIÓN", 20, 95, ALTO - 70, NEGRO)
        dibujar_texto(pantalla, "TIENDA", 24, ANCHO // 2, ALTO - 70, NEGRO)
        dibujar_texto(pantalla, "SALIR", 24, ANCHO - 95, ALTO - 70, NEGRO)
        
        pygame.display.flip()
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
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
    """Pantalla de configuración con opciones de controles"""
    global CONTROLES
    controles_originales = CONTROLES.copy()
    
    while True:
        pantalla.fill(NEGRO)
        
        dibujar_texto(pantalla, "CONFIGURACIÓN", 48, ANCHO // 2, ALTO // 4, AMARILLO)
        
        # Mostrar controles actuales
        dibujar_texto(pantalla, "Controles actuales:", 24, ANCHO // 2, ALTO // 2 - 80, BLANCO)
        dibujar_texto(pantalla, f"Izquierda: {pygame.key.name(CONTROLES['izquierda']).upper()}", 20, ANCHO // 2, ALTO // 2 - 50, VERDE)
        dibujar_texto(pantalla, f"Derecha: {pygame.key.name(CONTROLES['derecha']).upper()}", 20, ANCHO // 2, ALTO // 2 - 20, VERDE)
        dibujar_texto(pantalla, f"Disparo: {pygame.key.name(CONTROLES['disparo']).upper()}", 20, ANCHO // 2, ALTO // 2 + 10, VERDE)
        
        # Botones
        boton_flechas = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 50, 140, 40)
        boton_wasd = pygame.Rect(ANCHO // 2 + 10, ALTO // 2 + 50, 140, 40)
        boton_volver = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 120, 200, 50)
        
        # Dibujar botones
        pygame.draw.rect(pantalla, CYAN, boton_flechas)
        pygame.draw.rect(pantalla, CYAN, boton_wasd)
        pygame.draw.rect(pantalla, VERDE, boton_volver)
        
        # Texto de los botones
        dibujar_texto(pantalla, "FLECHAS", 18, ANCHO // 2 - 80, ALTO // 2 + 60, NEGRO)
        dibujar_texto(pantalla, "WASD", 18, ANCHO // 2 + 80, ALTO // 2 + 60, NEGRO)
        dibujar_texto(pantalla, "VOLVER", 24, ANCHO // 2, ALTO // 2 + 130, NEGRO)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
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
                elif boton_volver.collidepoint(evento.pos):
                    return "volver"
        
        clock.tick(FPS)

def mostrar_pantalla_tienda():
    """Pantalla de tienda del juego"""
    while True:
        pantalla.fill(NEGRO)
        
        # Título de la tienda
        dibujar_texto(pantalla, "TIENDA", 64, ANCHO // 2, ALTO // 4, AMARILLO)
        dibujar_texto(pantalla, "¡Próximamente más contenido!", 32, ANCHO // 2, ALTO // 2 - 50, CYAN)
        dibujar_texto(pantalla, "Mejoras, skins y power-ups", 24, ANCHO // 2, ALTO // 2, BLANCO)
        
        # Botón para volver al menú principal
        boton_volver = pygame.Rect(ANCHO // 2 - 100, ALTO - 100, 200, 50)
        pygame.draw.rect(pantalla, VERDE, boton_volver)
        dibujar_texto(pantalla, "VOLVER AL MENÚ", 24, ANCHO // 2, ALTO - 90, NEGRO)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            elif evento.type == pygame.MOUSEBUTTONUP:
                if boton_volver.collidepoint(evento.pos):
                    return "volver"
        
        clock.tick(FPS)

# Variables globales para controles
CONTROLES = {
    'izquierda': pygame.K_LEFT,
    'derecha': pygame.K_RIGHT,
    'disparo': pygame.K_SPACE
}

# Variables para guardado
ARCHIVO_GUARDADO = "guardado_infinito.json"

def serializar_enemigos():
    """Convierte el estado actual de los enemigos a formato JSON"""
    enemigos_data = []
    for enemigo in enemigos:
        enemigo_info = {
            'tipo': enemigo.__class__.__name__,
            'posicion': [enemigo.rect.x, enemigo.rect.y],
            'destrucciones': enemigo.destrucciones,
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
                return False
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
TOTAL_HORDAS = 5

def generar_horda(horda):
    """Genera bolas/enemigos según el número de horda."""
    if horda > 1:
        mostrar_pantalla_horda(horda)
    if horda == 1:
        for _ in range(3):
            b = BolaNegra()
            all_sprites.add(b)
            enemigos.add(b)
    elif horda == 2:
        for _ in range(4):
            b = BolaVerde()
            all_sprites.add(b)
            enemigos.add(b)
    elif horda == 3:
        for _ in range(4):
            b = BolaAzul()
            all_sprites.add(b)
            enemigos.add(b)
            bolas_azules.add(b)
    elif horda == 4:
        for _ in range(5):
            b = BolaRoja()
            all_sprites.add(b)
            enemigos.add(b)
    elif horda == 5:
        # Puedes modificar la cantidad o tipo de bolas por horda si lo deseas
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
    elif horda == 6:  # Nivel bonus
        for _ in range(3):
            b = BolaAzul()
            all_sprites.add(b)
            enemigos.add(b)
            bolas_azules.add(b)

def generar_horda_infinita(horda):
    """Genera bolas para niveles infinitos con dificultad creciente"""
    if horda > 1:
        mostrar_pantalla_horda(horda)
    
    # Dificultad creciente: más bolas según el número de horda
    num_bolas_verdes = min(3 + (horda // 3), 8)  # Máximo 8 bolas verdes
    num_bolas_rojas = min(2 + (horda // 2), 6)    # Máximo 6 bolas rojas
    num_bolas_negras = min(2 + (horda // 4), 5)   # Máximo 5 bolas negras
    num_bolas_azules = min(1 + (horda // 5), 4)   # Máximo 4 bolas azules
    
    for _ in range(num_bolas_verdes):
        b = BolaVerde()
        all_sprites.add(b)
        enemigos.add(b)
    
    for _ in range(num_bolas_rojas):
        b = BolaRoja()
        all_sprites.add(b)
        enemigos.add(b)
    
    for _ in range(num_bolas_negras):
        b = BolaNegra()
        all_sprites.add(b)
        enemigos.add(b)
    
    for _ in range(num_bolas_azules):
        b = BolaAzul()
        all_sprites.add(b)
        enemigos.add(b)
        bolas_azules.add(b)


def inicializar_juego(reset_horda=True):
    """Función para inicializar el juego y la primera horda"""
    global all_sprites, enemigos, bolas_azules, disparos_jugador, disparos_enemigos, jugador, jugador_mini_img, monedas, horda_actual, puntos
    all_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    bolas_azules = pygame.sprite.Group()
    disparos_jugador = pygame.sprite.Group()
    disparos_enemigos = pygame.sprite.Group()
    monedas = pygame.sprite.Group()
    if reset_horda:
        horda_actual = 1
        puntos = 0
    jugador = Jugador()
    jugador_mini_img = pygame.transform.scale(jugador.image_orig, (25, 5))
    jugador_mini_img.set_colorkey(NEGRO)
    all_sprites.add(jugador)
    if reset_horda:
        generar_horda(horda_actual)

# Inicializar el juego por primera vez
inicializar_juego()

# Reloj y Bucle principal
clock = pygame.time.Clock()
ejecutando_juego = True

# Pantalla de inicio
while ejecutando_juego:
    try:
        opcion = mostrar_pantalla_inicio()
        
        if opcion == "iniciar":
            # Iniciar el juego
            inicializar_juego()
            mostrar_pantalla_horda(horda_actual)
            game_over = False
            victory = False
            partida_en_curso = True
            while partida_en_curso:
                if game_over:
                    if show_game_over_screen() == "jugar":
                        # Reiniciar el juego
                        inicializar_juego()
                        mostrar_pantalla_horda(horda_actual)
                        partida_en_curso = False
                    elif show_game_over_screen() == "menu":
                        # Volver al menú principal
                        partida_en_curso = False
                    else:
                        partida_en_curso = False
                        ejecutando_juego = False
                elif victory:
                    if show_victory_screen():
                        # Reiniciar el juego
                        inicializar_juego()
                        mostrar_pantalla_horda(horda_actual)
                        partida_en_curso = False
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
                    # Hacer que las bolas disparen
                    for bola in enemigos:
                        if hasattr(bola, 'disparar'):
                            bola.disparar()

                    # Colisión: Disparos del jugador vs enemigos
                    golpeados = pygame.sprite.groupcollide(enemigos, disparos_jugador, False, True)
                    for enemigo in golpeados:
                        enemigo.on_hit()

                    # Colisión: Enemigos o sus disparos vs jugador
                    if not jugador.hidden:
                        if not jugador.escudo:
                            # Disparos enemigos vs jugador
                            impactos_disparos = pygame.sprite.spritecollide(jugador, disparos_enemigos, False)
                            for impacto in impactos_disparos:
                                if hasattr(impacto, 'explotar'): 
                                    impacto.explotar()
                                else: 
                                    impacto.kill()
                                jugador.hide()
                            # Bola azul vs jugador
                            colisiones_bola_azul = pygame.sprite.spritecollide(jugador, bolas_azules, False)
                            if colisiones_bola_azul:
                                jugador.hide()
                                for bola in colisiones_bola_azul:
                                    bola.on_hit()
                        else:
                            # Si tiene escudo, ignora cualquier daño
                            pass
                    # --- Colisión: Jugador recolecta monedas ---
                    monedas_recolectadas = pygame.sprite.spritecollide(jugador, monedas, True)
                    for moneda in monedas_recolectadas:
                        puntos += 10  # Sumar 10 puntos por cada moneda
                    # Verificar condiciones de fin de juego
                    if jugador.vidas == 0 and not jugador.hidden:
                        game_over = True
                    elif len(enemigos) == 0:
                        if horda_actual < TOTAL_HORDAS:
                            horda_actual += 1
                            jugador.vidas += 1  # Dar una vida extra al avanzar de horda
                            mostrar_vida_extra()
                            generar_horda(horda_actual)
                        elif horda_actual == TOTAL_HORDAS:
                            horda_actual += 1
                            jugador.vidas += 3  # Dar 3 vidas extra en el nivel bonus
                            mostrar_pantalla_bonus()
                            generar_horda(horda_actual)
                        else:
                            victory = True

                    # Dibujar todo
                    pantalla.fill(NEGRO)
                    all_sprites.draw(pantalla)
                    # Dibujar escudo si está activo
                    if jugador.escudo and not jugador.hidden:
                        # Escudo más notorio: círculo grueso y efecto de brillo
                        escudo_rect = jugador.rect.inflate(30, 30)
                        pygame.draw.ellipse(pantalla, CYAN, escudo_rect, 6)
                        for i in range(3):
                            color_brillo = (0, 255, 255, 80 - i*25)
                            s = pygame.Surface((escudo_rect.width+10, escudo_rect.height+10), pygame.SRCALPHA)
                            pygame.draw.ellipse(s, color_brillo, s.get_rect(), 6-i*2)
                            pantalla.blit(s, (escudo_rect.x-5, escudo_rect.y-5))
                    # HUD
                    dibujar_vidas_jugador(pantalla, ANCHO - 100, 10, jugador.vidas, jugador_mini_img)
                    powerup_text = "Poder: Ninguno"
                    if jugador.powerup_level == 1:
                        powerup_text = "Poder: Doble Disparo"
                    elif jugador.powerup_level == 2:
                        powerup_text = "Poder: Doble Daño"
                    elif jugador.powerup_level == 3:
                        powerup_text = "Poder: Triple Disparo"
                    dibujar_texto(pantalla, powerup_text, 18, ANCHO / 2, 10)
                    # Mostrar puntos en pantalla
                    dibujar_texto(pantalla, f"Puntos: {puntos}", 22, 90, 10, AMARILLO)
                    # Mostrar número de horda
                    dibujar_texto(pantalla, f"Horda: {horda_actual}/{TOTAL_HORDAS}", 22, ANCHO - 120, 40, CYAN)
                    pygame.display.flip()
        
        elif opcion == "infinito":
            # Mostrar pantalla de guardado/continuar
            opcion_infinito = mostrar_pantalla_guardado_infinito()
            
            if opcion_infinito == "nuevo":
                # Iniciar nuevo juego infinito
                inicializar_juego()
                mostrar_pantalla_horda(horda_actual)
                game_over = False
                partida_en_curso = True
            elif opcion_infinito == "continuar":
                # Cargar progreso guardado
                progreso = cargar_progreso_infinito()
                if progreso:
                    # Asignar los valores del progreso globalmente
                    horda_actual = progreso['horda']
                    puntos = progreso['puntos']
                    # Inicializar sin resetear la horda
                    inicializar_juego(reset_horda=False)
                    # Configurar las vidas del jugador
                    jugador.vidas = progreso['vidas']
                    # Recrear los enemigos exactos que se guardaron
                    if 'enemigos' in progreso and progreso['enemigos']:
                        recrear_enemigos(progreso['enemigos'])
                    else:
                        # Si no hay datos de enemigos (guardado antiguo), generar horda normal
                        generar_horda_infinita(horda_actual)
                    mostrar_pantalla_horda(horda_actual)
                    game_over = False
                    partida_en_curso = True
                else:
                    # Si no hay progreso, iniciar nuevo
                    inicializar_juego()
                    mostrar_pantalla_horda(horda_actual)
                    game_over = False
                    partida_en_curso = True
            elif opcion_infinito == "volver":
                continue
            elif opcion_infinito == "salir":
                ejecutando_juego = False
                break
            
            # Bucle del juego infinito
            while partida_en_curso:
                if game_over:
                    if show_game_over_screen() == "jugar":
                        # Reiniciar el juego
                        inicializar_juego()
                        mostrar_pantalla_horda(horda_actual)
                        partida_en_curso = False
                    elif show_game_over_screen() == "menu":
                        # Volver al menú principal
                        partida_en_curso = False
                    else:
                        partida_en_curso = False
                        ejecutando_juego = False
                else:
                    clock.tick(FPS)
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            # Guardar progreso automáticamente al cerrar el juego
                            guardar_progreso_infinito(horda_actual, puntos, jugador.vidas)
                            partida_en_curso = False
                            ejecutando_juego = False
                        elif evento.type == pygame.MOUSEBUTTONUP:
                            # Verificar si se hizo clic en el botón de salir
                            boton_salir = pygame.Rect(220, 5, 80, 30)
                            if boton_salir.collidepoint(evento.pos):
                                # Guardar progreso automáticamente al salir
                                guardar_progreso_infinito(horda_actual, puntos, jugador.vidas)
                                partida_en_curso = False
                            # Verificar si se hizo clic en el botón de guardar
                            boton_guardar = pygame.Rect(310, 5, 80, 30)
                            if boton_guardar.collidepoint(evento.pos):
                                if mostrar_pantalla_guardar():
                                    guardar_progreso_infinito(horda_actual, puntos, jugador.vidas)

                    all_sprites.update()
                    # Hacer que las bolas disparen
                    for bola in enemigos:
                        if hasattr(bola, 'disparar'):
                            bola.disparar()

                    # Colisión: Disparos del jugador vs enemigos
                    golpeados = pygame.sprite.groupcollide(enemigos, disparos_jugador, False, True)
                    for enemigo in golpeados:
                        enemigo.on_hit()

                    # Colisión: Enemigos o sus disparos vs jugador
                    if not jugador.hidden:
                        if not jugador.escudo:
                            # Disparos enemigos vs jugador
                            impactos_disparos = pygame.sprite.spritecollide(jugador, disparos_enemigos, False)
                            for impacto in impactos_disparos:
                                if hasattr(impacto, 'explotar'): 
                                    impacto.explotar()
                                else: 
                                    impacto.kill()
                                jugador.hide()
                            # Bola azul vs jugador
                            colisiones_bola_azul = pygame.sprite.spritecollide(jugador, bolas_azules, False)
                            if colisiones_bola_azul:
                                jugador.hide()
                                for bola in colisiones_bola_azul:
                                    bola.on_hit()
                        else:
                            # Si tiene escudo, ignora cualquier daño
                            pass
                    # --- Colisión: Jugador recolecta monedas ---
                    monedas_recolectadas = pygame.sprite.spritecollide(jugador, monedas, True)
                    for moneda in monedas_recolectadas:
                        puntos += 10  # Sumar 10 puntos por cada moneda
                    # Verificar condiciones de fin de juego
                    if jugador.vidas == 0 and not jugador.hidden:
                        game_over = True
                    elif len(enemigos) == 0:
                        # En modo infinito, siempre avanzar a la siguiente horda
                        horda_actual += 1
                        jugador.vidas += 1  # Dar una vida extra al avanzar de horda
                        # Guardar progreso automáticamente al avanzar de horda
                        guardar_progreso_infinito(horda_actual, puntos, jugador.vidas)
                        mostrar_vida_extra()
                        generar_horda_infinita(horda_actual)

                    # Dibujar todo
                    pantalla.fill(NEGRO)
                    all_sprites.draw(pantalla)
                    # Dibujar escudo si está activo
                    if jugador.escudo and not jugador.hidden:
                        # Escudo más notorio: círculo grueso y efecto de brillo
                        escudo_rect = jugador.rect.inflate(30, 30)
                        pygame.draw.ellipse(pantalla, CYAN, escudo_rect, 6)
                        for i in range(3):
                            color_brillo = (0, 255, 255, 80 - i*25)
                            s = pygame.Surface((escudo_rect.width+10, escudo_rect.height+10), pygame.SRCALPHA)
                            pygame.draw.ellipse(s, color_brillo, s.get_rect(), 6-i*2)
                            pantalla.blit(s, (escudo_rect.x-5, escudo_rect.y-5))
                    # HUD
                    dibujar_vidas_jugador(pantalla, ANCHO - 100, 10, jugador.vidas, jugador_mini_img)
                    powerup_text = "Poder: Ninguno"
                    if jugador.powerup_level == 1:
                        powerup_text = "Poder: Doble Disparo"
                    elif jugador.powerup_level == 2:
                        powerup_text = "Poder: Doble Daño"
                    elif jugador.powerup_level == 3:
                        powerup_text = "Poder: Triple Disparo"
                    dibujar_texto(pantalla, powerup_text, 18, ANCHO / 2, 10)
                    # Mostrar puntos en pantalla
                    dibujar_texto(pantalla, f"Puntos: {puntos}", 22, 90, 10, AMARILLO)
                    # Botón de salir a la izquierda del botón guardar
                    boton_salir = pygame.Rect(220, 5, 80, 30)
                    pygame.draw.rect(pantalla, ROJO, boton_salir)
                    dibujar_texto(pantalla, "SALIR", 16, 260, 10, BLANCO)
                    # Botón de guardar al lado del botón salir
                    boton_guardar = pygame.Rect(310, 5, 80, 30)
                    pygame.draw.rect(pantalla, VERDE, boton_guardar)
                    dibujar_texto(pantalla, "GUARDAR", 16, 350, 10, NEGRO)
                    # Mostrar número de horda (infinito)
                    dibujar_texto(pantalla, f"Horda: {horda_actual} (∞)", 22, ANCHO - 120, 40, MAGENTA)
                    
                    pygame.display.flip()
        
        elif opcion == "configuracion":
            # Mostrar pantalla de configuración
            config_opcion = mostrar_pantalla_configuracion()
            if config_opcion == "salir":
                ejecutando_juego = False
        
        elif opcion == "tienda":
            # Mostrar pantalla de tienda (por ahora solo muestra un mensaje)
            mostrar_pantalla_tienda()
        
        elif opcion == "salir":
            ejecutando_juego = False
    except Exception as e:
        print(f"Error en el juego: {e}")
        ejecutando_juego = False

pygame.quit()
sys.exit()