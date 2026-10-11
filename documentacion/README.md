# Documentación del proyecto

Esta carpeta contiene todo lo necesario para escribir el documento de la consigna (`fuentes/consigna.md`). Hay una carpeta por cada punto mayor y un archivo por cada punto menor.

## Cómo está organizado cada archivo

Cada `.md` de un punto tiene:

1. **Frontmatter** con `punto`, `titulo`, `capitulo`, `estado` y `origen_respuesta`.
2. **Consigna:** el texto literal de la consigna para ese punto.
3. **Qué se espera:** explicación de lo que hay que responder.
4. **Ideas y material disponible:** lo que ya existe en las fuentes y en otros puntos que sirve para este.
5. **Ejemplos:** formatos o ejemplos ilustrativos (no son contenido del proyecto).
6. **Preguntas abiertas y observaciones:** dudas a resolver, inconsistencias y erratas detectadas.
7. **Respuesta:** el texto que va al documento final. **Solo esta sección se compila al LaTeX.**

Los archivos que empiezan con `_` (guías de capítulo, formato, plantillas, relevamiento del código) son de referencia y **no** se compilan.

### Estados

- `pendiente`: sin respuesta todavía.
- `borrador`: tiene texto (en general migrado del Parcial, `fuentes/Progreso de trabajo actual.pdf`, con las correcciones confirmadas), pero falta revisarlo.
- `automatico`: lo genera LaTeX (por ejemplo, el índice o la bibliografía).
- `omitido`: no se compila aunque tenga contenido.
- Cuando un punto esté revisado, cambiar a `listo`.

### Imágenes

Todas las imágenes del documento final van en `imagenes/`. Se referencian desde la sección Respuesta con `![descripción](../imagenes/archivo.png)`.

## Compilar

`herramientas/compilar.sh` genera `latex/build/main.pdf` con las secciones Respuesta. Detalle en `herramientas/README.md`.

## Citas

Toda información de terceros se cita en APA: las fuentes se cargan en [[_Referencias]] y se citan en las secciones Respuesta con `[@clave]`. La verificación de cada dato está en [[_Investigación de contexto]].

## Decisiones confirmadas

Estas decisiones resolvieron las inconsistencias entre el Parcial y `fuentes/Idea de proyecto.md`. Ya están aplicadas en los `.md`:

| Tema | Decisión |
| --- | --- |
| Plataforma | Aplicación web, instalable en móviles como PWA |
| Canales del chatbot | Telegram en las etapas de prueba y en la presentación universitaria; WhatsApp como canal principal desde el lanzamiento comercial |
| Rango etario | 18 a 35 años |
| Tipo de cambio | Se descarta el arbitraje entre cotizaciones; solo seguimiento del dólar estadounidense e inflación |
| Alertas | Gasto recurrente que sube por encima de la inflación; gastos estimados + deuda + ajuste por inflación que se acercan al límite del presupuesto o lo superan |
| Inversiones | Seguimiento simple, con ajustes periódicos de ganancias y pérdidas |
| Equipo | Unipersonal; se consultó a profesionales del área de contabilidad |
| Identificación | Proyecto **Quickexpense** · Legajo B00067498-T1 · Sede Regional Rosario |
| Desarrollo | Ya existe código y una base funcional de la aplicación, en pruebas por el autor. Producción en servidor dedicado propio. IA por tool calling. Detalle en [[_Relevamiento del código]] |
| Funciones de IA | Se descartan el presupuesto dinámico y la predicción de flujos de caja. Se mantienen la categorización automática y las recomendaciones personalizadas (ver idea) |
| Espacios de trabajo | Multiusuario (implementado en el código) |
| Diferencial | Inflación como variable de planificación (alertas de recurrentes vs. IPC, presupuesto con inflación estimada, deuda y cuotas). Estrategia de Porter: enfoque con diferenciación |
| Etapas | Alpha (<20 usuarios, fines de 2026) → feedback → Beta (20–50, feb. 2027) → feedback y pulido → lanzamiento (junio 2027) |
| Funciones por etapa | Alpha: base actual + fotos de tickets, categorización automática, invitación por email, inflación, dólar, reportes, recurrentes, presupuesto, metas, tarjetas y cuotas, otras deudas, PWA. Lanzamiento: WhatsApp, alerta de recurrentes por encima de la inflación, préstamos, inversiones, carga masiva, plan pago. Después: alerta de presupuesto y recomendaciones (ver 5.2) |
| Entrega 4 (06/10/2026) | Fecha en la carátula; título del documento "Proyecto Final de Ingeniería en Sistemas Informáticos" (creado el 14/04/2026); ficha de seguimiento omitida (`estado: omitido`); Anexo A con la encuesta (11.2); FODA como matriz; Gantt en 5.2; "alto estrés financiero" como opinión del autor; canal WhatsApp confirmado para el lanzamiento |
| Inversión | 100% capital propio, principalmente tiempo; ≈USD 30/mes de servidor + USD 50/mes de tokens |
| Cobertura | Rosario |
| Competencia e inflación | Confirmado: Gasti y Piggy no tienen funciones basadas en la inflación |
| Metas | Primer año = jun. 2027 – may. 2028. 150 registrados (mínimo 100), 30% activos mensuales y 5% con plan pago (validadas por el autor) |
| Antecedentes | El autor trabaja en tecnología para un ALyC y una billetera virtual (herramientas de mercado y cotización) |
| Alianzas | Ninguna prevista |
| Segmentos 18-35 | Jóvenes con sus primeros ingresos + profesionales ya establecidos con una estructura financiera más desarrollada |

Además, se corrigieron las erratas del Parcial en 1.4, 1.5, 1.11 y 2.2.4.

## Foco actual: puntos 1 a 6.2

Del 1 al 6.2 todos los puntos tienen borrador. Material de soporte: [[_Investigación de contexto]] y [[_Resultados de la encuesta]] (31 respuestas, 19 a 27 años).

Pendientes para cerrar este bloque:
- Las cifras económicas están vigentes al 06/10/2026. Si la entrega es posterior a mediados de octubre, actualizar el IPC (septiembre) y el EMAE (agosto) en 2.1.2.

## Otros pendientes

- **Fechas:** carátula, ficha de seguimiento y descripción del documento.
- **Precio y límites** de los planes gratuito y premium: afecta 6.5, 8.1 y el resumen ejecutivo.
- **Supuestos del plan financiero:** ver `08 - Plan Financiero-Económico/_Guía del capítulo.md`.

## Estado por punto

### 00 - Preliminares

| Punto | Estado |
| --- | --- |
| [[00 - Preliminares/Carátula\|Carátula]] | borrador |
| [[00 - Preliminares/Ficha de seguimiento y revisión\|Ficha de seguimiento y revisión]] | pendiente |
| [[00 - Preliminares/Descripción del documento\|Descripción del documento]] | pendiente |
| [[00 - Preliminares/A. Resumen Ejecutivo\|A. Resumen Ejecutivo]] | borrador |

### 01 - Descripción General

| Punto | Estado |
| --- | --- |
| [[01 - Descripción General/1.1 Descripción básica del negocio\|1.1 Descripción básica del negocio]] | borrador |
| [[01 - Descripción General/1.2 Situación actual del negocio\|1.2 Situación actual del negocio]] | borrador |
| [[01 - Descripción General/1.3 Qué hace único al negocio\|1.3 Qué hace único al negocio]] | borrador |
| [[01 - Descripción General/1.4 Factores principales de éxito\|1.4 Factores principales de éxito]] | borrador |
| [[01 - Descripción General/1.5 Misión, visión y propósito estratégico\|1.5 Misión, visión y propósito estratégico]] | borrador |
| [[01 - Descripción General/1.6 Identificación de la oportunidad de negocio\|1.6 Identificación de la oportunidad de negocio]] | borrador |
| [[01 - Descripción General/1.7 Capacidades centrales\|1.7 Capacidades centrales]] | borrador |
| [[01 - Descripción General/1.8 Propuesta de valor para el cliente\|1.8 Propuesta de valor para el cliente]] | borrador |
| [[01 - Descripción General/1.9 Valores nucleares de la organización\|1.9 Valores nucleares de la organización]] | borrador |
| [[01 - Descripción General/1.10 Enfoque e iniciativas estratégicas\|1.10 Enfoque e iniciativas estratégicas]] | borrador |
| [[01 - Descripción General/1.11 Áreas claves de resultados\|1.11 Áreas claves de resultados]] | borrador |
| [[01 - Descripción General/1.12 Ingreso al sector - estrategias de inserción\|1.12 Ingreso al sector - estrategias de inserción]] | borrador |

### 02 - Análisis estratégico

| Punto | Estado |
| --- | --- |
| [[02 - Análisis estratégico/2.1.1 Descripción del escenario local\|2.1.1 Descripción del escenario local]] | borrador |
| [[02 - Análisis estratégico/2.1.2 Factores económicos\|2.1.2 Factores económicos]] | borrador |
| [[02 - Análisis estratégico/2.1.3 Factores políticos\|2.1.3 Factores políticos]] | borrador |
| [[02 - Análisis estratégico/2.1.4 Factores tecnológicos\|2.1.4 Factores tecnológicos]] | borrador |
| [[02 - Análisis estratégico/2.1.5 Escenario-meta\|2.1.5 Escenario-meta]] | borrador |
| [[02 - Análisis estratégico/2.1.6 Análisis sectorial - oportunidades y amenazas\|2.1.6 Análisis sectorial - oportunidades y amenazas]] | borrador |
| [[02 - Análisis estratégico/2.2.1 Principales competidores directos\|2.2.1 Principales competidores directos]] | borrador |
| [[02 - Análisis estratégico/2.2.2 Análisis de cadena de valor\|2.2.2 Análisis de cadena de valor]] | borrador |
| [[02 - Análisis estratégico/2.2.3 Factores Críticos de Éxito (FCE)\|2.2.3 Factores Críticos de Éxito (FCE)]] | borrador |
| [[02 - Análisis estratégico/2.2.4 Fortalezas y debilidades del negocio\|2.2.4 Fortalezas y debilidades del negocio]] | borrador |

### 03 - Análisis FODA

| Punto | Estado |
| --- | --- |
| [[03 - Análisis FODA/3.1 Cuadro FODA\|3.1 Cuadro FODA]] | borrador |
| [[03 - Análisis FODA/3.2 Análisis FODA\|3.2 Análisis FODA]] | borrador |
| [[03 - Análisis FODA/3.3 Conclusión - atractivo de la industria y fortalezas del negocio\|3.3 Conclusión - atractivo de la industria y fortalezas del negocio]] | borrador |

### 04 - Segmentación

| Punto | Estado |
| --- | --- |
| [[04 - Segmentación/4.1 Segmentación de consumidores y-o negocios\|4.1 Segmentación de consumidores y-o negocios]] | borrador |
| [[04 - Segmentación/4.2 Identificación de grupos diferenciados de consumidores\|4.2 Identificación de grupos diferenciados de consumidores]] | borrador |
| [[04 - Segmentación/4.3 Potenciales usuarios y compradores\|4.3 Potenciales usuarios y compradores]] | borrador |
| [[04 - Segmentación/4.4 Pautas de comportamiento esperado de cada segmento\|4.4 Pautas de comportamiento esperado de cada segmento]] | borrador |

### 05 - Plan de Acción

| Punto | Estado |
| --- | --- |
| [[05 - Plan de Acción/5.1 Programas generales de acción\|5.1 Programas generales de acción]] | borrador |
| [[05 - Plan de Acción/5.2 Programas específicos de acción\|5.2 Programas específicos de acción]] | borrador |

### 06 - Plan de Marketing

| Punto | Estado |
| --- | --- |
| [[06 - Plan de Marketing/6.1 Objetivos\|6.1 Objetivos]] | borrador |
| [[06 - Plan de Marketing/6.2 Resultados esperados en cobertura y participación\|6.2 Resultados esperados en cobertura y participación]] | borrador |
| [[06 - Plan de Marketing/6.3 Metas de posicionamiento\|6.3 Metas de posicionamiento]] | pendiente |
| [[06 - Plan de Marketing/6.4.1 Descripción del producto o servicio\|6.4.1 Descripción del producto o servicio]] | pendiente |
| [[06 - Plan de Marketing/6.4.2 Durabilidad o estacionalidad\|6.4.2 Durabilidad o estacionalidad]] | pendiente |
| [[06 - Plan de Marketing/6.4.3 Características que influyen en la decisión de compra\|6.4.3 Características que influyen en la decisión de compra]] | pendiente |
| [[06 - Plan de Marketing/6.4.4 Estudios que respalden las hipótesis\|6.4.4 Estudios que respalden las hipótesis]] | pendiente |
| [[06 - Plan de Marketing/6.5.1 Condicionantes del precio\|6.5.1 Condicionantes del precio]] | pendiente |
| [[06 - Plan de Marketing/6.5.2 Estrategia de precio\|6.5.2 Estrategia de precio]] | pendiente |
| [[06 - Plan de Marketing/6.6.1 Planificación estratégica de las acciones de comunicación\|6.6.1 Planificación estratégica de las acciones de comunicación]] | pendiente |
| [[06 - Plan de Marketing/6.6.2 Diseño del sitio web (7C y pantallas)\|6.6.2 Diseño del sitio web (7C y pantallas)]] | pendiente |
| [[06 - Plan de Marketing/6.7.1 Factores condicionantes de la distribución\|6.7.1 Factores condicionantes de la distribución]] | pendiente |
| [[06 - Plan de Marketing/6.7.2 Estrategia de distribución\|6.7.2 Estrategia de distribución]] | pendiente |
| [[06 - Plan de Marketing/6.7.3 Canales (tipo y nivel)\|6.7.3 Canales (tipo y nivel)]] | pendiente |
| [[06 - Plan de Marketing/6.7.4 Localización de puntos de venta propios\|6.7.4 Localización de puntos de venta propios]] | pendiente |
| [[06 - Plan de Marketing/6.7.5 Opciones de asociación\|6.7.5 Opciones de asociación]] | pendiente |
| [[06 - Plan de Marketing/6.7.6 Gestión del JIT (just in time)\|6.7.6 Gestión del JIT (just in time)]] | pendiente |

### 07 - Operaciones

| Punto | Estado |
| --- | --- |
| [[07 - Operaciones/7.1 Organización de la empresa\|7.1 Organización de la empresa]] | pendiente |
| [[07 - Operaciones/7.2 Grupo fundador, directorio y accionistas\|7.2 Grupo fundador, directorio y accionistas]] | pendiente |
| [[07 - Operaciones/7.3 Staff gerencial y perfil de ejecutivos clave\|7.3 Staff gerencial y perfil de ejecutivos clave]] | pendiente |
| [[07 - Operaciones/7.4 Estructura prevista al lanzamiento y evolución\|7.4 Estructura prevista al lanzamiento y evolución]] | pendiente |
| [[07 - Operaciones/7.5 Filosofía y sistema de trabajo\|7.5 Filosofía y sistema de trabajo]] | pendiente |
| [[07 - Operaciones/7.6 Requerimientos de RRHH\|7.6 Requerimientos de RRHH]] | pendiente |

### 08 - Plan Financiero-Económico

| Punto | Estado |
| --- | --- |
| [[08 - Plan Financiero-Económico/8.1 Modelo de ingresos\|8.1 Modelo de ingresos]] | pendiente |
| [[08 - Plan Financiero-Económico/8.2 Modelo de egresos\|8.2 Modelo de egresos]] | pendiente |
| [[08 - Plan Financiero-Económico/8.3 Modelo de inversión\|8.3 Modelo de inversión]] | pendiente |
| [[08 - Plan Financiero-Económico/8.4 Amortizaciones y depreciaciones\|8.4 Amortizaciones y depreciaciones]] | pendiente |
| [[08 - Plan Financiero-Económico/8.5 Impuesto a las ganancias\|8.5 Impuesto a las ganancias]] | pendiente |
| [[08 - Plan Financiero-Económico/8.6 Impuesto a los ingresos brutos\|8.6 Impuesto a los ingresos brutos]] | pendiente |
| [[08 - Plan Financiero-Económico/8.7 Remuneraciones y cargas sociales\|8.7 Remuneraciones y cargas sociales]] | pendiente |
| [[08 - Plan Financiero-Económico/8.8 Presupuesto financiero\|8.8 Presupuesto financiero]] | pendiente |
| [[08 - Plan Financiero-Económico/8.9 Evaluación de la inversión\|8.9 Evaluación de la inversión]] | pendiente |
| [[08 - Plan Financiero-Económico/8.10 Escenarios de riesgo\|8.10 Escenarios de riesgo]] | pendiente |
| [[08 - Plan Financiero-Económico/8.11 Plan de contingencia\|8.11 Plan de contingencia]] | pendiente |
| [[08 - Plan Financiero-Económico/8.12 Plan de salida\|8.12 Plan de salida]] | pendiente |

### 09 - Factibilidades

| Punto | Estado |
| --- | --- |
| [[09 - Factibilidades/9.1 Técnica\|9.1 Técnica]] | pendiente |
| [[09 - Factibilidades/9.2 Comercial\|9.2 Comercial]] | pendiente |
| [[09 - Factibilidades/9.3 Administrativa\|9.3 Administrativa]] | pendiente |
| [[09 - Factibilidades/9.4 Legal\|9.4 Legal]] | pendiente |

### 10 - Solución Tecnológica

| Punto | Estado |
| --- | --- |
| [[10 - Solución Tecnológica/10.1 Carátula\|10.1 Carátula]] | pendiente |
| [[10 - Solución Tecnológica/10.2 Índice\|10.2 Índice]] | automatico |
| [[10 - Solución Tecnológica/10.3 Historial de revisión\|10.3 Historial de revisión]] | pendiente |
| [[10 - Solución Tecnológica/10.4.1 Propuesta de valor del proyecto para la empresa\|10.4.1 Propuesta de valor del proyecto para la empresa]] | pendiente |
| [[10 - Solución Tecnológica/10.4.2 Especificaciones de requerimientos\|10.4.2 Especificaciones de requerimientos]] | pendiente |
| [[10 - Solución Tecnológica/10.4.3 Alcance del desarrollo\|10.4.3 Alcance del desarrollo]] | pendiente |
| [[10 - Solución Tecnológica/10.4.4 Definiciones, acrónimos y abreviaciones\|10.4.4 Definiciones, acrónimos y abreviaciones]] | pendiente |
| [[10 - Solución Tecnológica/10.4.5 Descripción del entorno del sistema\|10.4.5 Descripción del entorno del sistema]] | pendiente |
| [[10 - Solución Tecnológica/10.5.1 Mapa de navegación\|10.5.1 Mapa de navegación]] | pendiente |
| [[10 - Solución Tecnológica/10.5.2 Índice de casos de uso\|10.5.2 Índice de casos de uso]] | pendiente |
| [[10 - Solución Tecnológica/10.5.3 Casos de uso\|10.5.3 Casos de uso]] | pendiente |
| [[10 - Solución Tecnológica/10.5.4 Diagrama de secuencia\|10.5.4 Diagrama de secuencia]] | pendiente |
| [[10 - Solución Tecnológica/10.5.5 Diagrama de paquetes\|10.5.5 Diagrama de paquetes]] | pendiente |
| [[10 - Solución Tecnológica/10.5.6 Diagrama de componentes\|10.5.6 Diagrama de componentes]] | pendiente |
| [[10 - Solución Tecnológica/10.5.7 Diagrama de clases\|10.5.7 Diagrama de clases]] | pendiente |
| [[10 - Solución Tecnológica/10.5.8 Diagrama entidad relación\|10.5.8 Diagrama entidad relación]] | pendiente |
| [[10 - Solución Tecnológica/10.5.9 Diagrama de despliegue\|10.5.9 Diagrama de despliegue]] | pendiente |
| [[10 - Solución Tecnológica/10.5.10 Especificación de casos de prueba\|10.5.10 Especificación de casos de prueba]] | pendiente |

### 11 - Anexos

| Punto | Estado |
| --- | --- |
| [[11 - Anexos/11.1 Normas de calidad\|11.1 Normas de calidad]] | pendiente |
| [[11 - Anexos/11.2 Anexos específicos del proyecto\|11.2 Anexos específicos del proyecto]] | pendiente |
| [[11 - Anexos/11.3 Bibliografía consultada\|11.3 Bibliografía consultada]] | pendiente |
