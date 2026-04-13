1. **Inicialización de la Aplicación:**
   - Se crea una ventana principal con un tamaño de 600x400 píxeles.
   - Se agrega un área de dibujo (`Canvas`) en el que se mostrarán los aviones.

2. **Creación y Movimiento de Aviones:**
   - La función `create_enemy` crea aviones aleatorios con colores rojos.
   - La función `move_enemies` mueve aleatoriamente los aviones dentro del área del radar.

3. **Animación Continua:**
   - La función `animate` se encarga de llamar a `move_enemies` y actualizar la pantalla cada 50 milisegundos.

4. **Función de Disparo:**
   - La función `shoot` detecta si el clic del usuario está cerca de un avión, lo elimina y muestra una
ventana emergente indicando el impacto.

Este es un ejemplo básico que puedes expandir para añadir más características, como diferentes tipos de
aviones, sonidos efectivos, o mejor control del movimiento de los aviones.