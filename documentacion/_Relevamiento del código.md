---
tipo: guia
fecha_relevamiento: 2026-10-05
---

# Relevamiento del código

Estado del desarrollo según lo que se ve en los repositorios. Este archivo **no** se compila: es material de referencia para completar los puntos 1.2, 9.1, 10.4.x y los diagramas del capítulo 10.

| Repositorio | Ruta | Historial |
| --- | --- | --- |
| Backend | `/home/martin/dev/projects/web/quickexpense` | 65 commits, desde el 2025-08-14 |
| Frontend | `/home/martin/dev/projects/web/quickexpense-frontend` | 78 commits, desde el 2025-09-05 |

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
- Tests: kotest, MockK, JUnit 5, Karate (integración) y Testcontainers.

**Frontend**
- Next.js 16 (App Router), React 19 y TypeScript.
- Tailwind CSS con shadcn/ui (Radix).
- TanStack Query, react-hook-form + zod y Recharts.
- NextAuth para el login federado con Keycloak.

**IA**

| Uso | Modelo |
| --- | --- |
| Asistente del chatbot | Anthropic Claude Haiku 4.5, con *tool calling*: herramientas de lectura y escritura sobre cuentas, movimientos y categorías, y memoria de conversación por usuario y espacio de trabajo |
| Resumen de documentos adjuntos | Claude Haiku 4.5 |
| Transcripción de audios | OpenAI `whisper-1` |

**Despliegue**
- GitHub Actions construye imágenes Docker en cada push a `master` y las publica en GitHub Container Registry.
- Después se conecta por SSH al servidor de producción —un **servidor dedicado propio (bare metal)**— y actualiza los servicios con `docker compose`.

## Arquitectura

Es un **monolito modular** con dos módulos Gradle:
- `expense`: el dominio y los casos de uso (entidades, repositorios, servicios de aplicación). No depende de ningún framework.
- `web`: controladores REST, integración de chat (Telegram), servicios de IA, procesamiento de documentos, persistencia JPA y seguridad.

Las capas son `domain` / `application` / `infrastructure`, en estilo hexagonal. La integración de chat está abstraída (`ChatIntegration`, `ChatPlatform`), lo que facilita sumar WhatsApp; hoy el único valor de `ChatPlatform` es `TELEGRAM`.

## Modelo de dominio

- **Contabilidad por partida doble.** Cada movimiento es un *asiento* (`JournalEntry`) con al menos dos *imputaciones* (`Posting`) al débito o al crédito sobre distintas cuentas.
- **Cuenta.** Tiene un tipo (activo, pasivo, ingreso, gasto o patrimonio neto/equidad), una moneda (ARS, USD, EUR, etc.) y una categoría de cuenta opcional.
- **Categorías** de cuentas y de movimientos, con nombre, descripción y color.
- **Espacio de trabajo.** Tiene un propietario y miembros con rol `ADMIN`, `MEMBER` o `READ_ONLY`. Todas las entidades pertenecen a un espacio de trabajo.
- **Documento.** Archivo adjunto (PDF, imagen, audio, planilla o texto) guardado en S3, con el contenido extraído y un resumen.
- **Configuración de usuario.** ID de Telegram vinculado y espacio de trabajo por defecto del chatbot.
- **Tablas** (Liquibase): `users`, `user_settings`, `workspaces`, `workspace_members`, `accounts`, `account_categories`, `categories`, `journal_entries`, `postings`, `journal_entries_postings`, `documents`, `chat_messages`, `chat_messages_documents`.

## Funciones de la idea frente al código

| Función (`Idea de proyecto.md`) | Estado en el código |
| --- | --- |
| Cuentas, movimientos y categorías | **Implementado** en la web y en el chatbot |
| Chatbot de Telegram | **Implementado** para texto, PDF (extracción de texto) y audio (transcripción). Las **imágenes** se reciben, pero no hay procesador para ellas, así que todavía no se interpretan |
| Espacios de trabajo multiusuario | **Implementado** el modelo de miembros y roles, la validación de pertenencia y el aislamiento con RLS. Hoy los miembros se agregan directamente en la base de datos; está planificada la **invitación por email** |
| Evolución de saldos | **Implementado**: reportes de saldo por cuenta en el tiempo, con gráfico |
| Categorización automática | **Parcial**: el asistente puede asignar categoría al crear un movimiento desde el chat |
| Multimoneda | **Implementado** a nivel de cuenta (cada cuenta tiene su moneda) |
| Deudas | **Parcial**: existen cuentas de pasivo; no hay seguimiento de cuotas ni de préstamos |
| Reportes mensuales de gastos | No encontrado |
| Inflación y tipo de cambio | No encontrado |
| Gastos recurrentes, presupuesto, metas de ahorro | No encontrado |
| Alertas, inversiones, carga masiva, recomendaciones | No encontrado |
| WhatsApp | No encontrado (planificado) |
| PWA | No encontrado: no hay manifest ni service worker |
| Suscripción / cobros (freemium) | No encontrado |

## Pantallas web

- Inicio
- Configuración
- Saldos
- Cuentas: listado, alta/edición y categorías
- Movimientos: listado, alta/edición, carga rápida y categorías
- Ingreso y cierre de sesión

También hay rutas de prueba (`/cars`, `/test`, `/private`, `/public`, `/dashboard/experiments`) que no deberían figurar en el mapa de navegación.

## Respuestas del autor (2026-10-05)

- Los miembros se agregan hoy directamente en la base; la idea es sumar invitación por email.
- Se usa *tool calling*, no MCP.
- Producción: servidor dedicado propio (bare metal).
- Usuario de prueba: el propio autor.

## Preguntas pendientes sobre el código

- ¿Keycloak y el almacenamiento S3 corren en el mismo servidor dedicado?
