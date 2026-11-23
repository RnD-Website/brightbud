"""Build the Brightbud inner pages from the homepage's shared parts.

Run from the project folder:  python3 src/build.py
- Reads index.html for the shared <head>, brand shapes, menu, sign-up band and footer.
- Wraps each src/<page>.body.html into a full page (<page>.html).
- Points every menu/footer/homepage link at the real pages.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    'classes':  ('Classes',  'Classes — Brightbud',  'Five colour-coded classes for ages 5 to 10, from Tiny Explorers to Future Makers.'),
    'subjects': ('Subjects', 'Subjects — Brightbud', 'Reading, maths, science, art, coding and life skills, growing from Class 1 to Class 5.'),
    'mentors':  ('Mentors',  'Mentors — Brightbud',  'Meet the trained, caring educators who guide every Brightbud learner.'),
    'clubs':    ('Clubs',    'Clubs — Brightbud',    'Live after-school clubs for building, science, coding, art, stories and music.'),
    'pricing':  ('Pricing',  'Pricing — Brightbud',  'Simple Explorer, Family and School plans. Start free for 14 days.'),
    'about':    ('About us', 'About us — Brightbud', 'The story, values and journey behind Brightbud.'),
    'careers':  ('Careers',  'Careers — Brightbud',  'Join the Brightbud team of teachers, designers and builders.'),
    'printables': ('Printables', 'Printables — Brightbud', 'Free printable worksheets, colouring pages and activity packs for Class 1 to 5.'),
    'faq':      ('FAQ',      'FAQ — Brightbud',      'Answers about getting started, learning, safety and billing.'),
    'safety':   ('Safety',   'Safety — Brightbud',   'How Brightbud keeps every child safe online.'),
    'parent-guide': ('Parent guide', 'Parent guide — Brightbud', 'Tips for parents to get started and support learning at home.'),
    'contact':  ('Contact',  'Contact — Brightbud',  'Email, call or message the Brightbud family team.'),
}
NAV_LINKS = [('Classes', 'classes.html'), ('Subjects', 'subjects.html'), ('Mentors', 'mentors.html'),
             ('Clubs', 'clubs.html'), ('Pricing', 'pricing.html')]


def between(s, start, end, include_end=True):
    i = s.index(start)
    j = s.index(end, i) + (len(end) if include_end else 0)
    return s[i:j]


def nav_html(active=None):
    items = '\n'.join(
        f'      <li><a href="{href}"{" class=\"is-active\" aria-current=\"page\"" if name == active else ""}>{name}</a></li>'
        for name, href in NAV_LINKS)
    return f'''<header class="nav" id="nav">
  <div class="nav__bar">
    <a href="index.html" class="logo" aria-label="Brightbud home"><svg><use href="#bud"/></svg><span>brightbud<i>.</i></span></a>
    <ul class="nav__links">
{items}
    </ul>
    <div class="nav__right">
      <a href="#" class="nav__login">Log in</a>
      <a href="pricing.html" class="btn btn--sun">Start free <span class="ar"><svg><use href="#arrow"/></svg></span></a>
      <button class="nav__burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>'''


def fix_footer(f):
    for label, href in [('Classes', 'classes.html'), ('Subjects', 'subjects.html'), ('Clubs', 'clubs.html'),
                        ('Mentors', 'mentors.html'), ('Pricing', 'pricing.html'), ('FAQ', 'faq.html'),
                        ('Printables', 'printables.html'), ('About us', 'about.html'), ('Careers', 'careers.html'),
                        ('Safety', 'safety.html'), ('Parent guide', 'parent-guide.html'), ('Contact', 'contact.html')]:
        f = re.sub(r'<a href="[^"]*">' + re.escape(label) + '</a>', f'<a href="{href}">{label}</a>', f)
    return f.replace('<a href="#" class="logo">', '<a href="index.html" class="logo">')


def link_homepage(s):
    """Point homepage buttons and cards at the new pages."""
    s = re.sub(r'<header class="nav" id="nav">.*?</header>', lambda m: nav_html(), s, count=1, flags=re.S)
    s = s.replace('<a href="#classes" class="btn btn--navy">Explore classes', '<a href="classes.html" class="btn btn--navy">Explore classes')
    s = s.replace('<a href="#mentors" class="btn btn--plain" style="--bg:var(--sun-t)">Meet our mentors', '<a href="mentors.html" class="btn btn--plain" style="--bg:var(--sun-t)">Meet our mentors')
    for n in range(1, 6):
        s = re.sub(r'<a href="[^"]*" class="cls reveal"(?=[^>]*>(?:(?!</a>).)*?<b>%d</b>)' % n,
                   f'<a href="classes.html#class-{n}" class="cls reveal"', s, count=1, flags=re.S)
    subj_ids = {'Reading &amp; Phonics': 'reading', 'Maths Magic': 'maths', 'Little Scientists': 'science',
                'Art &amp; Craft': 'art', 'Coding Club': 'coding', 'Life Skills': 'life'}
    for title, sid in subj_ids.items():
        s = re.sub(r'<a href="[^"]*" class="tile reveal"((?:(?!</a>).)*?<h3>' + re.escape(title) + '</h3>)',
                   lambda m: f'<a href="subjects.html#{sid}" class="tile reveal"' + m.group(1), s, count=1, flags=re.S)
    s = s.replace('<a href="#" class="tile tile--photo reveal">', '<a href="subjects.html" class="tile tile--photo reveal">')
    s = s.replace('<a href="#" class="tile tile--wide reveal">', '<a href="subjects.html" class="tile tile--wide reveal">')
    s = s.replace('<a href="#" class="btn btn--sun">Meet the mentor team', '<a href="mentors.html" class="btn btn--sun">Meet the mentor team')
    s = re.sub(r'<a href="#" class="club reveal"', '<a href="clubs.html" class="club reveal"', s)
    s = s.replace('<a href="#start" class="btn btn--sun">Start free trial', '<a href="pricing.html" class="btn btn--sun">Start free trial')
    s = s.replace('<a href="#start" class="btn btn--plain" style="--bg:var(--sun-t)">Start free trial', '<a href="pricing.html" class="btn btn--plain" style="--bg:var(--sun-t)">Start free trial')
    s = s.replace('<a href="#start" class="btn btn--sun">Choose Family', '<a href="pricing.html" class="btn btn--sun">Choose Family')
    s = s.replace('<a href="#" class="btn btn--navy">See open roles', '<a href="careers.html" class="btn btn--navy">See open roles')
    s = s.replace('<a href="#" class="btn btn--navy">Talk to us', '<a href="pricing.html#schools" class="btn btn--navy">Talk to us')
    footer = between(s, '<footer class="footer', '</footer>')
    return s.replace(footer, fix_footer(footer))


def build():
    index_path = ROOT / 'index.html'
    home = link_homepage(index_path.read_text())
    index_path.write_text(home)

    head = home[:home.index('</head>')]
    defs = between(home, '<svg class="svg-defs"', '</defs>\n</svg>')
    cta = between(home, '<!-- ===== CTA ===== -->', '</section>')
    footer = between(home, '<!-- ===== Footer ===== -->', '</footer>')
    script = '<script src="main.js"></script>'

    for slug, (name, title, desc) in PAGES.items():
        body = (ROOT / 'src' / f'{slug}.body.html').read_text()
        h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1)
        h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h, count=1)
        h = h.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="styles.css">\n  <link rel="stylesheet" href="pages.css">')
        page = (f'{h}</head>\n<body class="page-{slug}">\n\n{defs}\n\n{nav_html(name)}\n\n<main>\n{body}\n{cta}\n</main>\n\n'
                f'{footer}\n\n{script}\n</body>\n</html>\n')
        (ROOT / f'{slug}.html').write_text(page)
        print('built', f'{slug}.html')

    # Homepage also loads pages.css so the active-menu style is shared
    if 'pages.css' not in home:
        home = home.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="styles.css">\n  <link rel="stylesheet" href="pages.css">')
        index_path.write_text(home)


if __name__ == '__main__':
    build()
