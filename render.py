from PIL import Image, ImageDraw, ImageFont

S = 2
W = H = 1024
PAPER = (247, 244, 235)
INK = (22, 27, 37)
MUTED = (88, 94, 104)
WHITE = (255, 254, 250)
rule = (62, 68, 78)
COLORS = {
    'NA': (36, 72, 122), 'EU': (142, 42, 48), 'ME': (176, 108, 32),
    'AS': (24, 108, 110), 'AF': (108, 62, 142), 'LA': (38, 118, 72),
    'OC': (32, 88, 148), 'SCI': (94, 92, 34),
}
FONTS = 'C:/Windows/Fonts/'
Regular = lambda n: ImageFont.truetype(FONTS + 'arial.ttf', n * S)
Bold = lambda n: ImageFont.truetype(FONTS + 'arialbd.ttf', n * S)
Serif = lambda n: ImageFont.truetype(FONTS + 'timesbd.ttf', n * S)

img = Image.new('RGB', (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)


def px(v):
    return int(round(v * S))


def text(x, y, s, font, fill=INK):
    d.text((px(x), px(y)), s, font=font, fill=fill, anchor='la')


def width(s, font):
    b = d.textbbox((0, 0), s, font=font)
    return (b[2] - b[0]) / S


def bottom(y, s, font):
    b = d.textbbox((0, 0), s, font=font)
    return y + (b[3] - b[1]) / S


def fitted(s, box_w, size, bold=True):
    n = size
    while n > 8:
        f = Bold(n) if bold else Regular(n)
        if width(s, f) <= box_w:
            return f
        n -= 1
    return Bold(9) if bold else Regular(9)


def rect(x0, y0, x1, y1, fill=None, outline=None, w=1):
    d.rectangle((px(x0), px(y0), px(x1), px(y1)), fill=fill, outline=outline, width=px(w))


def line(x0, y0, x1, y1, fill=rule, w=1):
    d.line((px(x0), px(y0), px(x1), px(y1)), fill=fill, width=px(w))


def icon(kind, x, y, size, color):
    s = size
    cx, cy = x + s / 2, y + s / 2
    if kind == 'missile':
        d.polygon([(px(cx), px(y + 1)), (px(cx + s * .22), px(cy)), (px(cx), px(y + s - 1)), (px(cx - s * .22), px(cy))], fill=color)
        d.ellipse((px(cx - s * .12), px(y + s * .72), px(cx + s * .12), px(y + s * .95)), fill=(238, 138, 40))
    elif kind == 'ship':
        d.polygon([(px(x + 1), px(cy + s * .12)), (px(x + s - 1), px(cy + s * .12)), (px(x + s * .78), px(y + s - 1)), (px(x + s * .22), px(y + s - 1))], fill=color)
        line(x + s * .5, y + 1, x + s * .5, y + s * .5, color, 2)
    elif kind == 'card':
        rect(x + 1, y + s * .25, x + s - 1, y + s * .78, color)
        line(x + 1, y + s * .45, x + s - 1, y + s * .45, WHITE, 1)
    elif kind == 'police':
        d.polygon([(px(x + 1), px(cy)), (px(x + s - 1), px(cy)), (px(x + s - 1), px(y + s - 1)), (px(x + 1), px(y + s - 1))], fill=color)
        d.ellipse((px(cx - s * .28), px(y + 1), px(cx + s * .28), px(cy + 2)), fill=color)
    elif kind == 'shield':
        d.polygon([(px(cx), px(y + 1)), (px(x + s - 1), px(y + s * .28)), (px(cx), px(y + s - 1)), (px(x + 1), px(y + s * .28))], fill=color)
    elif kind == 'chip':
        rect(x + s * .22, y + s * .22, x + s * .78, y + s * .78, color)
        for k in range(3):
            line(x + s * .35 + k * s * .15, y, x + s * .35 + k * s * .15, y + s * .22, color, 1)
            line(x + s * .35 + k * s * .15, y + s * .78, x + s * .35 + k * s * .15, y + s, color, 1)
    elif kind == 'jail':
        rect(x + 2, y + s * .22, x + s - 2, y + s - 1, color)
        for k in range(3):
            line(x + s * (.3 + k * .2), y + s * .22, x + s * (.3 + k * .2), y + s - 1, WHITE, 1)
    elif kind == 'car':
        rect(x + 1, y + s * .42, x + s - 1, y + s * .8, color)
        d.ellipse((px(x + 2), px(y + s * .7), px(x + s * .35), px(y + s - 1)), fill=color)
        d.ellipse((px(x + s * .65), px(y + s * .7), px(x + s - 2), px(y + s - 1)), fill=color)
    elif kind == 'protest':
        line(cx, y + s * .3, cx, y + s - 1, color, 2)
        d.ellipse((px(cx - s * .12), px(y + 1), px(cx + s * .12), px(y + s * .3)), fill=color)
        d.polygon([(px(cx), px(y + s * .3)), (px(x + s - 1), px(y + s * .55)), (px(cx), px(y + s * .7))], fill=color)
    elif kind == 'fire':
        d.polygon([(px(cx), px(y + 1)), (px(x + s - 1), px(y + s - 1)), (px(x + 1), px(y + s - 1))], fill=color)
        d.polygon([(px(cx), px(y + s * .45)), (px(cx + s * .22), px(y + s - 1)), (px(cx - s * .22), px(y + s - 1))], fill=(238, 138, 40))
    elif kind == 'quake':
        d.polygon([(px(x + 1), px(y + s - 1)), (px(cx), px(y + 1)), (px(x + s - 1), px(y + s - 1))], outline=color, width=px(2))
        line(x + s * .28, y + s * .6, x + s * .72, y + s * .6, color, 2)
    elif kind == 'boat':
        d.polygon([(px(x + 1), px(cy + s * .15)), (px(x + s - 1), px(cy + s * .15)), (px(x + s * .75), px(y + s - 1)), (px(x + s * .25), px(y + s - 1))], fill=color)
        line(cx, y + 1, cx, cy + s * .15, color, 2)
    elif kind == 'pick':
        line(x + s * .25, y + s - 1, cx, y + 1, color, 2)
        line(x + s * .15, y + s * .3, x + s * .8, y + 1, color, 2)
    elif kind == 'leaf':
        d.ellipse((px(x + 1), px(y + 1), px(x + s - 1), px(y + s - 1)), fill=color)
        line(x + s * .2, y + s * .8, x + s * .8, y + s * .2, PAPER, 1)
    elif kind == 'flag':
        line(cx, y + 1, cx, y + s - 1, color, 2)
        d.polygon([(px(cx), px(y + 1)), (px(x + s - 1), px(y + s * .32)), (px(cx), px(y + s * .55))], fill=color)
    elif kind == 'tunnel':
        d.arc((px(x + 1), px(y + 1), px(x + s - 1), px(y + s * 1.5)), 180, 360, fill=color, width=px(2))
        line(x + 1, y + s * .7, x + s - 1, y + s * .7, color, 2)
    elif kind == 'planet':
        d.ellipse((px(x + 1), px(y + 1), px(x + s - 1), px(y + s - 1)), outline=color, width=px(2))
        d.ellipse((px(x + s * .2), px(y + s * .2), px(x + s * .8), px(y + s * .8)), fill=color)
    elif kind == 'robot':
        rect(x + s * .2, y + s * .25, x + s * .8, y + s * .85, color)
        d.ellipse((px(cx - s * .1), px(y + s * .1), px(cx + s * .1), px(y + s * .3)), fill=color)
        d.ellipse((px(x + s * .35), px(y + s * .45), px(x + s * .44), px(y + s * .55)), fill=PAPER)
        d.ellipse((px(x + s * .56), px(y + s * .45), px(x + s * .65), px(y + s * .55)), fill=PAPER)
    elif kind == 'castle':
        rect(x + s * .18, y + s * .35, x + s * .82, y + s - 1, color)
        for k in range(3):
            rect(x + s * (.2 + k * .22), y + s * .18, x + s * (.36 + k * .22), y + s * .4, color)
    elif kind == 'trophy':
        rect(x + s * .3, y + 1, x + s * .7, y + s * .6, color)
        line(x + s * .3, y + s * .3, x + s * .12, y + s * .3, color, 2)
        line(x + s * .7, y + s * .3, x + s * .88, y + s * .3, color, 2)
        rect(x + s * .42, y + s * .6, x + s * .58, y + s * .8, color)
    elif kind == 'swim':
        for k in range(3):
            line(x + 1, y + s * (.35 + k * .22), x + s - 1, y + s * (.35 + k * .22), color, 2)
    else:
        d.ellipse((px(x + 2), px(y + 2), px(x + s - 2), px(y + s - 2)), fill=color)


LEAD = ('EU', 'missile', 'RUSSIAN STRIKE HITS UKRAINE',
        'Two killed and 58 wounded as a missile and drone barrage batters civilian sites.')

BLOCKS = [
    ('NA', 'NORTH AMERICA', [
        ('card', 'TRUMP PLEDGES 10% CARD CAP'), ('police', 'ICE ARRESTS SPARK SEATTLE OUTCRY'),
        ('shield', 'FBI PROBES JUSTICE DATABASE HACK'), ('chip', 'TRUMP TARGETS OFFSHORE DATA CENTRES'),
        ('chip', 'SEC PROBES NVIDIA ACCOUNTING'), ('jail', 'MAMDANI PLANS RIKERS CLOSURE'),
    ]),
    ('EU', 'EUROPE', [
        ('ship', 'DRONE HITS BALTIC CARGO SHIP'), ('shield', 'UKRAINE FACES WINDOW SHORTAGE'),
        ('protest', 'LISBON MARCH OVER LIVING COSTS'), ('robot', 'LONDON MARCH DEMANDS AI RULES'),
        ('castle', 'BULGARI FOUNDER DIES AT 89'), ('missile', 'ZELENSKYY CALLS SUMMIT UNSUCCESSFUL'),
    ]),
    ('ME', 'MIDDLE EAST', [
        ('missile', 'IRAN STRIKE HITS BAHRAIN PLANT'), ('missile', 'GAZA VEHICLE STRIKE KILLS THREE'),
        ('shield', 'UNIFIL HANDS POSTS TO LEBANON'), ('flag', 'NETANYAHU INVITED TO COALITION TALKS'),
        ('tunnel', 'HAGIA SOPHIA TUNNELS REVEALED'), ('swim', 'SWIMMER CROSSES WAR-HIT HORMUZ'),
    ]),
    ('AS', 'ASIA', [
        ('fire', 'JAVA FACTORY FIRE: 36 MISSING'), ('flag', 'MYANMAR JUNTA DECRIES ASEAN RULING'),
        ('chip', 'CHINA OPPOSES US FCC TELECOM BAN'), ('protest', 'INDIA YOUTH PROTEST AT META'),
        ('castle', 'SHURI CASTLE HALL RESTORED'), ('flag', 'NORTH KOREA DELAYS PYONGYANG RACE'),
    ]),
    ('LA', 'LATIN AMERICA + AFRICA', [
        ('shield', 'BOLSONARO MOVED TO INTENSIVE CARE'), ('fire', 'STORM DEVASTATES BRAZILIAN TOWN'),
        ('police', 'CARTEL BOSS CAUGHT, 11 DEAD'), ('quake', 'MAGNITUDE 6.7 QUAKE HITS PERU'),
        ('boat', 'NIGERIA BOAT CAPSIZES: 24 DEAD'), ('pick', 'KENYA PICKS US MINERALS GROUP'),
    ]),
    ('OC', 'OCEANIA + WORLD', [
        ('shield', 'AUSTRALIA CRITICISES CBO ON AUKUS'), ('leaf', 'COP31 NEARS FINAL CLIMATE DEAL'),
        ('robot', 'UN TALKS ON KILLER ROBOTS SET'), ('planet', 'MERCURY WELCOMES FIRST VISITOR'),
        ('trophy', 'KANSAS CITY TAKE NWSL TITLE'),
    ]),
]

# masthead
line(22, 16, 1002, 16, INK, 2)
text(22, 26, 'WORLD NEWS', Serif(56), INK)
assert bottom(26, 'WORLD NEWS', Serif(56)) < 86
text(724, 40, 'SUNDAY', Bold(20), COLORS['EU'])
text(724, 66, '22 NOVEMBER 2026', Bold(20), INK)
text(22, 94, '36 STORIES  ·  SIX REGIONS  ·  ONE DAY', Regular(12), MUTED)
line(22, 112, 1002, 112, INK, 3)

# lead box
rect(22, 122, 1002, 296, WHITE, rule, 1)
rect(22, 122, 28, 296, COLORS[LEAD[0]])
text(42, 130, 'LEAD  /  ' + LEAD[0], Bold(11), COLORS[LEAD[0]])
f = fitted(LEAD[2], 720, 30)
text(42, 150, LEAD[2], f, INK)
assert bottom(150, LEAD[2], f) < 196
f2 = fitted(LEAD[3], 700, 14, False)
text(42, 202, LEAD[3], f2, MUTED)
assert bottom(202, LEAD[3], f2) < 245
icon(LEAD[1], 838, 152, 96, COLORS[LEAD[0]])
text(42, 258, 'RUSSIA UKRAINE WAR  ·  CIVILIAN SITES  ·  58 WOUNDED', Regular(10), MUTED)

# six region blocks
BW, BH, GX, GY = 483, 213, 14, 10
for idx, (key, title, stories) in enumerate(BLOCKS):
    col, row = idx % 2, idx // 2
    x0 = 22 + col * (BW + GX)
    y0 = 306 + row * (BH + GY)
    rect(x0, y0, x0 + BW, y0 + BH, WHITE, rule, 1)
    rect(x0, y0, x0 + BW, y0 + 23, COLORS[key])
    text(x0 + 10, y0 + 5, title, Bold(12), WHITE)
    n = len(stories)
    step = min(30, (BH - 34) / max(n, 1))
    for k, (kind, headline) in enumerate(stories):
        ly = y0 + 31 + k * step
        f = fitted(headline, BW - 44, 13)
        assert bottom(ly, headline, f) <= y0 + BH - 4, (title, headline)
        rect(x0 + 9, ly + 3, x0 + 13, ly + 13, COLORS[key])
        icon(kind, x0 + 18, ly + 1, 12, COLORS[key])
        text(x0 + 36, ly, headline, f, INK)
        if k + 1 < n:
            line(x0 + 9, ly + step - 4, x0 + BW - 9, ly + step - 4, (222, 220, 212), 1)

# footer
rect(22, 968, 1002, 1000, INK)
text(32, 976, 'ALSO TODAY:  HAGIA SOPHIA TUNNELS  ·  MERCURY FLYBY  ·  COP31 DEAL  ·  FIRST NWSL TITLE', Regular(11), WHITE)
text(22, 1004, 'SOURCES: REUTERS · AP · BBC · NHK · ANADOLU  |  COMPILED 22 NOV 2026', Regular(9), MUTED)

out = img.resize((W, H), Image.Resampling.LANCZOS)
out.save('C:/Users/ainur/AppData/Local/hermes/cache/scratch/makefun/news-entry/entry.png', optimize=False)
print('wrote entry.png', W, H)
