# -*- coding: utf-8 -*-
"""Empacota Model.bim + Layout.json em .pbit e em projeto .pbip."""
import io, json, os, struct, sys, zipfile, shutil, codecs
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELO = os.path.join(ROOT, "modelo")
DIST = os.path.join(ROOT, "dist")
NOME = "Dashboard_Novos_Negocios"

def u16(text):
    """UTF-16LE com BOM — codificação que o Power BI usa nas partes de texto."""
    return codecs.BOM_UTF16_LE + text.encode("utf-16-le")

model = json.load(io.open(os.path.join(MODELO, "Model.bim"), encoding="utf-8"))
layout = json.load(io.open(os.path.join(MODELO, "Layout.json"), encoding="utf-8"))

# ---------------------------------------------------------------- Section1.m
def m_name(n):
    ok = n and (n[0].isalpha() or n[0] == "_") and all(c.isalnum() or c == "_" for c in n)
    return n if ok else '#"' + n.replace('"', '""') + '"'

linhas = ["section Section1;", ""]
for e in model["model"]["expressions"]:
    linhas.append(f"shared {m_name(e['name'])} = {e['expression'].rstrip()};")
    linhas.append("")
for t in model["model"]["tables"]:
    for p in t.get("partitions", []):
        src = p.get("source", {})
        if src.get("type") == "m":
            linhas.append(f"shared {m_name(t['name'])} = {src['expression'].rstrip()};")
            linhas.append("")
SECTION1 = "\n".join(linhas)

# ---------------------------------------------------------------- DataMashup
PKG_CT = ('<?xml version="1.0" encoding="utf-8"?>'
  '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
  '<Default Extension="m" ContentType="" />'
  '<Default Extension="xml" ContentType="application/xml" />'
  '</Types>')
PKG_XML = ('<?xml version="1.0" encoding="utf-8"?>'
  '<Package xmlns="http://schemas.microsoft.com/DataMashup">'
  '<Version>2.126.0.0</Version><MinVersion>2.21.0.0</MinVersion>'
  '<Culture>pt-BR</Culture></Package>')
PERMISSIONS = ('<?xml version="1.0" encoding="utf-8"?>'
  '<PermissionList xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
  'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
  '<CanEvaluateFuturePackages>false</CanEvaluateFuturePackages>'
  '<FirewallEnabled>true</FirewallEnabled></PermissionList>')
METADATA_XML = ('<?xml version="1.0" encoding="utf-8"?>'
  '<LocalPackageMetadataFile xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
  'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Items>'
  '<Item><ItemLocation><ItemType>AllFormulas</ItemType><ItemPath /></ItemLocation>'
  '<StableEntries /></Item></Items></LocalPackageMetadataFile>')

def build_package_parts():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", PKG_CT)
        z.writestr("Config/Package.xml", PKG_XML)
        z.writestr("Formulas/Section1.m", SECTION1.encode("utf-8"))
    return buf.getvalue()

def build_datamashup():
    parts = build_package_parts()
    perms = PERMISSIONS.encode("utf-8")
    meta_xml = METADATA_XML.encode("utf-8")
    # Metadata = Version(4) + XmlSize(4) + Xml + Content(4 = vazio)
    metadata = struct.pack("<I", 0) + struct.pack("<I", len(meta_xml)) + meta_xml + struct.pack("<I", 0)
    bindings = struct.pack("<I", 0)
    out = io.BytesIO()
    out.write(struct.pack("<I", 0))                 # Version
    out.write(struct.pack("<I", len(parts)));  out.write(parts)
    out.write(struct.pack("<I", len(perms)));  out.write(perms)
    out.write(struct.pack("<I", len(metadata))); out.write(metadata)
    out.write(struct.pack("<I", len(bindings))); out.write(bindings)
    return out.getvalue()

# ---------------------------------------------------------------- partes texto
CONTENT_TYPES = ('<?xml version="1.0" encoding="utf-8"?>'
  '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
  '<Default Extension="json" ContentType="" />'
  '<Override PartName="/Version" ContentType="" />'
  '<Override PartName="/DataModelSchema" ContentType="" />'
  '<Override PartName="/DiagramLayout" ContentType="" />'
  '<Override PartName="/Report/Layout" ContentType="" />'
  '<Override PartName="/Settings" ContentType="" />'
  '<Override PartName="/Metadata" ContentType="" />'
  '<Override PartName="/DataMashup" ContentType="" />'
  '</Types>')

SETTINGS = {"Version": 4, "ReportSettings": {"UseStylableVisualContainerHeader": True},
            "QueriesSettings": {"Version": 4}}
METADATA = {"Version": 3, "AutoCreatedRelationships": [],
            "FileDescription": "Dashboard Novos Negócios — gerado por script"}
DIAGRAM = {"version": "1.1.0", "diagrams": [{"ordinal": 0, "scrollPosition": {"x": 0, "y": 0},
           "nodes": [], "name": "Todas as tabelas", "zoomValue": 100, "pinKeyFieldsToTop": False,
           "showExtraHeaderInfo": False, "hideKeyFieldsWhenCollapsed": False,
           "tablesLocked": False}], "selectedDiagram": "Todas as tabelas", "defaultDiagram": "Todas as tabelas"}

def build_pbit():
    os.makedirs(DIST, exist_ok=True)
    path = os.path.join(DIST, NOME + ".pbit")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("Version", u16("1.28"))
        z.writestr("DataModelSchema", u16(json.dumps(model, ensure_ascii=False)))
        z.writestr("DataMashup", build_datamashup())
        z.writestr("Report/Layout", u16(json.dumps(layout, ensure_ascii=False)))
        z.writestr("Settings", u16(json.dumps(SETTINGS, ensure_ascii=False)))
        z.writestr("Metadata", u16(json.dumps(METADATA, ensure_ascii=False)))
        z.writestr("DiagramLayout", u16(json.dumps(DIAGRAM, ensure_ascii=False)))
    return path

def build_pbip():
    base = os.path.join(DIST, NOME + "_PBIP")
    if os.path.exists(base): shutil.rmtree(base)
    ds = os.path.join(base, NOME + ".Dataset")
    rp = os.path.join(base, NOME + ".Report")
    os.makedirs(ds); os.makedirs(rp)

    def wj(p, obj):
        io.open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False, indent=2))

    io.open(os.path.join(base, NOME + ".pbip"), "w", encoding="utf-8").write(
        json.dumps({"version": "1.0", "artifacts": [
            {"report": {"path": NOME + ".Report"}}],
            "settings": {"enableAutoRecovery": True}}, ensure_ascii=False, indent=2))

    # ---- Dataset
    wj(os.path.join(ds, "model.bim"), model)
    wj(os.path.join(ds, "definition.pbidataset"), {"version": "1.0",
        "settings": {"qnaEnabled": True}})
    wj(os.path.join(ds, "item.metadata.json"), {"type": "dataset", "displayName": NOME})
    wj(os.path.join(ds, "item.config.json"), {"version": "1.0", "logicalId":
        "00000000-0000-0000-0000-0000000000d5"})
    wj(os.path.join(ds, ".platform"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": NOME},
        "config": {"version": "2.0", "logicalId": "00000000-0000-0000-0000-0000000000d5"}})
    wj(os.path.join(ds, "diagramLayout.json"), DIAGRAM)

    # ---- Report
    wj(os.path.join(rp, "report.json"), layout)
    wj(os.path.join(rp, "definition.pbir"), {"version": "1.0",
        "datasetReference": {"byPath": {"path": "../" + NOME + ".Dataset"}}})
    wj(os.path.join(rp, "item.metadata.json"), {"type": "report", "displayName": NOME})
    wj(os.path.join(rp, "item.config.json"), {"version": "1.0", "logicalId":
        "00000000-0000-0000-0000-0000000000r5"})
    wj(os.path.join(rp, ".platform"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": NOME},
        "config": {"version": "2.0", "logicalId": "00000000-0000-0000-0000-0000000000r5"}})
    os.makedirs(os.path.join(rp, "StaticResources", "RegisteredResources"), exist_ok=True)
    return base

if __name__ == "__main__":
    p = build_pbit()
    print(f"OK  .pbit  -> {p}  ({os.path.getsize(p)/1024:.0f} KB)")
    b = build_pbip()
    print(f"OK  .pbip  -> {b}")
    io.open(os.path.join(MODELO, "Section1.m"), "w", encoding="utf-8").write(SECTION1)
    print(f"OK  Section1.m ({len(SECTION1)} chars, "
          f"{SECTION1.count('shared ')} consultas)")
