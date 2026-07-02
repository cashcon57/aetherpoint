/* AetherPoint Digital Infrastructure Advisors — interactions */
(function () {
  'use strict';

  /* ---- Sticky header shadow ---- */
  const header = document.getElementById('header');
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 20);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- Mobile nav ---- */
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('nav');
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', (e) => {
    if (e.target.tagName === 'A') {
      nav.classList.remove('open');
      toggle.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });

  /* ---- Scroll reveal ---- */
  const revealTargets = document.querySelectorAll(
    '.service-card, .step, .ind, .why-copy, .why-card, .section-head, .stat, .contact-form, .contact-copy'
  );
  revealTargets.forEach((el) => el.classList.add('reveal'));

  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealTargets.forEach((el) => io.observe(el));

  /* ---- Animated stat counters ---- */
  const nums = document.querySelectorAll('.stat-num');
  const animate = (el) => {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || '';
    const decimals = (el.dataset.target.split('.')[1] || '').length;
    const duration = 1500;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      const val = (target * eased).toFixed(decimals);
      el.textContent = val + suffix;
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = target.toFixed(decimals) + suffix;
    };
    requestAnimationFrame(tick);
  };
  const statIO = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) { animate(entry.target); statIO.unobserve(entry.target); }
    });
  }, { threshold: 0.5 });
  nums.forEach((el) => statIO.observe(el));

  /* ---- Contact form → open a pre-filled email OR text with the visitor's info ---- */
  const CONTACT_EMAIL = 'contact@aetherpointadvisors.com';
  const CONTACT_SMS = '+17373594061';
  const form = document.getElementById('contactForm');
  const note = document.getElementById('formNote');
  if (form) {
    const getData = () => {
      const fd = new FormData(form);
      return {
        name: (fd.get('name') || '').toString().trim(),
        email: (fd.get('email') || '').toString().trim(),
        company: (fd.get('company') || '').toString().trim(),
        message: (fd.get('message') || '').toString().trim(),
      };
    };
    const valid = () => {
      if (form.checkValidity()) return true;
      form.reportValidity();
      return false;
    };
    const openEmail = () => {
      const d = getData();
      const subject = `IT assessment request — ${d.name}${d.company ? ' (' + d.company + ')' : ''}`;
      const body = [`Name: ${d.name}`, `Email: ${d.email}`, `Company: ${d.company || '—'}`, '', d.message].join('\n');
      note.hidden = false;
      window.location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    };
    const openText = () => {
      const d = getData();
      const msg =
        `IT assessment request — ${d.name}${d.company ? ' (' + d.company + ')' : ''}. ` +
        `${d.message}${d.email ? ' (reply: ' + d.email + ')' : ''}`;
      note.hidden = false;
      window.location.href = `sms:${CONTACT_SMS}?body=${encodeURIComponent(msg)}`;
    };
    // Primary submit = email; secondary button = text.
    form.addEventListener('submit', (e) => { e.preventDefault(); if (valid()) openEmail(); });
    const textBtn = document.getElementById('textBtn');
    if (textBtn) textBtn.addEventListener('click', () => { if (valid()) openText(); });
  }

  /* ---- Newsletter (demo) ---- */
  const news = document.getElementById('newsForm');
  if (news) {
    news.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = news.querySelector('input');
      if (input.value) { input.value = ''; input.placeholder = 'Subscribed ✓'; }
    });
  }

  /* ---- Reactive node-lattice background ---- */
  (function lattice() {
    const canvas = document.getElementById('lattice');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const LINK = 150;   // max distance to connect two nodes
    const MOUSE = 200;  // cursor interaction radius
    const MAX_NODES = 110;
    let w = 0, h = 0, dpr = 1, nodes = [], raf = null;
    const mouse = { x: null, y: null };

    function build() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = window.innerWidth;
      h = window.innerHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.min(MAX_NODES, Math.round((w * h) / 15000));
      nodes = [];
      for (let i = 0; i < count; i++) {
        nodes.push({
          x: Math.random() * w,
          y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.45,
          vy: (Math.random() - 0.5) * 0.45,
        });
      }
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      // move
      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i];
        n.x += n.vx; n.y += n.vy;
        if (n.x <= 0 || n.x >= w) n.vx *= -1;
        if (n.y <= 0 || n.y >= h) n.vy *= -1;
      }
      // links between nodes
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i], b = nodes[j];
          const dx = a.x - b.x, dy = a.y - b.y;
          const d = Math.sqrt(dx * dx + dy * dy);
          if (d < LINK) {
            ctx.strokeStyle = 'rgba(31,159,212,' + (1 - d / LINK) * 0.22 + ')';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
          }
        }
      }
      // cursor links + node dots
      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i];
        if (mouse.x !== null) {
          const dx = mouse.x - n.x, dy = mouse.y - n.y;
          const d = Math.sqrt(dx * dx + dy * dy);
          if (d < MOUSE) {
            ctx.strokeStyle = 'rgba(31,159,212,' + (1 - d / MOUSE) * 0.5 + ')';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(mouse.x, mouse.y); ctx.lineTo(n.x, n.y); ctx.stroke();
          }
        }
        ctx.fillStyle = 'rgba(22,41,75,0.5)';
        ctx.beginPath();
        ctx.arc(n.x, n.y, 1.6, 0, Math.PI * 2); ctx.fill();
      }
    }

    function loop() { draw(); raf = requestAnimationFrame(loop); }
    function start() { if (!raf && !reduce) loop(); }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

    build();
    if (reduce) draw(); else start();

    let rt;
    window.addEventListener('resize', () => {
      clearTimeout(rt);
      rt = setTimeout(() => { stop(); build(); if (reduce) draw(); else start(); }, 150);
    });
    window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
    window.addEventListener('mouseout', () => { mouse.x = null; mouse.y = null; });
    document.addEventListener('visibilitychange', () => { document.hidden ? stop() : start(); });
  })();
})();
