---
capitulo: "Preliminares"
tipo: guia
---

# Formato del documento

Requisitos de formato que pide la consigna ("Aspectos comunes a considerar"). Este archivo **no** se compila: es la referencia para armar la plantilla LaTeX.

> [!quote] Consigna
> Esta plantilla está basada en los modelos sugeridos por MSF le permitirá homogenizar la estructura de su proyecto siguiendo un estándar. [...] Al comenzar la escritura de la carpeta borrar los párrafos entre [..].
> - Primera línea de la cabecera: Fuente Arial Bold 14.
> - Segunda línea de la cabecera: Fuente Arial Bold 13.
> - Tercera línea de la cabecera: Fuente Arial Bold 11.
>
> El cuerpo del documento debe estar justificado y utilizar la fuente Arial 11.
> La carátula de la carpeta debe respetar los títulos expuestas en la hoja anterior junto con el logo de la universidad, nombre del proyecto, apellido y nombre junto con el legajo y la localización donde cursa, fecha y nombre de los profesores.
>
> **Contenido del encabezado de página:** Debe contener el logo de la Universidad, el nombre del proyecto más el nombre y apellido del autor.
> **Contenido del Pie de página:** Número de página y número total de páginas.
>
> Los ANEXOS en los que incorporaremos el conjunto de la información ampliatoria [...] Es importante NO MEZCLAR el desarrollo de lo que es el Plan de Negocios en sí con información que naturalmente debería incluirse como anexo [...]

## Resumen para la plantilla LaTeX

| Elemento | Requisito |
| --- | --- |
| Título nivel 1 (`\section`) | Arial Bold 14 |
| Título nivel 2 (`\subsection`) | Arial Bold 13 |
| Título nivel 3 (`\subsubsection`) | Arial Bold 11 |
| Cuerpo | Arial 11, justificado |
| Encabezado | Logo UAI + nombre del proyecto + nombre y apellido del autor |
| Pie | "Página N de M" |
| Carátula | Logo, nombre del proyecto, apellido y nombre, legajo, sede, fecha, profesores |
| Anexos | Separados del cuerpo principal |

Además, la consigna pide **no** meter la "carpeta técnica" (planos, diagramas detallados) en el cuerpo del Plan de Negocios, sino presentarla como cuerpo separado. Hay que definir si el capítulo 10 se compila como documento aparte o como parte del mismo PDF.

## Imágenes disponibles

- `imagenes/logo-uai-escudo.png`: escudo, extraído de la carátula del Parcial.
- `imagenes/logo-uai.jpg`: logo horizontal, extraído del encabezado de la consigna.
