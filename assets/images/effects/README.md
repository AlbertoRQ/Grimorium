# Diseños base de efectos

El juego carga estos 12 PNG directamente. Para cambiar el dibujo, edita el PNG
de esta carpeta y reinicia el juego (las imágenes se guardan en caché).
Usa fondo transparente y conserva el nombre y las dimensiones del lienzo.
Los originales de `artifacts/disenos_base` ya no son la fuente del juego.

| PNG | Uso |
| --- | --- |
| 01_calavera_pequena.png | Cada acumulación de veneno |
| 02_calavera_huesos.png | Marca de cinco acumulaciones |
| 03_cristal_fragil.png | Marca frágil normal |
| 04_cristal_plus.png | Marca frágil plus, incluido su halo |
| 05_llamas.png | Cuatro variantes de llama de quemadura |
| 06_hielo_1.png | Congelación: un pico |
| 07_hielo_2.png | Congelación: dos picos |
| 08_hielo_3.png | Congelación: picos desiguales |
| 10_charco.png | Agua del charco de hielo |
| 13_estaca.png | Estaca del combo hielo-fuego; dibujada hacia la derecha |
| 14_roca_lava.png | Tres estados de calentamiento de Fragmentación voltaica |
| 15_piedra_brasa.png | Fragmentos finales y partículas de roca incandescente |

Las tiras se leen de izquierda a derecha, con coordenadas desde cero:

- Llamas: lienzo de 38 × 7; cuatro celdas de 5 × 7 en x = 0, 11, 22 y 33.
- Lava: lienzo de 51 × 14; celdas de 11 × 14 en x = 0, y de 14 × 14
  en x = 17 y 37. Orden: rojo, naranja, amarillo. Conserva los huecos transparentes.

El hielo conserva el ajuste al área pintada del enemigo y alterna sus tres diseños.
Las imágenes se escalan sin suavizado. Movimiento, desvanecimiento, rotación,
destellos y arcos eléctricos siguen animándose por código; el diseño base sale
del PNG. Los efectos sin PNG en esta entrega conservan su dibujo actual.

La carga y las celdas de las tiras están en `src/game/visuals/effect_images.py`.
