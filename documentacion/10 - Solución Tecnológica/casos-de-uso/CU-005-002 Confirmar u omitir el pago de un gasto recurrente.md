---
id: "CU-005-002"
nombre: "Confirmar u omitir el pago de un gasto recurrente"
componente: "005 Gastos recurrentes"
core: false
estado: pendiente
---

# CU-005-002 Confirmar u omitir el pago de un gasto recurrente

## Notas internas

- Relacionado con el caso de uso core 2 («extend» de CU-005-001).

## Respuesta

<!-- Todo lo que esté debajo de este título es el texto que se compila al documento final. El título del caso de uso se arma con `id` y `nombre` del frontmatter. -->

**Historial de revisión de la especificación**

| Versión | Responsable | Descripción de la Revisión | Fecha |
| --- | --- | --- | --- |
| 1.0 | Martín Luraschi | Versión inicial | DD/MM/AAAA |

**Ficha del caso de uso**

| Campo | Detalle |
| ------ | ------------------ |
| Identificación | CU-005-002 |
| Nombre | Confirmar u omitir el pago de un gasto recurrente |
| Componente | 005 Gastos recurrentes |
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

![CU-005-002 · Nombre de la pantalla](../../imagenes/cu-005-002-pantalla.png)

[Para pantallas web, los datos del formulario:]

| Campo | Tipo | Obligatorio | Validación |
| --- | --- | --- | --- |
| [Monto] | [Número decimal] | [Sí] | [Mayor que cero] |

[Para el chatbot, en lugar de la tabla de campos, un ejemplo de conversación (mensaje del usuario y respuesta del sistema).]

[Criterios de usabilidad tenidos en cuenta, en una o dos oraciones.]
