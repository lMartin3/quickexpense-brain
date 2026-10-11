---
tipo: referencias
# Referencias bibliográficas en formato CSL (lo lee pandoc al compilar; salen en APA 7).
# Para citar en una sección Respuesta: [@clave] → (Autor, año); @clave → Autor (año).
# Varias: [@clave1; @clave2]. Con página: [@clave, p. 12].
references:

# --- Bibliografía teórica ------------------------------------------------------
- id: porter1980
  type: book
  author: [{family: Porter, given: Michael E.}]
  issued: {date-parts: [[1980]]}
  title: "Competitive strategy: Techniques for analyzing industries and competitors"
  publisher: Free Press

- id: kotler2016
  type: book
  author: [{family: Kotler, given: Philip}, {family: Keller, given: Kevin Lane}]
  issued: {date-parts: [[2016]]}
  title: Marketing management
  edition: "15"
  publisher: Pearson

# --- Investigación primaria ----------------------------------------------------
- id: luraschi2026encuesta
  type: dataset
  author: [{family: Luraschi, given: Martín}]
  issued: {date-parts: [[2026, 9]]}
  title: Encuesta sobre hábitos de gestión de las finanzas personales
  genre: Conjunto de datos no publicado

# --- Economía ---------------------------------------------------------------------
- id: indec2026ipc
  type: report
  author: [{literal: Instituto Nacional de Estadística y Censos}]
  issued: {date-parts: [[2026, 9, 10]]}
  title: "Índice de precios al consumidor (IPC). Agosto de 2026"
  collection-title: Informes técnicos
  URL: https://www.indec.gob.ar/uploads/informesdeprensa/ipc_09_26A1BE2DC4CD.pdf

- id: indec2026pib
  type: report
  author: [{literal: Instituto Nacional de Estadística y Censos}]
  issued: {date-parts: [[2026, 9]]}
  title: "Informe de avance del nivel de actividad. Segundo trimestre de 2026"
  collection-title: Informes técnicos
  URL: https://www.indec.gob.ar/uploads/informesdeprensa/pib_09_26065D6A3612.pdf

- id: indec2026emae
  type: report
  author: [{literal: Instituto Nacional de Estadística y Censos}]
  issued: {date-parts: [[2026, 9]]}
  title: "Estimador mensual de actividad económica. Julio de 2026"
  collection-title: Informes técnicos
  URL: https://www.indec.gob.ar/uploads/informesdeprensa/emae_09_26FE154D8FFE.pdf

- id: indec2026eph
  type: report
  author: [{literal: Instituto Nacional de Estadística y Censos}]
  issued: {date-parts: [[2026, 9]]}
  title: "Mercado de trabajo. Tasas e indicadores socioeconómicos (EPH). Segundo trimestre de 2026"
  collection-title: Informes técnicos
  URL: https://www.indec.gob.ar/uploads/informesdeprensa/mercado_trabajo_eph_2trim26433FCBC5A8.pdf

- id: lanacion2026pbi
  type: article-newspaper
  author: [{family: Manzoni, given: Carlos}]
  issued: {date-parts: [[2026, 3, 20]]}
  title: "La economía creció 4,4% en 2025, impulsada por los bancos, el agro y la minería"
  container-title: La Nación
  URL: https://www.lanacion.com.ar/arquitectura/la-economia-crecio-44-en-2025-con-sectores-ganadores-y-perdedores-nid20032026/

- id: mdz2026emae
  type: article-newspaper
  issued: {date-parts: [[2026, 9, 24]]}
  title: "Día D para la economía: el Indec revela el EMAE de julio y se define si Argentina entra en recesión"
  container-title: MDZ
  URL: https://www.mdzol.com/dinero/dia-d-la-economia-el-indec-revela-el-emae-julio-y-se-define-si-argentina-entra-recesion-n1613691

- id: gimenez2026bandas
  type: article-newspaper
  author: [{family: Giménez, given: José}]
  issued: {date-parts: [[2026, 1, 2]]}
  title: "Dólar y nuevo esquema cambiario: cómo quedan las bandas de flotación a partir del 2 de enero de 2026"
  container-title: Chequeado
  URL: https://chequeado.com/el-explicador/bandas-de-flotacion-del-dolar-que-cambia-desde-2026-y-como-funcionaron-hasta-ahora/

- id: gasalla2026dolar
  type: article-newspaper
  author: [{family: Gasalla, given: Juan}]
  issued: {date-parts: [[2026, 10, 5]]}
  title: "El dólar operó sin cambios y quedó a más de 400 pesos del techo de las bandas cambiarias"
  container-title: Infobae
  URL: https://www.infobae.com/economia/2026/10/05/el-dolar-opero-sin-cambios-y-quedo-a-mas-de-400-pesos-del-techo-de-las-bandas-cambiarias/

- id: lepiscopo2026iva
  type: webpage
  author: [{family: L'Episcopo, given: Ignacio}]
  issued: {date-parts: [[2026, 10]]}
  title: "IVA RG 4240: qué es y cómo se cobra en Netflix y Spotify 2026"
  container-title: nacho.com.ar
  URL: https://nacho.com.ar/iva-netflix-cobraran-el-impuesto-a-los-usuarios-de-servicios-digitales/

# --- Marco político y regulatorio ---------------------------------------------------
- id: ley25326
  type: legislation
  title: "Ley 25.326 de Protección de los Datos Personales"
  issued: {date-parts: [[2000, 11, 2]]}
  container-title: Boletín Oficial de la República Argentina
  URL: https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm

- id: decreto353
  type: legislation
  title: "Decreto 353/2025"
  issued: {date-parts: [[2025, 5, 23]]}
  container-title: Boletín Oficial de la República Argentina
  URL: https://www.boletinoficial.gob.ar/detalleAviso/primera/325767/20250523

- id: szlak2025
  type: article-magazine
  author: [{family: Szlak, given: Gabriela}]
  issued: {date-parts: [[2025, 6, 3]]}
  title: "Novedades legislativas en Argentina sobre protección de datos personales e inteligencia artificial"
  container-title: IAPP
  URL: https://iapp.org/news/a/novedades-legislativas-en-argentina-sobre-protecci-n-de-datos-personales-e-inteligencia-artificial

- id: marval2026datos
  type: webpage
  author: [{literal: Marval O'Farrell Mairal}]
  issued: {date-parts: [[2026, 8, 27]]}
  title: "Nuevo proyecto de ley de protección de datos"
  URL: https://www.marval.com/Publicacion/nuevo-proyecto-de-ley-de-proteccion-de-datos-17691

- id: dpa1751
  type: webpage
  author: [{literal: Digital Policy Alert}]
  title: "Data protection regulation in bill providing regulatory framework for protection of personal data and privacy (No. 1751-D-2026)"
  URL: https://digitalpolicyalert.org/change/19257-data-protection-regulation-in-bill-providing-regulatory-framework-for-protection-of-personal-data-and-privacy-no-1751-d-2026
  accessed: {date-parts: [[2026, 10, 6]]}

- id: cronica2026ia
  type: article-newspaper
  issued: {date-parts: [[2026, 6, 14]]}
  title: "Presentan un proyecto para convertir a Argentina en un polo global de IA"
  container-title: Diario Crónica
  URL: https://www.diariocronica.com.ar/noticias/2026/06/14/149011-presentan-un-proyecto-para-convertir-a-argentina-en-un-polo-global-de-ia

- id: fiskil2026
  type: webpage
  author: [{literal: Fiskil}]
  title: "Open Banking Argentina: guía completa BCRA para fintechs"
  URL: https://www.fiskil.com/es/open-finance/solutions/argentina/overview
  accessed: {date-parts: [[2026, 10, 6]]}

- id: whatsapp-terms
  type: webpage
  author: [{literal: WhatsApp}]
  title: WhatsApp Business Solution Terms
  URL: https://www.whatsapp.com/legal/business-solution-terms
  accessed: {date-parts: [[2026, 10, 6]]}

- id: filgueira2025
  type: post-weblog
  author: [{family: Filgueira, given: Román}]
  issued: {date-parts: [[2025, 10, 27]]}
  title: "Not all chatbots are banned: WhatsApp's 2026 AI policy explained"
  container-title: respond.io
  URL: https://respond.io/blog/whatsapp-general-purpose-chatbots-ban

# --- Tecnología y adopción ------------------------------------------------------------
- id: kemp2025digital
  type: report
  author: [{family: Kemp, given: Simon}]
  issued: {date-parts: [[2025, 11, 8]]}
  title: "Digital 2026: Argentina"
  publisher: DataReportal
  URL: https://datareportal.com/reports/digital-2026-argentina

- id: statista2025redes
  type: dataset
  author: [{literal: Statista}]
  issued: {date-parts: [[2025, 11, 8]]}
  title: "Most popular social media platforms in Argentina as of 2nd quarter 2025, by usage reach"
  genre: Gráfico
  URL: https://www.statista.com/statistics/284401/argentina-social-network-penetration/

- id: indec2025tic
  type: report
  author: [{literal: Instituto Nacional de Estadística y Censos}]
  issued: {date-parts: [[2025, 5]]}
  title: "Acceso y uso de tecnologías de la información y la comunicación. EPH. Cuarto trimestre de 2024"
  collection-title: Informes técnicos
  volume: "9"
  number: "113"
  URL: https://www.indec.gob.ar/uploads/informesdeprensa/mautic_05_25FD0D0C4A71.pdf

- id: utdt2025ia
  type: webpage
  author: [{literal: Universidad Torcuato Di Tella}]
  issued: {date-parts: [[2025, 11, 18]]}
  title: "Cómo y para qué usamos la inteligencia artificial en Argentina, según un estudio académico"
  URL: https://www.utdt.edu/ver_nota_prensa.php?id_nota_prensa=23080

# --- Educación financiera y población -------------------------------------------------
- id: bcracaf2018
  type: report
  author: [{literal: Banco Central de la República Argentina}, {literal: CAF - Banco de Desarrollo de América Latina}]
  issued: {date-parts: [[2018]]}
  title: "Encuesta de medición de capacidades financieras en Argentina: 2017"
  URL: https://scioteca.caf.com/handle/123456789/1341

- id: correa2023censo
  type: article-newspaper
  author: [{family: Correa, given: Guillermo}]
  issued: {date-parts: [[2023, 11, 25]]}
  title: "Cuántos somos, cómo estamos: deudas de los 40 años de democracia en el departamento Rosario"
  container-title: El Ciudadano
  URL: https://elciudadanoweb.com/cuantos-somos-como-estamos-deudas-de-los-40-anos-de-democracia-en-el-departamento-rosario/

# --- Competencia ------------------------------------------------------------------------
- id: gasti2026
  type: webpage
  author: [{literal: Gasti}]
  title: "Gasti — Finanzas personales, más allá de trackear gastos"
  URL: https://gasti.pro/
  accessed: {date-parts: [[2026, 10, 6]]}

- id: piggy2026
  type: webpage
  author: [{literal: Equipo Piggy}]
  issued: {date-parts: [[2026, 9, 17]]}
  title: "¿Cuál es la mejor app de finanzas personales en Argentina en 2026?"
  container-title: Piggy
  URL: https://piggy.com.ar/guias/mejor-app-finanzas-personales-argentina/

- id: quewallet
  type: webpage
  author: [{literal: QueWallet}]
  title: "QueWallet - Control de gastos por WhatsApp"
  URL: https://www.quewallet.com/
  accessed: {date-parts: [[2026, 10, 5]]}

- id: chanchito
  type: webpage
  author: [{literal: Chanchito}]
  title: "Las mejores apps para controlar gastos en 2026"
  URL: https://www.chanchito.app/blog/app-para-controlar-gastos
  accessed: {date-parts: [[2026, 10, 5]]}

- id: aimoney
  type: webpage
  author: [{literal: AI Money}]
  title: "La mejor app de finanzas y gastos con IA, gratis"
  URL: https://www.ai-money.app/
  accessed: {date-parts: [[2026, 10, 5]]}

- id: ynab-pricing
  type: webpage
  author: [{literal: YNAB}]
  title: Pricing
  URL: https://www.ynab.com/pricing
  accessed: {date-parts: [[2026, 10, 6]]}

- id: focusfolio2026
  type: webpage
  author: [{literal: Focus·Folio}]
  issued: {date-parts: [[2026]]}
  title: "Las mejores apps de finanzas personales en Argentina (2026)"
  URL: https://focusfolio.com.ar/mejores-apps-finanzas-personales-argentina
  accessed: {date-parts: [[2026, 10, 7]]}

- id: monthly2026
  type: post-weblog
  author: [{literal: Equipo Monthly}]
  issued: {date-parts: [[2026, 6, 1]]}
  title: "Las mejores apps de finanzas personales para Android en Argentina"
  container-title: Monthly
  URL: https://monthly.com.ar/blog/mejores-apps-finanzas-personales-android-argentina/

- id: ynab-monedas
  type: webpage
  author: [{literal: YNAB}]
  title: "Using multiple currencies in YNAB: A guide"
  URL: https://support.ynab.com/en_us/using-multiple-currencies-in-ynab-a-guide-SyBF6PHno
  accessed: {date-parts: [[2026, 10, 7]]}

# --- Benchmarks de la industria -------------------------------------------------------------
- id: whitman2026revenuecat
  type: post-weblog
  author: [{family: Whitman, given: Lorelei}]
  issued: {date-parts: [[2026, 3, 19]]}
  title: "The state of subscription apps in 10 minutes: Lessons, trends, and benchmarks for 2026"
  container-title: RevenueCat
  URL: https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026

- id: mishchuk2026promodo
  type: post-weblog
  author: [{family: Mishchuk, given: Yanina}, {family: Loshak, given: Victoria}, {family: Afanasieva, given: Yana}]
  issued: {date-parts: [[2026, 7, 31]]}
  title: "Mobile marketing benchmarks: Know what good performance looks like in 2026"
  container-title: Promodo
  URL: https://www.promodo.com/blog/mobile-marketing-benchmarks
---

# Referencias

Este archivo guarda **todas las fuentes citadas** en las secciones Respuesta, en formato CSL (en el frontmatter). Al compilar, pandoc las formatea en **APA 7** y arma la lista de [[11.3 Bibliografía consultada]] con las que efectivamente se citan.

## Cómo citar

| En el `.md` | Resultado |
| --- | --- |
| `[@indec2026ipc]` | (Instituto Nacional de Estadística y Censos, 2026) |
| `@kemp2025digital indica que…` | Kemp (2025) indica que… |
| `[@porter1980; @kotler2016]` | (Kotler y Keller, 2016; Porter, 1980) |
| `[@bcracaf2018, p. 12]` | (Banco Central…, 2018, p. 12) |

Para agregar una fuente, sumar una entrada en el frontmatter con un `id` nuevo. Tipos más usados: `article-newspaper` (nota de diario), `webpage`, `report` (informe), `book`, `legislation` (normas), `dataset`. Si la página no tiene fecha, se omite `issued` y se agrega `accessed` (fecha de consulta).

Todos los datos fueron verificados contra la fuente indicada el 05 y 06/10/2026. Notas de verificación en [[_Investigación de contexto]].
