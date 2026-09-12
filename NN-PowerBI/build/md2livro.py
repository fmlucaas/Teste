# -*- coding: utf-8 -*-
"""Converte o dossiê Markdown em PDF com capa, sumário e figuras."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle, Preformatted, Image, PageBreak,
                                KeepTogether, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents

F = "/usr/share/fonts/truetype/dejavu"
for n, p in [("DJ", f"{F}/DejaVuSans.ttf"), ("DJ-B", f"{F}/DejaVuSans-Bold.ttf"),
             ("DJ-I", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"),
             ("DJM", f"{F}/DejaVuSansMono.ttf"), ("DJM-B", f"{F}/DejaVuSansMono-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, p))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ-I")

AZUL   = colors.HexColor("#1F5FA9"); AZUL_E = colors.HexColor("#0F3A6B")
CINZA  = colors.HexColor("#5A6672"); LINHA  = colors.HexColor("#D8DFE8")
FUNDO  = colors.HexColor("#F5F7FA"); DEST   = colors.HexColor("#FFF8E1")
DEST_B = colors.HexColor("#E0A800"); PERIGO = colors.HexColor("#C0392B")
VERDE  = colors.HexColor("#1E7A4C")
LARG   = A4[0] - 34*mm

EMOJI = {"⚠️":"", "⚠":"", "→":"->", "←":"<-", "✅":"[ok]", "❌":"[x]", "·":"·"}
def limpa(t):
    for k,v in EMOJI.items(): t = t.replace(k,v)
    return t
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def inline(t):
    t = limpa(t); cod=[]
    t = re.sub(r'`([^`]+)`', lambda m:(cod.append(m.group(1)), f"\x00{len(cod)-1}\x00")[1], t)
    e = esc(t)
    e = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#1F5FA9"><u>\1</u></link>', e)
    e = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', e)
    e = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', e)
    e = e.replace("\\|","|").replace("¶", "<br/>")
    return re.sub(r'\x00(\d+)\x00',
        lambda m: f'<font face="DJM" size="8.5" color="#A03020">{esc(cod[int(m.group(1))])}</font>', e)

def st(**kw):
    b = dict(fontName="DJ", fontSize=9.8, leading=14.4, textColor=colors.HexColor("#18202C"),
             spaceAfter=5, alignment=TA_LEFT)
    b.update(kw)
    nome = b.pop("name", "s")
    return ParagraphStyle(nome, **b)

S = {
 "h1": st(name="h1", fontName="DJ-B", fontSize=20, leading=25, textColor=AZUL_E, spaceBefore=4, spaceAfter=14),
 "h2": st(name="h2", fontName="DJ-B", fontSize=14.5, leading=19, textColor=AZUL, spaceBefore=15, spaceAfter=7),
 "h3": st(name="h3", fontName="DJ-B", fontSize=11.5, leading=15.5, textColor=AZUL_E, spaceBefore=11, spaceAfter=5),
 "h4": st(name="h4", fontName="DJ-B", fontSize=10, leading=14, textColor=CINZA, spaceBefore=8, spaceAfter=4),
 "p":  st(name="p"),
 "li": st(name="li", leftIndent=14, bulletIndent=4, spaceAfter=3.5),
 "cap": st(name="cap", fontSize=8.6, leading=11.5, textColor=CINZA, alignment=TA_CENTER, spaceBefore=4),
 "th": st(name="th", fontName="DJ-B", fontSize=8, leading=11, textColor=colors.white, spaceAfter=0),
 "td": st(name="td", fontSize=8.2, leading=11.2, spaceAfter=0),
 "quote": st(name="q", fontSize=9.4, leading=13.6, textColor=colors.HexColor("#59460B")),
}
CODE = ParagraphStyle("code", fontName="DJM", fontSize=7.3, leading=9.4,
                      textColor=colors.HexColor("#18202C"))

def tabela(linhas):
    linhas = [l for l in linhas if not re.match(r'^\s*\|[\s:\-|]+\|\s*$', l)]
    if not linhas: return None
    rows=[[c.strip() for c in l.strip().strip("|").split("|")] for l in linhas]
    n=max(len(r) for r in rows); rows=[r+[""]*(n-len(r)) for r in rows]
    dados=[[Paragraph(inline(c), S["th"] if i==0 else S["td"]) for c in r] for i,r in enumerate(rows)]
    if n==1: w=[LARG]
    elif n==2: w=[LARG*0.32, LARG*0.68]
    else:
        p=0.26 if n<=4 else 0.20
        w=[LARG*p]+[LARG*(1-p)/(n-1)]*(n-1)
    t=Table(dados, colWidths=w, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),AZUL),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,FUNDO]),
        ("GRID",(0,0),(-1,-1),0.4,LINHA),("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),3.5),("BOTTOMPADDING",(0,0),(-1,-1),3.5)]))
    return t

def bloco_codigo(linhas):
    txt = limpa("\n".join(linhas))
    txt = "\n".join(l[:132] for l in txt.split("\n"))
    t=Table([[Preformatted(txt, CODE)]], colWidths=[LARG], hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),FUNDO),("BOX",(0,0),(-1,-1),0.5,LINHA),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    return t

def citacao(linhas):
    txt=" ".join(l.lstrip("> ").rstrip() for l in linhas).strip()
    if not txt: return None
    cor, borda = DEST, DEST_B
    if txt.upper().startswith("CUIDADO") or txt.upper().startswith("NUNCA"):
        cor, borda = colors.HexColor("#FDECEA"), PERIGO
    t=Table([[Paragraph(inline(txt), S["quote"])]], colWidths=[LARG], hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),cor),
        ("LINEBEFORE",(0,0),(0,-1),2.6,borda),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    return t

def figura(caminho, legenda, raiz):
    p = os.path.join(raiz, caminho)
    if not os.path.exists(p): return None
    from PIL import Image as PILImage
    iw, ih = PILImage.open(p).size
    w = min(LARG, 172*mm); h = w*ih/iw
    maxh = 205*mm
    if h > maxh: h = maxh; w = h*iw/ih
    img = Image(p, width=w, height=h)
    img.hAlign = "CENTER"
    partes=[img]
    if legenda: partes.append(Paragraph(inline(legenda), S["cap"]))
    return KeepTogether([Spacer(1,5)]+partes+[Spacer(1,9)])

BLOCO = re.compile(r'^\s*(?:[-*]\s|\d+\.\s|#{1,4}\s|>|\||```|!\[|-{3,}\s*$)')
def continua(linhas, i):
    partes=[linhas[i].strip()]; j=i+1
    while j < len(linhas):
        if not linhas[j].strip() or BLOCO.match(linhas[j]): break
        partes.append(linhas[j].strip()); j+=1
    return " ".join(partes), j


class Livro(BaseDocTemplate):
    def __init__(self, *a, **kw):
        self.subtitulo = kw.pop("subtitulo","")
        BaseDocTemplate.__init__(self, *a, **kw)
    def afterFlowable(self, fl):
        if getattr(fl, "_toc", None):
            nivel, texto = fl._toc
            self.notify("TOCEntry", (nivel, texto, self.page))

def converte(md, pdf, titulo, subtitulo, raiz="."):
    linhas = io.open(md, encoding="utf-8").read().split("\n")
    flow=[]

    # ---------------- capa ----------------
    flow += [Spacer(1, 46*mm),
        Paragraph(titulo, st(name="cvt", fontName="DJ-B", fontSize=30, leading=36,
                             textColor=AZUL_E, alignment=TA_CENTER)),
        Spacer(1, 6*mm),
        Paragraph(subtitulo, st(name="cvs", fontSize=13.5, leading=19, textColor=CINZA,
                                alignment=TA_CENTER)),
        Spacer(1, 14*mm)]
    cx = Table([[Paragraph(
        "<b>Para quem nunca abriu o Power BI.</b><br/><br/>"
        "Cada passo diz em que botão clicar, o que a janela mostra e o que digitar.<br/>"
        "As figuras são desenhos das telas, com o ponto exato marcado em vermelho.<br/><br/>"
        "Siga na ordem. Não pule partes.",
        st(name="cvb", fontSize=11, leading=17, alignment=TA_CENTER))]],
        colWidths=[LARG*0.86], hAlign="CENTER")
    cx.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),FUNDO),("BOX",(0,0),(-1,-1),0.6,LINHA),
        ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
        ("LEFTPADDING",(0,0),(-1,-1),18),("RIGHTPADDING",(0,0),(-1,-1),18)]))
    flow += [cx, Spacer(1, 20*mm),
        Paragraph("Power BI Desktop 2.157.1354.0 (64 bits) · agosto de 2026 · português do Brasil",
                  st(name="cvf", fontSize=9.5, textColor=CINZA, alignment=TA_CENTER)),
        PageBreak()]

    # ---------------- sumário ----------------
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("t0", fontName="DJ-B", fontSize=11, leading=19, textColor=AZUL_E,
                       spaceBefore=8, leftIndent=0, firstLineIndent=-14),
        ParagraphStyle("t1", fontName="DJ", fontSize=9.6, leading=15, textColor=CINZA,
                       leftIndent=16, firstLineIndent=-14),
        ParagraphStyle("t2", fontName="DJ", fontSize=8.8, leading=13.5,
                       textColor=colors.HexColor("#7B8AA3"), leftIndent=34, firstLineIndent=-14),
    ]
    flow += [Paragraph("Sumário", S["h1"]), toc, PageBreak()]

    # ---------------- corpo ----------------
    i=0; buf_t=[]; buf_c=[]; buf_q=[]; em_cod=False
    def fecha_t():
        if buf_t:
            t=tabela(list(buf_t))
            if t: flow.extend([Spacer(1,3), t, Spacer(1,8)])
            buf_t.clear()
    def fecha_q():
        if buf_q:
            c=citacao(list(buf_q))
            if c: flow.extend([Spacer(1,2), c, Spacer(1,7)])
            buf_q.clear()
    while i < len(linhas):
        l = linhas[i].rstrip()
        if l.strip().startswith("```"):
            if em_cod:
                flow.extend([Spacer(1,3), bloco_codigo(buf_c), Spacer(1,8)]); buf_c.clear(); em_cod=False
            else:
                fecha_t(); fecha_q(); em_cod=True
            i+=1; continue
        if em_cod: buf_c.append(linhas[i]); i+=1; continue
        if l.strip().startswith("|"): fecha_q(); buf_t.append(l); i+=1; continue
        fecha_t()
        if l.startswith(">"): buf_q.append(l); i+=1; continue
        fecha_q()
        if not l.strip(): i+=1; continue
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', l.strip())
        if m:
            fig = figura(m.group(2), m.group(1), raiz)
            if fig: flow.append(fig)
            i+=1; continue
        if re.match(r'^\\pagebreak\s*$', l.strip()):
            flow.append(PageBreak()); i+=1; continue
        if re.match(r'^-{3,}$', l.strip()):
            flow += [Spacer(1,5),
                Table([[""]], colWidths=[LARG], style=[("LINEBELOW",(0,0),(-1,-1),0.6,LINHA)], hAlign="LEFT"),
                Spacer(1,8)]
            i+=1; continue
        m = re.match(r'^(#{1,4})\s+(.*)$', l)
        if m:
            niv=len(m.group(1)); texto=m.group(2)
            # a quebra de página vem do marcador \pagebreak do texto,
            # não do título — senão nasce uma página em branco entre os dois
            p = Paragraph(inline(texto), S[f"h{niv}"])
            if niv<=3: p._toc = (niv-1, re.sub(r'[*`]','',texto))
            flow.append(CondPageBreak(26*mm) if niv>=2 else Spacer(1,0))
            flow.append(p); i+=1; continue
        m = re.match(r'^\s*[-*]\s+(.*)$', l)
        if m:
            txt,i = continua(linhas,i); txt=re.sub(r'^\s*[-*]\s+','',txt)
            flow.append(Paragraph(inline(txt), S["li"], bulletText="•")); continue
        m = re.match(r'^\s*(\d+)\.\s+(.*)$', l)
        if m:
            num=m.group(1); txt,i=continua(linhas,i); txt=re.sub(r'^\s*\d+\.\s+','',txt)
            flow.append(Paragraph(inline(txt), S["li"], bulletText=num+".")); continue
        txt,i = continua(linhas,i)
        flow.append(Paragraph(inline(txt), S["p"]))
    fecha_t(); fecha_q()

    def pagina(canvas, doc):
        canvas.saveState()
        if doc.page > 1:
            canvas.setFont("DJ",7.4); canvas.setFillColor(CINZA)
            canvas.drawString(17*mm, 11*mm, subtitulo)
            canvas.drawRightString(A4[0]-17*mm, 11*mm, f"página {doc.page}")
            canvas.setStrokeColor(LINHA); canvas.setLineWidth(0.4)
            canvas.line(17*mm, 14*mm, A4[0]-17*mm, 14*mm)
        canvas.restoreState()

    doc = Livro(pdf, pagesize=A4, leftMargin=17*mm, rightMargin=17*mm,
                topMargin=15*mm, bottomMargin=19*mm, title=titulo,
                author="Novos Negócios", subtitulo=subtitulo)
    doc.addPageTemplates([PageTemplate(id="p",
        frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")],
        onPage=pagina)])
    doc.multiBuild(flow)
    return pdf
