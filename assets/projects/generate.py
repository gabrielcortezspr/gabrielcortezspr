"""Gera assets/projects/*.svg: cartas animadas (pixel art + SMIL) no estilo do site."""
import os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

INK, INK2, INK3, INK4, LINE, BG, SEAL = '#f2f2f2', '#b8b8b8', '#7a7a7a', '#4a4a4a', '#262626', '#0a0a0a', '#e0443a'
RAR = {'legendary': INK, 'rare': SEAL, 'uncommon': '#9a9a9a'}
FONT = "ui-monospace, 'JetBrains Mono', 'Cascadia Code', 'SF Mono', Menlo, Consolas, monospace"
PAL = {'#': INK, '+': '#6c6c6c', 'r': SEAL, 'o': '#2a2a2a', 'g': INK3, 'd': '#1c1c1c', 'w': INK2}

def px(grid, x0, y0, s, pal=PAL, extra=''):
    """grade de caracteres -> rects nítidos"""
    out = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in pal:
                out.append(f'<rect x="{x0+x*s}" y="{y0+y*s}" width="{s}" height="{s}" fill="{pal[ch]}"{extra}/>')
    return ''.join(out)

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;')

# área da arte: x 22..278, y 52..228 (256 x 176), centro (150,140)
AX, AY, AW, AH = 22, 52, 256, 176

# ───────────────────────── artes ─────────────────────────
def art_narrater():
    s = 6
    term = ['##########',
            '#r+g####g#',
            '##########',
            '#dddddddd#',
            '#d+ddwwdd#',
            '#dd+ddddd#',
            '#d+dwwwdd#',
            '#dddddddd#',
            '##########']
    L = (40, 104); R = (200, 104)   # centros
    g = []
    # aresta (fio pontilhado que "corre")
    g.append(f'<path d="M{L[0]+30} {L[1]} C 120 70, 150 70, {R[0]-30} {R[1]}" fill="none" stroke="{INK3}" stroke-width="2" stroke-dasharray="4 4" shape-rendering="crispEdges">'
             f'<animate attributeName="stroke-dashoffset" values="16;0" dur="0.8s" repeatCount="indefinite"/></path>')
    g.append(f'<g>{px(term, L[0]-30, L[1]-24, s)}</g>')
    g.append(f'<g>{px(term, R[0]-30, R[1]-24, s)}</g>')
    # cursores piscando
    for (cx, cy), d in ((L, '0s'), (R, '0.6s')):
        g.append(f'<rect x="{cx-30+6*6}" y="{cy-24+6*4}" width="6" height="6" fill="{SEAL}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.2s" begin="{d}" repeatCount="indefinite"/></rect>')
    # pacote viajando pela aresta, ida e volta
    path = f'M{L[0]+30} {L[1]} C 120 70, 150 70, {R[0]-30} {R[1]}'
    g.append(f'<rect x="-5" y="-5" width="10" height="10" fill="{INK}"><animateMotion dur="3.2s" repeatCount="indefinite" keyPoints="0;1;1;0;0" keyTimes="0;.4;.5;.9;1" calcMode="linear" path="{path}"/></rect>')
    g.append(f'<rect x="-3" y="-3" width="6" height="6" fill="{SEAL}"><animateMotion dur="3.2s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;.5;.9;1" calcMode="linear" path="M{R[0]-30} {R[1]} C 150 70, 120 70, {L[0]+30} {L[1]}"/>'
             f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.5;.52;.9;.92" dur="3.2s" repeatCount="indefinite"/></rect>')
    # nós no fim da aresta
    for x in (L[0]+30, R[0]-30):
        g.append(f'<rect x="{x-4}" y="{L[1]-4}" width="8" height="8" fill="{BG}" stroke="{INK}" stroke-width="2"/>')
    # rótulos
    g.append(f'<text x="{L[0]}" y="152" text-anchor="middle" font-size="10" fill="{INK3}">claude</text>')
    g.append(f'<text x="{R[0]}" y="152" text-anchor="middle" font-size="10" fill="{INK3}">codex</text>')
    return f'<g transform="translate({AX+8},{AY+10})">{"".join(g)}</g>'

def art_prolink():
    trophy = ['############',
              '##.######.##',
              '#..#rr###..#',
              '#..##r###..#',
              '##.#rrr##.##',
              '...######...',
              '....####....',
              '.....##.....',
              '.....##.....',
              '....++++....',
              '...######...',
              '...######...']
    s = 9
    tw = 12 * s
    cx, cy = AX + AW/2, AY + AH/2
    body = px(trophy, cx - tw/2, cy - tw/2 - 4, s)
    g = [f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="3s" repeatCount="indefinite"/>{body}</g>']
    # brilho no troféu
    g.append(f'<rect x="{cx-tw/2+2*s}" y="{cy-tw/2-4}" width="{s}" height="{3*s}" fill="#ffffff" opacity="0"><animate attributeName="opacity" values="0;0;.55;0" keyTimes="0;.7;.8;1" dur="4s" repeatCount="indefinite"/></rect>')
    # evidências (ART/CAT) orbitando
    doc = ['pppp', 'pllp', 'pppp', 'plpp', 'pppr']
    dp = {'p': '#e8e4da', 'l': '#9a9a9a', 'r': SEAL}
    orbit = f'M {cx-104} {cy+6} a 104 30 0 1 0 208 0 a 104 30 0 1 0 -208 0'
    for i, b in enumerate(('0s', '-2s', '-4s')):
        g.append(f'<g>{px(doc, -8, -10, 4, dp)}<animateMotion dur="6s" begin="{b}" repeatCount="indefinite" path="{orbit}"/></g>')
    g.append(f'<text x="{cx}" y="{AY+AH-8}" text-anchor="middle" font-size="10" fill="{INK3}">1st · CREA-AM · CENATEC 2026</text>')
    return ''.join(g)

def art_busflow():
    board = ['oooooooooooooooo',
             'o+o+o+o+o+o+o+oo',
             'oddddddddddddddo',
             'odd####dddd##ddo',
             'od#gggg#dd#gg#do',
             'od#gggg#dddddddo',
             'odd####ddddrdddo',
             'oddddddddddddddo',
             'o+o+o+o+o+o+o+oo',
             'oooooooooooooooo']
    s = 7
    bx, by = AX + 24, AY + 70
    g = [px(board, bx, by, s)]
    # sensor ultrassônico
    sx, sy = bx + 16*s + 6, by + 2*s
    for k in (0, 1):
        g.append(f'<circle cx="{sx+10}" cy="{sy+10+k*26}" r="10" fill="#1c1c1c" stroke="{INK}" stroke-width="3"/>')
    # ondas
    for i in range(3):
        g.append(f'<path d="M {sx+26} {sy+5} q 10 18 0 36" fill="none" stroke="{INK}" stroke-width="3" opacity="0">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;48 0" dur="1.8s" begin="{i*0.6}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;0" dur="1.8s" begin="{i*0.6}s" repeatCount="indefinite"/></path>')
    # LED do led piscando
    g.append(f'<rect x="{bx+11*s}" y="{by+6*s}" width="{s}" height="{s}" fill="{SEAL}"><animate attributeName="fill" values="{SEAL};#3a1512;{SEAL}" dur="0.9s" repeatCount="indefinite"/></rect>')
    # pacotes MQTT subindo para o broker
    brk = (bx + 4*s, AY + 14)
    g.append(f'<rect x="{brk[0]-22}" y="{brk[1]}" width="44" height="16" fill="none" stroke="{INK3}" stroke-width="2"/>'
             f'<text x="{brk[0]}" y="{brk[1]+12}" text-anchor="middle" font-size="9" fill="{INK2}">mqtt</text>')
    for i in range(3):
        g.append(f'<rect x="{brk[0]-4}" y="{by-8}" width="8" height="8" fill="{INK}" opacity="0">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -{by-8-brk[1]-18}" dur="2.1s" begin="{i*0.7}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="2.1s" begin="{i*0.7}s" repeatCount="indefinite"/></rect>')
    # contador de passageiros
    g.append(f'<text x="{AX+AW-14}" y="{AY+24}" text-anchor="end" font-size="11" fill="{INK3}">pax <tspan fill="{INK}">'
             '<animate attributeName="opacity" values="1;.4;1" dur="1.8s" repeatCount="indefinite"/>27</tspan></text>')
    return ''.join(g)

def art_tabletop():
    knight = ['.....##.....',
              '....####....',
              '...##r###...',
              '..#######...',
              '..##..###...',
              '......###...',
              '.....####...',
              '....#####...',
              '...######...',
              '...######...',
              '..++++++++..',
              '.##########.']
    sq = 36
    n = 5
    bx = AX + (AW - n*sq)/2
    by = AY + 10
    g = []
    for r in range(4):
        for c in range(n):
            g.append(f'<rect x="{bx+c*sq}" y="{by+r*sq}" width="{sq}" height="{sq}" fill="{"#1a1a1a" if (r+c)%2 else "#101010"}"/>')
    g.append(f'<rect x="{bx}" y="{by}" width="{n*sq}" height="{4*sq}" fill="none" stroke="{LINE}" stroke-width="2"/>')
    # rota do cavalo em L: (c,r)
    route = [(0, 3), (1, 1), (3, 0), (4, 2), (2, 3), (0, 3)]
    pts = [(bx + c*sq, by + r*sq) for c, r in route]
    # marca as casas visitadas (pegadas)
    for i, (x, y) in enumerate(pts[1:-1]):
        t = (i+1)/(len(pts)-1)
        g.append(f'<rect x="{x+14}" y="{y+14}" width="8" height="8" fill="{SEAL}" opacity="0"><animate attributeName="opacity" values="0;0;.8;.8;0" keyTimes="0;{t-0.001:.3f};{t:.3f};.98;1" dur="6s" repeatCount="indefinite"/></rect>')
    # cavalo: salto discreto com "pulo"
    vals, keys = [], []
    steps = len(pts) - 1
    for i in range(steps):
        (x0, y0), (x1, y1) = pts[i], pts[i+1]
        t0, t1 = i/steps, (i+1)/steps
        tm = t0 + (t1-t0)*0.25
        tj = t0 + (t1-t0)*0.45
        vals += [f'{x0} {y0}', f'{x0} {y0}', f'{(x0+x1)/2} {min(y0,y1)-22}', f'{x1} {y1}']
        keys += [t0, tm, tj, t0 + (t1-t0)*0.65]
    vals.append(f'{pts[-1][0]} {pts[-1][1]}'); keys.append(1)
    # keyTimes precisam ser crescentes e únicos
    kt = ';'.join(f'{k:.4f}' for k in keys)
    g.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(vals)}" keyTimes="{kt}" dur="6s" repeatCount="indefinite"/>'
             f'{px(knight, 0, 0, 3)}</g>')
    g.append(f'<text x="{AX+AW/2}" y="{AY+AH-6}" text-anchor="middle" font-size="10" fill="{INK3}">Nb1-c3 · chess &amp; go</text>')
    return ''.join(g)

def art_suminagashi():
    cx, cy = AX + AW/2, AY + AH/2
    g = [f'<g filter="url(#marble)" clip-path="url(#artclip)">']
    for d in range(6):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="none" stroke="{INK}" stroke-width="{2.2 if d%2==0 else 1.1}">'
                 f'<animate attributeName="r" values="4;150" dur="6s" begin="{-d}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values=".9;0" dur="6s" begin="{-d}s" repeatCount="indefinite"/></circle>')
    for d in range(3):
        ox, oy = cx + (-70, 72, 40)[d], cy + (-34, 26, -50)[d]
        g.append(f'<circle cx="{ox}" cy="{oy}" r="2" fill="none" stroke="{INK2}" stroke-width="1.2">'
                 f'<animate attributeName="r" values="2;60" dur="4.5s" begin="{-d*1.5}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values=".8;0" dur="4.5s" begin="{-d*1.5}s" repeatCount="indefinite"/></circle>')
    g.append('</g>')
    # gota caindo
    g.append(f'<rect x="{cx-3}" y="{AY+4}" width="6" height="6" fill="{INK}"><animate attributeName="y" values="{AY+4};{cy-3}" dur="6s" keyTimes="0;1" keySplines=".5 0 1 1" calcMode="spline" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;.95;1" dur="6s" repeatCount="indefinite"/></rect>')
    g.append(f'<text x="{AX+AW-12}" y="{AY+22}" text-anchor="end" font-size="16" fill="{INK3}">墨流し</text>')
    return ''.join(g)

def art_site():
    cx = AX + AW/2
    mw, mh = 168, 112
    mx, my = cx - mw/2, AY + 18
    g = [f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="#141414" stroke="{INK}" stroke-width="4"/>',
         f'<rect x="{cx-14}" y="{my+mh+2}" width="28" height="10" fill="{INK3}"/>',
         f'<rect x="{cx-40}" y="{my+mh+12}" width="80" height="6" fill="{INK}"/>']
    # tabuleiro em perspectiva (pixel) dentro do monitor
    inner = f'<g clip-path="url(#scr)">'
    sq = 14
    for r in range(8):
        for c in range(12):
            if (r+c) % 2:
                inner += f'<rect x="{mx+4+c*sq}" y="{my+4+r*sq}" width="{sq}" height="{sq}" fill="#202020"/>'
    # tinta circulando
    inner += f'<circle cx="{cx}" cy="{my+mh/2}" r="10" fill="none" stroke="{INK3}" stroke-width="2"><animate attributeName="r" values="6;70" dur="3s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="1;0" dur="3s" repeatCount="indefinite"/></circle>'
    knight = ['..##..', '.####.', '##r##.', '..###.', '.####.', '######']
    inner += f'<g>{px(knight, cx-12, my+mh/2-14, 4)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="1.6s" repeatCount="indefinite"/></g>'
    # scanline descendo
    inner += f'<rect x="{mx}" y="{my}" width="{mw}" height="6" fill="#ffffff" opacity=".07"><animate attributeName="y" values="{my};{my+mh}" dur="2.4s" repeatCount="indefinite"/></rect>'
    inner += '</g>'
    g.append(inner)
    g.append(f'<defs><clipPath id="scr"><rect x="{mx+2}" y="{my+2}" width="{mw-4}" height="{mh-4}"/></clipPath></defs>')
    g.append(f'<rect x="{mx+mw-14}" y="{my+mh-12}" width="6" height="6" fill="{SEAL}"><animate attributeName="opacity" values="1;.2;1" dur="2s" repeatCount="indefinite"/></rect>')
    return ''.join(g)

# ───────────────────────── carta ─────────────────────────
CARDS = [
    dict(file='narrater', no='01', name='NarraTer', rarity='legendary', art=art_narrater,
         lines=['Infinite canvas for terminals and', 'AI agents on Linux: each terminal', 'is a node, edges decide who can', 'talk to whom.'],
         tags=['Rust', 'Tauri 2', 'React', 'xterm.js']),
    dict(file='prolink', no='02', name='Pro-Link', rarity='legendary', art=art_prolink,
         lines=['Marketplace matching technical', 'demands to CREA professionals by', 'documentary evidence (ART/CAT).', 'Winning team, CREA-AM challenge.'],
         tags=['PHP 8.2', 'MariaDB', 'Twig', 'Docker']),
    dict(file='busflow', no='03', name='BusFlow', rarity='rare', art=art_busflow,
         lines=['IoT prototype that measures bus', 'and bus-stop occupancy in real', 'time. State finalist, Liga Jovem', '2025.'],
         tags=['ESP32', 'MQTT', 'Prisma', 'Next.js']),
    dict(file='tabletop', no='04', name='Tabletop', rarity='rare', art=art_tabletop,
         lines=['Chess and Go in 2D pixel art with', 'shader effects, a full rules', 'engine and tests.', ''],
         tags=['Python', 'pygame', 'ModernGL']),
    dict(file='suminagashi', no='05', name='Suminagashi', rarity='uncommon', art=art_suminagashi,
         lines=['GLSL shader recreating the', 'Japanese ink-marbling art. It is', 'the live background of my site.', ''],
         tags=['GLSL', 'Shadertoy', 'Generative']),
    dict(file='site', no='06', name='Portfolio', rarity='rare', art=art_site,
         lines=['This profile as a site: 3D', 'chessboard, pixel post-processing', 'and a live suminagashi background.', ''],
         tags=['three.js', 'WebGL', 'Web Audio']),
]

W, H = 300, 420

def card(c):
    col = RAR[c['rarity']]
    leg = c['rarity'] == 'legendary'
    parts = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">',
             f'<title>{esc(c["name"])}</title>',
             '<defs>',
             '<filter id="marble" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.014 0.021" numOctaves="2" seed="8"/><feDisplacementMap in="SourceGraphic" scale="28" xChannelSelector="R" yChannelSelector="G"/></filter>',
             f'<clipPath id="artclip"><rect x="{AX}" y="{AY}" width="{AW}" height="{AH}"/></clipPath>',
             f'<clipPath id="cardclip"><rect x="6" y="6" width="{W-20}" height="{H-20}" rx="10"/></clipPath>',
             '<linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
             '<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" opacity=".025"/></pattern>',
             '<pattern id="chk" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#121212"/><rect x="8" y="8" width="8" height="8" fill="#121212"/></pattern>',
             '</defs>']
    # sombra offset (vermelha nas lendárias, como no site)
    parts.append(f'<rect x="14" y="14" width="{W-20}" height="{H-20}" rx="10" fill="{SEAL if leg else "#050505"}" opacity="{1 if leg else .9}"/>')
    parts.append(f'<rect x="6" y="6" width="{W-20}" height="{H-20}" rx="10" fill="{BG}" stroke="{col}" stroke-width="3"/>')
    parts.append(f'<g clip-path="url(#cardclip)">')
    # cabeçalho
    parts.append(f'<text x="22" y="36" font-size="11" letter-spacing="2" fill="{col}">{c["rarity"].upper()}</text>')
    parts.append(f'<text x="{W-36}" y="36" text-anchor="end" font-size="11" fill="{INK4}">{c["no"]}</text>')
    # área da arte
    parts.append(f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" fill="#0d0d0d"/><rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" fill="url(#chk)"/>')
    parts.append(f'<g clip-path="url(#artclip)" shape-rendering="crispEdges">{c["art"]()}</g>')
    parts.append(f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" fill="none" stroke="{LINE}" stroke-width="2"/>')
    # nome e descrição
    parts.append(f'<text x="22" y="262" font-size="22" font-weight="700" fill="{INK}">{esc(c["name"])}</text>')
    parts.append(f'<rect x="22" y="272" width="28" height="3" fill="{col}"/>')
    for i, ln in enumerate(c['lines']):
        if ln:
            parts.append(f'<text x="22" y="{296+i*16}" font-size="11.5" fill="{INK2}">{esc(ln)}</text>')
    # tags
    x = 22
    for t in c['tags']:
        w = len(t)*6.6 + 14
        parts.append(f'<rect x="{x}" y="364" width="{w:.1f}" height="20" rx="2" fill="#141414" stroke="{LINE}"/><text x="{x+7}" y="378" font-size="10.5" fill="{INK3}">{esc(t)}</text>')
        x += w + 6
    # scanlines + foil varrendo
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    parts.append(f'<rect x="-300" y="0" width="200" height="{H}" fill="url(#foil)" transform="skewX(-20)"><animate attributeName="x" values="-300;-300;500" keyTimes="0;.6;1" dur="7s" begin="{int(c["no"])*0.7:.1f}s" repeatCount="indefinite"/></rect>')
    parts.append('</g></svg>')
    return '\n'.join(parts)

for c in CARDS:
    with open(os.path.join(OUT, c['file'] + '.svg'), 'w') as f:
        f.write(card(c))
print('ok', [c['file'] for c in CARDS])
