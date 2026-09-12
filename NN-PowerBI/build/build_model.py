# -*- coding: utf-8 -*-
import io, json, os, sys, uuid, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schema import (COLUMNS, CALC_COLUMNS, RELATIONSHIPS, PARAMETERS,
                    TABLE_QUERIES, HELPER_QUERIES)
from measures import MEASURES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(ROOT, "M", "queries")

def read_q(fname):
    return io.open(os.path.join(QDIR, fname + ".pq"), encoding="utf-8").read().rstrip()

def rel_id(a, b, c, d):
    return str(uuid.UUID(hashlib.md5(f"{a}|{b}|{c}|{d}".encode()).hexdigest()))

# ---------------- validação prévia ----------------
erros = []
allcols = {t: {c[0] for c in cols} for t, cols in COLUMNS.items()}
for t, cc in CALC_COLUMNS.items():
    allcols.setdefault(t, set()).update(c[0] for c in cc)

for dt, dc, ft, fc, active in RELATIONSHIPS:
    if dt not in allcols: erros.append(f"relacionamento: tabela '{dt}' inexistente")
    elif dc not in allcols[dt]: erros.append(f"relacionamento: {dt}[{dc}] inexistente")
    if ft not in allcols: erros.append(f"relacionamento: tabela '{ft}' inexistente")
    elif fc not in allcols[ft]: erros.append(f"relacionamento: {ft}[{fc}] inexistente")

for t, cols in COLUMNS.items():
    for name, dtype, fmt, sortby in cols:
        if sortby and sortby not in allcols.get(t, set()):
            erros.append(f"sortByColumn: {t}[{name}] -> '{sortby}' inexistente")

for t in TABLE_QUERIES:
    if t not in COLUMNS: erros.append(f"consulta '{t}' sem colunas declaradas")
for t in COLUMNS:
    if t not in TABLE_QUERIES: erros.append(f"tabela '{t}' sem consulta M")
    f = os.path.join(QDIR, TABLE_QUERIES.get(t, "") + ".pq")
    if t in TABLE_QUERIES and not os.path.exists(f):
        erros.append(f"arquivo M faltando: {f}")

if erros:
    print("ERROS DE CONSISTÊNCIA:")
    for e in erros: print("  -", e)
    sys.exit(1)

# ---------------- montagem do model.bim ----------------
expressions = []
for nome, expr in PARAMETERS:
    expressions.append({
        "name": nome, "kind": "m", "expression": expr,
        "queryGroup": "00 Parâmetros"})
for nome, fname in HELPER_QUERIES.items():
    expressions.append({
        "name": nome, "kind": "m", "expression": read_q(fname),
        "queryGroup": "01 Auxiliares"})

def col_obj(name, dtype, fmt, sortby, calc=False, expr=None):
    o = {"name": name, "dataType": dtype}
    if calc:
        o["type"] = "calculated"
        o["expression"] = expr
        o["isDataTypeInferred"] = False
    else:
        o["sourceColumn"] = name
    if fmt: o["formatString"] = fmt
    if sortby: o["sortByColumn"] = sortby
    if dtype == "dateTime" and not fmt: o["formatString"] = "dd/mm/yyyy"
    o["summarizeBy"] = "none"
    return o

MEASURE_TABLE = "_Medidas"
tables = []
for t, cols in COLUMNS.items():
    tbl = {"name": t, "columns": [], "partitions": [{
        "name": t, "mode": "import",
        "source": {"type": "m", "expression": read_q(TABLE_QUERIES[t])}}]}
    for name, dtype, fmt, sortby in cols:
        tbl["columns"].append(col_obj(name, dtype, fmt, sortby))
    for name, dtype, expr, fmt, sortby in CALC_COLUMNS.get(t, []):
        tbl["columns"].append(col_obj(name, dtype, fmt, sortby, calc=True, expr=expr))
    if t == "Calendário":
        tbl["dataCategory"] = "Time"
        for c in tbl["columns"]:
            if c["name"] == "Data": c["isKey"] = True
    tables.append(tbl)

# tabela dedicada só para medidas
med_tbl = {
    "name": MEASURE_TABLE,
    "columns": [{"name": "_", "dataType": "string", "sourceColumn": "_",
                 "isHidden": True, "summarizeBy": "none"}],
    "partitions": [{"name": MEASURE_TABLE, "mode": "import", "source": {
        "type": "m",
        "expression": 'let\n    Fonte = #table(type table [_ = text], {{"x"}})\nin\n    Fonte'}}],
    "measures": []}
for nome, expr, fmt, folder in MEASURES:
    m = {"name": nome, "expression": expr, "displayFolder": folder}
    if fmt: m["formatString"] = fmt
    med_tbl["measures"].append(m)
tables.append(med_tbl)

relationships = []
for dt, dc, ft, fc, active in RELATIONSHIPS:
    r = {"name": rel_id(dt, dc, ft, fc),
         "fromTable": ft, "fromColumn": fc,
         "toTable": dt, "toColumn": dc}
    if not active: r["isActive"] = False
    relationships.append(r)

model = {
    "name": "SemanticModel",
    "compatibilityLevel": 1550,
    "model": {
        "culture": "pt-BR",
        "dataAccessOptions": {"legacyRedirects": True, "returnErrorValuesAsNull": True},
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "pt-BR",
        "tables": tables,
        "relationships": relationships,
        "expressions": expressions,
        "annotations": [
            {"name": "PBI_QueryOrder", "value": json.dumps(
                [p[0] for p in PARAMETERS] + list(HELPER_QUERIES.keys()) +
                list(TABLE_QUERIES.keys()) + [MEASURE_TABLE], ensure_ascii=False)},
            {"name": "__PBI_TimeIntelligenceEnabled", "value": "0"},
            {"name": "PBIDesktopVersion", "value": "Gerado por script — Novos Negócios"},
        ],
    },
}

out = os.path.join(ROOT, "modelo", "Model.bim")
os.makedirs(os.path.dirname(out), exist_ok=True)
io.open(out, "w", encoding="utf-8").write(json.dumps(model, ensure_ascii=False, indent=2))
print(f"OK  Model.bim  ->  {out}")
print(f"    tabelas={len(tables)}  medidas={len(MEASURES)}  relacionamentos={len(relationships)}  expressões={len(expressions)}")
