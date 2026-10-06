-- Filtro de pandoc: convierte la tabla "Campo | Valor" de 00 - Preliminares/Carátula.md
-- en macros de LaTeX (\qeProyecto, \qeAlumno, etc.) que usa latex/main.tex.

local stringify = pandoc.utils.stringify

local macros = {
  ["Universidad"] = "qeUniversidad",
  ["Facultad"] = "qeFacultad",
  ["Carrera"] = "qeCarrera",
  ["Materia"] = "qeMateria",
  ["Nombre del proyecto"] = "qeProyecto",
  ["Alumno"] = "qeAlumno",
  ["Legajo"] = "qeLegajo",
  ["Sede / localización"] = "qeSede",
  ["Docentes"] = "qeDocentes",
  ["Fecha"] = "qeFecha",
}

local function latex(inlines)
  return pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), "latex"):gsub("%s+$", "")
end

local function definir(nombre, valor)
  return string.format("\\newcommand{\\%s}{%s}", nombre, valor)
end

function Pandoc(doc)
  local salida = {}
  for _, b in ipairs(doc.blocks) do
    if b.t == "Table" then
      for _, body in ipairs(b.bodies) do
        for _, fila in ipairs(body.body) do
          local campo = stringify(fila.cells[1].contents)
          local nombre = macros[campo]
          if nombre then
            local inlines = pandoc.utils.blocks_to_inlines(fila.cells[2].contents)
            local valor = latex(inlines)
            if nombre == "qeDocentes" then
              valor = valor:gsub("%s*;%s*", "\\\\ ")
            end
            table.insert(salida, definir(nombre, valor))
            if nombre == "qeAlumno" then
              -- "Apellido, Nombre" → "Nombre Apellido" para el encabezado de página
              local apellido, nombres = stringify(inlines):match("^(.-),%s*(.+)$")
              local autor = apellido and (nombres .. " " .. apellido) or stringify(inlines)
              table.insert(salida, definir("qeAutor", latex(pandoc.Inlines(autor))))
            end
          end
        end
      end
      break
    end
  end
  return pandoc.Pandoc({ pandoc.RawBlock("latex", table.concat(salida, "\n")) })
end
