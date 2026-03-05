from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

from models import Tarea, Usuario


def _dt_to_iso(d: date | datetime | None) -> str | None:
    if d is None:
        return None
    return d.isoformat()


def _dt_from_iso_date(s: str | None) -> date | None:
    if not s:
        return None
    return date.fromisoformat(s)


def _dt_from_iso_datetime(s: str | None) -> datetime | None:
    if not s:
        return None
    return datetime.fromisoformat(s)


def save_state(
    *,
    path: str | Path,
    usuarios: list[Usuario],
    tareas: list[Tarea],
    siguiente_usuario_id: int,
    siguiente_tarea_id: int,
) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    data: dict[str, Any] = {
        "counters": {
            "siguiente_usuario_id": siguiente_usuario_id,
            "siguiente_tarea_id": siguiente_tarea_id,
        },
        "usuarios": [asdict(u) for u in usuarios],
        "tareas": [
            {
                "id": t.id,
                "descripcion": t.descripcion,
                "prioridad": t.prioridad,
                "fecha_max": _dt_to_iso(t.fecha_max),
                "fecha_creado": _dt_to_iso(t.fecha_creado),
                "fecha_realizada": _dt_to_iso(t.fecha_realizada),
                "creador_id": (t.creador.id if t.creador else None),
                "completador_id": (t.completador.id if t.completador else None),
                "tipo_tarea": t.tipo_tarea,
                "completo": t.completo,
            }
            for t in tareas
        ],
    }

    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def load_state(
    *,
    path: str | Path,
) -> tuple[list[Usuario], list[Tarea], int, int]:
    p = Path(path)
    if not p.exists():
        return [], [], 1, 1

    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], [], 1, 1

    usuarios_raw = raw.get("usuarios", [])
    tareas_raw = raw.get("tareas", [])
    counters = raw.get("counters", {})

    usuarios: list[Usuario] = []
    for u in usuarios_raw:
        try:
            usuarios.append(Usuario(id=int(u["id"]), nombre=str(u["nombre"])))
        except Exception:
            continue

    usuarios_por_id = {u.id: u for u in usuarios}

    tareas: list[Tarea] = []
    for t in tareas_raw:
        try:
            tarea = Tarea(
                id=int(t["id"]),
                descripcion=str(t["descripcion"]),
                prioridad=int(t.get("prioridad", 3)),
                fecha_max=_dt_from_iso_date(t.get("fecha_max")),
                fecha_creado=_dt_from_iso_datetime(t.get("fecha_creado"))
                or datetime.now(),
                fecha_realizada=_dt_from_iso_datetime(t.get("fecha_realizada")),
                creador=usuarios_por_id.get(t.get("creador_id")),
                completador=usuarios_por_id.get(t.get("completador_id")),
                tipo_tarea=t.get("tipo_tarea"),
                completo=bool(t.get("completo", False)),
            )
            tareas.append(tarea)
        except Exception:
            continue

    siguiente_usuario_id = int(counters.get("siguiente_usuario_id") or (max([u.id for u in usuarios], default=0) + 1))
    siguiente_tarea_id = int(counters.get("siguiente_tarea_id") or (max([t.id for t in tareas], default=0) + 1))

    return usuarios, tareas, siguiente_usuario_id, siguiente_tarea_id

