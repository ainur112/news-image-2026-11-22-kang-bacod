from PIL import Image, ImageDraw, ImageFont
import textwrap

S = 2
W = H = 1024
PAPER = (247, 244, 235)
INK = (22, 27, 37)
MUTED = (86, 92, 102)
WHITE = (255, 254, 250)
RULE = (62, 68, 78)
C = {
    'NA': (36, 72, 122), 'EU': (142, 42, 48), 'ME': (176, 108, 32),
    'AS': (24, 108, 110), 'AF': (108, 62, 142), 'LA': (38, 118, 72),
    'OC': (32, 88, 148), 'WT': (94, 92, 34),
}
F = 'C:/Windows/Fonts/'
Reg = lambda n: ImageFont.truetype(F + 'arial.ttf', n * S)
Bold = lambda n: ImageFont.truetype(F + 'arialbd.ttf', n * S)
Serif = lambda n: ImageFont.truetype(F + 'timesbd.ttf', n * S)

im = Image.new('RGB', (W * S, H * S), PAPER)
d = ImageDraw.Draw(im)
p = lambda v: int(round(v * S))


def txt(x, y, s, font, fill=INK):
    d.text((p(x), p(y)), s, font=font, fill=fill, anchor='la')


def wid(s, font):
    b = d.textbbox((0, 0), s, font=font)
    return (b[2] - b[0]) / S


def bot(y, s, font):
    b = d.textbbox((0, 0), s, font=font)
    return y + (b[3] - b[1]) / S


def fit(s, maxw, n, bold=True):
    while n > 8:
        f = Bold(n) if bold else Reg(n)
        if wid(s, f) <= maxw:
            return f
        n -= 1
    return Bold(9) if bold else Reg(9)


def box(x0, y0, x1, y1, fill=None, outline=None, w=1):
    d.rectangle((p(x0), p(y0), p(x1), p(y1)), fill=fill, outline=outline, width=p(w))


def ln(x0, y0, x1, y1, fill=RULE, w=1):
    d.line((p(x0), p(y0), p(x1), p(y1)), fill=fill, width=p(w))


def icon(k, x, y, s, col):
    cx = x + s / 2
    if k == 'missile':
        d.polygon([(p(cx), p(y + 1)), (p(cx + s * .22), p(y + s * .42)), (p(cx), p(y + s - 1)), (p(cx - s * .22), p(y + s * .42))], fill=col)
        d.ellipse((p(cx - s * .12), p(y + s * .68), p(cx + s * .12), p(y + s * .92)), fill=(238, 138, 40))
    elif k == 'fire':
        d.polygon([(p(cx), p(y + 1)), (p(x + s - 1), p(y + s - 1)), (p(x + 1), p(y + s - 1))], fill=col)
        d.polygon([(p(cx), p(y + s * .42)), (p(cx + s * .22), p(y + s - 1)), (p(cx - s * .22), p(y + s - 1))], fill=(238, 138, 40))
    elif k == 'card':
        box(x + 1, y + s * .24, x + s - 1, y + s * .78, col)
        ln(x + 1, y + s * .45, x + s - 1, y + s * .45, WHITE, 2)
    elif k == 'shield':
        d.polygon([(p(cx), p(y + 1)), (p(x + s - 1), p(y + s * .28)), (p(cx), p(y + s - 1)), (p(x + 1), p(y + s * .28))], fill=col)
    elif k == 'quake':
        d.polygon([(p(x + 1), p(y + s - 1)), (p(cx), p(y + 1)), (p(x + s - 1), p(y + s - 1))], outline=col, width=p(3))
        ln(x + s * .3, y + s * .62, x + s * .7, y + s * .62, col, 3)
    elif k == 'boat':
        d.polygon([(p(x + 1), p(y + s * .5)), (p(x + s - 1), p(y + s * .5)), (p(x + s * .75), p(y + s - 1)), (p(x + s * .25), p(y + s - 1))], fill=col)
        ln(cx, y + 1, cx, y + s * .5, col, 3)
    elif k == 'police':
        box(x + 2, y + s * .4, x + s - 2, y + s - 1, col)
        d.ellipse((p(cx - s * .28), p(y + 1), p(cx + s * .28), p(y + s * .45)), fill=col)
    elif k == 'chip':
        box(x + s * .22, y + s * .22, x + s * .78, y + s * .78, col)
        for i in range(3):
            ln(x + s * (.35 + i * .15), y, x + s * (.35 + i * .15), y + s * .22, col, 2)
            ln(x + s * (.35 + i * .15), y + s * .78, x + s * (.35 + i * .15), y + s, col, 2)
    elif k == 'protest':
        ln(cx, y + s * .3, cx, y + s - 1, col, 3)
        d.ellipse((p(cx - s * .12), p(y + 1), p(cx + s * .12), p(y + s * .3)), fill=col)
        d.polygon([(p(cx), p(y + s * .3)), (p(x + s - 1), p(y + s * .55)), (p(cx), p(y + s * .72))], fill=col)
    elif k == 'leaf':
        d.ellipse((p(x + 1), p(y + 1), p(x + s - 1), p(y + s - 1)), fill=col)
        ln(x + s * .2, y + s * .8, x + s * .8, y + s * .2, PAPER, 2)
    elif k == 'trophy':
        box(x + s * .3, y + 1, x + s * .7, y + s * .6, col)
        ln(x + s * .3, y + s * .3, x + s * .12, y + s * .3, col, 2)
        ln(x + s * .7, y + s * .3, x + s * .88, y + s * .3, col, 2)
    elif k == 'flag':
        ln(cx, y + 1, cx, y + s - 1, col, 3)
        d.polygon([(p(cx), p(y + 1)), (p(x + s - 1), p(y + s * .32)), (p(cx), p(y + s * .58))], fill=col)
    elif k == 'castle':
        box(x + s * .18, y + s * .35, x + s * .82, y + s - 1, col)
        for i in range(3):
            box(x + s * (.2 + i * .22), y + s * .18, x + s * (.36 + i * .22), y + s * .4, col)
    elif k == 'swim':
        for i in range(3):
            ln(x + 1, y + s * (.35 + i * .22), x + s - 1, y + s * (.35 + i * .22), col, 3)
    else:
        d.ellipse((p(x + 2), p(y + 2), p(x + s - 2), p(y + s - 2)), fill=col)


PANELS = [
    ('EU', 'missile', 'RUSSIAN STRIKE HITS UKRAINE', 'Two killed and 58 wounded as missiles hit civilian sites.'),
    ('ME', 'fire', 'IRAN STRIKE HITS BAHRAIN PLANT', 'Industrial facility damaged; more attacks intercepted.'),
    ('AS', 'fire', 'JAVA FACTORY FIRE: 36 MISSING', 'Western Java blaze kills three and injures four.'),
    ('NA', 'card', 'TRUMP PLEDGES 10% CARD CAP', 'President invites Democrats to cap card interest.'),
    ('AF', 'boat', 'NIGERIA BOAT CAPSIZES: 24 DEAD', 'Overloaded boat sinks; two dozen people die.'),
    ('LA', 'quake', 'MAGNITUDE 6.7 QUAKE HITS PERU', 'Andes shaken; no immediate deaths reported.'),
]

BRIEFS = [
    ('NA', 'SEATTLE ICE ARRESTS DRAW OUTCRY'), ('NA', 'FBI PROBES JUSTICE DATABASE HACK'),
    ('NA', 'TRUMP TARGETS OFFSHORE DATA CENTRES'), ('NA', 'SEC PROBES NVIDIA ACCOUNTING'),
    ('NA', 'MAMDANI PLANS RIKERS CLOSURE'), ('NA', 'HONDA RECALLS 810,000 US CARS'),
    ('EU', 'DRONE HITS BALTIC CARGO SHIP'), ('EU', 'UKRAINE FACES WINDOW SHORTAGE'),
    ('EU', 'LISBON MARCH OVER LIVING COSTS'), ('EU', 'LONDON MARCH DEMANDS AI RULES'),
    ('EU', 'BULGARI FOUNDER DIES AT 89'), ('EU', 'ZELENSKYY CALLS SUMMIT UNSUCCESSFUL'),
    ('ME', 'GAZA VEHICLE STRIKE KILLS THREE'), ('ME', 'UNIFIL HANDS POSTS TO LEBANON'),
    ('ME', 'NETANYAHU INVITED TO COALITION TALKS'), ('ME', 'HAGIA SOPHIA TUNNELS REVEALED'),
    ('ME', 'SWIMMER CROSSES WAR-HIT HORMUZ'), ('AS', 'MYANMAR JUNTA DECRIES ASEAN RULING'),
    ('AS', 'CHINA OPPOSES US FCC TELECOM BAN'), ('AS', 'INDIA YOUTH PROTEST AT META'),
    ('AS', 'OKINAWA CASTLE HALL RESTORED'), ('AS', 'NORTH KOREA DELAYS PYONGYANG RACE'),
    ('LA', 'BRAZIL STORM DEVASTATES TOWN'), ('LA', 'CARTEL BOSS CAUGHT, 11 DEAD'),
    ('LA', 'BOLSONARO MOVED TO INTENSIVE CARE'), ('AF', 'KENYA PICKS US MINERALS GROUP'),
    ('OC', 'AUSTRALIA CRITICISES CBO ON AUKUS'), ('WT', 'COP31 NEARS FINAL CLIMATE DEAL'),
    ('WT', 'UN TALKS ON KILLER ROBOTS SET'), ('WT', 'KANSAS CITY TAKE NWSL TITLE'),
]

ln(22, 14, 1002, 14, INK, 2)
txt(22, 22, 'WORLD NEWS', Serif(52), INK)
assert bot(22, 'WORLD NEWS', Serif(52)) < 82
txt(744, 30, 'SUNDAY', Bold(19), C['EU'])
txt(744, 54, '22 NOVEMBER 2026', Bold(19), INK)
txt(22, 80, '36 DATED STORIES  ·  SIX REGIONS  ·  ONE DAY', Reg(11), MUTED)
ln(22, 96, 1002, 96, INK, 3)

PW, PH, GX, GY = 484, 180, 12, 10
for i, (reg, kind, head, detail) in enumerate(PANELS):
    col, row = i % 2, i // 2
    x = 22 + col * (PW + GX)
    y = 106 + row * (PH + GY)
    box(x, y, x + PW, y + PH, WHITE, RULE, 1)
    box(x, y, x + 5, y + PH, C[reg])
    icon(kind, x + 15, y + 26, 102, C[reg])
    txt(x + 128, y + 14, reg, Bold(11), C[reg])
    hf = fit(head, PW - 145, 20)
    lines = textwrap.wrap(head, width=30)
    for j, line in enumerate(lines[:2]):
        txt(x + 128, y + 34 + j * 27, line, hf, INK)
    df = fit(detail, PW - 145, 12, False)
    for j, line in enumerate(textwrap.wrap(detail, width=48)[:2]):
        txt(x + 128, y + 100 + j * 17, line, df, MUTED)
    assert y + 140 < y + PH

box(22, 676, 1002, 968, WHITE, RULE, 1)
box(22, 676, 1002, 698, INK)
txt(32, 680, 'ALSO TODAY — 30 MORE DATED STORIES', Bold(12), WHITE)
CW, RH = 320, 26
for i, (reg, head) in enumerate(BRIEFS):
    col, row = i % 3, i // 3
    x = 22 + col * CW
    y = 704 + row * RH
    f = fit(head, CW - 32, 12)
    assert bot(y, head, f) < y + RH
    box(x + 2, y + 5, x + 6, y + 15, C[reg])
    txt(x + 13, y, head, f, INK)

box(22, 976, 1002, 1008, INK)
txt(32, 982, 'ALSO: HAGIA SOPHIA TUNNELS  ·  COP31 DEAL  ·  FIRST NWSL TITLE', Reg(11), WHITE)
txt(22, 1012, 'SOURCES: REUTERS · AP · BBC · NHK · ANADOLU  |  COMPILED 22 NOV 2026', Reg(8), MUTED)

out = im.resize((W, H), Image.Resampling.LANCZOS)
out.save('C:/Users/ainur/AppData/Local/hermes/cache/scratch/makefun/news-entry/entry.png', optimize=False)
print('wrote entry.png', W, H)
