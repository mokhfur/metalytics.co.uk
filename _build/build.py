#!/usr/bin/env python3
"""Build the static Metalytics site. Run:  python3 _build/build.py"""
import os, html, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.metalytics.co.uk"
GUIDE_PDF = "/assets/docs/metalytics-tlf-lifecycle-guide.pdf"


def asset(path):
    """Append a short content hash so a changed file gets a brand-new URL.

    Without this, the year-long immutable cache in .htaccess pins visitors to
    whatever CSS they first downloaded.
    """
    full = os.path.join(ROOT, path.lstrip("/"))
    try:
        with open(full, "rb") as fh:
            return f"{path}?v={hashlib.sha1(fh.read()).hexdigest()[:8]}"
    except OSError:
        return path

GLYPHS = {
 "story": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M4 19.5V6a2 2 0 0 1 2-2h11a1 1 0 0 1 1 1v13"/><path d="M6 17h12v3H6a2 2 0 0 1 0-4"/><path d="M9 8h6"/></svg>',
 "vision": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12Z"/><circle cx="12" cy="12" r="2.6"/></svg>',
 "tech": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="8" height="8" rx="1.6"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/></svg>',
 "report": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20h18"/><rect x="5" y="11" width="3.4" height="6" rx="1"/><rect x="10.3" y="6" width="3.4" height="11" rx="1"/><rect x="15.6" y="9" width="3.4" height="8" rx="1"/></svg>',
 "quality": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.8 20 6v6c0 4.6-3.3 8-8 9.3C8 20 4.7 16.6 4.7 12V6Z"/><path d="m9 12 2.2 2.2L15.4 10"/></svg>',
 "collab": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.2"/><path d="M2.6 19.5a6.6 6.6 0 0 1 12.8 0"/><circle cx="17.5" cy="9.5" r="2.4"/><path d="M16 14.2a5.6 5.6 0 0 1 5.4 5.3"/></svg>',
}
LINKEDIN = '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-.95 1.83-1.95 3.76-1.95 4.02 0 4.76 2.5 4.76 5.76V21h-4v-5.6c0-1.34-.03-3.06-1.9-3.06-1.9 0-2.19 1.45-2.19 2.96V21H9z"/></svg>'
FACEBOOK = '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.77-3.89 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 10 0 0 0 22 12Z"/></svg>'

def header(active, title, desc, path):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:site_name" content="Metalytics">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/favicon.png">
<meta name="theme-color" content="#0c0718">
<link rel="preload" as="image" href="/assets/img/hero-circuit.jpg">
<link rel="stylesheet" href="{asset('/assets/css/site.css')}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/img/logo.png" alt="Metalytics" width="513" height="120"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu">
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav" id="primary-nav" aria-label="Main">
      {link('/about', 'About', 'about')}
      {link('/automation', 'Automation', 'automation')}
      {link('/pharma', 'Pharma', 'pharma')}
      <a class="btn btn--primary" href="#contact">Contact Us</a>
    </nav>
  </div>
</header>
<main id="main">
"""

FOOTER = f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <img src="/assets/img/logo.png" alt="Metalytics" width="513" height="120">
        <p style="margin:0;max-width:34ch">Metadata empowered efficiency.</p>
      </div>
      <div>
        <ul class="footer-links">
          <li><a href="/about">About</a></li>
          <li><a href="/automation">Automation</a></li>
          <li><a href="/pharma">Pharma</a></li>
          <li><a href="/privacy-policy">Privacy Policy</a></li>
          <li><a href="/cookie-policy">Cookie Policy</a></li>
        </ul>
        <div class="social">
          <a href="https://www.linkedin.com/company/metalytics" aria-label="Metalytics on LinkedIn" rel="noopener">{LINKEDIN}</a>
          <a href="https://www.facebook.com/metalytics.application" aria-label="Metalytics on Facebook" rel="noopener">{FACEBOOK}</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      Copyright &copy; 2020&ndash;<span data-year>2026</span> Shafi Consultancy Limited. All rights reserved.<br>
      Registered in England and Wales No. 4194731
    </div>
  </div>
</footer>
<script src="{asset('/assets/js/hero-bg.js')}" defer></script>
<script src="{asset('/assets/js/site.js')}" defer></script>
</body>
</html>
"""

def form(form_name, heading, blurb, button="Send"):
    return f"""<section class="section section--soft" id="contact">
  <div class="wrap center">
    <h2>{heading}</h2>
    <p class="lede" style="margin-bottom:2.3rem">{blurb}</p>
    <form class="form-card" action="/contact.php" method="post" data-ajax>
      <p class="form-msg" role="status" aria-live="polite"></p>
      <input type="hidden" name="form_name" value="{form_name}">
      <div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <div class="field-row">
        <div class="field"><label for="{form_name}-fn">First Name <span class="req">*</span></label><input id="{form_name}-fn" name="first_name" type="text" autocomplete="given-name" required></div>
        <div class="field"><label for="{form_name}-ln">Last Name <span class="req">*</span></label><input id="{form_name}-ln" name="last_name" type="text" autocomplete="family-name" required></div>
      </div>
      <div class="field"><label for="{form_name}-em">Email <span class="req">*</span></label><input id="{form_name}-em" name="email" type="email" autocomplete="email" required></div>
      <div class="field-row">
        <div class="field"><label for="{form_name}-co">Company</label><input id="{form_name}-co" name="company" type="text" autocomplete="organization"></div>
        <div class="field"><label for="{form_name}-po">Position</label><input id="{form_name}-po" name="position" type="text" autocomplete="organization-title"></div>
      </div>
      <div class="field"><label for="{form_name}-ms">Message</label><textarea id="{form_name}-ms" name="message" rows="5"></textarea></div>
      <div class="form-actions"><button class="btn btn--primary" type="submit">{button}</button></div>
      <p class="form-note">We use your details only to respond to this enquiry. See our <a href="/privacy-policy">Privacy Policy</a>.</p>
    </form>
  </div>
</section>
"""

def closer(line1, line2):
    return f"""<section class="section closer">
  <div class="wrap">
    <h2>{line1}</h2>
    <p>{line2}</p>
  </div>
</section>
"""

def pillar(glyph, title, body):
    return f'<div class="pillar"><div class="glyph">{GLYPHS[glyph]}</div><h3>{title}</h3><p>{body}</p></div>'

pages = {}

# ----------------------------------------------------------------- home
pages["index.html"] = header(
    "home", "Metalytics | Analytics",
    "Metalytics uses analytics on your metadata to drive automation, increase operational efficiency and reduce costs.",
    "/") + f"""
<section class="hero">
  <div class="wrap">
    <h1>Metadata empowered growth</h1>
    <p>You know how valuable your data is, now let our analytics on your metadata drive automation, increase operational efficiency, and reduce costs.</p>
    <a class="btn btn--primary" href="#contact">Request a meeting</a>
  </div>
</section>

<section class="section" id="about">
  <div class="wrap">
    <div class="grid grid--3">
      {pillar("story", "Our Story", "We are committed to empowering businesses with the potential of their metadata. Our journey began with a vision to revolutionize the way data is managed and utilized.")}
      {pillar("vision", "Our Vision", "We envision a future where metadata becomes the driving force behind seamless automation with AI, enabling businesses to thrive in a data-driven environment.")}
      {pillar("tech", "Technology", "Metalytics leverages cutting-edge technology to harness the power of metadata and Artificial Intelligence, enabling organizations to be more efficient and reduce costs.")}
    </div>
  </div>
</section>

<section class="section guide">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">Free guide</span>
        <h2>5 Benefits and Strategies to drive efficiency and productivity in the TLF lifecycle, without increasing the team size!</h2>
        <p>Download our FREE GUIDE</p>
        <a class="btn btn--ghost" href="{GUIDE_PDF}" download>Download the guide (PDF, 3 pages)</a>
      </div>
      <div class="split__media"><img src="/assets/img/tlf-guide.png" alt="Preview of the TLF Process Guide" width="900" height="600" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section section--dark" id="how-it-works">
  <div class="wrap">
    <div class="center" style="margin-bottom:clamp(2.5rem,5vw,4rem)"><h2>How it works</h2></div>
    <div class="split">
      <div class="split__media"><picture>
        <source media="(max-width:520px)" srcset="{asset('/assets/img/art-metadata-review-stacked.svg')}" width="420" height="680">
        <img src="{asset('/assets/img/art-metadata-review.svg')}" alt="The review in four steps: business objectives, the metadata you hold, processes and workflows, then a plan to improve. It powers efficiency, quality, informed decisions and operational excellence." width="720" height="480" loading="lazy">
      </picture></div>
      <div>
        <h3>Do you know your metadata?</h3>
        <p>Our expert team of data analysts will identify your business objectives, what useful metadata your organisation holds, review your processes and workflows, then strategise a plan on how improvements can be made by allowing your metadata to empower efficiency, quality, informed decision-making and operational excellence.</p>
      </div>
    </div>
    <div class="split split--flip">
      <div class="split__media"><img src="/assets/img/art-dashboard.png" alt="" width="800" height="600" loading="lazy"></div>
      <div>
        <h3>Bespoke Solutions</h3>
        <p>With our highly experienced team of programmers, web developers and data analysts we are able to develop bespoke tools and applications according to your business objectives. Our solutions make the very best use of your metadata ensuring optimisation in workflow processes including the automation of routine tasks.</p>
      </div>
    </div>
  </div>
</section>

""" + form("meeting", "Request a meeting",
           "Get in touch with one of our consultants to see how we can let your metadata empower you.",
           button="Submit") \
  + closer("Elevate your productivity with Metalytics&rsquo; advanced workflow solutions.",
           "Streamline your processes and achieve superior efficiency and quality.") + FOOTER

# ----------------------------------------------------------- automation
pages["automation.html"] = header(
    "automation", "Automation | Metalytics",
    "Metadata driven automation, from real-time dashboards to fully automated reports, across any industry and any programming language.",
    "/automation") + f"""
<section class="hero hero--inner">
  <div class="wrap">
    <h1>Metadata Driven Automation</h1>
    <p>Whether you need a dashboard to instantly visualise real-time status of tasks or require full on automated reports from your data on a large scale, our innovative metadata driven solutions has got you covered.</p>
    <a class="btn btn--primary" href="#contact">Request a Review</a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="split__media"><img src="/assets/img/automation-robot.jpg" alt="Robotic arm working alongside a keyboard" width="760" height="922" loading="lazy"></div>
      <div>
        <span class="eyebrow">Any sector</span>
        <h2>Whatever your industry</h2>
        <p>If you have data, whether you are just storing it, using it, analysing it or reporting it, then the Metalytics philosophy can be applied to drive efficiency, automation and reduce cost. From Pharma to Finance, Insurance and Manufacturing, contact us for an independent review.</p>
      </div>
    </div>
    <div class="split split--flip">
      <div class="split__media"><img src="/assets/img/automation-tablet.jpg" alt="Automation workflow shown on a tablet" width="760" height="922" loading="lazy"></div>
      <div>
        <span class="eyebrow">Any language</span>
        <h2>Whatever your language</h2>
        <p>Whether you are programming in SAS, R or Python your existing tools can be seamlessly integrated and streamlined with Metalytics.</p>
      </div>
    </div>
  </div>
</section>

""" + form("review", "Request a Review",
           "Schedule a review with one of our Data Reviewers.") \
  + closer("Elevate your productivity with Metalytics&rsquo; advanced workflow solutions.",
           "Streamline your processes and achieve superior efficiency and consistency.") + FOOTER

# --------------------------------------------------------------- pharma
BENEFITS = [
 "Never need to re-write a program again as everything within the system is searchable",
 "Quality and consistency of programs that are easy to read for reviewers",
 "Automation can reduce programming time and resources by up to 60%",
 "Instantly visualise the current progress and status of programs and outputs",
 "Never need to worry about differences in programs or results as everything is fully traceable and comparable",
]
FEATURES = [
 ("Quality &amp; Consistency", "What steps are you taking to raise the quality and consistency across your processes?"),
 ("Traceability",             "Are the results and outputs in your study report traceable back to your data as required by FDA?"),
 ("Oversight",                "Do you have adequate oversight of programming, validation and QC across your clinical studies?"),
 ("Audit",                    "Can you demonstrate that all actions from the data to the study reports are audited?"),
 ("Harmonization",            "Do you have harmonization across your data sources and output generation?"),
 ("Minimising Risk",          "Can you show regulatory how you are minimising risk in the entire programming and QC process?"),
]

SLIDES = "".join(
    f'''<li class="carousel__slide" role="group" aria-roledescription="slide" aria-label="{i} of {len(FEATURES)}: {title}">
        <img src="/assets/img/pharma-feature-{i}.png" alt="{alt}" width="828" height="520" loading="lazy" decoding="async">
      </li>'''
    for i, (title, alt) in enumerate(FEATURES, 1))

DOTS = "".join(
    f'''<button class="carousel__dot" type="button" role="tab" aria-label="{title}" aria-selected="{"true" if i == 1 else "false"}"></button>'''
    for i, (title, alt) in enumerate(FEATURES, 1))

DEMOS = [
 ("pharma-summary-table", "Produce a Summary Table with just a few clicks",
  "Choose a template, pick the analysis, preview the table and save it. No program is written by hand."),
 ("pharma-figures", "Effortlessly generate Figures",
  "Set the covariate and the axes, update the chart, and the figure is ready to save alongside the tables."),
]

DEMO_BLOCKS = "".join(
    f'''<div class="demo">
        <div class="demo__head">
          <h3 id="demo-{slug}">{title}</h3>
          <p>{note}</p>
        </div>
        <div class="demo__frame">
          <video data-demo controls muted loop playsinline preload="metadata"
                 width="1920" height="1080" aria-labelledby="demo-{slug}"
                 poster="/assets/img/{slug}-poster.jpg">
            <source src="/assets/video/{slug}.mp4" type="video/mp4">
            <p>Your browser cannot play this video. <a href="/assets/video/{slug}.mp4">Download the recording</a> instead.</p>
          </video>
        </div>
        <p class="demo__note">The recording has no sound. Use the full screen control for a closer look.</p>
      </div>'''
    for slug, title, note in DEMOS)

ARROW = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>'

FEATURE_CARDS = f'''<div class="carousel" data-carousel aria-roledescription="carousel" aria-label="Metalytics clinical reporting features">
      <div class="carousel__stage">
        <button class="carousel__arrow carousel__arrow--prev" type="button" aria-label="Previous feature">{ARROW}</button>
        <div class="carousel__viewport">
          <ul class="carousel__track">{SLIDES}</ul>
        </div>
        <button class="carousel__arrow carousel__arrow--next" type="button" aria-label="Next feature">{ARROW}</button>
      </div>
      <p class="carousel__caption" aria-live="polite"><span class="carousel__count">1 / {len(FEATURES)}</span><span class="carousel__title">{FEATURES[0][0]}</span></p>
      <div class="carousel__dots" role="tablist" aria-label="Choose a feature">{DOTS}</div>
    </div>'''

pages["pharma.html"] = header(
    "pharma", "Pharma | Metalytics",
    "Metalytics for Pharma helps sponsors and CROs manage clinical trials from one application, with the oversight to make informed decisions quickly.",
    "/pharma") + f"""
<section class="hero hero--inner">
  <div class="wrap">
    <h1>Increase Statistical Programming Efficiency with Metalytics</h1>
    <p>Metalytics for Pharma helps pharmaceutical sponsors and CROs manage all their clinical trials from one intuitive application, giving them the oversight to make informed decisions, very quickly.</p>
    <a class="btn btn--primary" href="#contact">Get a Demo</a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid--3">
      {pillar("report", "Intuitive Reporting", "Produce summary tables and figures from one application, without rebuilding a program each time.")}
      {pillar("quality", "Efficiency &amp; Quality", "Consistent, readable programs that reviewers can follow, with automation cutting the manual work.")}
      {pillar("collab", "Collaboration &amp; Traceability", "Everything is searchable, comparable and fully traceable back to the data.")}
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">PharmaBot</span>
        <h2>PharmaBot Empowering Clinical Trial Reporting</h2>
        <p>PharmaBot is developed to streamline the statistical reporting process, with the power of AI and Automation.</p>
        <p>Metalytics is dedicated to empowering clinical trial reporting through intuitive solutions designed to enhance efficiency, traceability, quality and oversight.</p>
        <a class="btn btn--primary" href="#contact">Get a Demo</a>
      </div>
      <div class="split__media"><img src="/assets/img/pharma-ai.jpg" alt="AI-driven clinical data processing" width="760" height="721" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.6rem">
      <h2>The questions reviewers and auditors ask</h2>
      <p class="lede">See how Metalytics answers them.</p>
    </div>
    {FEATURE_CARDS}
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.8rem">
      <span class="eyebrow">Product tour</span>
      <h2>Metalytics in action</h2>
      <p class="lede">Two short recordings taken straight from the application.</p>
    </div>
    <div class="demos">
      {DEMO_BLOCKS}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Some of the benefits of using Metalytics</h2>
        <ul class="benefits">{"".join(f"<li>{b}</li>" for b in BENEFITS)}</ul>
      </div>
      <div class="split__media"><img src="/assets/img/pharma-gears.jpg" alt="Workflow efficiency illustrated as interlocking gears" width="761" height="664" loading="lazy"></div>
    </div>
  </div>
</section>

""" + form("demo", "Request a Demo",
           "Schedule a demo with one of our product consultants.") \
  + closer("Elevate your statistical programming productivity with Metalytics&rsquo; advanced workflow solutions.",
           "Streamline your processes and achieve superior traceability and quality in clinical trial reporting.") + FOOTER

# ------------------------------------------------------------- policies
def policy(slug, title, heading, blocks, updated=None):
    body = "".join(
        f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps) if h else "".join(f"<p>{p}</p>" for p in ps)
        for h, ps in blocks)
    note = f'<p class="updated">This policy was last updated on {updated}.</p>' if updated else ""
    return header(slug, title, f"{heading} for the Metalytics website, operated by Shafi Consultancy Limited.",
                  f"/{slug}") + f"""
<section class="hero hero--inner">
  <div class="wrap"><h1>{heading}</h1></div>
</section>
<section class="section">
  <div class="wrap"><div class="prose">{body}{note}</div></div>
</section>
""" + FOOTER

pages["privacy-policy.html"] = policy(
 "privacy-policy", "Privacy Policy | Metalytics", "Privacy policy",
 [(None, ["Shafi Consultancy are strongly committed to protecting your privacy. You can navigate the majority of our site without giving us any personal information about yourself. However, sometimes we need additional information about you in order to provide the information or services that you are requesting."]),
  ("The information we collect on this site", [
    "We collect Personally Identifiable Information in the following way:",
    "We have a contact us page on our website that enables you to submit questions to us. The personal information you provide on these forms may include your name, title, company name, address, contact numbers, and email."]),
  ("Right to Access", [
    'You have a right to see what personally identifiable information Shafi Consultancy holds on you at any time by contacting us in writing at <a href="mailto:dpo@shaficonsultancy.com">dpo@shaficonsultancy.com</a>. A copy of the information will be provided free of charge within one month of receipt once the identity of the person making the request has been verified. You may also request that your data be updated, corrected or deleted from our systems, unless we have a compelling reason such as a legal obligation to retain it.']),
  ("The way we use information", [
    "We store the information you provide about yourself in a secure environment in order to provide you with the information, products, and/or services you request. The information is stored for the lifetime of the system unless you request that it be removed. You must opt-in or give consent for us to share your identifiable information with third parties, who would be bound by a confidentiality agreement. However, the information that you provide about yourself may be shared with Shafi Consultancy employees to the extent necessary to accommodate your request. For example, if you provide your name, mailing address, telephone and email address and request more information about Shafi Consultancy&rsquo;s services, this information will be shared with appropriate Shafi Consultancy personnel to meet your request. We use non-identifying and aggregate information about the use of our Web site to improve the navigation, content, and design of our site. We do not use your personally identifiable information that you provide us online for purposes other than those you requested."]),
  ("Cookies and other anonymous web tracking techniques", [
    "When you use our website, we may assign cookie files to you, which are a small amount of data we send to your web browser. Cookies enable the computers operating our websites to differentiate between visitors and to track the patterns of activities engaged in by different visitors. By tracking such activities, the computers operating our websites can recognise a visitor and customise certain features for that visitor. We may also use aggregated, non-identifiable data regarding persons who visit our site in order to learn more about the use of the site and how we can improve it."]),
  ("Links", [
    "Our website may contain links to other websites. You should carefully review the privacy policies and practices of other websites, as we cannot control or be responsible for privacy policies or practices of third-party websites that are not Shafi Consultancy's property."]),
  ("Changes", [
    "We may occasionally update this Privacy Statement. We encourage you to periodically review this Privacy Statement to stay informed about how we are helping to protect the personally identifiable information that we collect."])],
 updated="20 May 2018")

pages["cookie-policy.html"] = policy(
 "cookie-policy", "Cookie Policy | Metalytics", "Cookie policy",
 [(None, ["This page explains the cookie policy of this website and provides information on the cookies used at this website."]),
  ("What is a cookie?", [
    "A cookie is a small snippet of text that a website asks your browser to store. All cookies have expiration dates in them that determine how long they stay in your browser. Cookies can be removed in two ways: automatically, when they expire, or when you manually delete them. We&rsquo;ve included more details below to help you understand what kinds of cookies we use."]),
  ("Does this website use cookies?", ["Yes, with the primary purpose to make the website work more effectively."]),
  ("What kinds of cookies do you use and why?", [
    "We use different kinds of cookies for various reasons:",
    "Session cookies &ndash; these are temporary cookies that expire (and are automatically erased) whenever you close your browser. We use session cookies to grant access to content.",
    "Persistent cookies &ndash; these usually have an expiration date far into the future and thus stay in your browser until they expire, or until you manually delete them. We use persistent cookies to better understand usage patterns so we can improve the site for our customers. This information is anonymised &ndash; when we look at the data, in other words, we look at patterns, but we do not see individuals&rsquo; personally identified information (PII)."]),
  ("What other cookies might I encounter at this website?", [
    "There are also limited third-party cookies on the site. These cookies could be session or persistent and are set by third parties like Google and Facebook. To ensure the best user experience, we restrict the use of third-party cookies to trusted partners. For example, we currently allow: Audience measurement and validation &ndash; We use services such as Google Analytics to understand how many people come and what is popular which helps us improve the website. No personally identifiable information (PII) is stored and site usage is always looked at on an aggregate (and anonymous) level."]),
  ("What kinds of cookies do you not use?", [
    "We do not use re-targeting cookies and do not use flash cookies (sometimes known as local shared objects or LSOs). We do not allow third-party advertising networks to drop cookies on our site to behaviourally target advertising to our users, either."]),
  ("Do you use any so-called &ldquo;intrusive&rdquo; cookies?", [
    "No. We don&rsquo;t use re-targeting cookies or flash cookies or any other kind of cookie that can capture personally identifiable information (PII)."]),
  ("Do you use cookies to sell customer information?", ["No."]),
  ("Will the site work if I disable cookies?", ["You can browse this site with cookies disabled, though some interactions may not work."])])


# ------------------------------------------------- thank you + not found
def simple(slug, title, heading, body_html, noindex=False):
    h = header(slug, title, heading, f"/{slug}")
    if noindex:
        h = h.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
    return h + f"""
<section class="hero hero--inner">
  <div class="wrap"><h1>{heading}</h1>{body_html}</div>
</section>
""" + FOOTER

pages["thank-you.html"] = simple(
 "thank-you", "Thank you | Metalytics", "Thanks for submitting!",
 '<p>We have your enquiry and one of our consultants will be in touch shortly.</p>'
 '<a class="btn btn--primary" href="/">Back to the homepage</a>', noindex=True)

pages["404.html"] = simple(
 "404", "Page not found | Metalytics", "We could not find that page",
 '<p>The page you were looking for may have moved. Try the homepage, or get in touch and we will point you in the right direction.</p>'
 '<a class="btn btn--primary" href="/">Back to the homepage</a>', noindex=True)


# ---------------------------------------------------------------- about
SC = "https://www.shaficonsultancy.com"

CAPABILITIES = [
 ("Statistical Programming", f"{SC}/statistical-programming/",
  "SDTM and ADaM datasets, tables, listings and figures for interim and final analyses."),
 ("CDISC Implementation", f"{SC}/cdisc/",
  "Standards-compliant mapping, specifications and Define-XML for regulatory submission."),
 ("PK/PD and NONMEM", f"{SC}/nonmem/",
  "Analysis-ready PK/PD datasets and NONMEM input files, supporting modelling teams."),
 ("Validation and QC", f"{SC}/validation-and-qc/",
  "Independent double programming and review against specifications and shells."),
 ("Programming Resourcing", f"{SC}/statistical-programming-resourcing-support/",
  "Programmers who integrate into client teams onsite, remotely or in a hybrid model."),
 ("Training &amp; Knowledge Transfer", f"{SC}/training-and-knowledge-transfer/",
  "Practical SAS training for pharma companies, CROs and clinical research professionals."),
]

CAP_CARDS = "".join(
    f'''<div class="cap">
        <h3><a href="{url}" rel="noopener">{name}</a></h3>
        <p>{desc}</p>
      </div>'''
    for name, url, desc in CAPABILITIES)

PAIN = [
 "Programs rewritten from scratch because nobody could find the last one",
 "Outputs that cannot be traced back to the data when a regulator asks",
 "No single view of where a study&rsquo;s programs and outputs have actually got to",
 "Review cycles that repeat because programs are hard for a reviewer to read",
 "Standards applied inconsistently from one study to the next",
]

SCHEMA = """<script type=\"application/ld+json\">
{
  \"@context\": \"https://schema.org\",
  \"@type\": \"AboutPage\",
  \"url\": \"https://www.metalytics.co.uk/about\",
  \"mainEntity\": {
    \"@type\": \"Organization\",
    \"name\": \"Shafi Consultancy Limited\",
    \"url\": \"https://www.shaficonsultancy.com\",
    \"description\": \"A specialist contract research organisation providing statistical programming, CDISC implementation and PK/PD support to pharmaceutical and biotechnology companies.\",
    \"makesOffer\": {
      \"@type\": \"Offer\",
      \"itemOffered\": {
        \"@type\": \"SoftwareApplication\",
        \"name\": \"Metalytics\",
        \"applicationCategory\": \"BusinessApplication\",
        \"url\": \"https://www.metalytics.co.uk/\"
      }
    }
  }
}
</script>"""

pages["about.html"] = header(
    "about", "About Metalytics | Built by Statistical Programmers at Shafi Consultancy",
    "Metalytics is built by Shafi Consultancy, a specialist statistical programming CRO with 25 years of CDISC, SDTM, ADaM and TLF delivery for pharma and biotech.",
    "/about") + f"""
<section class="hero hero--inner">
  <div class="wrap">
    <h1>Built by statistical programmers, for statistical programmers</h1>
    <p>Metalytics did not begin as a software product. It began as a list of problems that statistical programmers kept running into on real clinical studies, and then set about solving.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid--3">
      {pillar("story", "Our Story", "We are committed to empowering businesses with the potential of their metadata. Our journey began with a vision to revolutionize the way data is managed and utilized.")}
      {pillar("vision", "Our Vision", "We envision a future where metadata becomes the driving force behind seamless automation with AI, enabling businesses to thrive in a data-driven environment.")}
      {pillar("tech", "Technology", "Metalytics leverages cutting-edge technology to harness the power of metadata and Artificial Intelligence, enabling organizations to be more efficient and reduce costs.")}
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">The company behind the platform</span>
        <h2>Shafi Consultancy Limited</h2>
        <p>Metalytics is developed by <a href="{SC}" rel="noopener">Shafi Consultancy Limited</a>, a specialist contract research organisation that does one thing and does it deeply: statistical programming for pharmaceutical and biotechnology companies.</p>
        <p>Across 25 years the team has delivered CDISC-compliant SDTM and ADaM datasets, tables, listings and figures for Phase I to Phase IV studies, working both directly for sponsors and as a programming partner to other CROs.</p>
        <p>That delivery experience is the raw material for this platform. Every feature answers a question a programmer, a reviewer or an auditor actually asked on a live study.</p>
        <a class="btn btn--primary" href="{SC}/About_Shafi_Consultancy/" rel="noopener">More about Shafi Consultancy</a>
      </div>
      <div class="split__media"><img src="/assets/img/art-dashboard.png" alt="Metalytics study reporting dashboard" width="800" height="600" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.8rem">
      <h2>The statistical programming expertise behind it</h2>
      <p class="lede">Metalytics draws on the same capabilities Shafi Consultancy delivers as a service. Each one links through to the detail.</p>
    </div>
    <div class="caps">{CAP_CARDS}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split split--flip">
      <div class="split__media"><img src="/assets/img/pharma-gears.jpg" alt="Clinical reporting workflow" width="761" height="664" loading="lazy"></div>
      <div>
        <h2>Why it matters that programmers built it</h2>
        <p>Most clinical reporting tools are designed by software teams and handed to statistical programmers. Metalytics was built the other way round: the people who specified it had already written the macros, chased the traceability and sat through the review cycles.</p>
        <p>So it starts from the things that genuinely cost a programming team time:</p>
        <ul class="benefits">{"".join(f"<li>{x}</li>" for x in PAIN)}</ul>
        <p style="margin-top:1.4rem">If you have spent a submission season solving those by hand, you already know what you want out of a tool like this. See how that works in practice on the <a href="/pharma">Pharma page</a>, or across other sectors on <a href="/automation">Automation</a>.</p>
      </div>
    </div>
  </div>
</section>

{SCHEMA}
""" + closer("Elevate your productivity with Metalytics&rsquo; advanced workflow solutions.",
             "Streamline your processes and achieve superior efficiency and quality.") + FOOTER

for name, content in pages.items():
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"{name:<24} {len(content):>7,} bytes")
