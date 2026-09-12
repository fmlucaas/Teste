# -*- coding: utf-8 -*-
"""Kit para desenhar telas esquemáticas do Power BI Desktop (pt-BR)."""
from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/truetype/dejavu"
def fnt(sz, b=False, mono=False):
    n = ("DejaVuSansMono" if mono else "DejaVuSans") + ("-Bold" if b else "")
    return ImageFont.truetype(f"{F}/{n}.ttf", sz)

# paleta da interface
JANELA   = (243,243,243); CHROME=(255,255,255); BORDA=(205,210,218); BORDA2=(228,232,238)
TEXTO    = (32,38,48);    TEXTO2=(96,106,120); TEXTO3=(140,150,163)
FAIXA    = (250,250,250); ABA_ON=(255,255,255); ACENTO=(0,102,180)
BOTAO    = (250,251,252); BOTAO_B=(200,206,214)
PAINEL   = (249,250,251)
DEST     = (214,64,32)     # destaque: laranja-vermelho
DEST_BG  = (255,241,236)
SETA     = (214,64,32)
AMARELO  = (255,196,0)

class Fig:
    def __init__(self, w=1100, h=640, bg=JANELA):
        self.im = Image.new("RGB", (w, h), bg)
        self.d = ImageDraw.Draw(self.im)
        self.w, self.h = w, h
        self.n = 0

    # ---------- primitivas ----------
    def rr(self, box, r=5, fill=None, outline=None, width=1):
        self.d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)
    def rect(self, box, fill=None, outline=None, width=1):
        self.d.rectangle(box, fill=fill, outline=outline, width=width)
    def txt(self, xy, s, sz=14, b=False, cor=TEXTO, mono=False, anchor="la"):
        self.d.text(xy, s, font=fnt(sz, b, mono), fill=cor, anchor=anchor)
    def txtc(self, box, s, sz=14, b=False, cor=TEXTO, mono=False):
        x0,y0,x1,y1 = box
        self.d.text(((x0+x1)/2, (y0+y1)/2), s, font=fnt(sz,b,mono), fill=cor, anchor="mm")

    # ---------- componentes ----------
    def titulo_janela(self, texto, y=0, h=30, cor=CHROME):
        self.rect((0,y,self.w,y+h), fill=cor, outline=BORDA)
        self.txt((14, y+h/2), texto, 13, True, TEXTO, anchor="lm")
        for i,c in enumerate([(200,200,200),(200,200,200),(232,90,80)]):
            cx = self.w-88+i*28
            self.rr((cx,y+h/2-7,cx+16,y+h/2+7), 3, fill=c)

    def faixa(self, abas, ativa=0, y=30, h=34):
        """Faixa de opções (as abas de cima)."""
        self.rect((0,y,self.w,y+h), fill=FAIXA, outline=BORDA)
        x = 10
        for i,a in enumerate(abas):
            larg = 13 + len(a)*8
            if i==ativa:
                self.rect((x,y+2,x+larg,y+h), fill=ABA_ON, outline=BORDA)
                self.rect((x,y+h-3,x+larg,y+h), fill=ACENTO)
            self.txtc((x,y,x+larg,y+h), a, 13, i==ativa, TEXTO if i==ativa else TEXTO2)
            x += larg + 4
        return y+h

    def botao_faixa(self, x, y, rot, larg=104, alt=62, icone=None, cor_ic=ACENTO):
        self.rr((x,y,x+larg,y+alt), 4, fill=BOTAO, outline=BORDA2)
        if icone is None: icone = "▦"
        self.txtc((x,y+8,x+larg,y+34), icone, 22, cor=cor_ic)
        for i,l in enumerate(rot.split("\n")):
            self.txtc((x,y+32+i*15,x+larg,y+46+i*15), l, 11, cor=TEXTO)
        return (x,y,x+larg,y+alt)

    def painel(self, box, titulo, itens=None, larg_tit=None):
        x0,y0,x1,y1 = box
        self.rect(box, fill=PAINEL, outline=BORDA)
        self.rect((x0,y0,x1,y0+26), fill=(240,242,245), outline=BORDA)
        self.txt((x0+10,y0+13), titulo, 12, True, TEXTO, anchor="lm")
        if itens:
            yy = y0+36
            for it in itens:
                ind = 0
                if it.startswith("  "): ind = 14; it = it.strip()
                marc = "▾ " if it.endswith(":") else ""
                self.txt((x0+10+ind, yy), marc+it.rstrip(":"), 12,
                         it.endswith(":"), TEXTO if it.endswith(":") else TEXTO2)
                yy += 21
        return box

    def caixa_texto(self, box, texto, sz=12, mono=True, fill=(255,255,255)):
        self.rect(box, fill=fill, outline=BORDA)
        x0,y0,_,_ = box
        yy = y0+9
        for l in texto.split("\n"):
            self.txt((x0+10, yy), l, sz, False, TEXTO2 if mono else TEXTO, mono=mono)
            yy += sz+5

    def botao(self, box, rot, primario=False):
        self.rr(box, 4, fill=ACENTO if primario else BOTAO,
                outline=ACENTO if primario else BOTAO_B)
        self.txtc(box, rot, 12, True, (255,255,255) if primario else TEXTO)
        return box

    def campo_visual(self, box, rot, valores):
        """Um 'poço' do painel Visualizações (ex.: Eixo Y)."""
        x0,y0,x1,y1 = box
        self.txt((x0, y0), rot, 11, True, TEXTO2)
        cy = y0+17
        for v in valores:
            self.rr((x0, cy, x1, cy+21), 3, fill=(255,255,255), outline=BORDA)
            self.txt((x0+7, cy+10), v, 11, False, TEXTO, anchor="lm")
            cy += 25
        if not valores:
            self.rr((x0, cy, x1, cy+21), 3, fill=(252,252,252), outline=BORDA2)
            self.txt((x0+7, cy+10), "Adicione dados aqui", 10, False, TEXTO3, anchor="lm")

    # ---------- anotações ----------
    def marca(self, box, num=None, cor=DEST, larg=3, r=5, dx=-13, dy=-13):
        """Contorna um elemento e coloca a bolinha numerada."""
        self.rr(box, r, outline=cor, width=larg)
        if num is None:
            self.n += 1; num = self.n
        cx, cy = box[0]+dx, box[1]+dy
        self.d.ellipse((cx-13,cy-13,cx+13,cy+13), fill=cor)
        self.txtc((cx-13,cy-13,cx+13,cy+13), str(num), 14, True, (255,255,255))
        return num

    def seta(self, p1, p2, cor=SETA, larg=3):
        self.d.line([p1,p2], fill=cor, width=larg)
        import math
        ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
        for s in (0.5, -0.5):
            self.d.line([p2, (p2[0]-15*math.cos(ang-s), p2[1]-15*math.sin(ang-s))], fill=cor, width=larg)

    def nota(self, xy, texto, cor=DEST, sz=12, anchor="la"):
        self.txt(xy, texto, sz, True, cor, anchor=anchor)

    def legenda(self, itens, y=None, x=14):
        """Bloco de legenda numerada no rodapé da figura."""
        y = y if y is not None else self.h - 18 - 20*len(itens)
        self.rect((0, y-12, self.w, self.h), fill=(252,249,247))
        self.d.line([(0,y-12),(self.w,y-12)], fill=BORDA, width=1)
        for i, t in enumerate(itens, 1):
            cy = y + i*20 - 10
            self.d.ellipse((x, cy-9, x+18, cy+9), fill=DEST)
            self.txtc((x, cy-9, x+18, cy+9), str(i), 12, True, (255,255,255))
            self.txt((x+26, cy), t, 12, False, TEXTO, anchor="lm")

    def salvar(self, nome):
        self.im.save(f"docs/figuras/{nome}.png")
        return f"docs/figuras/{nome}.png"
