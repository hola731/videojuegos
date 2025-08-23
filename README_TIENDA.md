# Tienda del Juego "Destruye las Bolas"

## 🎮 Funcionalidades de la Tienda

La tienda del juego permite a los jugadores comprar objetos y mejoras usando las monedas que recolectan durante el juego.

## 🎯 Sistema de Hordas

### Hordas Normales (1-6)
- **Horda 1**: 3 Bolas Negras
- **Horda 2**: 4 Bolas Verdes
- **Horda 3**: 4 Bolas Azules
- **Horda 4**: 5 Bolas Rojas
- **Horda 5**: Mezcla de todas las bolas anteriores
- **Horda 6**: Nivel Bonus con 3 Bolas Azules

### Horda 7 (Nuevas Bolas)
- **2 Bolas Moradas**: Con teletransporte automático
- **2 Bolas Naranjas**: Con disparo de 3 rayos láser
- **2 Bolas Grises**: Con división en bolas pequeñas

### Modo Infinito
- **Dificultad Creciente**: Más enemigos según el número de horda
- **Nuevas Bolas**: Aparecen progresivamente en hordas avanzadas
- **Máximos**: Hasta 8 verdes, 6 rojas, 5 negras, 4 azules, 3 moradas, 3 naranjas, 3 grises

## 🎯 Características del Juego

### Enemigos Profesionales
- **Tamaño Aumentado**: Los enemigos ahora tienen un tamaño de 60x60 píxeles para una apariencia más profesional
- **Imágenes Optimizadas**: Sprites de aliens redimensionados para mejor visibilidad
- **Colisiones Mejoradas**: Hitboxes más precisas y visibles

### Nuevas Bolas Enemigas
- **Bola Morada/Rosa**: Se teletransporta automáticamente cada 4 segundos
- **Bola Naranja**: Dispara 3 rayos láser pequeños en diferentes direcciones (permanece quieta)
- **Bola Gris**: Se mueve en diagonal y al destruirse crea 3 bolas pequeñas
- **Bola Pequeña**: Bolas grises pequeñas que mueren con un solo golpe y tienen 8 segundos de vida

### Jugador Mejorado
- **Tamaño Aumentado**: La nave del jugador ahora es de 70x15 píxeles para mejor visibilidad
- **Proporciones Optimizadas**: Mejor balance visual entre jugador y enemigos

## 💰 Sistema de Monedas

- **Recolección**: Las monedas se obtienen al destruir bolas verdes y azules
- **Almacenamiento**: Las monedas se guardan automáticamente en `monedas_globales.json`
- **Persistencia**: Las monedas se mantienen entre sesiones de juego

## 🛍️ Objetos y Poderes Disponibles

### 📦 **OBJETOS** (Efectos inmediatos y defensivos)

#### 1. Vida Extra
- **Precio**: 50 monedas
- **Efecto**: Añade una vida extra al jugador
- **Tipo**: Permanente

#### 2. Escudo Temporal
- **Precio**: 75 monedas
- **Efecto**: Escudo que protege por 10 segundos
- **Tipo**: Temporal
- **Indicador**: Muestra tiempo restante en pantalla

### ⚡ **PODERES** (Mejoras de combate y bonificaciones)

#### 3. Doble Disparo
- **Precio**: 100 monedas
- **Efecto**: Dispara dos balas simultáneamente
- **Tipo**: Permanente hasta que se pierda

#### 4. Triple Disparo
- **Precio**: 200 monedas
- **Efecto**: Dispara tres balas simultáneamente
- **Tipo**: Permanente hasta que se pierda

#### 5. Velocidad de Disparo
- **Precio**: 150 monedas
- **Efecto**: Aumenta la velocidad de disparo
- **Tipo**: Permanente

#### 6. Doble Puntos
- **Precio**: 300 monedas
- **Efecto**: Duplica los puntos por 30 segundos
- **Tipo**: Temporal
- **Indicador**: Muestra tiempo restante en pantalla

## 🎯 Cómo Usar la Tienda

1. **Acceder**: Selecciona "TIENDA" en el menú principal
2. **Navegar**: Usa los botones de flecha o la rueda del mouse para desplazarte
3. **Comprar**: Haz clic en "COMPRAR" en el objeto deseado
4. **Confirmación**: Se muestra un mensaje de compra exitosa
5. **Volver**: Usa "VOLVER AL MENÚ" para regresar

## 🎨 Interfaz de la Tienda

- **Título**: "TIENDA" en amarillo (centro superior)
- **Monedas**: Muestra las monedas disponibles del jugador (esquina superior derecha)
- **Botón Volver**: "VOLVER AL MENÚ" ubicado en la esquina superior izquierda
- **Secciones Separadas**:
  - **OBJETOS** (en cyan): Efectos inmediatos y defensivos
  - **PODERES** (en magenta): Mejoras de combate y bonificaciones
- **Cada Item**: 
  - Nombre y descripción (texto centrado)
  - Precio en monedas
  - Botón de compra (solo si tienes suficientes monedas)
- **Diseño**: 
  - Cuadros compactos de 70px de altura
  - Espaciado optimizado entre elementos
  - Texto centrado para mejor legibilidad
  - Separación visual clara entre categorías
- **Colores**: 
  - Verde: Puedes comprar
  - Gris: No tienes suficientes monedas
- **Navegación**: Botones de flecha para desplazarte

## 🔧 Mejoras Técnicas

### Sistema de Mejoras Temporales
- **Doble Puntos**: Se activa por 30 segundos
- **Escudo Temporal**: Se activa por 10 segundos
- **Indicadores Visuales**: Muestran tiempo restante en pantalla

### Sistema de Dificultad
- **Dificultad Difícil**: Los enemigos disparan 0.5 segundos más rápido
- **Resistencia Aumentada**: Los enemigos soportan 1-2 golpes extra
- **Balance de Juego**: Mayor desafío manteniendo la jugabilidad

### Integración con el Juego
- **Aplicación Automática**: Las mejoras se aplican inmediatamente
- **Persistencia**: Las mejoras permanentes se mantienen
- **Compatibilidad**: Funciona en modo normal e infinito

## 📁 Archivos del Sistema

- `proyecto_de_pigame.py`: Juego principal con tienda integrada
- `monedas_globales.json`: Almacena las monedas del jugador
- `guardado_infinito.json`: Guarda el progreso del modo infinito

## ⚙️ Configuración del Juego

### Controles
- **FLECHAS**: Usar teclas de dirección para movimiento
- **WASD**: Usar teclas WASD para movimiento
- **ESPACIO**: Disparar

### Dificultad
- **Acceso**: Presiona el botón "DIFICULTAD →" en la pantalla de configuración
- **Opciones**:
  - **FÁCIL**: Para principiantes
  - **NORMAL**: Dificultad estándar
      - **DIFÍCIL**: Para jugadores experimentados
      - **Enemigos Resistentes**: Soportan 1-2 golpes extra
      - **Disparo Acelerado**: Los enemigos disparan 0.5 segundos más rápido
      - **Mayor Desafío**: Requiere más precisión y estrategia
- **Navegación**: Pantalla separada con descripción de cada nivel

## 🎮 Consejos de Uso

1. **Prioriza**: Compra vidas extra cuando estés en dificultad
2. **Estrategia**: Usa doble puntos en momentos de alta actividad
3. **Protección**: El escudo temporal es útil en situaciones difíciles
4. **Ahorro**: Guarda monedas para mejoras más costosas

## 🚀 Futuras Mejoras

- Más tipos de objetos y mejoras
- Sistema de descuentos y ofertas
- Logros y recompensas especiales
- Personalización de personajes
- Power-ups únicos

## 🎯 Nuevas Bolas Enemigas

### 🔮 Bola Morada/Rosa
- **Color**: Magenta/Morado
- **Habilidad**: Teletransporte automático cada 4 segundos
- **Comportamiento**: Se mueve aleatoriamente por la pantalla
- **Disparo**: Proyectiles explosivos morados
- **Estrategia**: Difícil de predecir debido al teletransporte

### 🟠 Bola Naranja
- **Color**: Naranja
- **Habilidad**: Dispara 3 rayos láser pequeños consecutivamente
- **Comportamiento**: Se mueve horizontalmente de izquierda a derecha
- **Patrón de Disparo**: 
  - Rayo 1: Hacia abajo (0°)
  - Rayo 2: Diagonal (45°)
  - Rayo 3: Hacia la derecha (90°)
- **Teletransporte**: Se teletransporta cada 5 segundos si no es destruida
- **Estrategia**: Evitar estar en las líneas de fuego y predecir su movimiento

### ⚫ Bola Gris
- **Color**: Gris
- **Habilidad**: Se divide en 3 bolas pequeñas al destruirse
- **Comportamiento**: Movimiento diagonal con rebote en bordes
- **Disparo**: Proyectiles explosivos grises
- **Bolas Pequeñas**:
  - Tamaño: 15x15 píxeles
  - Vida: 1 golpe
  - Duración: 8 segundos
  - Movimiento: Aleatorio con rebote

### 🎮 Consejos para las Nuevas Bolas
1. **Bola Morada**: Mantén distancia y espera que aparezca cerca
2. **Bola Naranja**: Identifica las direcciones de los rayos y evítalos, ten en cuenta su movimiento horizontal
3. **Bola Gris**: Destrúyela en una esquina para limitar el movimiento de las bolas pequeñas
4. **Bolas Pequeñas**: Prioriza eliminarlas rápidamente antes de que se dispersen

---

¡Disfruta comprando mejoras y haciendo tu juego más divertido! 🎉
