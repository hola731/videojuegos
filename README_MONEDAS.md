# Monedas en el juego "Destruye las bolas"

## ¿Cómo funciona el código de las monedas?
Las monedas en el juego están implementadas como una clase llamada `Moneda`, que hereda de `pygame.sprite.Sprite`. Cada moneda es un sprite que se puede dibujar, mover y detectar colisiones con el jugador.

### Clase Moneda
```python
class Moneda(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Dibujar moneda dorada
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
        if self not in monedas:
            monedas.add(self)
```

## ¿Cómo se generan las monedas?
Las monedas se generan cuando destruyes bolas verdes (y a veces otras bolas). Esto ocurre en el método `on_hit` de la clase `BolaVerde`:

```python
class BolaVerde(Bola): #Esta linea de codigo es para crear una clase
    def on_hit(self):# Esta es una funcion 
        self.destrucciones += 1 #Este una es un atrubito 
        if self.destrucciones >= 5: #Este es una condicional
            # Crear varias monedas cuando la bola desaparece permanentemente
            for _ in range(random.randint(2, 4)): #Este es un arreglo
                moneda = Moneda(self.rect.center)# Es para incertar la moneda
                all_sprites.add(moneda) #Añade el sprite de la moneda
            self.kill() #Destruye la moneda
        else:
            # Crear una moneda cuando la bola reaparece
            moneda = Moneda(self.rect.center) #Es para incertar la moneda
            all_sprites.add(moneda)#Añade el sprite de la moneda
            self.reaparecer()# Esto hace que reaparezca la moneda
```

Cada vez que una bola verde es golpeada, se crea al menos una moneda en la posición donde estaba la bola. Si la bola desaparece definitivamente, pueden aparecer varias monedas.

## ¿Cómo se recolectan las monedas?
La recolección de monedas se realiza detectando la colisión entre el jugador y las monedas usando el siguiente código en el bucle principal del juego:

```python
# --- Colisión: Jugador recolecta monedas ---
monedas_recolectadas = pygame.sprite.spritecollide(jugador, monedas, True)
for moneda in monedas_recolectadas:
    # Aquí puedes sumar puntos, vidas, etc.
    pass
```

Cuando el jugador toca una moneda, esta desaparece del juego (gracias al argumento `True` en `spritecollide`). Puedes agregar lógica adicional dentro del bucle para sumar puntos, dar vidas, reproducir sonidos, etc.

---
Con este sistema, puedes personalizar fácilmente el comportamiento de las monedas y las recompensas al recolectarlas. ¡Experimenta y haz tu juego más divertido! 