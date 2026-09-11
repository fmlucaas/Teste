# -*- coding: utf-8 -*-
"""Converte os documentos Markdown do projeto em PDF legível."""
import io, os, re, sys
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, Preformatted, KeepTogether)

F = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DJ",   f"{F}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJ-B", f"{F}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DJ-I", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DJM",  f"{F}/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DJM-B",f"{F}/DejaVuSansMono-Bold.ttf"))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ-I")

AZUL   = colors.HexColor("#1F5FA9")
AZUL_E = colors.HexColor("#123E73")
CINZA  = colors.HexColor("#5A6672")
LINHA  = colors.HexColor("#D8DFE8")
FUNDO  = colors.HexColor("#F4F6F9")
DEST   = colors.HexColor("#FFF8E1")

# emoji não existem no DejaVu -> viram texto
EMOJI = {"⚠️":"[!]", "⚠":"[!]", "🔴":"[vermelho]", "🟡":"[amarelo]", "🟢":"[verde]",
         "🔵":"[azul]", "🟠":"[laranja]", "⚪":"[branco]", "⚫":"[preto]",
         "✅":"[sim]", "❌":"[nao]", "→":"->", "←":"<-", "▼":"v", "···":"...",
         "½":"1/2", "¼":"1/4"}

def limpa(t):
    for k, v in EMOJI.items(): t = t.replace(k, v)
    return t

def esc(t):
    return (t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def inline(t):
    """Converte marcação inline do Markdown para as tags do ReportLab.

    Os trechos `código` saem primeiro como sentinelas — senão eles partem a
    string no meio e um **negrito** que atravessa o código não é reconhecido.
    """
    t = limpa(t)
    codigos = []
    def guarda(m):
        codigos.append(m.group(1))
        return f"\x00{len(codigos)-1}\x00"
    t = re.sub(r'`([^`]+)`', guarda, t)

    e = esc(t)
    e = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
               r'<link href="\2" color="#1F5FA9"><u>\1</u></link>', e)
    e = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', e)
    e = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', e)
    e = e.replace("\\|", "|")

    def devolve(m):
        c = esc(codigos[int(m.group(1))])
        return f'<font face="DJM" size="8.5" color="#B03A2E">{c}</font>'
    return re.sub(r'\x00(\d+)\x00', devolve, e)


ss = getSampleStyleSheet()
def st(name, **kw):
    base = dict(fontName="DJ", fontSize=9.5, leading=14, textColor=colors.HexColor("#1F2933"),
                spaceAfter=5, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
 "h1": st("h1", fontName="DJ-B", fontSize=19, leading=24, textColor=AZUL_E, spaceBefore=6, spaceAfter=12),
 "h2": st("h2", fontName="DJ-B", fontSize=14, leading=19, textColor=AZUL,   spaceBefore=16, spaceAfter=7),
 "h3": st("h3", fontName="DJ-B", fontSize=11, leading=15, textColor=AZUL_E, spaceBefore=11, spaceAfter=5),
 "h4": st("h4", fontName="DJ-B", fontSize=10, leading=14, textColor=CINZA,  spaceBefore=8,  spaceAfter=4),
 "p":  st("p"),
 "li": st("li", leftIndent=13, bulletIndent=4, spaceAfter=3),
 "quote": st("quote", leftIndent=9, rightIndent=6, fontSize=9, leading=13.5,
             textColor=colors.HexColor("#59460B"), spaceBefore=4, spaceAfter=4),
 "th": st("th", fontName="DJ-B", fontSize=8, leading=11, textColor=colors.white, spaceAfter=0),
 "td": st("td", fontSize=8, leading=11, spaceAfter=0),
}
CODE = ParagraphStyle("code", fontName="DJM", fontSize=7.4, leading=9.6,
                      textColor=colors.HexColor("#1F2933"))

def tabela(linhas, largura):
    linhas = [l for l in linhas if not re.match(r'^\s*\|[\s:\-|]+\|\s*$', l)]
    if not linhas: return None
    rows = []
    for l in linhas:
        cel = [c.strip() for c in l.strip().strip("|").split("|")]
        rows.append(cel)
    n = max(len(r) for r in rows)
    rows = [r + [""] * (n - len(r)) for r in rows]
    dados = [[Paragraph(inline(c), S["th"] if i == 0 else S["td"]) for c in r]
             for i, r in enumerate(rows)]
    # 1ª coluna um pouco mais larga quando há muitas colunas
    if n == 1: w = [largura]
    elif n == 2: w = [largura*0.34, largura*0.66]
    else:
        prim = 0.26 if n <= 4 else 0.22
        w = [largura*prim] + [largura*(1-prim)/(n-1)]*(n-1)
    t = Table(dados, colWidths=w, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, FUNDO]),
        ("GRID", (0,0), (-1,-1), 0.4, LINHA),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 3.5), ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
    ]))
    return t

def bloco_codigo(linhas, largura):
    txt = limpa("\n".join(linhas))
    # trunca linhas absurdamente longas para não estourar a página
    txt = "\n".join(l[:150] for l in txt.split("\n"))
    p = Preformatted(txt, CODE)
    t = Table([[p]], colWidths=[largura], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), FUNDO),
        ("BOX", (0,0), (-1,-1), 0.5, LINHA),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return t

def citacao(linhas, largura):
    txt = " ".join(l.lstrip("> ").rstrip() for l in linhas).strip()
    if not txt: return None
    p = Paragraph(inline(txt), S["quote"])
    t = Table([[p]], colWidths=[largura], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DEST),
        ("LINEBEFORE", (0,0), (0,-1), 2.5, colors.HexColor("#E0A800")),
        ("LEFTPADDING", (0,0), (-1,-1), 9), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return t

BLOCO = re.compile(r'^\s*(?:[-*]\s|\d+\.\s|#{1,4}\s|>|\||```|-{3,}\s*$)')

def continua(linhas, i):
    """Devolve o texto do parágrafo/item começando em i, juntando as linhas
    seguintes que forem continuação (o Markdown quebra por largura, não por
    parágrafo — sem isso cada quebra virava um parágrafo solto no PDF)."""
    partes = [linhas[i].strip()]
    j = i + 1
    while j < len(linhas):
        nxt = linhas[j]
        if not nxt.strip() or BLOCO.match(nxt): break
        partes.append(nxt.strip()); j += 1
    return " ".join(partes), j


def converte(md_path, pdf_path, subtitulo=""):
    linhas = io.open(md_path, encoding="utf-8").read().split("\n")
    largura = A4[0] - 34*mm
    flow, i = [], 0
    buf_t, buf_c, buf_q = [], [], []
    em_codigo = False

    def fecha_tabela():
        if buf_t:
            t = tabela(list(buf_t), largura)
            if t: flow.extend([Spacer(1, 3), t, Spacer(1, 7)])
            buf_t.clear()
    def fecha_cit():
        if buf_q:
            c = citacao(list(buf_q), largura)
            if c: flow.extend([Spacer(1, 2), c, Spacer(1, 6)])
            buf_q.clear()

    while i < len(linhas):
        l = linhas[i].rstrip()
        if l.strip().startswith("```"):
            if em_codigo:
                flow.extend([Spacer(1, 3), bloco_codigo(buf_c, largura), Spacer(1, 7)])
                buf_c.clear(); em_codigo = False
            else:
                fecha_tabela(); fecha_cit(); em_codigo = True
            i += 1; continue
        if em_codigo:
            buf_c.append(linhas[i]); i += 1; continue
        if l.strip().startswith("|"):
            fecha_cit(); buf_t.append(l); i += 1; continue
        fecha_tabela()
        if l.startswith(">"):
            buf_q.append(l); i += 1; continue
        fecha_cit()

        if not l.strip():
            i += 1; continue
        if re.match(r'^-{3,}$', l.strip()):
            flow.append(Spacer(1, 5))
            flow.append(Table([[""]], colWidths=[largura],
                        style=[("LINEBELOW", (0,0), (-1,-1), 0.6, LINHA)], hAlign="LEFT"))
            flow.append(Spacer(1, 7)); i += 1; continue
        m = re.match(r'^(#{1,4})\s+(.*)$', l)
        if m:
            niv = len(m.group(1))
            flow.append(Paragraph(inline(m.group(2)), S[f"h{niv}"]))
            i += 1; continue
        m = re.match(r'^\s*[-*]\s+(.*)$', l)
        if m:
            txt, i = continua(linhas, i)
            txt = re.sub(r'^\s*[-*]\s+', '', txt)
            flow.append(Paragraph(inline(txt), S["li"], bulletText="•"))
            continue
        m = re.match(r'^\s*(\d+)\.\s+(.*)$', l)
        if m:
            num = m.group(1)
            txt, i = continua(linhas, i)
            txt = re.sub(r'^\s*\d+\.\s+', '', txt)
            flow.append(Paragraph(inline(txt), S["li"], bulletText=num+"."))
            continue
        txt, i = continua(linhas, i)
        flow.append(Paragraph(inline(txt), S["p"]))
    fecha_tabela(); fecha_cit()

    titulo = os.path.basename(md_path).replace(".md", "")
    def rodape(canvas, doc):
        canvas.saveState()
        canvas.setFont("DJ", 7.2); canvas.setFillColor(CINZA)
        canvas.drawString(17*mm, 11*mm, subtitulo or titulo)
        canvas.drawRightString(A4[0]-17*mm, 11*mm, f"pág. {doc.page}")
        canvas.setStrokeColor(LINHA); canvas.setLineWidth(0.4)
        canvas.line(17*mm, 14*mm, A4[0]-17*mm, 14*mm)
        canvas.restoreState()

    doc = BaseDocTemplate(pdf_path, pagesize=A4,
                          leftMargin=17*mm, rightMargin=17*mm,
                          topMargin=15*mm, bottomMargin=19*mm,
                          title=subtitulo or titulo, author="Novos Negócios")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=rodape)])
    doc.build(flow)
    return pdf_path

if __name__ == "__main__":
    alvos = [
        ("docs/DOSSIE.md", "docs/pdf/Dossie_Implantacao.pdf",
         "Dashboard Novos Negócios — Dossiê de Implantação"),
        ("docs/DIAGNOSTICO_BASE.md", "docs/pdf/Diagnostico_da_Base.pdf",
         "Dashboard Novos Negócios — Diagnóstico da Base"),
        ("docs/ESPECIFICACAO_TELAS.md", "docs/pdf/Especificacao_das_Telas.pdf",
         "Dashboard Novos Negócios — Especificação das Telas"),
    ]
    os.makedirs("docs/pdf", exist_ok=True)
    for md, pdf, sub in alvos:
        converte(md, pdf, sub)
        print(f"OK  {pdf}  ({os.path.getsize(pdf)/1024:.0f} KB)")
