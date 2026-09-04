#!/usr/bin/env python3
"""Patch shared markup in locations/*.html. Idempotent. Run from repo root."""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_hubs import icon  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'

NAV = '''      <nav class="nav" id="nav">
        <a href="#services">Services</a>
        <a href="../index.html#solutions">Solutions</a>
        <a href="#why">Why Us</a>
        <a href="../index.html#areas">Locations</a>
        <a href="#contact">Contact</a>
        <a href="#contact" class="btn btn-primary nav-cta">Get a Quote</a>
      </nav>
      <a href="#contact" class="btn btn-primary header-cta">Get a Quote</a>'''

BADGES = f'''        <ul class="hero-badges">
          <li>{CHECK} 20+ years in IT</li>
          <li>{CHECK} 300+ carriers &amp; providers</li>
          <li>{CHECK} One advisor, one direct line</li>
        </ul>'''

CARDS = [
    ("cybersecurity", "Cybersecurity", "shield-check", "#16294b", "#2a86c4",
     "Assessments, managed firewalls, endpoint protection, SIEM, SOC as a Service, and incident response from vetted providers."),
    ("mobility", "Mobility", "smartphone", "#1f6fa5", "#45c1e8",
     "Devices, carrier plans, private LTE/5G, and managed mobility across AT&amp;T, Verizon, and T-Mobile."),
    ("advanced-networking", "Advanced Networking", "network", "#2a86c4", "#5cc7e8",
     "Dedicated fiber, SD-WAN with auto-failover, SASE, managed WiFi, and network monitoring."),
    ("cloud-managed-services", "Cloud &amp; Managed Services", "cloud", "#1f9fd4", "#7ad6ef",
     "AWS, Azure, GCP, private and hybrid cloud, colocation, DRaaS, and helpdesk or IT outsourcing."),
    ("iot", "IoT", "cpu", "#3a5f93", "#5fa8d8",
     "Sensors, cameras and access control, energy monitoring, and telematics for connected operations."),
]


def cards_html(city):
    out = []
    for slug, name, ico, c1, c2, blurb in CARDS:
        out.append(f'''          <article class="service-card">
            <span class="svc-icon" style="--c1:{c1};--c2:{c2}">{icon(ico)}</span>
            <h3>{name}</h3>
            <p>{blurb}</p>
            <a class="svc-link" href="../services/{slug}.html">{name} solutions &rarr;</a>
          </article>''')
    return "\n".join(out)


FOOTER_SERVICES = '''      <div class="footer-col">
        <h4>Services</h4>
        <a href="../services/cybersecurity.html">Cybersecurity</a>
        <a href="../services/mobility.html">Mobility</a>
        <a href="../services/advanced-networking.html">Advanced Networking</a>
        <a href="../services/cloud-managed-services.html">Cloud &amp; Managed Services</a>
        <a href="../services/iot.html">IoT</a>
      </div>'''

# Copied verbatim from index.html so location pages match the form script.js expects
# (phone, services checkboxes, details, #svcError).
CONTACT_FORM = '''        <form class="contact-form" id="contactForm" novalidate>
          <div class="field">
            <label for="name">Full name</label>
            <input id="name" name="name" type="text" required placeholder="Jane Doe" autocomplete="name" />
          </div>
          <div class="field">
            <label for="email">Work email</label>
            <input id="email" name="email" type="email" required placeholder="jane@company.com" autocomplete="email" />
          </div>
          <div class="field">
            <label for="phone">Phone <span class="muted">(optional)</span></label>
            <input id="phone" name="phone" type="tel" placeholder="(512) 555-0100" autocomplete="tel" />
          </div>
          <div class="field">
            <label for="company">Company <span class="muted">(optional)</span></label>
            <input id="company" name="company" type="text" placeholder="Company name" autocomplete="organization" />
          </div>
          <fieldset class="field" aria-describedby="svcError">
            <legend class="field-group-label">What are you looking for?</legend>
            <div class="check-group">
              <label><input type="checkbox" name="services" value="Cybersecurity" /> Cybersecurity</label>
              <label><input type="checkbox" name="services" value="Mobility" /> Mobility</label>
              <label><input type="checkbox" name="services" value="Advanced Networking" /> Advanced Networking</label>
              <label><input type="checkbox" name="services" value="Cloud & Managed Services" /> Cloud &amp; Managed Services</label>
              <label><input type="checkbox" name="services" value="IoT" /> IoT</label>
              <label><input type="checkbox" name="services" value="Customer Experience" /> Customer Experience</label>
              <label><input type="checkbox" name="services" value="Other" /> Something else</label>
            </div>
            <p class="field-error" id="svcError" role="alert" hidden>Pick at least one.</p>
          </fieldset>
          <div class="field">
            <label for="details">Details</label>
            <textarea id="details" name="details" rows="4" required placeholder="e.g. ransomware protection for about 100 endpoints, and moving our lines to AT&amp;T"></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary btn-lg">Email My Request</button>
            <button type="button" id="textBtn" class="btn btn-accent btn-lg">Text My Request</button>
          </div>
          <p class="form-note" id="formNote" hidden>Opening your email or text app with the details filled in &mdash; just hit send and we'll reply within one business day.</p>
        </form>'''

CONTACT_COPY = '''          <span class="eyebrow">Get a Quote</span>
          <h2>Tell us what you're looking for</h2>
          <p>Describe what you need. Your advisor replies within one business day with next steps and has options ready within two to three.</p>'''

FOOTER_BRAND_P = ('<p>Independent IT advisory for businesses that want enterprise-grade '
                  'technology without the enterprise runaround.</p>')

KNOWS_ABOUT = ('"knowsAbout":["Cybersecurity","Mobility","Advanced Networking",'
               '"Cloud & Managed Services","IoT"]')

# Residual stale copy that lives inside otherwise city-specific sections.
TEXT_REPLACEMENTS = [
    # Hero + CTA band buttons
    ('>Get a Free IT Assessment</a>', '>Get a Quote</a>'),
    ('>Schedule Your Assessment</a>', '>Get a Quote</a>'),
    ("<p>Book a free 30-minute assessment. We'll map your risks and opportunities &mdash; no pressure, no cost.</p>",
     '<p>Tell us what you need. Your advisor replies within one business day and has options ready within two to three.</p>'),
    # Services section intro (two template variants)
    ('<p>From day-to-day help desk to cloud, cybersecurity, and telecom &mdash; enterprise-grade IT, right-sized for small and growing businesses.</p>',
     '<p>Sourced from 300+ carriers and providers and managed through one advisor &mdash; enterprise-grade technology, right-sized for your business.</p>'),
    ('<p>From day-to-day help desk to Dell hardware and VoIP phones &mdash; enterprise-grade IT, right-sized for small and growing businesses.</p>',
     '<p>Sourced from 300+ carriers and providers and managed through one advisor &mdash; enterprise-grade technology, right-sized for your business.</p>'),
    # Why-copy paragraphs on individual cities
    ('We provide SOC 2-ready managed IT, modernize your cloud, and source the best providers',
     'We match you with providers that meet your compliance requirements, modernize your cloud, and handle the sourcing'),
    ('We provide HIPAA- and SOC 2-ready managed IT, modernize your cloud, and source the best providers',
     'We match you with providers that meet your compliance requirements, modernize your cloud, and handle the sourcing'),
    ('We deliver SOC 2- and HIPAA-ready managed IT, modernize your cloud, and source the best providers',
     'We match you with providers that meet your compliance requirements, modernize your cloud, and handle the sourcing'),
    ('we handle your networks, security, and help desk so a tech headache never costs you a day of business.',
     'we line up your networks, security, and support so a tech headache never costs you a day of business.'),
    ('You get senior engineers who answer the phone, flat monthly pricing, and a team that actually knows Austin.',
     'You get one advisor who answers the phone, 300+ carriers and providers behind them, and someone who actually knows Austin.'),
    ('with flat pricing and senior engineers on call.',
     'with one advisor on call and 300+ carriers and providers behind them.'),
    # AetherPoint is paid by the providers, so it cannot promise flat monthly pricing.
    ('<strong>Fixed, predictable pricing</strong><span>Flat monthly plans &mdash; no surprise invoices.</span>',
     '<strong>Pricing you see up front</strong><span>Quotes before commitments &mdash; no surprise invoices.</span>'),
    ('and source the best cloud and carrier deals &mdash; managed remotely, with straight answers and flat pricing.',
     'and source the best cloud and carrier deals &mdash; managed remotely, with straight answers and one advisor on call.'),
    ('and cut through carrier and software sprawl &mdash; with flat pricing and no runaround.',
     'and cut through carrier and software sprawl &mdash; with one advisor on call and no runaround.'),
    ('and connect you with the right providers &mdash; all managed remotely with flat pricing and a real human on call.',
     'and connect you with the right providers &mdash; all managed remotely, with one advisor on call and 300+ carriers and providers behind them.'),
    ('and negotiate the right telecom and software providers &mdash; with flat pricing and honest advice.',
     'and negotiate the right telecom and software providers &mdash; with one advisor on call and honest advice.'),
    ('and handle the sourcing &mdash; with flat pricing and a direct line to a 20-year veteran.',
     'and handle the sourcing &mdash; with 300+ carriers and providers behind you and a direct line to a 20-year veteran.'),
    ('and connect you with the right cloud and telecom providers &mdash; with flat, predictable pricing.',
     'and connect you with the right cloud and telecom providers &mdash; with quotes up front and one advisor on call.'),
]


def sub_once(pattern, repl, s, path, flags=re.S):
    new, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"{path}: pattern not found: {pattern[:60]}")
    return new


def meta_description(area):
    d = (f"AetherPoint is an independent IT advisor for businesses in {area}. "
         "One advisor, 300+ carriers and providers, and a reply within one business day.")
    assert len(d) < 160, (area, len(d))
    return d


def patch(path):
    s = open(path).read()
    city = re.search(r"<h1>.*?in <span class=\"grad-text\">(.*?)</span>", s, re.S)
    city = city.group(1) if city else ""
    area = re.search(r'"areaServed":"([^"]*)"', s)
    area = area.group(1) if area else city

    s = sub_once(r'      <nav class="nav" id="nav">.*?</nav>\s*<a href="#contact" class="btn btn-primary header-cta">[^<]*</a>', lambda m: NAV, s, path)
    s = sub_once(r'        <ul class="hero-badges">.*?</ul>', lambda m: BADGES, s, path)
    s = sub_once(r'(<section class="section services" id="services">.*?<div class="card-grid">\n).*?(\n        </div>\n      </div>\n    </section>)',
                 lambda m: m.group(1) + cards_html(city) + m.group(2), s, path)
    s = sub_once(r'(<div class="contact-copy">\s*)<span class="eyebrow">[^<]*</span>\s*<h2>.*?</h2>\s*<p>.*?</p>',
                 lambda m: m.group(1) + CONTACT_COPY.lstrip(), s, path)
    s = sub_once(r'        <form class="contact-form" id="contactForm" novalidate>.*?</form>', lambda m: CONTACT_FORM, s, path)
    s = sub_once(r'      <div class="footer-col">\s*<h4>Services</h4>.*?</div>', lambda m: FOOTER_SERVICES, s, path)
    s = sub_once(r'(<div class="footer-brand">.*?</a>\s*)<p>.*?</p>', lambda m: m.group(1) + FOOTER_BRAND_P, s, path)
    s = sub_once(r'<meta name="description" content="[^"]*" />',
                 lambda m: f'<meta name="description" content="{meta_description(area)}" />', s, path)
    s = sub_once(r'"knowsAbout":\[[^\]]*\]', lambda m: KNOWS_ABOUT, s, path)

    # Homepage-parity footer cleanup (no-ops on pages that never had these blocks).
    s = re.sub(r'\s*<div class="footer-col footer-news">.*?</form>\s*</div>', "", s, count=1, flags=re.S)
    s = re.sub(r'\s*<div class="socials">.*?</div>', "", s, count=1, flags=re.S)
    s = re.sub(r'<a href="[^"]*">Security</a>', "", s, count=1)

    for old, new in TEXT_REPLACEMENTS:
        s = s.replace(old, new)

    open(path, "w").write(s)


def main():
    paths = sorted(glob.glob(os.path.join(ROOT, "locations", "*.html")))
    for p in paths:
        patch(p)
    print(f"patched {len(paths)} location pages")


if __name__ == "__main__":
    main()
