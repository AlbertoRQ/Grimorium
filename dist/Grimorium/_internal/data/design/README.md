# Contenido de Grimorium

`grimorium_content.xlsx` es la fuente maestra editable de la tienda. El juego
no abre el Excel: carga los JSON generados de `data/game/` y las traducciones
de `data/lang/`.

## Flujo de trabajo

1. Edita el Excel. No cambies los nombres de las hojas ni de las columnas.
2. Instala las dependencias con `py -m pip install -r requirements.txt`.
3. Ejecuta `py tools/export_content.py` desde la raiz del proyecto.
4. Corrige todos los errores que muestre el validador.
5. Ejecuta el juego normalmente.

Para validar sin sobrescribir los JSON usa:

```powershell
py tools/export_content.py --check
```

## Hojas

- `Dashboard`: resumen automatico del contenido activo y en borrador.
- `Items`: identidad, categoria, precio, asset, texto y activacion.
- `Effects`: cambios numericos o booleanos aplicados por cada objeto.
- `Requirements`: poderes necesarios para que aparezca cada libro.
- `Texts`: nombres y descripciones cortas en español e ingles.
- `Detail Lines`: lineas ordenadas de los tooltips detallados.
- `Assets`: inventario de imagenes usadas, borradores y huerfanas.
- `Balance`: vista calculada para comparar precios, efectos y requisitos.

Una fila con `enabled = FALSE` se conserva como borrador, pero el juego no la
carga. Actualmente `luck` y `electric_poison` estan documentados asi porque sus
assets llevan `_` y no formaban parte efectiva de la tienda.
