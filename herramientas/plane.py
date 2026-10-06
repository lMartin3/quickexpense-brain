#!/usr/bin/env python3
"""Cliente de línea de comandos para el Plane del proyecto (plane.atwire.net).

Pensado para que lo usen agentes y personas: lee la información del proyecto
y lista, muestra, crea, edita, comenta y borra work items. Solo usa la
biblioteca estándar de Python; si `pandoc` está instalado, las descripciones
y los comentarios se convierten entre Markdown y HTML.

Configuración (variables de entorno o el archivo herramientas/plane.env):
  PLANE_API_KEY    token personal (Plane > Profile settings > Personal access tokens)
  PLANE_WORKSPACE  slug del workspace (lo que sigue a plane.atwire.net/ en la URL)
  PLANE_PROJECT    identificador (p. ej. QE), nombre o UUID del proyecto por defecto
  PLANE_URL        opcional, por defecto https://plane.atwire.net

Ver `herramientas/plane.py --help` y `herramientas/plane.py <comando> --help`.
"""

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERRAMIENTAS = Path(__file__).resolve().parent
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
PRIORIDADES = ["urgent", "high", "medium", "low", "none"]
GRUPOS = ["backlog", "unstarted", "started", "completed", "cancelled"]


class ErrorPlane(Exception):
    pass


# --- Configuración y conversión de formatos ---------------------------------

def cargar_config():
    archivo = HERRAMIENTAS / "plane.env"
    if archivo.exists():
        for linea in archivo.read_text().splitlines():
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            os.environ.setdefault(clave.strip(), valor.strip().strip("\"'"))
    faltan = [v for v in ("PLANE_API_KEY", "PLANE_WORKSPACE") if not os.environ.get(v)]
    if faltan:
        raise ErrorPlane(f"Faltan {', '.join(faltan)}: definirlas en el entorno o en {archivo} "
                         f"(ver plane.env.ejemplo)")
    return {
        "url": os.environ.get("PLANE_URL", "https://plane.atwire.net").rstrip("/"),
        "api_key": os.environ["PLANE_API_KEY"],
        "workspace": os.environ["PLANE_WORKSPACE"],
        "proyecto": os.environ.get("PLANE_PROJECT", ""),
    }


def pandoc(texto, desde, hacia):
    if not shutil.which("pandoc"):
        return None
    r = subprocess.run(["pandoc", "-f", desde, "-t", hacia, "--wrap=none"],
                       input=texto, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def md_a_html(texto):
    convertido = pandoc(texto, "gfm", "html")
    if convertido is not None:
        return convertido
    parrafos = [p.strip() for p in re.split(r"\n\s*\n", texto) if p.strip()]
    return "".join(f"<p>{html.escape(p).replace(chr(10), '<br>')}</p>" for p in parrafos)


def html_a_md(texto):
    if not texto or texto.strip() in ("<p></p>", ""):
        return ""
    convertido = pandoc(texto, "html", "gfm")
    if convertido is not None:
        return convertido
    texto = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>", "\n", texto)
    texto = re.sub(r"<li[^>]*>", "- ", texto)
    return html.unescape(re.sub(r"<[^>]+>", "", texto)).strip()


def leer_texto(valor):
    """Devuelve el texto tal cual, o lee stdin si es '-' o un archivo si empieza con '@'."""
    if valor == "-":
        return sys.stdin.read()
    if valor.startswith("@"):
        return Path(valor[1:]).read_text()
    return valor


# --- Cliente de la API -------------------------------------------------------

class Plane:
    def __init__(self, url, api_key, workspace, proyecto=""):
        self.url = url
        self.api_key = api_key
        self.ws = f"workspaces/{workspace}"
        self.ref_proyecto = proyecto
        self._proyecto = None
        self._cache = {}

    def pedir(self, metodo, ruta, datos=None, params=None):
        url = f"{self.url}/api/v1/{ruta.lstrip('/')}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        cuerpo = json.dumps(datos).encode() if datos is not None else None
        headers = {"X-API-Key": self.api_key, "Content-Type": "application/json",
                   "Accept": "application/json", "User-Agent": "quickexpense-brain/plane.py"}
        for intento in range(5):
            req = urllib.request.Request(url, data=cuerpo, method=metodo, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    texto = r.read().decode()
                    return json.loads(texto) if texto.strip() else None
            except urllib.error.HTTPError as e:
                if e.code == 429 and intento < 4:
                    # Plane limita a 60 pedidos por minuto por token
                    reinicio = e.headers.get("X-RateLimit-Reset")
                    espera = int(e.headers.get("Retry-After") or 0) or (
                        max(1, int(reinicio) - int(time.time())) if reinicio else 10)
                    time.sleep(min(espera, 60))
                    continue
                detalle = e.read().decode(errors="replace")[:1000]
                raise ErrorPlane(f"{metodo} {ruta} -> HTTP {e.code}: {detalle}")
            except urllib.error.URLError as e:
                raise ErrorPlane(f"No se pudo conectar a {self.url}: {e.reason}")

    def listar(self, ruta, params=None):
        """GET que recorre todas las páginas (Plane pagina con cursores)."""
        params = {"per_page": 100, **(params or {})}
        resultados = []
        while True:
            r = self.pedir("GET", ruta, params=params)
            if isinstance(r, list):
                return resultados + r
            resultados += r.get("results", [])
            if not r.get("next_page_results") or not r.get("next_cursor"):
                return resultados
            params["cursor"] = r["next_cursor"]

    # Proyecto y catálogos

    def proyectos(self):
        return self.listar(f"{self.ws}/projects/")

    @property
    def proyecto(self):
        if self._proyecto is None:
            ref = self.ref_proyecto
            if not ref:
                raise ErrorPlane("No hay proyecto: definir PLANE_PROJECT o usar --proyecto")
            if UUID_RE.match(ref):
                self._proyecto = self.pedir("GET", f"{self.ws}/projects/{ref}/")
            else:
                for p in self.proyectos():
                    if ref.lower() in (p["identifier"].lower(), p["name"].lower()):
                        self._proyecto = p
                        break
                else:
                    raise ErrorPlane(f"No existe el proyecto '{ref}' (ver el comando 'proyectos')")
        return self._proyecto

    def fijar_proyecto(self, proyecto_id):
        if self._proyecto is None or self._proyecto["id"] != proyecto_id:
            self.ref_proyecto = proyecto_id
            self._proyecto = None
            self._cache = {}

    @property
    def pr(self):
        return f"{self.ws}/projects/{self.proyecto['id']}"

    def catalogo(self, nombre):
        if nombre not in self._cache:
            self._cache[nombre] = self.listar(f"{self.pr}/{nombre}/")
        return self._cache[nombre]

    def estados(self):
        return self.catalogo("states")

    def etiquetas(self):
        return self.catalogo("labels")

    def miembros(self):
        # Según la versión, cada elemento es el usuario o tiene el usuario en "member"
        return [m.get("member") if isinstance(m.get("member"), dict) else m
                for m in self.catalogo("members")]

    def ciclos(self):
        return self.catalogo("cycles")

    def modulos(self):
        return self.catalogo("modules")

    def yo(self):
        if "yo" not in self._cache:
            self._cache["yo"] = self.pedir("GET", "users/me/")
        return self._cache["yo"]

    # Resolución de nombres a UUID

    def _buscar(self, elementos, ref, claves, tipo):
        if UUID_RE.match(ref):
            return ref
        ref_l = ref.lower()
        exactos = [e for e in elementos if any(str(e.get(c) or "").lower() == ref_l for c in claves)]
        if not exactos:
            exactos = [e for e in elementos if any(ref_l in str(e.get(c) or "").lower() for c in claves)]
        if len(exactos) == 1:
            return exactos[0]["id"]
        opciones = ", ".join(str(e.get(claves[0])) for e in (exactos or elementos))
        problema = "es ambiguo" if exactos else "no existe"
        raise ErrorPlane(f"{tipo} '{ref}' {problema}. Opciones: {opciones}")

    def id_estado(self, ref):
        return self._buscar(self.estados(), ref, ["name"], "El estado")

    def id_etiqueta(self, ref):
        return self._buscar(self.etiquetas(), ref, ["name"], "La etiqueta")

    def id_miembro(self, ref):
        if ref.lower() in ("yo", "me"):
            return self.yo()["id"]
        return self._buscar(self.miembros(), ref,
                            ["display_name", "email", "first_name", "last_name"], "El miembro")

    def id_ciclo(self, ref):
        return self._buscar(self.ciclos(), ref, ["name"], "El ciclo")

    def id_modulo(self, ref):
        return self._buscar(self.modulos(), ref, ["name"], "El módulo")

    # Work items

    def item(self, ref):
        """Acepta QE-12, 12 (del proyecto actual) o el UUID."""
        ref = ref.strip()
        if UUID_RE.match(ref):
            item = self.pedir("GET", f"{self.pr}/work-items/{ref}/")
        else:
            if ref.isdigit():
                ref = f"{self.proyecto['identifier']}-{ref}"
            item = self.pedir("GET", f"{self.ws}/work-items/{ref.upper()}/")
        self.fijar_proyecto(item["project"])
        return item

    def ruta_item(self, item):
        return f"{self.ws}/projects/{item['project']}/work-items/{item['id']}"

    def items(self):
        return self.listar(f"{self.pr}/work-items/")

    def items_de(self, tipo, id_):
        ruta = {"ciclo": f"cycles/{id_}/cycle-issues", "modulo": f"modules/{id_}/module-issues"}[tipo]
        return {i["id"] if isinstance(i, dict) else i for i in self.listar(f"{self.pr}/{ruta}/")}

    def agregar_a(self, tipo, id_, item_id):
        ruta = {"ciclo": f"cycles/{id_}/cycle-issues", "modulo": f"modules/{id_}/module-issues"}[tipo]
        self.pedir("POST", f"{self.pr}/{ruta}/", {"issues": [item_id]})

    def codigo(self, item):
        return f"{self.proyecto['identifier']}-{item['sequence_id']}"


# --- Formato de salida -------------------------------------------------------

def nombres(plane):
    estados = {e["id"]: e for e in plane.estados()}
    etiquetas = {e["id"]: e["name"] for e in plane.etiquetas()}
    miembros = {m["id"]: m.get("display_name") or m.get("email") for m in plane.miembros()}
    return estados, etiquetas, miembros


def ids(valor):
    """Normaliza listas que pueden venir como UUID o como objetos expandidos."""
    return [v["id"] if isinstance(v, dict) else v for v in (valor or [])]


def linea_item(plane, item, n):
    estados, etiquetas, miembros = n
    estado = estados.get(item.get("state"), {}).get("name", "?")
    partes = [f"{plane.codigo(item):<8}", f"[{estado}]"]
    if item.get("priority") and item["priority"] != "none":
        partes.append(f"({item['priority']})")
    partes.append(item["name"])
    partes += [f"@{miembros.get(a, a)}" for a in ids(item.get("assignees"))]
    partes += [f"#{etiquetas.get(e, e)}" for e in ids(item.get("labels"))]
    if item.get("target_date"):
        partes.append(f"vence {item['target_date']}")
    return " ".join(partes)


def mostrar_item(plane, item, comentarios):
    estados, etiquetas, miembros = n = nombres(plane)
    print(f"{plane.codigo(item)}: {item['name']}")
    print(f"  id:         {item['id']}")
    estado = estados.get(item.get("state"), {})
    print(f"  estado:     {estado.get('name', '?')} ({estado.get('group', '?')})")
    print(f"  prioridad:  {item.get('priority') or 'none'}")
    print(f"  asignados:  {', '.join(miembros.get(a, a) for a in ids(item.get('assignees'))) or '-'}")
    print(f"  etiquetas:  {', '.join(etiquetas.get(e, e) for e in ids(item.get('labels'))) or '-'}")
    print(f"  inicio:     {item.get('start_date') or '-'}")
    print(f"  vence:      {item.get('target_date') or '-'}")
    if item.get("parent"):
        try:
            padre = plane.pedir("GET", f"{plane.pr}/work-items/{item['parent']}/")
            print(f"  padre:      {plane.codigo(padre)} {padre['name']}")
        except ErrorPlane:
            print(f"  padre:      {item['parent']}")
    print(f"  creado:     {item.get('created_at', '')[:16]}  actualizado: {item.get('updated_at', '')[:16]}")
    print(f"  url:        {plane.url}/{plane.ws.split('/')[1]}/browse/{plane.codigo(item)}/")
    descripcion = html_a_md(item.get("description_html") or "") or item.get("description_stripped") or ""
    print("\nDescripción:\n" + (descripcion or "(vacía)"))
    if comentarios is not None:
        print(f"\nComentarios ({len(comentarios)}):")
        for c in comentarios:
            autor = miembros.get(c.get("actor") or c.get("created_by"), "?")
            print(f"- {autor}, {c.get('created_at', '')[:16]}:")
            print("  " + html_a_md(c.get("comment_html") or "").replace("\n", "\n  "))


def imprimir_json(datos):
    print(json.dumps(datos, ensure_ascii=False, indent=2))


# --- Comandos ----------------------------------------------------------------

def cmd_yo(plane, a):
    yo = plane.yo()
    if a.json:
        return imprimir_json(yo)
    print(f"{yo.get('display_name')} <{yo.get('email')}> id={yo['id']}")


def cmd_proyectos(plane, a):
    proyectos = plane.proyectos()
    if a.json:
        return imprimir_json(proyectos)
    for p in proyectos:
        print(f"{p['identifier']:<8} {p['name']}  id={p['id']}")


def cmd_proyecto(plane, a):
    p = plane.proyecto
    if a.json:
        return imprimir_json({"proyecto": p, "estados": plane.estados(), "etiquetas": plane.etiquetas(),
                              "miembros": plane.miembros(), "ciclos": plane.ciclos(),
                              "modulos": plane.modulos()})
    print(f"{p['identifier']}: {p['name']}  id={p['id']}")
    if p.get("description"):
        print(p["description"])
    print()
    for comando in (cmd_estados, cmd_etiquetas, cmd_miembros, cmd_ciclos, cmd_modulos):
        comando(plane, a)
        print()


def cmd_estados(plane, a):
    if a.json:
        return imprimir_json(plane.estados())
    print("Estados (nombre - grupo):")
    for e in sorted(plane.estados(), key=lambda e: (GRUPOS.index(e["group"]) if e["group"] in GRUPOS else 9,
                                                   e.get("sequence", 0))):
        print(f"  {e['name']} - {e['group']}{' (por defecto)' if e.get('default') else ''}")


def cmd_etiquetas(plane, a):
    if a.json:
        return imprimir_json(plane.etiquetas())
    print("Etiquetas: " + (", ".join(e["name"] for e in plane.etiquetas()) or "-"))


def cmd_miembros(plane, a):
    if a.json:
        return imprimir_json(plane.miembros())
    print("Miembros:")
    for m in plane.miembros():
        print(f"  {m.get('display_name')} <{m.get('email', '')}>")


def cmd_ciclos(plane, a):
    if a.json:
        return imprimir_json(plane.ciclos())
    print("Ciclos:")
    for c in plane.ciclos():
        print(f"  {c['name']}  {c.get('start_date') or '?'} -> {c.get('end_date') or '?'}")


def cmd_modulos(plane, a):
    if a.json:
        return imprimir_json(plane.modulos())
    print("Módulos:")
    for m in plane.modulos():
        print(f"  {m['name']} ({m.get('status', '')})")


def cmd_items(plane, a):
    items = plane.items()
    estados = {e["id"]: e for e in plane.estados()}
    if a.estado:
        buscados = {plane.id_estado(e) for e in a.estado}
        items = [i for i in items if i.get("state") in buscados]
    if a.grupo:
        items = [i for i in items if estados.get(i.get("state"), {}).get("group") in a.grupo]
    if a.abiertos:
        items = [i for i in items
                 if estados.get(i.get("state"), {}).get("group") not in ("completed", "cancelled")]
    if a.asignado:
        buscados = {plane.id_miembro(m) for m in a.asignado}
        items = [i for i in items if buscados & set(ids(i.get("assignees")))]
    if a.etiqueta:
        buscadas = {plane.id_etiqueta(e) for e in a.etiqueta}
        items = [i for i in items if buscadas & set(ids(i.get("labels")))]
    if a.prioridad:
        items = [i for i in items if (i.get("priority") or "none") in a.prioridad]
    if a.buscar:
        texto = a.buscar.lower()
        items = [i for i in items if texto in i["name"].lower()
                 or texto in (i.get("description_stripped") or "").lower()]
    if a.ciclo:
        items = [i for i in items if i["id"] in plane.items_de("ciclo", plane.id_ciclo(a.ciclo))]
    if a.modulo:
        items = [i for i in items if i["id"] in plane.items_de("modulo", plane.id_modulo(a.modulo))]
    items.sort(key=lambda i: i["sequence_id"])
    if a.limite:
        items = items[:a.limite]
    if a.json:
        return imprimir_json(items)
    n = nombres(plane)
    for i in items:
        print(linea_item(plane, i, n))
    print(f"({len(items)} work items)", file=sys.stderr)


def cmd_ver(plane, a):
    item = plane.item(a.ref)
    comentarios = None if a.sin_comentarios else plane.listar(f"{plane.ruta_item(item)}/comments/")
    if a.json:
        return imprimir_json({**item, "comentarios": comentarios} if comentarios is not None else item)
    mostrar_item(plane, item, comentarios)


def datos_item(plane, a, item=None):
    """Arma el cuerpo de crear/editar. Con `item`, etiquetas y asignados se suman a los actuales."""
    datos = {}
    if a.titulo:
        datos["name"] = a.titulo
    if a.descripcion is not None:
        datos["description_html"] = md_a_html(leer_texto(a.descripcion))
    if a.estado:
        datos["state"] = plane.id_estado(a.estado)
    if a.prioridad:
        datos["priority"] = a.prioridad
    for campo, valor in (("start_date", a.inicio), ("target_date", a.vence)):
        if valor is not None:
            datos[campo] = valor or None
    if a.padre is not None:
        datos["parent"] = plane.item(a.padre)["id"] if a.padre else None
    for campo, agregar, quitar, resolver in (
            ("labels", a.etiqueta, getattr(a, "quitar_etiqueta", None), plane.id_etiqueta),
            ("assignees", a.asignado, getattr(a, "quitar_asignado", None), plane.id_miembro)):
        if not agregar and not quitar:
            continue
        actuales = ids(item.get(campo)) if item else []
        nuevos = [resolver(v) for v in agregar or []]
        sacar = {resolver(v) for v in quitar or []}
        datos[campo] = [v for v in dict.fromkeys(actuales + nuevos) if v not in sacar]
    return datos


def asociar(plane, a, item):
    if a.ciclo:
        plane.agregar_a("ciclo", plane.id_ciclo(a.ciclo), item["id"])
    if a.modulo:
        plane.agregar_a("modulo", plane.id_modulo(a.modulo), item["id"])


def cmd_crear(plane, a):
    datos = datos_item(plane, a)
    item = plane.pedir("POST", f"{plane.pr}/work-items/", datos)
    asociar(plane, a, item)
    if a.json:
        return imprimir_json(item)
    print(f"Creado {plane.codigo(item)}: {item['name']}")


def cmd_editar(plane, a):
    item = plane.item(a.ref)
    datos = datos_item(plane, a, item)
    if datos:
        item = plane.pedir("PATCH", f"{plane.ruta_item(item)}/", datos)
    elif not (a.ciclo or a.modulo):
        raise ErrorPlane("No se indicó ningún cambio (ver editar --help)")
    asociar(plane, a, item)
    if a.json:
        return imprimir_json(item)
    print(f"Actualizado {plane.codigo(item)}: {', '.join(datos) or 'asociaciones'}")


def cmd_comentar(plane, a):
    item = plane.item(a.ref)
    comentario = plane.pedir("POST", f"{plane.ruta_item(item)}/comments/",
                             {"comment_html": md_a_html(leer_texto(a.texto))})
    if a.json:
        return imprimir_json(comentario)
    print(f"Comentario agregado a {plane.codigo(item)}")


def cmd_borrar(plane, a):
    item = plane.item(a.ref)
    if not a.confirmar:
        raise ErrorPlane(f"Para borrar {plane.codigo(item)} ('{item['name']}') agregar --confirmar")
    plane.pedir("DELETE", f"{plane.ruta_item(item)}/")
    print(f"Borrado {plane.codigo(item)}: {item['name']}")


def cmd_crear_etiqueta(plane, a):
    datos = {"name": a.nombre}
    if a.color:
        datos["color"] = a.color
    etiqueta = plane.pedir("POST", f"{plane.pr}/labels/", datos)
    if a.json:
        return imprimir_json(etiqueta)
    print(f"Etiqueta creada: {etiqueta['name']}")


def cmd_api(plane, a):
    ruta = a.ruta.replace("{ws}", plane.ws)
    if "{proyecto}" in ruta:
        ruta = ruta.replace("{proyecto}", plane.pr)
    datos = json.loads(leer_texto(a.datos)) if a.datos else None
    imprimir_json(plane.pedir(a.metodo.upper(), ruta, datos))


# --- Argumentos --------------------------------------------------------------

def argumentos():
    comun = argparse.ArgumentParser(add_help=False)
    comun.add_argument("--json", action="store_true", help="salida en JSON crudo de la API")
    comun.add_argument("--proyecto", help="identificador, nombre o UUID (por defecto PLANE_PROJECT)")

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="comando", required=True, metavar="comando")

    def comando(nombre, funcion, ayuda):
        s = sub.add_parser(nombre, help=ayuda, description=ayuda, parents=[comun])
        s.set_defaults(funcion=funcion)
        return s

    comando("yo", cmd_yo, "usuario dueño del token (sirve para probar la conexión)")
    comando("proyectos", cmd_proyectos, "proyectos del workspace")
    comando("proyecto", cmd_proyecto, "resumen del proyecto: estados, etiquetas, miembros, ciclos y módulos")
    comando("estados", cmd_estados, "estados del proyecto")
    comando("etiquetas", cmd_etiquetas, "etiquetas del proyecto")
    comando("miembros", cmd_miembros, "miembros del proyecto")
    comando("ciclos", cmd_ciclos, "ciclos del proyecto")
    comando("modulos", cmd_modulos, "módulos del proyecto")

    s = comando("items", cmd_items, "lista work items (los filtros se pueden repetir)")
    s.add_argument("--estado", action="append", help="nombre del estado")
    s.add_argument("--grupo", action="append", choices=GRUPOS, help="grupo de estado")
    s.add_argument("--abiertos", action="store_true", help="excluye los completados y cancelados")
    s.add_argument("--asignado", action="append", help="miembro (nombre, email o 'yo')")
    s.add_argument("--etiqueta", action="append", help="nombre de la etiqueta")
    s.add_argument("--prioridad", action="append", choices=PRIORIDADES)
    s.add_argument("--buscar", help="texto en el título o la descripción")
    s.add_argument("--ciclo", help="nombre del ciclo")
    s.add_argument("--modulo", help="nombre del módulo")
    s.add_argument("--limite", type=int, help="cantidad máxima de resultados")

    s = comando("ver", cmd_ver, "muestra un work item con su descripción y comentarios")
    s.add_argument("ref", help="QE-12, 12 o UUID")
    s.add_argument("--sin-comentarios", action="store_true")

    def campos(s, editar):
        s.add_argument("--descripcion", help="Markdown; '-' lee stdin, '@archivo' lee un archivo")
        s.add_argument("--estado", help="nombre del estado")
        s.add_argument("--prioridad", choices=PRIORIDADES)
        s.add_argument("--etiqueta", action="append", help="etiqueta a " + ("agregar" if editar else "poner"))
        s.add_argument("--asignado", action="append", help="miembro a " + ("agregar" if editar else "asignar")
                       + " (nombre, email o 'yo')")
        s.add_argument("--inicio", help="fecha de inicio AAAA-MM-DD" + (" ('' la borra)" if editar else ""))
        s.add_argument("--vence", help="fecha límite AAAA-MM-DD" + (" ('' la borra)" if editar else ""))
        s.add_argument("--padre", help="work item padre (QE-12)" + (" ('' lo quita)" if editar else ""))
        s.add_argument("--ciclo", help="agrega el item a este ciclo")
        s.add_argument("--modulo", help="agrega el item a este módulo")
        if editar:
            s.add_argument("--titulo", help="nuevo título")
            s.add_argument("--quitar-etiqueta", action="append")
            s.add_argument("--quitar-asignado", action="append")

    s = comando("crear", cmd_crear, "crea un work item")
    s.add_argument("titulo")
    campos(s, editar=False)

    s = comando("editar", cmd_editar, "modifica un work item; etiquetas y asignados se suman a los actuales")
    s.add_argument("ref", help="QE-12, 12 o UUID")
    campos(s, editar=True)

    s = comando("comentar", cmd_comentar, "agrega un comentario a un work item")
    s.add_argument("ref", help="QE-12, 12 o UUID")
    s.add_argument("texto", help="Markdown; '-' lee stdin, '@archivo' lee un archivo")

    s = comando("borrar", cmd_borrar, "borra un work item (requiere --confirmar)")
    s.add_argument("ref", help="QE-12, 12 o UUID")
    s.add_argument("--confirmar", action="store_true")

    s = comando("crear-etiqueta", cmd_crear_etiqueta, "crea una etiqueta en el proyecto")
    s.add_argument("nombre")
    s.add_argument("--color", help="hexadecimal, p. ej. #3b82f6")

    s = comando("api", cmd_api, "pedido crudo a /api/v1/ para lo que no cubren los otros comandos. "
                                "En la ruta, {ws} se reemplaza por el workspace y {proyecto} por "
                                "workspaces/<ws>/projects/<id>")
    s.add_argument("metodo", help="GET, POST, PATCH o DELETE")
    s.add_argument("ruta", help="p. ej. '{proyecto}/work-items/<id>/links/'")
    s.add_argument("--datos", help="cuerpo JSON; '-' lee stdin, '@archivo' lee un archivo")

    return p.parse_args()


def main():
    a = argumentos()
    try:
        config = cargar_config()
        if a.proyecto:
            config["proyecto"] = a.proyecto
        a.funcion(Plane(**config), a)
    except ErrorPlane as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
