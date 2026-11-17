# Herramientas

## Compilar el documento

```sh
herramientas/compilar.sh
```

Genera `latex/build/main.pdf` a partir de `documentacion/`.

| Opción | Efecto |
| --- | --- |
| `--con-pendientes` | Incluye también los puntos sin respuesta, con la leyenda "Pendiente" |
| `--solo-latex` | Regenera `latex/generado/` sin compilar |
| `--limpiar` | Borra `latex/build/` |

Requiere `pandoc`, `xelatex` y `latexmk` (en Arch: `pandoc-cli` y los paquetes `texlive-*` instalados).

## Cómo funciona

1. De cada `.md` de `documentacion/` se toma **solo la sección `## Respuesta`**. El título del punto sale del frontmatter (`punto` y `titulo`).
2. Los puntos con `estado: pendiente` o sin respuesta se omiten, salvo con `--con-pendientes`. La ficha de seguimiento y la descripción del documento siempre se incluyen.
3. Los archivos que empiezan con `_` (guías, relevamientos) no se compilan.
   - **Casos de uso:** cada uno es un archivo `10 - Solución Tecnológica/casos-de-uso/CU-*.md`. Los que no están pendientes se agregan debajo de 10.5.3, ordenados por ID, con el título armado desde `id` y `nombre` del frontmatter. El índice de 10.5.2 (identificación, nombre y página) se genera solo con esos mismos archivos.
4. La carátula se arma con la tabla de `00 - Preliminares/Carátula.md`.
5. La conversión de Markdown a LaTeX la hace pandoc con los filtros de `herramientas/latex/`:
   - `respuesta.lua`: extrae la respuesta;
   - `caratula.lua`: arma la carátula.
6. Los títulos de los capítulos y de los subtítulos intermedios (2.1, 6.4, etc.) están definidos en `compilar.sh`.
7. `latex/main.tex` es la plantilla con el formato de la consigna: títulos en Arial Bold 14/13/11, cuerpo en Arial 11 justificado, encabezado con el logo, el proyecto y el autor, y pie "Página N de M". Si Arial no está instalada se usa Liberation Sans, que tiene las mismas métricas (`paru -S ttf-ms-fonts` instala Arial).
8. `latex/generado/` se regenera en cada compilación: no editarlo a mano.
9. **Citas en APA 7:** las fuentes están en el frontmatter de `documentacion/_Referencias.md` y se citan con `[@clave]` en las secciones Respuesta. El contenido se convierte en un solo paso con `pandoc --citeproc` y el estilo `herramientas/latex/apa.csl` (oficial de CSL); la lista de referencias se arma sola en 11.3 con las fuentes citadas. Si una cita no existe en `_Referencias.md`, la compilación falla y la muestra.

## Consejos para escribir en los `.md`

- **Imágenes:** guardarlas en `documentacion/imagenes/` y referenciarlas con `![Descripción](../imagenes/archivo.png)`.
- **Figuras apaisadas:** agregar `{.apaisada}` después de la imagen (`![Descripción](../imagenes/diagramas/x.svg){.apaisada}`) la ubica sola en una página, rotada 90°. Conviene para diagramas mucho más anchos que altos (lo resuelve `herramientas/latex/figuras.lua`).
- **Diagramas:** las fuentes PlantUML están en `documentacion/imagenes/diagramas/*.puml` e incluyen `_estilo.iuml`. `herramientas/diagramas.sh` genera el SVG (para Obsidian) y el PDF (para LaTeX); en el `.md` se enlaza el SVG. Para que el texto se lea en A4, cada diagrama no debería pasar de unos 900 px de ancho.
- **Ancho de las columnas de una tabla:** se controla con la cantidad de guiones de la línea separadora. Por ejemplo, `| ---------- | ------------------------------ |` da una columna angosta y otra ancha. Obsidian lo ignora al mostrar. Pandoc solo usa esos anchos si alguna línea de la tabla supera los 72 caracteres (si no, alargar la línea separadora manteniendo la proporción) y, además, los reajusta según el contenido. Para que se respete la proporción exacta, agregar `anchos_exactos: true` al frontmatter del punto; los casos de uso ya lo tienen activado.

## Plane (gestión de tareas)

`herramientas/plane.py` conecta con el Plane del proyecto (plane.atwire.net) para leer el proyecto y administrar work items. Solo necesita Python 3; si está `pandoc`, las descripciones y comentarios se escriben y se leen en Markdown.

**Configuración:** copiar `herramientas/plane.env.ejemplo` como `herramientas/plane.env` (está en `.gitignore`) y completar el token, el workspace y el proyecto. Probar con `herramientas/plane.py yo`.

| Comando | Efecto |
| --- | --- |
| `proyecto` | Resumen: estados, etiquetas, miembros, ciclos y módulos |
| `items [--abiertos] [--estado X] [--asignado yo] [--etiqueta X] [--buscar texto] ...` | Lista work items |
| `ver QE-12` | Muestra un work item con descripción y comentarios |
| `crear "Título" [--descripcion md] [--estado X] [--prioridad high] [--etiqueta X] [--asignado yo] [--vence AAAA-MM-DD]` | Crea un work item |
| `editar QE-12 [--titulo] [--estado] [--etiqueta] [--quitar-etiqueta] ...` | Modifica un work item |
| `comentar QE-12 "texto"` | Agrega un comentario |
| `borrar QE-12 --confirmar` | Borra un work item |
| `api GET '{proyecto}/work-items/'` | Pedido crudo a la API para lo que no cubren los otros comandos |

- Estados, etiquetas, miembros, ciclos y módulos se indican **por nombre** (no hace falta el UUID).
- `--json` devuelve la respuesta cruda de la API; `--proyecto` cambia el proyecto por defecto.
- En `--descripcion` y en `comentar`, `-` lee de stdin y `@archivo.md` lee un archivo.
- Cada comando tiene su ayuda: `herramientas/plane.py <comando> --help`.
