# Tienda del Juego "Destruye las Bolas"

## 🎮 Funcionalidades de la Tienda

La tienda del juego permite a los jugadores comprar objetos y mejoras usando las monedas que recolectan durante el juego.

## 🎯 Características del Juego

### Enemigos Profesionales
- **Tamaño Aumentado**: Los enemigos ahora tienen un tamaño de 60x60 píxeles para una apariencia más profesional
- **Imágenes Optimizadas**: Sprites de aliens redimensionados para mejor visibilidad
- **Colisiones Mejoradas**: Hitboxes más precisas y visibles

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

---

¡Disfruta comprando mejoras y haciendo tu juego más divertido! 🎉
