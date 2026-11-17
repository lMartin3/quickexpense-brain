---
tipo: guia
fecha_relevamiento: 2026-10-05
actualizado: 2026-11-13
---

# Relevamiento del código

Estado del desarrollo según lo que se ve en los repositorios. Este archivo **no** se compila: es material de referencia para completar los puntos 1.2, 9.1, 10.4.x y los diagramas del capítulo 10.

| Repositorio | Ruta | Historial |
| --- | --- | --- |
| Backend | `/home/martin/dev/projects/web/quickexpense` | 65 commits, desde el 2025-08-14 (+12 hasta el 2026-11-11) |
| Frontend | `/home/martin/dev/projects/web/quickexpense-frontend` | 78 commits, desde el 2025-09-05 (+4 hasta el 2026-11-01) |

## Stack tecnológico

**Backend**
- Kotlin 2.3 sobre JVM 21, Spring Boot 4.0.
- Spring Security como servidor de recursos OAuth2; los tokens JWT los emite **Keycloak**.
- Spring Data JPA / Hibernate sobre **PostgreSQL 16**. Migraciones con **Liquibase**.
- **Row-Level Security** de PostgreSQL para aislar los datos de cada espacio de trabajo.
- **Spring AI 2.0** con Anthropic y OpenAI. El agente opera mediante *tool calling* (la dependencia de cliente MCP está declarada, pero no se usa).
- Apache PDFBox para extraer texto de PDFs.
- AWS SDK S3: almacenamiento de archivos en un servicio compatible con S3.
- springdoc-openapi: documentación de la API REST.
- Spring Scheduling con ShedLock (tabla `shedlock`) para procesos programados, como la generación de ocurrencias de gastos recurrentes.
- Tests: kotest, MockK, JUnit 5, Karate (integración) y Testcontainers.

**Frontend**
- Next.js 16 (App Router), React 19 y TypeScript.
- Tailwind CSS con shadcn/ui (Radix).
- TanStack Query, react-hook-form + zod y Recharts.
- NextAuth para el login federado con Keycloak.

**IA**

| Uso | Modelo |
| --- | --- |
| Asistente del chatbot | Anthropic Claude Haiku 5.5 (`claude-haiku-5-5`, actualizado el 2026-10-07), con *tool calling*: herramientas de lectura y escritura sobre cuentas, movimientos, categorías y gastos recurrentes, y memoria de conversación por usuario y espacio de trabajo |
| Resumen de documentos adjuntos | Claude Haiku 5.5 |
| Transcripción de audios | OpenAI `whisper-1` |

**Despliegue**
- GitHub Actions construye imágenes Docker en cada push a `master` y las publica en GitHub Container Registry.
- Después se conecta por SSH al servidor de producción —un **servidor dedicado propio (bare metal)**— y actualiza los servicios con `docker compose`.

## Arquitectura

Es un **monolito modular** con dos módulos Gradle:
- `expense`: el dominio y los casos de uso (entidades, repositorios, servicios de aplicación). No depende de ningún framework.
- `web`: controladores REST, integración de chat (Telegram), servicios de IA, procesamiento de documentos, persistencia JPA y seguridad.

Las capas son `domain` / `application` / `infrastructure`, en estilo hexagonal. La integración de chat está abstraída (`ChatIntegration`, `ChatPlatform`), lo que facilita sumar WhatsApp; hoy el único valor de `ChatPlatform` es `TELEGRAM`. Desde el 2026-11-11 el bot puede recibir mensajes por *webhook* (producción) o por *long polling* (desarrollo local).

## Modelo de dominio

- **Contabilidad por partida doble.** Cada movimiento es un *asiento* (`JournalEntry`) con al menos dos *imputaciones* (`Posting`) al débito o al crédito sobre distintas cuentas.
- **Cuenta.** Tiene un tipo (activo, pasivo, ingreso, gasto o patrimonio neto/equidad), una moneda (ARS, USD, EUR, etc.) y una categoría de cuenta opcional.
- **Categorías** de cuentas y de movimientos, con nombre, descripción y color.
- **Espacio de trabajo.** Tiene un propietario y miembros con rol `ADMIN`, `MEMBER` o `READ_ONLY`. Todas las entidades pertenecen a un espacio de trabajo.
- **Documento.** Archivo adjunto (PDF, imagen, audio, planilla o texto) guardado en S3, con el contenido extraído y un resumen.
- **Gasto recurrente** (`RecurringExpense`). Pago periódico de una cuenta de activo o pasivo a una cuenta de gasto, con regla de recurrencia, fecha de inicio y de fin opcional, monto y moneda, categoría de movimiento y días de anticipación. El costo puede ser **fijo** o **variable**; los variables llevan una estrategia de estimación (tolerancia en % sobre el monto esperado).
- **Ocurrencia de gasto recurrente** (`RecurringExpenseInstance`). Cada vencimiento, con estado `PENDING` (pendiente), `CONFIRMED` (pagado, con monto y fecha reales y el movimiento asociado) o `SKIPPED` (no ocurrió). Un proceso programado (cada hora, con ShedLock) crea las ocurrencias pendientes a medida que vencen.
- **Usuarios.** La tabla `users` es una copia local de la identidad de Keycloak (id = *subject* del token, correo, correo verificado, nombre para mostrar, fecha de alta y de última vez visto). La mantiene `AuthenticatedUserSyncFilter` a partir de los claims del JWT, escribiendo solo si cambió la identidad o pasó `quickexpense.users.sync-interval` (6 h). No hay registro ni contraseñas propias. (Cambio del 13/11/2026; migración de Liquibase `2026/11/14-01-changelog.sql` del 14/11/2026.)
- **Configuración de usuario.** ID de Telegram vinculado, espacio de trabajo por defecto del chatbot e idioma de la interfaz (`uiLanguage`, desde el 2026-10-11).
- **Tablas** (Liquibase): `users`, `user_settings`, `workspaces`, `workspace_members`, `accounts`, `account_categories`, `categories`, `journal_entries`, `postings`, `journal_entries_postings`, `documents`, `chat_messages`, `chat_messages_documents`, `recurring_expenses`, `recurring_expense_instances` y `shedlock`.

## Funciones de la idea frente al código

| Función (`Idea de proyecto.md`) | Estado en el código |
| --- | --- |
| Cuentas, movimientos y categorías | **Implementado** en la web y en el chatbot |
| Chatbot de Telegram | **Implementado** para texto, PDF (extracción de texto), audio (transcripción) e imágenes (`ImageProcessingService`, commit «add ai image processing», revisado el 16/11/2026) |
| Espacios de trabajo multiusuario | **Implementado** el modelo de miembros y roles, la validación de pertenencia y el aislamiento con RLS. Hoy los miembros se agregan directamente en la base de datos; está planificada la **invitación por email** |
| Evolución de saldos | **Implementado**: reportes de saldo por cuenta en el tiempo, con gráfico; desde octubre, saldo total y totales por moneda |
| Categorización automática | **Parcial**: el asistente puede asignar categoría al crear un movimiento desde el chat |
| Multimoneda | **Implementado** a nivel de cuenta (cada cuenta tiene su moneda) |
| Deudas | **Parcial**: existen cuentas de pasivo; no hay seguimiento de cuotas ni de préstamos |
| Reportes mensuales de gastos | No implementado: existe la clase de dominio `ExpenseReport` (total y desglose por categoría), pero no se usa (sin cálculo, endpoint ni pantalla) |
| Inflación y tipo de cambio | No encontrado en Quickexpense. Los datos los provee un API de indicadores propio del autor, escrito en Go, que corre en el mismo servidor en otro `docker compose` (17/11/2026); falta consumirlo desde Quickexpense |
| Gastos recurrentes | **Casi completo**: alta, edición y baja en la web; generación automática de ocurrencias pendientes; confirmación u omisión de cada ocurrencia asociándole un movimiento existente; RLS. Herramientas del asistente para gastos recurrentes commiteadas. Falta: el reconocimiento automático del pago en los gastos variables (la tolerancia se guarda, pero no se usa; revisado el 16/11/2026) |
| Presupuesto, metas de ahorro | No encontrado |
| Alertas, inversiones, carga masiva, recomendaciones | No encontrado |
| Invitación de miembros por email | No encontrado: la API de espacios de trabajo permite crear, editar y borrar, pero no hay operaciones para administrar miembros ni invitaciones (revisado el 16/11/2026) |
| WhatsApp | No encontrado (planificado) |
| PWA | No encontrado: no hay manifest ni service worker |
| Suscripción / cobros (freemium) | No encontrado |

## Pantallas web

- Inicio
- Configuración
- Saldos
- Cuentas: listado, alta/edición y categorías
- Movimientos: listado, alta/edición, carga rápida y categorías
- Gastos recurrentes: listado, alta/edición y detalle (desde el 2026-11-01)
- Ingreso y cierre de sesión

También hay rutas de prueba (`/cars`, `/test`, `/private`, `/public`, `/dashboard/experiments`) que no deberían figurar en el mapa de navegación.

## Respuestas del autor (2026-10-05)

- Los miembros se agregan hoy directamente en la base; la idea es sumar invitación por email.
- Se usa *tool calling*, no MCP.
- Producción: servidor dedicado propio (bare metal) con Ubuntu Server y firewall. Cloudflare enruta el tráfico (protección contra ataques) y Traefik hace de proxy inverso, con certificados HTTPS automáticos vía Cloudflare. Keycloak corre en el mismo servidor, en otro `docker compose`, aislado de la aplicación (confirmado el 13/11/2026).
- Usuario de prueba: el propio autor.

## Trabajo sin commitear (2026-11-13)

- **Backend:** herramientas del asistente para gastos recurrentes y tests nuevos. `expense/.../application/account/AccountService.kt` tiene un `JournalEntryPosting(j` que parece un error de tipeo y hace que el backend no compile.
- **Frontend:** cambios en la pantalla de cuentas, en la edición de movimientos y en el selector de espacio de trabajo.

## Preguntas pendientes sobre el código

- ~~¿Keycloak y el almacenamiento S3 corren en el mismo servidor dedicado?~~ Sí (25/10/2026): toda la cadena corre en el dedicado; el almacenamiento S3 es RustFS.
