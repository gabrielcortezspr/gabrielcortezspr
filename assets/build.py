"""Gera os painéis animados do README: player, skills, quests e achievements.

    python3 assets/build.py

Paleta e conteúdo seguem o site (gabrielcortezspr-site/assets/js/data.js).
Tudo é SVG + SMIL, que o GitHub anima dentro de <img>.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

INK, INK2, INK3, INK4 = '#f2f2f2', '#b8b8b8', '#7a7a7a', '#4a4a4a'
LINE, BG, PANEL, SEAL = '#262626', '#0a0a0a', '#111111', '#e0443a'
FONT = "ui-monospace, 'JetBrains Mono', 'Cascadia Code', 'SF Mono', Menlo, Consolas, monospace"
W = 900

PAL = {'#': INK, '+': '#6c6c6c', 'r': SEAL, 'o': '#2a2a2a', 'g': INK3, 'd': '#1c1c1c', 'w': INK2,
       'p': '#e8e4da', 'l': '#9a9a9a'}

ICONS = {
    'knight': ['....##......', '...####.....', '..##r###....', '.########...', '.###..###...', '......###...',
               '.....####...', '....#####...', '...######...', '...######...', '..++++++++..', '.##########.'],
    'trophy': ['############', '##.######.##', '#..#rr###..#', '#..##r###..#', '##.#rrr##.##', '...######...',
               '....####....', '.....##.....', '.....##.....', '....++++....', '...######...', '...######...'],
    'scroll': ['oooooooooooo', '.pppppppppp.', '.pllllllllp.', '.pppppppppp.', '.plllllpppp.', '.pppppppppp.',
               '.pllllllllp.', '.pppppppppp.', '.ppppprrrpp.', '.ppppprrrpp.', '.ppppprprpp.', 'oooooooooooo'],
    'chip':   ['.+.+.+.+.+..', '############', '+#oooooooo#.', '.#o######o#+', '+#o#rr###o#.', '.#o#rr###o#+',
               '+#o######o#.', '.#o######o#+', '+#oooooooo#.', '############', '.+.+.+.+.+..', '............'],
    'brain':  ['...######...', '..#oo#oo##..', '.#o##o##oo#.', '#oo#oooo#oo#', '#o#oorroo#o#', '#oo#orro#oo#',
               '#o#oooo##oo#', '.#oo##oooo#.', '..##oo#o##..', '....####....', '.....##.....', '.....##.....'],
    'server': ['############', '#oooooooooo#', '#o+o+ooorro#', '#oooooooooo#', '############', '#oooooooooo#',
               '#o+o+oooo#o#', '#oooooooooo#', '############', '.....##.....', '..########..', '............'],
    'flow':   ['##..........', '##++++......', '.....+......', '.....+..##..', '.....++++#..', '.....+..##..',
               '.....+......', '.....++++rr.', '.........rr.', '............', '............', '............'],
    'check':  ['############', '#oooooooooo#', '#o#ooooooro#', '#oo#oooorro#', '#ooo#oorroo#', '#oooo#rrooo#',
               '#ooooorroooo', '#oooooooooo#', '#o######ooo#', '#oooooooooo#', '#o####oooo#.', '############'],
}


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def px(grid, x0, y0, s, pal=PAL):
    out = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in pal:
                out.append(f'<rect x="{x0 + x * s:g}" y="{y0 + y * s:g}" width="{s:g}" height="{s:g}" fill="{pal[ch]}"/>')
    return ''.join(out)


def frame(h, cmd, body, title=None):
    """painel padrão: fundo escuro, borda, scanlines, prompt no topo"""
    t = f'<title>{esc(title or cmd)}</title>'
    return f'''<svg width="{W}" height="{h}" viewBox="0 0 {W} {h}" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">
{t}
<defs>
  <pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" opacity=".022"/></pattern>
  <linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <filter id="marble" x="-40%" y="-40%" width="180%" height="180%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.019" numOctaves="2" seed="8"/><feDisplacementMap in="SourceGraphic" scale="40" xChannelSelector="R" yChannelSelector="G"/></filter>
  <clipPath id="panel"><rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="6"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="6" fill="{BG}" stroke="#1e1e1e" stroke-width="2"/>
<g clip-path="url(#panel)">
{body}
<rect width="{W}" height="{h}" fill="url(#scan)"/>
</g>
<text x="40" y="40" font-size="15" fill="{INK4}">$ <tspan fill="{INK3}">{esc(cmd)}</tspan></text>
</svg>
'''


def ink_bloom(cx, cy, n=9, step=12, op=.32):
    rings = ''.join(f'<circle r="{4 + i * step}" stroke-width="{1.2 if i % 2 == 0 else .6}" stroke-opacity="{op - i * op / (n + 1):.3f}"/>' for i in range(n))
    return (f'<g filter="url(#marble)" transform="translate({cx},{cy})" fill="none" stroke="{INK}">{rings}'
            f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="120s" repeatCount="indefinite" additive="sum"/></g>')


def chip(x, y, text, color=INK3, fill='#141414', fs=12):
    w = len(text) * fs * .62 + 16
    return w, (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="22" rx="2" fill="{fill}" stroke="{LINE}"/>'
               f'<text x="{x + 8:.1f}" y="{y + 15}" font-size="{fs}" fill="{color}">{esc(text)}</text>')


# ═════════════════════════ player ═════════════════════════
def player():
    h = 300
    b = [ink_bloom(820, 40, 12, 14, .22)]
    # retrato
    b.append(f'<rect x="40" y="70" width="168" height="168" fill="{PANEL}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<rect x="48" y="78" width="168" height="168" fill="none" stroke="{SEAL}" stroke-width="2" opacity=".9"/>')
    b.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="2.4s" repeatCount="indefinite"/>'
             f'{px(ICONS["knight"], 64, 88, 10)}</g>')
    b.append(f'<rect x="64" y="210" width="120" height="4" fill="#1c1c1c"/>')
    b.append(f'<text x="124" y="262" text-anchor="middle" font-size="12" letter-spacing="2" fill="{INK3}">PLAYER 1</text>')
    # nome e atributos
    x = 248
    b.append(f'<text x="{x}" y="92" font-size="30" font-weight="700" fill="{INK}" letter-spacing="1">GABRIEL CORTEZ</text>')
    b.append(f'<rect x="{x + 276}" y="70" width="12" height="24" fill="{INK}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    rows = [('CLASS', 'Software Engineer · AI · Data'),
            ('GUILD', 'Samsung Electronics · Visual Display'),
            ('PARTY', 'Kacto (co-founder) · NarraTer'),
            ('BASE', 'Manaus · Amazonas · Brazil')]
    for i, (k, v) in enumerate(rows):
        y = 124 + i * 22
        b.append(f'<text x="{x}" y="{y}" font-size="12" letter-spacing="2" fill="{INK4}">{k}</text>'
                 f'<text x="{x + 70}" y="{y}" font-size="14" fill="{INK2}">{esc(v)}</text>')
    # barra de XP: graduação 2022 → 2027
    y = 222
    b.append(f'<text x="{x}" y="{y - 8}" font-size="12" letter-spacing="2" fill="{INK4}">XP</text>'
             f'<text x="{x + 70}" y="{y - 8}" font-size="12" fill="{INK3}">B.Eng. Computer Eng. · UEA · 2022 → 2027</text>')
    bw = 330
    b.append(f'<rect x="{x}" y="{y}" width="{bw}" height="14" fill="#141414" stroke="{LINE}"/>')
    b.append(f'<rect x="{x + 2}" y="{y + 2}" width="0" height="10" fill="{INK}"><animate attributeName="width" values="0;{bw * .8 - 4:.0f};{bw * .8 - 4:.0f}" keyTimes="0;.35;1" dur="6s" repeatCount="indefinite"/></rect>')
    for k in range(1, 10):
        b.append(f'<rect x="{x + k * bw / 10:.0f}" y="{y + 2}" width="2" height="10" fill="{BG}"/>')
    b.append(f'<text x="{x + bw + 10}" y="{y + 12}" font-size="12" fill="{INK2}">80%</text>')
    # missão atual
    b.append(f'<rect x="{x}" y="250" width="8" height="8" fill="{SEAL}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></rect>'
             f'<text x="{x + 16}" y="258" font-size="12" fill="{INK3}">QUEST <tspan fill="{INK2}">data &amp; AI tools for TV production lines</tspan></text>')
    # placar
    stats = [('9', 'olympiad medals'), ('1', 'championship'), ('3', 'clinics live on Kacto'), ('2', 'countries: BR · KR')]
    sx = 676
    for i, (n, label) in enumerate(stats):
        yy = 74 + i * 52
        b.append(f'<rect x="{sx}" y="{yy}" width="184" height="44" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(f'<text x="{sx + 14}" y="{yy + 31}" font-size="24" font-weight="700" fill="{SEAL if i == 1 else INK}">{n}</text>')
        b.append(f'<text x="{sx + 46}" y="{yy + 27}" font-size="11.5" fill="{INK3}">{esc(label)}</text>')
    b.append(f'<rect x="-300" y="60" width="160" height="200" fill="url(#sheen)" transform="skewX(-20)"><animate attributeName="x" values="-300;-300;1100" keyTimes="0;.7;1" dur="8s" repeatCount="indefinite"/></rect>')
    return frame(h, 'whoami --stats', ''.join(b), 'Gabriel Cortez, player card')


# ═════════════════════════ skills ═════════════════════════
SKILLS = [
    ('flow', 'DATA & AUTOMATION', 'Real-time pipelines, ETL and RPA, including legacy systems with no API.',
     'Samsung · Fundação Muraki', ['Python', 'SQL', 'Pandas', 'NumPy', 'Selenium', 'PyAutoGUI', 'OpenCV']),
    ('brain', 'AI & MACHINE LEARNING', 'Agents, RAG and models trained on real data, with real evaluation.',
     'Kacto · NarraTer · Samsung', ['LLMs', 'RAG', 'Embeddings', 'Agents', 'Scikit-Learn', 'YOLO', 'n8n']),
    ('server', 'BACK-END & APPS', 'APIs, dashboards and end-to-end apps, from requirements to deploy.',
     'Samsung · BusFlow · Pro-Link', ['FastAPI', 'Flask', 'Node.js', 'TypeScript', 'React', 'Next.js', 'PostgreSQL', 'Rust · Tauri']),
    ('chip', 'HARDWARE & EMBEDDED', 'From sensor to broker: firmware, FPGA and IoT.',
     'BusFlow · FAPEAM/SENAI research', ['ESP32', 'FPGA · Verilog', 'MQTT', 'Arduino', 'Raspberry Pi', 'C/C++']),
    ('check', 'QUALITY & EVALUATION', 'Functional and regression testing; benchmarks with hidden tests for agents.',
     'Sidia (Samsung Galaxy) · Muraki · NarraTer', ['JUnit', 'Selenium', 'Postman', 'Cucumber', 'Android QA', 'Git · Linux']),
]


def skills():
    rh, top = 100, 64
    h = top + len(SKILLS) * rh + 26
    b = [ink_bloom(860, h - 30, 10, 13, .18)]
    for i, (icon, title, what, where, items) in enumerate(SKILLS):
        y = top + i * rh
        d = i * .5
        # trilha que liga os nós
        if i < len(SKILLS) - 1:
            b.append(f'<rect x="83" y="{y + 70}" width="2" height="{rh - 44}" fill="{LINE}"/>'
                     f'<rect x="83" y="{y + 70}" width="2" height="0" fill="{INK3}"><animate attributeName="height" values="0;0;{rh - 44};{rh - 44}" keyTimes="0;{(d + .4) / 6:.3f};{(d + .7) / 6:.3f};1" dur="6s" repeatCount="indefinite"/></rect>')
        # nó com ícone
        b.append(f'<rect x="50" y="{y + 4}" width="68" height="68" fill="{PANEL}" stroke="{INK4}" stroke-width="2"/>')
        b.append(f'<rect x="50" y="{y + 4}" width="68" height="68" fill="none" stroke="{INK}" stroke-width="2" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{d / 6:.3f};{(d + .2) / 6:.3f};.92;1" dur="6s" repeatCount="indefinite"/></rect>')
        b.append(px(ICONS[icon], 60, y + 14, 4))
        # texto
        b.append(f'<text x="140" y="{y + 22}" font-size="15" font-weight="700" letter-spacing="2" fill="{INK}">{esc(title)}</text>')
        b.append(f'<text x="140" y="{y + 42}" font-size="13" fill="{INK2}">{esc(what)}</text>')
        b.append(f'<text x="{W - 40}" y="{y + 22}" text-anchor="end" font-size="11.5" fill="{INK4}">used at <tspan fill="{INK3}">{esc(where)}</tspan></text>')
        cx = 140
        for it in items:
            w, s = chip(cx, y + 52, it)
            b.append(s)
            cx += w + 6
    return frame(h, 'cat skills.tree', ''.join(b), 'Skill tree')


# ═════════════════════════ quests ═════════════════════════
QUESTS = [
    ('feb 2026 → now', 'Software Engineer', 'Samsung Electronics · Visual Display Division',
     'Real-time production data, dashboards for BR/KR leadership, RPA, ML.', True),
    ('oct 2025 → feb 2026', 'Co-founder & AI Developer', 'Kacto · Ocean Launch program',
     'GPT-4o + RAG service agent live in 3 clinics, with evals and guardrails.', False),
    ('feb 2025 → feb 2026', 'QA Intern', 'Sidia Institute · Samsung Galaxy devices',
     'Android firmware, OS and app testing alongside the Korea team.', False),
    ('sep 2024 → dec 2024', 'Test Developer', 'Fundação Muraki',
     'Test automation: Java, Selenium, JUnit, Postman, Cucumber (BDD).', False),
    ('aug 2024 → jul 2025', 'Embedded Systems Researcher', 'FAPEAM · SENAI',
     'FPGA greenhouse (Cyclone IV, Verilog), shown at Chip in the Jungle.', False),
    ('2022 → 2027', 'B.Eng. Computer Engineering', 'UEA · Universidade do Estado do Amazonas',
     'Image processing, graphics, distributed systems, data science.', False),
]


def quests():
    rh, top = 74, 72
    h = top + len(QUESTS) * rh + 14
    b = [ink_bloom(70, h - 20, 9, 13, .16)]
    lx = 70
    b.append(f'<rect x="{lx - 1}" y="{top + 10}" width="2" height="{(len(QUESTS) - 1) * rh}" fill="{LINE}"/>')
    for i, (period, role, org, text, active) in enumerate(QUESTS):
        y = top + i * rh
        col = SEAL if active else INK3
        b.append(f'<rect x="{lx - 7}" y="{y + 3}" width="14" height="14" fill="{BG}" stroke="{col}" stroke-width="3"/>')
        if active:
            b.append(f'<rect x="{lx - 7}" y="{y + 3}" width="14" height="14" fill="none" stroke="{SEAL}" stroke-width="2">'
                     f'<animate attributeName="x" values="{lx - 7};{lx - 15}" dur="1.6s" repeatCount="indefinite"/><animate attributeName="y" values="{y + 3};{y - 5}" dur="1.6s" repeatCount="indefinite"/>'
                     f'<animate attributeName="width" values="14;30" dur="1.6s" repeatCount="indefinite"/><animate attributeName="height" values="14;30" dur="1.6s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></rect>')
        b.append(f'<text x="100" y="{y + 15}" font-size="15" font-weight="700" fill="{INK}">{esc(role)} <tspan font-weight="400" fill="{INK3}">@ {esc(org)}</tspan></text>')
        b.append(f'<text x="100" y="{y + 37}" font-size="12.5" fill="{INK2}">{esc(text)}</text>')
        tag = 'ACTIVE' if active else 'CLEARED'
        tw = len(tag) * 7.5 + 14
        b.append(f'<text x="{W - 40}" y="{y + 15}" text-anchor="end" font-size="11.5" fill="{INK4}">{esc(period)}</text>')
        if active:
            b.append(f'<rect x="{W - 40 - tw}" y="{y + 24}" width="{tw:.0f}" height="18" fill="{SEAL}"><animate attributeName="opacity" values="1;.55;1" dur="1.6s" repeatCount="indefinite"/></rect>'
                     f'<text x="{W - 40 - tw / 2:.0f}" y="{y + 37}" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="1" fill="{BG}">{tag}</text>')
        else:
            b.append(f'<text x="{W - 40}" y="{y + 37}" text-anchor="end" font-size="11" letter-spacing="1" fill="{INK4}">✓ {tag}</text>')
    return frame(h, 'git log --career', ''.join(b), 'Career quest log')


# ═════════════════════════ achievements ═════════════════════════
FEATURED = [
    ('trophy', 'CHAMPION', 'Pro-Link Challenge', 'CREA-AM · II CENATEC 2026', 'Led the winning team.', SEAL),
    ('knight', 'STATE FINALIST', 'Liga Jovem 2025', 'BusFlow · IoT with ESP32 + MQTT', 'Real-time bus occupancy.', INK),
    ('scroll', 'SPEAKER', 'Chip in the Jungle', 'International event 2025', 'FPGA greenhouse research.', INK),
]
TIER = {'gold': ('#ededed', BG), 'silver': ('#a9a9a9', BG), 'bronze': ('#6c6c6c', INK), 'honor': ('#2a2a2a', INK)}
MEDALS = [  # (tier, glyph, short, year, intl)
    ('gold', '✦', 'OBA', 'Astronomy', 2020, False),
    ('bronze', '∑', 'AMO', 'Math · intl', 2021, True),
    ('bronze', 'π', 'SMO', 'Math · intl', 2021, True),
    ('bronze', '∞', 'MSF', 'Math · intl', 2021, True),
    ('silver', '⚛', 'ONC', 'Science', 2019, False),
    ('silver', '$', 'OBEF', 'Finance', 2020, False),
    ('silver', '⊕', 'MOBFOG', 'Rockets', 2020, False),
    ('bronze', '⊕', 'MOBFOG', 'Rockets', 2021, False),
    ('bronze', '⚗', 'OAQ', 'Chemistry', 2020, False),
    ('honor', '✓', 'ONC', 'Science', 2021, False),
]


def achievements():
    h = 470
    b = [ink_bloom(840, 60, 10, 13, .2)]
    b.append(f'<text x="{W - 40}" y="40" text-anchor="end" font-size="12" fill="{INK4}">13 unlocked · <tspan fill="{INK3}">3 international</tspan></text>')
    # destaques
    cw, gap, y0 = 256, 22, 64
    for i, (icon, badge, title, sub, line, col) in enumerate(FEATURED):
        x = 40 + i * (cw + gap)
        b.append(f'<rect x="{x + 6}" y="{y0 + 6}" width="{cw}" height="136" fill="{SEAL if i == 0 else "#050505"}"/>')
        b.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="136" fill="{PANEL}" stroke="{col if i == 0 else INK4}" stroke-width="2"/>')
        b.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="2.6s" begin="{i * .4}s" repeatCount="indefinite"/>'
                 f'{px(ICONS[icon], x + 16, y0 + 18, 6)}</g>')
        b.append(f'<text x="{x + 104}" y="{y0 + 30}" font-size="11" font-weight="700" letter-spacing="2" fill="{SEAL if i == 0 else INK3}">{badge}</text>')
        b.append(f'<text x="{x + 104}" y="{y0 + 52}" font-size="13" font-weight="700" fill="{INK}">{esc(title)}</text>')
        # quebra simples do subtítulo
        words, lines, cur = sub.split(' '), [], ''
        for wd in words:
            if len(cur) + len(wd) + 1 > 20:
                lines.append(cur)
                cur = wd
            else:
                cur = (cur + ' ' + wd).strip()
        lines.append(cur)
        for k, ln in enumerate(lines[:2]):
            b.append(f'<text x="{x + 104}" y="{y0 + 72 + k * 16}" font-size="11.5" fill="{INK3}">{esc(ln)}</text>')
        b.append(f'<text x="{x + 16}" y="{y0 + 120}" font-size="12" fill="{INK2}">{esc(line)}</text>')
        b.append(f'<rect x="{x - 200}" y="{y0}" width="120" height="136" fill="url(#sheen)" transform="skewX(-20)" clip-path="none">'
                 f'<animate attributeName="x" values="{x - 200};{x - 200};{x + cw + 100}" keyTimes="0;.75;1" dur="7s" begin="{i * .9}s" repeatCount="indefinite"/></rect>')
    # vitrine de medalhas
    vy = 248
    b.append(f'<text x="40" y="{vy}" font-size="12" letter-spacing="2" fill="{INK3}">SCIENCE OLYMPIADS · 2019 → 2021</text>')
    b.append(f'<rect x="40" y="{vy + 16}" width="{W - 80}" height="4" fill="#1c1c1c"/>')
    n = len(MEDALS)
    step = (W - 80) / n
    for i, (tier, glyph, short, area, year, intl) in enumerate(MEDALS):
        cx = 40 + step * i + step / 2
        top = vy + 20
        fill, gcol = TIER[tier]
        sw = 2.6 + (i % 3) * .5
        ribbon = SEAL if intl else INK4
        b.append(f'<g><animateTransform attributeName="transform" type="rotate" values="-5 {cx:.1f} {top};5 {cx:.1f} {top};-5 {cx:.1f} {top}" dur="{sw:.1f}s" begin="{-i * .37:.2f}s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
                     f'<path d="M{cx - 11:.1f} {top} L{cx - 4:.1f} {top + 44} L{cx + 4:.1f} {top + 44} L{cx + 11:.1f} {top} Z" fill="{ribbon}"/>'
                     f'<rect x="{cx - 3:.1f}" y="{top}" width="6" height="44" fill="{BG}" opacity=".35"/>'
                     f'<circle cx="{cx:.1f}" cy="{top + 70}" r="25" fill="{fill}" stroke="{BG}" stroke-width="3"/>'
                     f'<circle cx="{cx:.1f}" cy="{top + 70}" r="19" fill="none" stroke="{gcol}" stroke-opacity=".35" stroke-width="1.5"/>'
                     f'<text x="{cx:.1f}" y="{top + 77}" text-anchor="middle" font-size="19" fill="{gcol}">{glyph}</text></g>')
        b.append(f'<text x="{cx:.1f}" y="{top + 120}" text-anchor="middle" font-size="12" font-weight="700" fill="{INK2}">{short}</text>')
        b.append(f'<text x="{cx:.1f}" y="{top + 136}" text-anchor="middle" font-size="10.5" fill="{INK4}">{esc(area)}</text>')
        b.append(f'<text x="{cx:.1f}" y="{top + 151}" text-anchor="middle" font-size="10.5" fill="{INK4}">{year}</text>')
    # legenda
    ly = h - 18
    lx = 40
    for name, (fill, _) in TIER.items():
        b.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="6" fill="{fill}" stroke="{INK4}"/><text x="{lx + 16}" y="{ly}" font-size="11" fill="{INK4}">{name}</text>')
        lx += 16 + len(name) * 7 + 18
    b.append(f'<rect x="{lx}" y="{ly - 9}" width="6" height="12" fill="{SEAL}"/><text x="{lx + 14}" y="{ly}" font-size="11" fill="{INK4}">red ribbon = international</text>')
    return frame(h, 'ls ~/trophies', ''.join(b), 'Achievements')


OUT = {
    'player.svg': player,
    'skills.svg': skills,
    'quests.svg': quests,
    'achievements.svg': achievements,
}

if __name__ == '__main__':
    for name, fn in OUT.items():
        with open(os.path.join(HERE, name), 'w') as f:
            f.write(fn())
    print('ok:', ', '.join(OUT))
