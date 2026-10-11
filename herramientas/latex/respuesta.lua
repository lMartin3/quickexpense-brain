-- Filtro de pandoc: de un .md de documentacion/ deja solo la sección "## Respuesta",
-- precedida por un título armado con el frontmatter (punto + titulo).
--
-- Metadatos que lee (frontmatter del .md o -M en la línea de comandos):
--   punto, titulo, estado    → del frontmatter (estado "omitido": nunca se incluye)
--   incluir_pendientes=true  → incluye los puntos sin respuesta con la leyenda "Pendiente"
--   siempre_incluir=true     → incluye el punto aunque esté pendiente (preliminares)

local stringify = pandoc.utils.stringify

local function meta_str(meta, key)
  return meta[key] and stringify(meta[key]) or ""
end

local function meta_bool(meta, key)
  local v = meta[key]
  if v == nil then return false end
  if type(v) == "boolean" then return v end
  return stringify(v) == "true"
end

-- "1.1" → 2 (subsection), "2.1.1" → 3 (subsubsection); "A." o vacío → 1 (section)
local function nivel_de(punto)
  local partes = 0
  for _ in punto:gmatch("%d+") do partes = partes + 1 end
  if partes < 2 then return 1 end
  return math.min(partes, 4)
end

local function es_vacio(bloques)
  for _, b in ipairs(bloques) do
    if not (b.t == "RawBlock" and b.format == "html") then return false end
  end
  return true
end

function Pandoc(doc)
  local meta = doc.meta
  local punto = meta_str(meta, "punto")
  local titulo = meta_str(meta, "titulo"):gsub("%.%s*$", "")
  local estado = meta_str(meta, "estado")

  -- Bloques posteriores al encabezado "Respuesta"
  local respuesta, dentro = {}, false
  for _, b in ipairs(doc.blocks) do
    if dentro then
      if not (b.t == "RawBlock" and b.format == "html") then
        table.insert(respuesta, b)
      end
    elseif b.t == "Header" and stringify(b.content) == "Respuesta" then
      dentro = true
    end
  end

  if estado == "omitido" then
    return pandoc.Pandoc({}, meta)
  end

  local pendiente = estado == "pendiente" or es_vacio(respuesta)
  if pendiente and not meta_bool(meta, "siempre_incluir") then
    if meta_bool(meta, "incluir_pendientes") then
      if es_vacio(respuesta) then
        respuesta = { pandoc.Para({ pandoc.Emph({ pandoc.Str("Pendiente.") }) }) }
      end
    else
      return pandoc.Pandoc({}, meta)
    end
  end

  local nivel = nivel_de(punto)

  -- Los títulos internos de la respuesta quedan por debajo del título del punto
  for i, b in ipairs(respuesta) do
    if b.t == "Header" then
      b.level = math.min(nivel + b.level - 1, 5)
      b.classes:insert("unnumbered")
      respuesta[i] = b
    end
  end

  local texto = (punto ~= "" and (punto .. " ") or "") .. titulo
  local encabezado = pandoc.Header(nivel, pandoc.Inlines(texto), pandoc.Attr("", { "unnumbered" }))
  table.insert(respuesta, 1, encabezado)

  return pandoc.Pandoc(respuesta, meta)
end

-- Las imágenes se buscan por nombre en documentacion/imagenes (ver \graphicspath en main.tex)
function Image(img)
  img.src = img.src:match("([^/]+)$")
  return img
end
