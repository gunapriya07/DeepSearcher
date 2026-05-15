import os
import streamlit as st
import requests

BACKEND = os.environ.get("DEEPSEARCHER_BACKEND", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="DeepSearcher — AI Document Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Mono:wght@300;400;500&family=Bricolage+Grotesque:wght@400;500;600;700;800&display=swap');

:root {
    --bg-deep:    #020408;
    --bg-surface: #080E1A;
    --bg-card:    #0D1525;
    --bg-hover:   #111E35;
    --border:     rgba(99,179,255,0.10);
    --border-hi:  rgba(99,179,255,0.25);
    --accent:     #3B82F6;
    --accent-lo:  rgba(59,130,246,0.12);
    --accent-md:  rgba(59,130,246,0.25);
    --cyan:       #06B6D4;
    --cyan-lo:    rgba(6,182,212,0.10);
    --green:      #10B981;
    --amber:      #F59E0B;
    --red:        #EF4444;
    --txt-hi:     #F0F6FF;
    --txt-mid:    rgba(200,220,255,0.65);
    --txt-lo:     rgba(160,190,230,0.38);
    --radius-sm:  8px;
    --radius-md:  12px;
    --radius-lg:  20px;
    --radius-xl:  28px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg-deep) !important;
    color: var(--txt-hi);
    font-family: 'Space Grotesk', sans-serif;
}

[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stHeader"]           { display: none !important; }
[data-testid="stSidebar"]          { display: none !important; }
[data-testid="collapsedControl"]   { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }

/* ─── Streamlit widget overrides ─────────────────── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 22px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.18s !important;
    box-shadow: 0 0 0 0 rgba(59,130,246,0) !important;
}
.stButton > button:hover {
    background: #2563EB !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(59,130,246,0.35) !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--txt-hi) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 10px 14px !important;
    transition: border 0.18s, box-shadow 0.18s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.18) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: var(--txt-lo) !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--txt-hi) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stFileUploader > div {
    background: var(--bg-card) !important;
    border: 1.5px dashed var(--border-hi) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem !important;
}
.stFileUploader label { color: var(--txt-mid) !important; }
.stFileUploader [data-testid="stFileUploaderDropzoneInput"] { color: var(--txt-mid) !important; }

.stSuccess {
    background: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    border-radius: var(--radius-md) !important;
    color: #6EE7B7 !important;
}
.stError {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    border-radius: var(--radius-md) !important;
    color: #FCA5A5 !important;
}
.stWarning {
    background: rgba(245,158,11,0.08) !important;
    border: 1px solid rgba(245,158,11,0.25) !important;
    border-radius: var(--radius-md) !important;
    color: #FDE68A !important;
}

div[data-testid="stTabs"] [role="tablist"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 5px !important;
    gap: 3px !important;
}
div[data-testid="stTabs"] [role="tab"] {
    border-radius: var(--radius-md) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.83rem !important;
    color: var(--txt-lo) !important;
    padding: 8px 16px !important;
    transition: all 0.15s !important;
    border: none !important;
}
div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.30) !important;
}
div[data-testid="stTabs"] [role="tabpanel"] {
    padding: 1.5rem 0 !important;
}
label[data-testid="stWidgetLabel"] p {
    color: var(--txt-mid) !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}
.stJson {
    background: var(--bg-card) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border) !important;
}
div[data-testid="stHorizontalBlock"] { gap: 1rem !important; }

/* ─── Scrollbar ───────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 999px; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "doc_id" not in st.session_state:
    st.session_state["doc_id"] = None


# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE  — split into small html chunks to avoid Streamlit's renderer
#                 silently dropping large unsafe_allow_html blocks.
# ══════════════════════════════════════════════════════════════════════════════
def landing_page():

    # ── background canvas (fixed orbs + grid) ──
    st.markdown("""
<style>
/* ─── Landing specific ──────────────────────────────── */
.ds-grid-bg {
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image:
        linear-gradient(rgba(59,130,246,.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(59,130,246,.05) 1px, transparent 1px);
    background-size: 56px 56px;
}
.ds-orb {
    position: fixed; border-radius: 50%;
    filter: blur(130px); pointer-events: none; z-index: 0;
}
.ds-orb-1 { width:700px;height:700px; background:rgba(37,99,235,.18); top:-200px; left:-180px; }
.ds-orb-2 { width:500px;height:500px; background:rgba(6,182,212,.11); top:300px; right:-120px; }
.ds-orb-3 { width:420px;height:420px; background:rgba(109,40,217,.10); bottom:-60px; left:35%; }

.ds-wrap {
    position: relative; z-index: 1;
    max-width: 1080px; margin: 0 auto; padding: 0 2rem 6rem;
}

/* NAV */
.ds-nav {
    display:flex; align-items:center; justify-content:space-between;
    padding: 1.5rem 0;
    border-bottom: 1px solid var(--border);
}
.ds-logo {
    font-family:'Bricolage Grotesque',sans-serif;
    font-size:1.35rem; font-weight:800; letter-spacing:-.03em; color:#fff;
}
.ds-logo em { font-style:normal; color:var(--accent); }
.ds-pill {
    display:inline-flex; align-items:center; gap:7px;
    background: var(--accent-lo);
    border: 1px solid var(--accent-md);
    color: #93C5FD; font-size:.72rem; font-weight:600;
    padding:4px 13px; border-radius:999px; letter-spacing:.06em;
    text-transform: uppercase;
}
.ds-pill-dot {
    width:6px;height:6px;border-radius:50%;background:var(--accent);
    box-shadow:0 0 8px var(--accent);
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.75)} }

/* HERO */
.ds-hero { padding: 6.5rem 0 4.5rem; text-align:center; }
.ds-eyebrow {
    display:inline-flex; align-items:center; gap:8px;
    background:var(--cyan-lo); border:1px solid rgba(6,182,212,.25);
    color:#67E8F9; font-size:.78rem; font-weight:600;
    padding:5px 18px; border-radius:999px; letter-spacing:.05em;
    margin-bottom:1.8rem;
}
.ds-eyebrow-dot {
    width:5px;height:5px;border-radius:50%;background:var(--cyan);
    box-shadow:0 0 7px var(--cyan);
    animation:blink 2s .5s ease-in-out infinite;
}
.ds-h1 {
    font-family:'Bricolage Grotesque',sans-serif;
    font-size:clamp(2.8rem,6vw,5.2rem);
    font-weight:800; line-height:1.04; letter-spacing:-.03em;
    color:#fff; margin-bottom:1.4rem;
}
.ds-h1 .grad {
    background: linear-gradient(130deg,#3B82F6 0%,#06B6D4 55%,#818CF8 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.ds-sub {
    font-size:1.1rem; color:var(--txt-mid);
    max-width:540px; margin:0 auto 2.8rem;
    line-height:1.8; font-weight:300;
}

/* STATS */
.ds-stats {
    display:grid; grid-template-columns:repeat(3,1fr);
    gap:1px; background:var(--border);
    border:1px solid var(--border);
    border-radius:var(--radius-xl); overflow:hidden;
    margin:4.5rem 0;
}
.ds-stat {
    background:var(--bg-surface);
    padding:2rem 1.5rem; text-align:center;
    transition:background .2s;
}
.ds-stat:hover { background:var(--bg-hover); }
.ds-stat-n {
    font-family:'Bricolage Grotesque',sans-serif;
    font-size:2.4rem; font-weight:800;
    letter-spacing:-.03em; color:var(--accent);
}
.ds-stat-l { font-size:.8rem; color:var(--txt-lo); margin-top:3px; letter-spacing:.04em; }

/* SECTION HEADER */
.ds-sec-label { font-size:.72rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); margin-bottom:.8rem; }
.ds-sec-title {
    font-family:'Bricolage Grotesque',sans-serif;
    font-size:clamp(1.7rem,3vw,2.4rem); font-weight:700;
    color:#fff; letter-spacing:-.025em; line-height:1.15; margin-bottom:.9rem;
}
.ds-sec-sub { font-size:.95rem; color:var(--txt-mid); line-height:1.75; max-width:500px; }

/* FEATURES GRID */
.ds-feats {
    display:grid; grid-template-columns:repeat(3,1fr);
    gap:1px; background:var(--border);
    border:1px solid var(--border);
    border-radius:var(--radius-xl); overflow:hidden;
    margin-top:2.5rem;
}
.ds-feat {
    background:var(--bg-surface);
    padding:1.9rem 1.7rem;
    transition:background .2s;
}
.ds-feat:hover { background:var(--bg-hover); }
.ds-feat-icon {
    width:42px;height:42px;
    background:var(--accent-lo); border:1px solid var(--accent-md);
    border-radius:var(--radius-sm);
    display:flex; align-items:center; justify-content:center;
    font-size:1.15rem; margin-bottom:1.1rem;
}
.ds-feat-name {
    font-family:'Bricolage Grotesque',sans-serif;
    font-weight:700; font-size:.97rem; color:#fff; margin-bottom:.45rem;
}
.ds-feat-desc { font-size:.84rem; color:var(--txt-lo); line-height:1.65; }

/* HOW IT WORKS */
.ds-steps {
    display:grid; grid-template-columns:repeat(3,1fr);
    gap:1.5rem; margin-top:2.5rem;
}
.ds-step {
    background:var(--bg-surface);
    border:1px solid var(--border);
    border-radius:var(--radius-lg); padding:1.9rem 1.6rem;
    position:relative; overflow:hidden;
    transition:border-color .2s, transform .2s;
}
.ds-step:hover { border-color:var(--border-hi); transform:translateY(-2px); }
.ds-step::before {
    content:'';
    position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,var(--accent),var(--cyan));
    opacity:0; transition:opacity .2s;
}
.ds-step:hover::before { opacity:1; }
.ds-step-n {
    font-family:'DM Mono',monospace;
    font-size:2.8rem; font-weight:500;
    color:rgba(59,130,246,.14); line-height:1; margin-bottom:.9rem;
}
.ds-step-title { font-family:'Bricolage Grotesque',sans-serif; font-weight:700; font-size:1rem; color:#fff; margin-bottom:.45rem; }
.ds-step-desc { font-size:.84rem; color:var(--txt-lo); line-height:1.65; }

/* CTA BANNER */
.ds-cta {
    background:linear-gradient(135deg,rgba(37,99,235,.10) 0%, rgba(6,182,212,.06) 100%);
    border:1px solid var(--accent-md);
    border-radius:var(--radius-xl);
    padding:4rem 2.5rem; text-align:center;
    margin:4.5rem 0 0; position:relative; overflow:hidden;
}
.ds-cta::before {
    content:''; position:absolute;
    top:-80px; left:50%; transform:translateX(-50%);
    width:500px; height:250px;
    background:rgba(59,130,246,.12);
    border-radius:50%; filter:blur(70px); pointer-events:none;
}
.ds-cta-h {
    font-family:'Bricolage Grotesque',sans-serif;
    font-size:2.1rem; font-weight:800;
    color:#fff; letter-spacing:-.025em;
    margin-bottom:.9rem; position:relative;
}
.ds-cta-p { color:var(--txt-mid); margin-bottom:2rem; position:relative; font-size:.97rem; }
</style>
<div class="ds-grid-bg"></div>
<div class="ds-orb ds-orb-1"></div>
<div class="ds-orb ds-orb-2"></div>
<div class="ds-orb ds-orb-3"></div>
<div class="ds-wrap">
  <!-- NAV -->
  <nav class="ds-nav">
    <div class="ds-logo">Deep<em>Searcher</em></div>
    <div class="ds-pill"><div class="ds-pill-dot"></div>AI Powered</div>
  </nav>

  <!-- HERO -->
  <div class="ds-hero">
    <div class="ds-eyebrow">
      <div class="ds-eyebrow-dot"></div>
      Intelligent Document Analysis
    </div>
    <h1 class="ds-h1">
      Your Documents.<br>
      <span class="grad">Deeply Understood.</span>
    </h1>
    <p class="ds-sub">
      Upload any PDF, Word doc, or text file and instantly unlock AI-powered Q&amp;A,
      smart summaries, quizzes, topic maps, and cross-document comparison.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

    # CTA button (real Streamlit widget)
    col1, col2, col3 = st.columns([2.5, 1.2, 2.5])
    with col2:
        if st.button("⚡  Start for free", use_container_width=True):
            st.session_state["page"] = "app"
            st.rerun()

    # ── stats + features + steps + CTA banner ──
    st.markdown("""
<div class="ds-wrap" style="padding-top:0;">
  <!-- STATS -->
  <div class="ds-stats">
    <div class="ds-stat">
      <div class="ds-stat-n">6</div>
      <div class="ds-stat-l">AI-powered tools</div>
    </div>
    <div class="ds-stat">
      <div class="ds-stat-n">3</div>
      <div class="ds-stat-l">File formats</div>
    </div>
    <div class="ds-stat">
      <div class="ds-stat-n">&lt;5s</div>
      <div class="ds-stat-l">Avg. response time</div>
    </div>
  </div>

  <!-- FEATURES -->
  <div class="ds-sec-label">Capabilities</div>
  <div class="ds-sec-title">Everything you need<br>from a document.</div>
  <p class="ds-sec-sub">Six purpose-built tools, all working from the same uploaded file — no re-uploading, no context loss.</p>
  <div class="ds-feats">
    <div class="ds-feat">
      <div class="ds-feat-icon">💬</div>
      <div class="ds-feat-name">Ask anything</div>
      <div class="ds-feat-desc">Natural-language Q&amp;A with precise, cited answers drawn directly from your document.</div>
    </div>
    <div class="ds-feat">
      <div class="ds-feat-icon">📋</div>
      <div class="ds-feat-name">Smart summaries</div>
      <div class="ds-feat-desc">Concise, detailed, or bullet-point summaries — tailored to how you consume information.</div>
    </div>
    <div class="ds-feat">
      <div class="ds-feat-icon">🧠</div>
      <div class="ds-feat-name">Quiz generator</div>
      <div class="ds-feat-desc">Auto-generate multiple-choice questions to test comprehension or train a team.</div>
    </div>
    <div class="ds-feat">
      <div class="ds-feat-icon">🏷️</div>
      <div class="ds-feat-name">Topic extraction</div>
      <div class="ds-feat-desc">Instantly surface key themes and concepts buried inside long or complex documents.</div>
    </div>
    <div class="ds-feat">
      <div class="ds-feat-icon">⚖️</div>
      <div class="ds-feat-name">Document compare</div>
      <div class="ds-feat-desc">Compare two documents side-by-side across any dimension — methodology, scope, conclusions.</div>
    </div>
    <div class="ds-feat">
      <div class="ds-feat-icon">🔍</div>
      <div class="ds-feat-name">Deep search</div>
      <div class="ds-feat-desc">Semantic search that finds related content and surfaces hidden connections in your data.</div>
    </div>
  </div>

  <!-- HOW IT WORKS -->
  <div style="padding:5.5rem 0 0;">
    <div class="ds-sec-label">How it works</div>
    <div class="ds-sec-title">Three steps.<br>Instant insight.</div>
    <div class="ds-steps">
      <div class="ds-step">
        <div class="ds-step-n">01</div>
        <div class="ds-step-title">Upload your file</div>
        <div class="ds-step-desc">Drag-and-drop or browse for any PDF, DOCX, or TXT. Parsing happens in seconds.</div>
      </div>
      <div class="ds-step">
        <div class="ds-step-n">02</div>
        <div class="ds-step-title">Choose a tool</div>
        <div class="ds-step-desc">Pick from Q&amp;A, Summary, Quiz, Topics, or Compare — each built for a specific workflow.</div>
      </div>
      <div class="ds-step">
        <div class="ds-step-n">03</div>
        <div class="ds-step-title">Get your answer</div>
        <div class="ds-step-desc">Receive structured AI-generated results in under 5 seconds — ready to use or share.</div>
      </div>
    </div>
  </div>

  <!-- CTA -->
  <div class="ds-cta">
    <div class="ds-cta-h">Ready to dig deeper?</div>
    <p class="ds-cta-p">No account needed. Upload a document and start exploring in seconds.</p>
  </div>
</div>
""", unsafe_allow_html=True)

    # second CTA button
    col1, col2, col3 = st.columns([2.5, 1.4, 2.5])
    with col2:
        if st.button("⚡  Open the app", key="cta2", use_container_width=True):
            st.session_state["page"] = "app"
            st.rerun()

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# APP PAGE
# ══════════════════════════════════════════════════════════════════════════════
def app_page():

    # ── app-level CSS & background ──
    st.markdown("""
<style>
/* ─── App page specific ─────────────────────────────── */
.ap-bg-grid {
    position:fixed; inset:0; pointer-events:none; z-index:0;
    background-image:
        linear-gradient(rgba(59,130,246,.03) 1px, transparent 1px),
        linear-gradient(90deg,rgba(59,130,246,.03) 1px, transparent 1px);
    background-size:56px 56px;
}
.ap-orb {
    position:fixed; border-radius:50%;
    filter:blur(110px); pointer-events:none; z-index:0;
}
.ap-orb-1 { width:550px;height:550px; background:rgba(37,99,235,.13); top:-150px; left:-130px; }
.ap-orb-2 { width:400px;height:400px; background:rgba(6,182,212,.08); bottom:0; right:-80px; }

.ap-wrap {
    position:relative; z-index:1;
    max-width:900px; margin:0 auto; padding:0 2rem 4rem;
}

/* Topbar */
.ap-topbar {
    display:flex; align-items:center; justify-content:space-between;
    padding:1.3rem 0;
    border-bottom:1px solid var(--border);
    margin-bottom:1.8rem;
}
.ap-logo {
    font-family:'Bricolage Grotesque',sans-serif;
    font-size:1.2rem; font-weight:800; letter-spacing:-.03em; color:#fff;
}
.ap-logo em { font-style:normal; color:var(--accent); }

/* Doc ID bar */
.ap-docbar {
    display:flex; align-items:center; gap:10px;
    background:var(--accent-lo);
    border:1px solid var(--accent-md);
    border-radius:var(--radius-md);
    padding:.65rem 1.1rem;
    margin-bottom:1.6rem;
    font-size:.84rem;
}
.ap-docbar-lbl { color:var(--txt-lo); }
.ap-docbar-val {
    font-family:'DM Mono',monospace;
    color:#93C5FD; font-weight:500; font-size:.83rem;
}
.ap-docbar-empty { color:var(--txt-mid); font-size:.84rem; }

/* Panel text */
.ap-panel-title {
    font-family:'Bricolage Grotesque',sans-serif;
    font-size:1.18rem; font-weight:700; color:#fff;
    letter-spacing:-.02em; margin-bottom:.25rem;
}
.ap-panel-sub { font-size:.84rem; color:var(--txt-lo); margin-bottom:1.4rem; }

/* Upload zone */
.ap-upload-zone {
    border:1.5px dashed var(--border-hi);
    border-radius:var(--radius-lg);
    padding:3rem 2rem; text-align:center;
    background:var(--accent-lo);
    margin-bottom:1rem;
}
.ap-upload-icon { font-size:2.2rem; margin-bottom:.6rem; }
.ap-upload-t {
    font-family:'Bricolage Grotesque',sans-serif;
    font-weight:700; font-size:1rem; color:#fff; margin-bottom:.3rem;
}
.ap-upload-s { font-size:.83rem; color:var(--txt-lo); margin-bottom:.8rem; }
.ap-file-pills { display:flex; gap:7px; justify-content:center; }
.ap-file-pill {
    background:var(--accent-lo); border:1px solid var(--accent-md);
    color:#93C5FD; font-size:.7rem; font-weight:700;
    padding:3px 11px; border-radius:999px; letter-spacing:.05em;
}

/* Result box */
.ap-result {
    background:var(--bg-card);
    border:1px solid var(--border);
    border-radius:var(--radius-md);
    padding:1.2rem 1.4rem;
    font-size:.89rem; color:var(--txt-mid);
    line-height:1.8; min-height:90px;
    white-space:pre-wrap;
    font-family:'Space Grotesk',sans-serif;
}

/* Topics */
.ap-topics { display:flex; flex-wrap:wrap; gap:9px; margin-top:1rem; }
.ap-topic {
    background:var(--cyan-lo); border:1px solid rgba(6,182,212,.22);
    color:#67E8F9; font-size:.83rem; font-weight:500;
    padding:5px 15px; border-radius:999px;
    transition:background .15s;
}
.ap-topic:hover { background:rgba(6,182,212,.18); }

/* Quiz */
.ap-quiz-q {
    background:var(--bg-card); border:1px solid var(--border);
    border-radius:var(--radius-md); padding:1.2rem 1.4rem; margin-bottom:10px;
    transition:border-color .15s;
}
.ap-quiz-q:hover { border-color:var(--border-hi); }
.ap-quiz-num { font-size:.72rem; font-weight:700; color:var(--accent); letter-spacing:.09em; text-transform:uppercase; margin-bottom:.45rem; font-family:'DM Mono',monospace; }
.ap-quiz-text { font-family:'Bricolage Grotesque',sans-serif; font-weight:600; font-size:.95rem; color:#fff; margin-bottom:.9rem; }
.ap-quiz-opts { display:flex; flex-direction:column; gap:5px; }
.ap-quiz-opt {
    padding:7px 13px; border-radius:var(--radius-sm);
    border:1px solid var(--border); font-size:.84rem;
    color:var(--txt-mid); background:transparent; cursor:pointer;
    text-align:left; transition:all .13s; font-family:'Space Grotesk',sans-serif;
}
.ap-quiz-opt:hover { background:var(--accent-lo); border-color:var(--accent-md); color:#93C5FD; }

/* Health grid */
.ap-health { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; }
.ap-health-item {
    background:var(--bg-card); border:1px solid var(--border);
    border-radius:var(--radius-md); padding:.95rem 1.2rem;
    display:flex; align-items:center; gap:11px;
    transition:border-color .15s;
}
.ap-health-item:hover { border-color:var(--border-hi); }
.ap-health-dot { width:9px;height:9px;border-radius:50%;flex-shrink:0; }
.ap-health-dot.ok   { background:var(--green); box-shadow:0 0 7px rgba(16,185,129,.5); }
.ap-health-dot.warn { background:var(--amber); box-shadow:0 0 7px rgba(245,158,11,.5); }
.ap-health-dot.err  { background:var(--red);   box-shadow:0 0 7px rgba(239,68,68,.5); }
.ap-health-key { font-size:.77rem; color:var(--txt-lo); font-weight:500; letter-spacing:.03em; font-family:'DM Mono',monospace; }
.ap-health-val { font-family:'Bricolage Grotesque',sans-serif; font-size:.93rem; color:#fff; font-weight:600; }

/* Divider */
.ap-divider { height:1px; background:var(--border); margin:1.2rem 0; }
</style>
<div class="ap-bg-grid"></div>
<div class="ap-orb ap-orb-1"></div>
<div class="ap-orb ap-orb-2"></div>
""", unsafe_allow_html=True)

    # ── Topbar ──
    col_logo, col_back = st.columns([5, 1])
    with col_logo:
        st.markdown('<div class="ap-wrap"><div class="ap-topbar"><div class="ap-logo">Deep<em>Searcher</em></div></div></div>', unsafe_allow_html=True)
    with col_back:
        st.markdown("<div style='padding-top:.9rem'></div>", unsafe_allow_html=True)
        if st.button("← Back", use_container_width=True):
            st.session_state["page"] = "landing"
            st.rerun()

    # ── main container opens ──
    st.markdown('<div class="ap-wrap" style="padding-top:0">', unsafe_allow_html=True)

    # ── Doc ID bar ──
    doc_id = st.session_state.get("doc_id")
    if doc_id:
        st.markdown(f"""
<div class="ap-docbar">
  <span>📄</span>
  <span class="ap-docbar-lbl">Active document:</span>
  <span class="ap-docbar-val">{doc_id}</span>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="ap-docbar">
  <span>📂</span>
  <span class="ap-docbar-empty">No document loaded — upload one below to get started</span>
</div>""", unsafe_allow_html=True)

    # ── Tabs ──
    tabs = st.tabs(["📤 Upload", "💬 Ask", "📋 Summary", "🧠 Quiz", "🏷️ Topics", "⚖️ Compare", "❤️ Health"])

    # ══ UPLOAD ══════════════════════════════════════════════
    with tabs[0]:
        st.markdown('<div class="ap-panel-title">Upload a document</div>', unsafe_allow_html=True)
        st.markdown('<div class="ap-panel-sub">PDF, TXT, and DOCX up to 50 MB. Parsing is instant.</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="ap-upload-zone">
  <div class="ap-upload-icon">☁️</div>
  <div class="ap-upload-t">Drag &amp; drop your file here</div>
  <div class="ap-upload-s">or use the file browser below</div>
  <div class="ap-file-pills">
    <span class="ap-file-pill">PDF</span>
    <span class="ap-file-pill">TXT</span>
    <span class="ap-file-pill">DOCX</span>
  </div>
</div>""", unsafe_allow_html=True)

        uploaded = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"], label_visibility="collapsed")
        if uploaded:
            st.markdown(f'<p style="font-size:.84rem;color:#93C5FD;margin:.4rem 0 .8rem">✓ Selected: <strong>{uploaded.name}</strong></p>', unsafe_allow_html=True)
            if st.button("Upload document →", use_container_width=False):
                with st.spinner("Uploading…"):
                    try:
                        resp = requests.post(f"{BACKEND}/upload", files={"file": (uploaded.name, uploaded.getvalue())})
                        resp.raise_for_status()
                        data = resp.json()
                        st.session_state["doc_id"] = data.get("document_id")
                        st.success(f"✅ Uploaded! Document ID: `{st.session_state['doc_id']}`")
                        st.json(data)
                    except Exception as e:
                        st.error(f"Upload failed: {e}")

    # ══ ASK ══════════════════════════════════════════════════
    with tabs[1]:
        st.markdown('<div class="ap-panel-title">Ask a question</div>', unsafe_allow_html=True)
        st.markdown('<div class="ap-panel-sub">Type anything you want to know about the document.</div>', unsafe_allow_html=True)
        doc_id_ask = st.text_input("Document ID", value=st.session_state.get("doc_id") or "", key="ask_doc")
        question   = st.text_input("Your question", placeholder="e.g. What is the main argument of this paper?")
        if st.button("Get answer →"):
            if not doc_id_ask or not question:
                st.warning("Please provide both a document ID and a question.")
            else:
                with st.spinner("Thinking…"):
                    try:
                        resp = requests.post(f"{BACKEND}/ask", json={"document_id": doc_id_ask, "question": question})
                        resp.raise_for_status()
                        data = resp.json()
                        ans = data.get("answer", "")
                        if ans:
                            st.markdown(f'<div class="ap-result">{ans}</div>', unsafe_allow_html=True)
                        else:
                            st.json(data)
                    except Exception as e:
                        st.error(str(e))

    # ══ SUMMARY ══════════════════════════════════════════════
    with tabs[2]:
        st.markdown('<div class="ap-panel-title">Summarize document</div>', unsafe_allow_html=True)
        st.markdown('<div class="ap-panel-sub">Choose how you want the summary delivered.</div>', unsafe_allow_html=True)
        doc_id_sum = st.text_input("Document ID", value=st.session_state.get("doc_id") or "", key="sum_doc")
        style      = st.selectbox("Summary style", ["concise", "detailed", "bullet"], key="sum_style")
        if st.button("Generate summary →"):
            if not doc_id_sum:
                st.warning("Please provide a document ID.")
            else:
                with st.spinner("Summarizing…"):
                    try:
                        resp = requests.post(f"{BACKEND}/summary", json={"document_id": doc_id_sum, "style": style})
                        resp.raise_for_status()
                        data = resp.json()
                        text = data.get("summary", "")
                        if text:
                            st.markdown(f'<div class="ap-result">{text}</div>', unsafe_allow_html=True)
                        else:
                            st.json(data)
                    except Exception as e:
                        st.error(str(e))

    # ══ QUIZ ══════════════════════════════════════════════════
    with tabs[3]:
        st.markdown('<div class="ap-panel-title">Quiz generator</div>', unsafe_allow_html=True)
        st.markdown('<div class="ap-panel-sub">Auto-generate multiple-choice questions to test comprehension.</div>', unsafe_allow_html=True)
        doc_id_quiz = st.text_input("Document ID", value=st.session_state.get("doc_id") or "", key="quiz_doc")
        num_q       = st.number_input("Number of questions", min_value=1, max_value=20, value=5)
        if st.button("Generate quiz →"):
            if not doc_id_quiz:
                st.warning("Please provide a document ID.")
            else:
                with st.spinner("Generating quiz…"):
                    try:
                        resp = requests.post(f"{BACKEND}/quiz", json={"document_id": doc_id_quiz, "num_questions": num_q, "approved": True})
                        resp.raise_for_status()
                        data = resp.json()
                        questions = data.get("questions", [])
                        if questions:
                            html_out = ""
                            for i, q in enumerate(questions):
                                opts = "".join([f'<button class="ap-quiz-opt">{o}</button>' for o in q.get("options", [])])
                                html_out += f"""
<div class="ap-quiz-q">
  <div class="ap-quiz-num">Question {i+1}</div>
  <div class="ap-quiz-text">{q.get("question","")}</div>
  <div class="ap-quiz-opts">{opts}</div>
</div>"""
                            st.markdown(html_out, unsafe_allow_html=True)
                        else:
                            st.json(data)
                    except Exception as e:
                        st.error(str(e))

    # ══ TOPICS ════════════════════════════════════════════════
    with tabs[4]:
        st.markdown('<div class="ap-panel-title">Topic extraction</div>', unsafe_allow_html=True)
        st.markdown('<div class="ap-panel-sub">Identify the key themes and concepts in the document.</div>', unsafe_allow_html=True)
        doc_id_topics = st.text_input("Document ID", value=st.session_state.get("doc_id") or "", key="topics_doc")
        if st.button("Extract topics →"):
            if not doc_id_topics:
                st.warning("Please provide a document ID.")
            else:
                with st.spinner("Extracting topics…"):
                    try:
                        resp = requests.get(f"{BACKEND}/topics/{doc_id_topics}")
                        resp.raise_for_status()
                        data = resp.json()
                        topics = data.get("topics", data if isinstance(data, list) else [])
                        if topics:
                            chips = "".join([f'<span class="ap-topic">{t}</span>' for t in topics])
                            st.markdown(f'<div class="ap-topics">{chips}</div>', unsafe_allow_html=True)
                        else:
                            st.json(data)
                    except Exception as e:
                        st.error(str(e))

    # ══ COMPARE ═══════════════════════════════════════════════
    with tabs[5]:
        st.markdown('<div class="ap-panel-title">Compare documents</div>', unsafe_allow_html=True)
        st.markdown('<div class="ap-panel-sub">Contrast two documents across any dimension you choose.</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            id1 = st.text_input("Document ID 1", placeholder="doc-id-aaa")
        with c2:
            id2 = st.text_input("Document ID 2", placeholder="doc-id-bbb")
        aspect = st.text_input("Comparison aspect", placeholder="e.g. methodology, scope, conclusions")
        if st.button("Compare →"):
            if not id1 or not id2:
                st.warning("Please provide both document IDs.")
            else:
                with st.spinner("Comparing…"):
                    try:
                        resp = requests.post(f"{BACKEND}/compare", json={"document_id_1": id1, "document_id_2": id2, "aspect": aspect})
                        resp.raise_for_status()
                        data = resp.json()
                        text = data.get("comparison", "")
                        if text:
                            st.markdown(f'<div class="ap-result">{text}</div>', unsafe_allow_html=True)
                        else:
                            st.json(data)
                    except Exception as e:
                        st.error(str(e))

    # ══ HEALTH ════════════════════════════════════════════════
    with tabs[6]:
        st.markdown('<div class="ap-panel-title">Backend health</div>', unsafe_allow_html=True)
        st.markdown('<div class="ap-panel-sub">Check the status of all DeepSearcher backend services.</div>', unsafe_allow_html=True)
        if st.button("Run health check →"):
            with st.spinner("Checking…"):
                try:
                    resp = requests.get(f"{BACKEND}/health")
                    resp.raise_for_status()
                    data = resp.json()
                    items_html = ""
                    for k, v in data.items():
                        ok = v in ("ok", True, "healthy", "running")
                        dot = "ok" if ok else "warn"
                        items_html += f"""
<div class="ap-health-item">
  <div class="ap-health-dot {dot}"></div>
  <div>
    <div class="ap-health-key">{k}</div>
    <div class="ap-health-val">{v}</div>
  </div>
</div>"""
                    st.markdown(f'<div class="ap-health">{items_html}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown("""
<div class="ap-health">
  <div class="ap-health-item">
    <div class="ap-health-dot err"></div>
    <div>
      <div class="ap-health-key">backend</div>
      <div class="ap-health-val">Unreachable</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                    st.error(str(e))

    # close main container
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Router ───────────────────────────────────────────────────────────────────
if st.session_state["page"] == "landing":
    landing_page()
else:
    app_page()