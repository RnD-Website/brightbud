// Brightbud site interactions (shared by every page)
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Nav: transparent over the homepage video, solid everywhere else
  const nav = $('#nav'), hero = $('.hero');
  if (nav) {
    if (hero) {
      const onScroll = () => nav.classList.toggle('is-solid', hero.getBoundingClientRect().bottom < 90);
      addEventListener('scroll', onScroll, { passive: true }); onScroll();
    } else {
      nav.classList.add('is-solid');
    }
    const burger = $('.nav__burger');
    if (burger) burger.addEventListener('click', () => burger.setAttribute('aria-expanded', nav.classList.toggle('open')));
    $$('.nav__links a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));
  }

  // Background videos loop quietly (paused for reduced motion)
  $$('video[autoplay]').forEach(v => { if (reduce) v.pause(); else v.play().catch(() => {}); });

  // Wavy scallop edge wherever the background colour changes between sections
  (() => {
    const blocks = [...document.querySelectorAll('main > section, body > footer')];
    const pageBg = getComputedStyle(document.body).backgroundColor;
    const bg = (el) => { const c = getComputedStyle(el).backgroundColor; return (c === 'rgba(0, 0, 0, 0)' || c === 'transparent') ? pageBg : c; };
    blocks.forEach(b => { if (!b.classList.contains('page-hero')) b.classList.remove('scallop-top', 'scallop-bottom'); });
    for (let i = 1; i < blocks.length; i++) {
      const prev = blocks[i - 1], cur = blocks[i];
      if (prev.classList.contains('hero') || prev.classList.contains('page-hero')) continue;
      const a = bg(prev), b = bg(cur);
      if (a === b) continue;
      if (b !== pageBg) { cur.classList.add('scallop-top'); cur.style.setProperty('--sc', b); }
      else { prev.classList.add('scallop-bottom'); prev.style.setProperty('--sc', a); }
    }
  })();

  // Reveal on scroll + count-up numbers
  const countUp = (el) => {
    if (reduce) return;
    const end = +el.dataset.count, suf = el.dataset.suffix || '', t0 = performance.now();
    const step = (t) => {
      const p = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * e).toLocaleString() + suf;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver((entries) => entries.forEach(en => {
    if (!en.isIntersecting) return;
    en.target.classList.add('is-in');
    $$('[data-count]', en.target).forEach(countUp);
    io.unobserve(en.target);
  }), { threshold: 0.15 });
  $$('.reveal').forEach((el, i) => { el.style.transitionDelay = `${(i % 4) * 70}ms`; io.observe(el); });

  // Testimonials (homepage): featured quote with arrows + dots
  const txt = $('#revText'), dots = $('#revDots');
  if (txt && dots) {
    const reviews = [
      { t: 'My daughter asks for her ‘Bud lessons’ before cartoons. Her reading has jumped in just two months.', n: 'Priya S.', r: 'Mum of a Class 1 explorer', a: 'PS' },
      { t: 'His mentor noticed he was shy and found a way in through blocks. Now he can’t stop explaining his builds.', n: 'Ahmed R.', r: 'Dad of a Class 3 inventor', a: 'AR' },
      { t: 'Finally, screen time I don’t feel guilty about. Short, kind, and always followed by something to make.', n: 'Sofia M.', r: 'Mum of twins, Class 2', a: 'SM' },
      { t: 'The weekly report tells me exactly what she learned and what to practise. It feels like a real partnership.', n: 'Grace L.', r: 'Mum of a Class 5 maker', a: 'GL' },
    ];
    let ri = 0, timer;
    dots.innerHTML = reviews.map((_, i) => '<button role="tab" aria-label="Review ' + (i + 1) + '" aria-selected="' + (i === 0) + '"></button>').join('');
    const show = (i) => {
      ri = (i + reviews.length) % reviews.length;
      const r = reviews[ri];
      txt.classList.add('out');
      setTimeout(() => {
        txt.textContent = r.t; $('#revName').textContent = r.n; $('#revRole').textContent = r.r; $('#revAv').textContent = r.a;
        txt.classList.remove('out');
      }, reduce ? 0 : 300);
      $$('button', dots).forEach((d, k) => d.setAttribute('aria-selected', k === ri));
    };
    const auto = () => { clearInterval(timer); if (!reduce) timer = setInterval(() => show(ri + 1), 7000); };
    $('#prevQ')?.addEventListener('click', () => { show(ri - 1); auto(); });
    $('#nextQ')?.addEventListener('click', () => { show(ri + 1); auto(); });
    $$('button', dots).forEach((d, k) => d.addEventListener('click', () => { show(k); auto(); }));
    auto();
  }

  // Pricing: monthly / yearly toggle
  $$('.toggle button').forEach(b => b.addEventListener('click', () => {
    $$('.toggle button').forEach(x => x.setAttribute('aria-pressed', x === b));
    $$('[data-m]').forEach(p => (p.textContent = p.dataset[b.dataset.bill]));
    $$('[data-bill-note]').forEach(n => (n.textContent = b.dataset.bill === 'y' ? 'billed yearly' : 'billed monthly'));
  }));

  // Clubs page: category filter
  const filterBtns = $$('.filters button');
  if (filterBtns.length) {
    filterBtns.forEach(b => b.addEventListener('click', () => {
      filterBtns.forEach(x => x.setAttribute('aria-pressed', x === b));
      const f = b.dataset.filter;
      let shown = 0;
      $$('.clubs__wrap [data-cat]').forEach(c => {
        const on = f === 'all' || c.dataset.cat === f;
        c.hidden = !on; if (on) shown++;
      });
      const empty = $('#clubsEmpty'); if (empty) empty.hidden = shown > 0;
    }));
  }

  // Classes page: highlight the class you are looking at in the jump bar
  const jump = $$('.jumpbar a');
  if (jump.length) {
    const map = new Map(jump.map(a => [a.getAttribute('href').slice(1), a]));
    const sio = new IntersectionObserver((entries) => entries.forEach(en => {
      if (en.isIntersecting) jump.forEach(a => a.classList.toggle('is-on', a === map.get(en.target.id)));
    }), { rootMargin: '-45% 0px -50% 0px' });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) sio.observe(s); });
  }

  // Forms are demo-only: show a thank-you instead of sending anything
  $$('form[data-demo]').forEach(f => f.addEventListener('submit', (e) => {
    e.preventDefault();
    const done = f.querySelector('.form__done');
    if (done) { done.hidden = false; }
    const btn = f.querySelector('button[type="submit"]');
    if (btn) btn.firstChild.textContent = 'Request sent ';
  }));
})();
