---
id: "CU-007-002"
nombre: "Consultar reporte mensual de gastos"
componente: "007 Reportes"
core: false
estado: pendiente
---

# CU-007-002 Consultar reporte mensual de gastos

## Notas internas

- No implementado: existe la clase `ExpenseReport`, sin uso (ya tiene la estructura del desglose: categoría de cuenta → categoría de movimiento, montos por moneda y "sin categoría" en ambos niveles).
- Decisiones del autor (17/11/2026):
  - **Qué es gasto:** las imputaciones (*postings*) a cuentas de tipo `EXPENSE` cuyo movimiento cae en el período; no el movimiento entero. Gasto = débitos − créditos en cuentas de gasto, así que los reintegros y devoluciones **restan**. La categoría de cuenta sale de la cuenta de cada imputación; la categoría de movimiento, del movimiento.
  - **Desglose:** monto por categoría de cuenta de gasto → monto por categoría de movimiento.
  - **Monedas:** solo totales por moneda, sin consolidar (por ahora).
  - **Período configurable:** semana, mes, año o rango de fechas libre. Límites según la zona horaria del espacio de trabajo; fecha de fin inclusiva.
  - **Comparación con el período anterior:** mes → mes calendario anterior; rango libre → rango de la misma duración inmediatamente anterior.
  - **Ajuste por inflación:** el autor lo quiere, con la limitación de que el IPC de un mes se publica alrededor del 12–15 del mes siguiente. Propuesta (a confirmar): comparación real solo para períodos de meses completos y cuando ya está publicado el IPC de los meses involucrados; si falta, se muestra solo la variación nominal con la aclaración de que el ajuste está pendiente; semanas y rangos parciales, solo nominal.
  - **Exportación a PDF:** generada en el backend (la reutiliza el envío automático).
  - **Reporte mensual por defecto:** se envía por **Telegram** como PDF; el envío por email queda para más adelante.
  - **Pendiente de confirmar:** el nombre del caso de uso ("mensual") ya no refleja el período configurable; QUICK-27 (Plane) menciona también las deudas, que con esta definición no cuentan como gasto.

## Respuesta

<!-- Todo lo que esté debajo de este título es el texto que se compila al documento final. El título del caso de uso se arma con `id` y `nombre` del frontmatter. -->

**Historial de revisión de la especificación**

| Versión | Responsable | Descripción de la Revisión | Fecha |
| --- | --- | --- | --- |
| 1.0 | Martín Luraschi | Versión inicial | DD/MM/AAAA |

**Ficha del caso de uso**

| Campo | Detalle |
| ------ | ------------------ |
| Identificación | CU-007-002 |
| Nombre | Consultar reporte mensual de gastos |
| Componente | 007 Reportes |
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

![CU-007-002 · Nombre de la pantalla](../../imagenes/cu-007-002-pantalla.png)

[Para pantallas web, los datos del formulario:]

| Campo | Tipo | Obligatorio | Validación |
| --- | --- | --- | --- |
| [Monto] | [Número decimal] | [Sí] | [Mayor que cero] |

[Para el chatbot, en lugar de la tabla de campos, un ejemplo de conversación (mensaje del usuario y respuesta del sistema).]

[Criterios de usabilidad tenidos en cuenta, en una o dos oraciones.]
