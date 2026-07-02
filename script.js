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
})();
