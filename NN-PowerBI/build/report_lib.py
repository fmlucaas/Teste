# -*- coding: utf-8 -*-
"""Helpers para gerar Report/Layout do Power BI."""
import json, itertools

_ctr = itertools.count(1)
def vid(prefix="v"):
    return f"{prefix}{next(_ctr):04d}aaaaaaaaaaaa"

AZUL      = "#1F5FA9"
AZUL_CLR  = "#3C8DDE"
VERDE     = "#2E7D4F"
VERMELHO  = "#C0392B"
LARANJA   = "#E08A1E"
CINZA     = "#5A6672"
FUNDO     = "#F4F6F9"
BRANCO    = "#FFFFFF"

def _lit(v):
    if isinstance(v, bool):  return {"Literal": {"Value": "true" if v else "false"}}
    if isinstance(v, (int, float)): return {"Literal": {"Value": f"{v}D"}}
    return {"Literal": {"Value": f"'{v}'"}}

def solid(color):
    return {"solid": {"color": {"expr": _lit(color)}}}

def prop(v):
    return {"expr": _lit(v)} if not isinstance(v, dict) else v


class Query:
    """Monta prototypeQuery + projections a partir de campos declarados."""
    def __init__(self):
        self.src = {}
        self.sel = []
        self.proj = {}
        self._alias = itertools.count(0)

    def _ent(self, entity):
        if entity not in self.src:
            self.src[entity] = chr(ord('a') + len(self.src))
        return self.src[entity]

    def add(self, role, entity, prop_name, kind="column", agg=None, name=None):
        a = self._ent(entity)
        ref = name or f"{entity}.{prop_name}"
        if kind == "measure":
            item = {"Measure": {"Expression": {"SourceRef": {"Source": a}},
                                "Property": prop_name}, "Name": ref}
        elif kind == "agg":
            item = {"Aggregation": {"Expression": {"Column": {
                        "Expression": {"SourceRef": {"Source": a}},
                        "Property": prop_name}}, "Function": agg},
                    "Name": f"{agg_name(agg)}({entity}.{prop_name})"}
            ref = item["Name"]
        else:
            item = {"Column": {"Expression": {"SourceRef": {"Source": a}},
                               "Property": prop_name}, "Name": ref}
        self.sel.append(item)
        self.proj.setdefault(role, []).append({"queryRef": ref})
        return ref

    def build(self, order_by=None, top=None):
        q = {"Version": 2,
             "From": [{"Name": a, "Entity": e, "Type": 0} for e, a in self.src.items()],
             "Select": self.sel}
        if order_by:
            ref, desc = order_by
            match = next((s for s in self.sel if s["Name"] == ref), None)
            if match:
                expr = {k: v for k, v in match.items() if k != "Name"}
                q["OrderBy"] = [{"Direction": 2 if desc else 1, "Expression": expr}]
        if top: q["Top"] = top
        return q


def agg_name(a):
    return {0: "Sum", 1: "Avg", 2: "Min", 3: "Max", 4: "Count", 5: "CountNonNull"}.get(a, "Sum")


def container(vtype, x, y, w, h, q, *, title=None, objects=None,
              vcobjects=None, order_by=None, top=None, z=None, tab=0,
              hide_title=False, extra_single=None):
    cfg = {
        "name": vid(),
        "layouts": [{"id": 0, "position": {
            "x": x, "y": y, "z": z if z is not None else tab,
            "width": w, "height": h, "tabOrder": tab}}],
        "singleVisual": {
            "visualType": vtype,
            "projections": q.proj if q else {},
            "drillFilterOtherVisuals": True,
        },
    }
    if q: cfg["singleVisual"]["prototypeQuery"] = q.build(order_by, top)
    if objects: cfg["singleVisual"]["objects"] = objects
    if extra_single: cfg["singleVisual"].update(extra_single)

    vco = vcobjects or {}
    t = {"show": prop(not hide_title and title is not None)}
    if title:
        t.update({"text": prop(title), "fontColor": prop(solid(AZUL)),
                  "fontSize": prop(11.0), "bold": prop(True),
                  "alignment": prop("center")})
    vco.setdefault("title", [{"properties": t}])
    vco.setdefault("background", [{"properties": {
        "show": prop(True), "color": prop(solid(BRANCO)), "transparency": prop(0.0)}}])
    vco.setdefault("border", [{"properties": {
        "show": prop(True), "color": prop(solid("#E3E8EF")), "radius": prop(6.0)}}])
    cfg["singleVisual"]["vcObjects"] = vco

    return {"x": x, "y": y, "z": z if z is not None else tab,
            "width": w, "height": h, "tabOrder": tab,
            "config": json.dumps(cfg, ensure_ascii=False),
            "filters": "[]"}


def textbox(x, y, w, h, runs, *, align="left", z=0):
    paragraphs = []
    for line in runs:
        tr = []
        for txt, style in line:
            tr.append({"value": txt, "textStyle": style})
        paragraphs.append({"horizontalTextAlignment": align, "textRuns": tr})
    cfg = {
        "name": vid("t"),
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z,
                                           "width": w, "height": h, "tabOrder": z}}],
        "singleVisual": {
            "visualType": "textbox",
            "drillFilterOtherVisuals": True,
            "objects": {"general": [{"properties": {"paragraphs": paragraphs}}]},
            "vcObjects": {"background": [{"properties": {"show": prop(False)}}],
                          "border": [{"properties": {"show": prop(False)}}],
                          "title": [{"properties": {"show": prop(False)}}]},
        },
    }
    return {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z,
            "config": json.dumps(cfg, ensure_ascii=False), "filters": "[]"}


def shape(x, y, w, h, color, *, z=-1, radius=8.0):
    cfg = {
        "name": vid("s"),
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z,
                                           "width": w, "height": h, "tabOrder": z}}],
        "singleVisual": {
            "visualType": "shape",
            "drillFilterOtherVisuals": True,
            "objects": {
                "shape": [{"properties": {"tileShape": prop("rectangle"),
                                          "roundEdge": prop(radius)}}],
                "fill": [{"properties": {"show": prop(True),
                                         "fillColor": prop(solid(color)),
                                         "transparency": prop(0.0)}}],
                "outline": [{"properties": {"show": prop(False)}}],
            },
            "vcObjects": {"background": [{"properties": {"show": prop(False)}}],
                          "title": [{"properties": {"show": prop(False)}}]},
        },
    }
    return {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z,
            "config": json.dumps(cfg, ensure_ascii=False), "filters": "[]"}


def kpi_card(x, y, w, h, entity, measure, label, color=AZUL):
    q = Query(); q.add("Values", entity, measure, kind="measure")
    objs = {
        "labels": [{"properties": {"color": prop(solid(color)),
                                   "fontSize": prop(26.0), "bold": prop(True)}}],
        "categoryLabels": [{"properties": {"show": prop(False)}}],
    }
    vco = {"title": [{"properties": {
        "show": prop(True), "text": prop(label), "fontColor": prop(solid(CINZA)),
        "fontSize": prop(10.0), "bold": prop(True), "alignment": prop("center")}}]}
    return container("card", x, y, w, h, q, objects=objs, vcobjects=vco)


def slicer(x, y, w, h, entity, column, title, *, dropdown=True):
    q = Query(); q.add("Values", entity, column)
    objs = {}
    if dropdown:
        objs["general"] = [{"properties": {"mode": prop("Dropdown")}}]
    objs["header"] = [{"properties": {"show": prop(True), "text": prop(title),
                                      "fontSize": prop(9.0)}}]
    return container("slicer", x, y, w, h, q, objects=objs, hide_title=True)


def page(name, display, visuals, *, w=1280, h=720, bg=FUNDO, ordinal=0):
    return {
        "id": ordinal,
        "name": name,
        "displayName": display,
        "filters": "[]",
        "ordinal": ordinal,
        "visualContainers": visuals,
        "width": w, "height": h,
        "config": json.dumps({
            "visibility": 0,
            "objects": {"background": [{"properties": {
                "color": prop(solid(bg)), "transparency": prop(0.0)}}]},
        }, ensure_ascii=False),
        "displayOption": 1,
    }
