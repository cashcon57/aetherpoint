#!/usr/bin/env python3
"""Render services/<slug>.html from hub_data.HUBS. Run from the repo root."""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from hub_data import HUBS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LUCIDE = os.environ.get("LUCIDE_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons"))
# TODO at DNS cutover: switch to https://www.aetherpointadvisors.com and regenerate
SITE = "https://cashcon57.github.io/aetherpoint"
EMAIL = "contact@aetherpointadvisors.com"
PHONE_TEL = "+15123488168"
PHONE_SCHEMA = "+1-512-348-8168"
PHONE_HUMAN = "(512) 348-8168"
FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap"

MAIL_ICO = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/><rect x="2" y="4" width="20" height="16" rx="2"/></svg>'
PHONE_ICO = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg>'
PIN_ICO = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>'

SERVICES = [("Cybersecurity", "cybersecurity"), ("Mobility", "mobility"), ("Advanced Networking", "advanced-networking"),
            ("Cloud & Managed Services", "cloud-managed-services"), ("IoT", "iot")]
CHECKBOXES = ["Cybersecurity", "Mobility", "Advanced Networking", "Cloud & Managed Services", "IoT", "Customer Experience", "Other"]


def e(s):
    return html.escape(s, quote=True)


def icon(name, size=26):
    with open(os.path.join(LUCIDE, f"{name}.svg")) as f:
        svg = f.read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\s+", " ", svg).strip()
    svg = re.sub(r'\s*class="[^"]*"', "", svg, count=1)
    svg = re.sub(r'width="\d+"', f'width="{size}"', svg, count=1)
    svg = re.sub(r'height="\d+"', f'height="{size}"', svg, count=1)
    svg = svg.replace("<svg ", '<svg aria-hidden="true" ', 1)
    return svg.replace('stroke="currentColor"', 'stroke="#fff"')


def nav():
    return f'''  <header class="site-header" id="header">
    <div class="container header-inner">
      <a href="../index.html" class="logo" aria-label="AetherPoint Digital Infrastructure Advisors home">
        <img class="logo-img" src="../logo-horizontal.png" width="600" height="200" alt="AetherPoint Digital Infrastructure Advisors" />
      </a>
      <nav class="nav" id="nav">
        <a href="../index.html#services">Services</a>
        <a href="../index.html#solutions">Solutions</a>
        <a href="../index.html#why">Why Us</a>
        <a href="../index.html#areas">Service Areas</a>
        <a href="#contact">Contact</a>
        <a href="#contact" class="btn btn-primary nav-cta">Get a Quote</a>
      </nav>
      <a href="#contact" class="btn btn-primary header-cta">Get a Quote</a>
      <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-controls="nav" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
'''


def form(checked):
    boxes = "\n".join(
        f'              <label><input type="checkbox" name="services" value="{e(c)}"{" checked" if c == checked else ""} /> {e("Something else" if c == "Other" else c)}</label>'
        for c in CHECKBOXES)
    return f'''    <section class="section contact" id="contact">
      <div class="container contact-inner">
        <div class="contact-copy">
          <span class="eyebrow">Get a Quote</span>
          <h2>Tell us what you're looking for</h2>
          <p>Describe what you need. Your advisor replies within one business day with next steps and has options ready within two to three.</p>
          <ul class="contact-list">
            <li><span class="ci">{MAIL_ICO}</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><span class="ci">{PHONE_ICO}</span><a href="tel:{PHONE_TEL}">{PHONE_HUMAN}</a></li>
            <li><span class="ci">{PIN_ICO}</span>Austin, TX &mdash; serving clients nationwide</li>
          </ul>
        </div>
        <form class="contact-form" id="contactForm" novalidate>
          <div class="field"><label for="name">Full name</label><input id="name" name="name" type="text" required placeholder="Jane Doe" autocomplete="name" /></div>
          <div class="field"><label for="email">Work email</label><input id="email" name="email" type="email" required placeholder="jane@company.com" autocomplete="email" /></div>
          <div class="field"><label for="phone">Phone <span class="muted">(optional)</span></label><input id="phone" name="phone" type="tel" placeholder="(512) 555-0100" autocomplete="tel" /></div>
          <div class="field"><label for="company">Company <span class="muted">(optional)</span></label><input id="company" name="company" type="text" placeholder="Company name" autocomplete="organization" /></div>
          <fieldset class="field" aria-describedby="svcError">
            <legend class="field-group-label">What are you looking for?</legend>
            <div class="check-group">
{boxes}
            </div>
            <p class="field-error" id="svcError" role="alert" hidden>Pick at least one.</p>
          </fieldset>
          <div class="field"><label for="details">Details</label><textarea id="details" name="details" rows="4" required placeholder="e.g. ransomware protection for about 100 endpoints, and moving our lines to AT&amp;T"></textarea></div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary btn-lg">Email My Request</button>
            <button type="button" id="textBtn" class="btn btn-accent btn-lg">Text My Request</button>
          </div>
          <p class="form-note" id="formNote" hidden>Opening your email or text app with the details filled in &mdash; just hit send and we'll reply within one business day.</p>
        </form>
      </div>
    </section>
'''


def footer():
    links = "\n".join(f'        <a href="{s}.html">{e(n)}</a>' for n, s in SERVICES)
    return f'''  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a href="../index.html" class="logo logo--light">
          <span class="logo-mark" aria-hidden="true">
            <svg viewBox="0 0 32 32" width="30" height="30" aria-hidden="true">
              <defs><radialGradient id="starF" cx="50%" cy="44%" r="62%">
                <stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#7ad6ef"/><stop offset=".7" stop-color="#2fa6dd"/><stop offset="1" stop-color="#2a86c4"/>
              </radialGradient></defs>
              <path d="M16 1.5 19.6 12.4 30.5 16 19.6 19.6 16 30.5 12.4 19.6 1.5 16 12.4 12.4Z" fill="url(#starF)"/>
            </svg>
          </span>
          <span class="logo-text">Aether<strong>Point</strong></span>
        </a>
        <p>Independent IT advisory for businesses that want enterprise-grade technology without the enterprise runaround.</p>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
{links}
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="../index.html#why">Why Us</a>
        <a href="../index.html#process">Our Process</a>
        <a href="../index.html#areas">Service Areas</a>
        <a href="#contact">Contact</a>
      </div>
    </div>

    <div class="container footer-areas">
      <span>Service areas:</span>
      <a href="../locations/austin.html">Austin</a>
      <a href="../locations/round-rock.html">Round Rock</a>
      <a href="../locations/cedar-park.html">Cedar Park</a>
      <a href="../locations/georgetown.html">Georgetown</a>
      <a href="../locations/leander.html">Leander</a>
      <a href="../locations/pflugerville.html">Pflugerville</a>
      <a href="../locations/san-marcos.html">San Marcos</a>
      <a href="../locations/kyle.html">Kyle</a>
      <a href="../locations/new-york.html">New York</a>
      <a href="../locations/los-angeles.html">Los Angeles</a>
      <a href="../locations/chicago.html">Chicago</a>
      <a href="../locations/houston.html">Houston</a>
      <a href="../locations/dallas.html">Dallas</a>
      <a href="../locations/phoenix.html">Phoenix</a>
      <a href="../locations/san-francisco.html">San Francisco</a>
      <a href="../locations/seattle.html">Seattle</a>
      <a href="../locations/denver.html">Denver</a>
      <a href="../index.html#areas">+ more metros</a>
    </div>

    <div class="container footer-bottom">
      <p>&copy; 2026 AetherPoint Digital Infrastructure Advisors LLC. All rights reserved.</p>
      <div class="footer-legal"><a href="../index.html#services">Services</a><a href="#contact">Contact</a></div>
    </div>
  </footer>
'''


def render(hub):
    assert len(hub["title"]) <= 60 and len(hub["description"]) <= 158, hub["slug"]
    sections = []
    for sec in hub["sections"]:
        chips = "".join(f'<span class="chip">{e(i)}</span>' for i in sec["items"])
        sections.append(f'''    <section class="hub-section">
      <div class="container">
        <h2>{e(sec["h2"])}</h2>
        <p>{e(sec["p"])}</p>
        <div class="chip-list">{chips}</div>
      </div>
    </section>
''')
    ai_chips = "".join(f'<span class="chip chip--ai">{e(i)}</span>' for i in hub["ai"])
    sections.append(f'''    <section class="hub-section">
      <div class="container">
        <h2>AI-powered options</h2>
        <p>Providers in this category now offer AI-driven capabilities. We'll tell you which ones are worth paying for.</p>
        <div class="chip-list">{ai_chips}</div>
      </div>
    </section>
''')
    knows = [s["h2"] for s in hub["sections"]]
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": hub["name"],
        "serviceType": hub["name"],
        "url": f"{SITE}/services/{hub['slug']}.html",
        "description": hub["description"],
        "areaServed": ["Central Texas", "United States"],
        "provider": {"@type": "ProfessionalService", "@id": f"{SITE}/#org", "name": "AetherPoint Digital Infrastructure Advisors", "telephone": PHONE_SCHEMA, "email": EMAIL, "url": f"{SITE}/"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": hub["name"], "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": k}} for k in knows]},
    }, ensure_ascii=False, separators=(",", ":"))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(hub["title"])}</title>
  <meta name="description" content="{e(hub["description"])}" />
  <link rel="canonical" href="{SITE}/services/{hub["slug"]}.html" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style" href="{FONTS}" />
  <link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="{FONTS}" /></noscript>
  <link rel="icon" type="image/png" href="../logo-transparent.png" />
  <link rel="stylesheet" href="../styles.css" />
  <script type="application/ld+json">{jsonld}</script>
</head>
<body>
  <canvas id="lattice" aria-hidden="true"></canvas>

{nav()}
  <main>
    <section class="hero" id="home">
      <div class="container hero-inner">
        <span class="svc-icon" style="--c1:#16294b;--c2:#2a86c4;margin:0 auto 18px">{icon(hub["icon"])}</span>
        <span class="eyebrow">{e(hub["name"])}</span>
        <h1>{e(hub["h1"])}</h1>
        <p class="hero-sub">{e(hub["intro"])}</p>
        <div class="hero-actions">
          <a href="#contact" class="btn btn-primary btn-lg">Get a Quote</a>
          <a href="tel:{PHONE_TEL}" class="btn btn-ghost btn-lg">Call {PHONE_HUMAN}</a>
        </div>
      </div>
    </section>

{"".join(sections)}
    <section class="hub-section">
      <div class="container">
        <h2>Why go through AetherPoint</h2>
        <div class="hub-why">
          <div><strong>Wholesale pricing</strong><span>Provider promotions and negotiated rates you won't get from a single sales rep.</span></div>
          <div><strong>One advisor, for good</strong><span>The same person on your account after go-live. No rep churn, no lost history.</span></div>
          <div><strong>Hundreds of providers</strong><span>We quote the options that fit, side by side, instead of one vendor's catalog.</span></div>
        </div>
        <p style="margin-top:22px"><a href="../index.html#solutions">See the full comparison &rarr;</a></p>
      </div>
    </section>

{form(hub["checkbox"])}  </main>

{footer()}  <script src="../script.js"></script>
</body>
</html>
'''


# Claims we cannot substantiate for a one-person advisory. Keep hub copy clean.
FORBIDDEN = [
    r"24/7",
    r"\d+-minute",
    r"\bSLA\b",
    r"SOC 2",
    r"HIPAA",
    r"flat (monthly|pricing)",
    r"\bengineers?\b",
    r"guarantee",
]


def scan_forbidden(pages):
    """Return a list of (slug, pattern, excerpt) for every forbidden phrase found."""
    hits = []
    for slug, content in pages:
        for pat in FORBIDDEN:
            for m in re.finditer(pat, content, re.I):
                hits.append((slug, pat, content[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")))
    return hits


def main():
    out_dir = os.path.join(ROOT, "services")
    os.makedirs(out_dir, exist_ok=True)
    pages = []
    for hub in HUBS:
        path = os.path.join(out_dir, f'{hub["slug"]}.html')
        content = render(hub)
        with open(path, "w") as f:
            f.write(content)
        pages.append((hub["slug"], content))
        print(f'wrote services/{hub["slug"]}.html')

    hits = scan_forbidden(pages)
    if hits:
        for slug, pat, excerpt in hits:
            print(f"FORBIDDEN {slug}: {pat} -> ...{excerpt}...", file=sys.stderr)
        print(f"{len(hits)} unsubstantiated claim(s) found", file=sys.stderr)
        return 1
    print(f"claim scan: clean across {len(pages)} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
