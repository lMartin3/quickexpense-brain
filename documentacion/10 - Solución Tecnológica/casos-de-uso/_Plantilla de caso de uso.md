---
id: "CU-CCC-XXX"
nombre: ""
componente: ""
core: false
estado: pendiente
---

<!--
Plantilla: copiá este archivo como `CU-CCC-XXX Nombre.md` para cada caso de uso.
Combina los campos de la consigna (10.5.3.1 a 10.5.3.14) con el formato de ficha en tabla del trabajo de 3.er año.
Los textos entre corchetes son guías; reemplazalos por el contenido.

Convenciones:
- ID: CU-CCC-XXX (CCC = número de componente, XXX = número de caso de uso dentro del componente).
- Requerimientos: los ID de 10.4.2 (RF-XX / RNF-XX) que cubre el caso de uso.
- Actores en los pasos: "Usuario", "Sistema" (incluye al asistente de IA, que es parte de la solución) y, cuando intervienen, los
  servicios externos por su nombre ("Telegram", "API de Anthropic", "API de transcripción", "API del IPC").
- El escenario principal describe qué hace cada actor, no cómo lo resuelve el sistema por dentro (consigna 10.5.3.12).
- Caminos alternativos: se numeran con el paso donde se desvían y una letra (4.a, 4.b...). Sus pasos siguen como 4.a.1, 4.a.2...
  El último paso indica cómo termina: "Vuelve al paso N" o "Fin del caso de uso". Los errores también van acá.
- La cantidad de guiones de la fila separadora fija el ancho relativo de cada columna en el PDF: no la cambies.
- En las tablas, cada celda es una sola línea: para enumerar dentro de una celda, separá con punto y coma.
- Solo se compila lo que está debajo de "## Respuesta". El título se arma con `id` y `nombre` del frontmatter.
- Imágenes: en `documentacion/imagenes/`, enlazadas con la ruta relativa `../../imagenes/...` (al compilar se buscan por nombre).
-->

# CU-CCC-XXX Nombre

## Notas internas

- [Ideas, dudas, referencias al código (clases, endpoints) y decisiones pendientes. No se compila.]

## Respuesta

<!-- Todo lo que esté debajo de este título es el texto que se compila al documento final. El título del caso de uso se arma con `id` y `nombre` del frontmatter. -->

**Historial de revisión de la especificación**

| Versión | Responsable | Descripción de la Revisión | Fecha |
| --- | --- | --- | --- |
| 1.0 | Martín Luraschi | Versión inicial | DD/MM/AAAA |

**Ficha del caso de uso**

| Campo | Detalle |
| ------ | ------------------ |
| Identificación | CU-CCC-XXX |
| Nombre | [Verbo en infinitivo + objeto, p. ej., "Registrar movimiento mediante el chatbot"] |
| Componente | [Nombre del componente] |
| Requerimientos | [RF-XX; RNF-XX] |
| Objetivo | [Los aspectos esperados: qué logra el usuario al terminar] |
| Descripción | [Visión del usuario, máximo 10 renglones; relacionada con la historia de usuario de 10.4.2] |
| Actores primarios | [Quién inicia el caso de uso y obtiene el resultado] |
| Actores secundarios | [Sistemas o personas que participan sin iniciarlo] |
| Evento disparador | [El evento que da comienzo al proceso] |
| Precondición | [Lo que debe cumplirse para iniciar] |
| Poscondición | [El estado en que queda el sistema al terminar con éxito] |
| Casos de uso relacionados | [«include»: CU-...; «extend»: CU-...; o "Ninguno"] |
| Puntos de extensión y condiciones | [Observaciones, condiciones y aclaraciones sobre los puntos anteriores] |
| Reglas de negocio | [Reglas del dominio que el caso de uso debe respetar; o "Ninguna"] |

**Escenario principal de éxito**

| N.° | Actor | Acción |
| -- | --- | ---------------- |
| 1 | Usuario | [...] |
| 2 | Sistema | [...] |
| 3 | Sistema | Fin del caso de uso. |

**Caminos alternativos**

*2.a · [Condición que desvía el escenario en el paso 2]*

| N.° | Actor | Acción |
| -- | --- | ---------------- |
| 2.a.1 | Sistema | [...] |
| 2.a.2 | Usuario | [...] |
| 2.a.3 | — | Vuelve al paso 2. |

**Prototipo de la interfaz de usuario**

[Captura de la pantalla o de la conversación, guardada en `imagenes/`:]

![CU-CCC-XXX · Nombre de la pantalla](../../imagenes/cu-ccc-xxx-pantalla.png)

[Para pantallas web, los datos del formulario:]

| Campo | Tipo | Obligatorio | Validación |
| --- | --- | --- | --- |
| [Monto] | [Número decimal] | [Sí] | [Mayor que cero] |

[Para el chatbot, en lugar de la tabla de campos, un ejemplo de conversación (mensaje del usuario y respuesta del sistema).]

[Criterios de usabilidad tenidos en cuenta, en una o dos oraciones.]
