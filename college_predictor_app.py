# ────────────────────────────────────────────────────────────────────────────────
# YOCKET STUDY-ABROAD | University Readiness Assessment Test  (Streamlit)
# Entire script with one adaptive CSS block – text is legible in **light & dark**
# ────────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import io
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# ─────────────────────────────────────────────
# 0. Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Yocket Study-Abroad | University Readiness Assessment Test",
    page_icon="🎓",
    layout="wide",
)

# ─────────────────────────────────────────────
# 1. Brand colours
# ─────────────────────────────────────────────
ORANGE = "#FF6B00"
RED    = "#E53935"
BLUE   = "#1E88E5"
GREEN  = "#43A047"

# ─────────────────────────────────────────────
# 2. ONE adaptive CSS block (light + dark)
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
#MainMenu, footer {{visibility:hidden;}}

/* ─── Base (light) ─── */
body            {{background:#f5f6f7;color:#212121;font-family:'Segoe UI',sans-serif;}}
.hero-title     {{font-size:2.4rem;font-weight:800;color:{ORANGE};margin:0;}}
.hero-sub       {{font-size:1.4rem;font-weight:600;margin-top:.3rem;}}
.hero-divider   {{height:2px;background:{ORANGE};margin:1.6rem 0 2.4rem;}}
.card           {{background:#fff;border-radius:14px;max-width:900px;margin:0 auto;
                 padding:2.1rem 2.6rem;box-shadow:0 4px 16px rgba(0,0,0,.06);color:#212121;}}
.card h3        {{font-size:1.65rem;margin-bottom:.9rem;}}
.step           {{display:flex;margin:.65rem 0;}}
.step-num       {{min-width:30px;height:30px;border-radius:50%;background:{ORANGE}33;
                 color:#000;font-weight:700;font-size:.85rem;display:flex;align-items:center;
                 justify-content:center;margin-right:.6rem;}}
.step-text      {{line-height:1.45rem;}}
.uni-card       {{background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.04);
                 padding:1rem 1.2rem;margin-bottom:1.2rem;color:#212121;}}
.uni-card h4    {{margin:0 0 .3rem 0;font-size:1rem;font-weight:700;}}

/* ─── Dark-mode overrides ─── */
@media (prefers-color-scheme: dark) {{
  body          {{background:#121212 !important;color:#E7E7E7 !important;}}
  .card         {{background:#1E1E1E !important;color:#E7E7E7 !important;}}
  .hero-divider {{background:{ORANGE}AA !important;}}
  .step-num     {{background:#FFFFFF !important;color:#000 !important;}}
  .uni-card     {{background:#1E1E1E !important;color:#E7E7E7 !important;}}
  .uni-card h4  {{color:#FFFFFF !important;}}
  .uni-card div {{color:#CCCCCC !important;}}
}}

/* ─── Mobile tweaks ─── */
@media (max-width:480px) {{
  .card       {{padding:1.5rem 1.2rem;}}
  .hero-title {{font-size:2rem;}}
  .hero-sub   {{font-size:1.2rem;}}
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. Hero + quick guide
# ─────────────────────────────────────────────
st.markdown("""
<div style='text-align:center'>
  <div class='hero-title'>YOCKET STUDY-ABROAD 🎓</div>
  <div class='hero-sub'>University Readiness Assessment Test</div>
</div>
<div class='hero-divider'></div>
""", unsafe_allow_html=True)

guide_steps = [
    "Choose one or more <strong>countries</strong>.",
    "Enter <strong>academic scores</strong> (Class 9-12 + SAT/ACT).",
    "Add <strong>AP</strong> test data (optional).",
    "Add <strong>activities</strong>, internships & extras.",
    "Select number of <strong>LORs</strong>.",
    "Click <strong>Find My Universities</strong> for Ambitious-Target-Safe lists."
]
st.markdown(
    "<div class='card'><h3>How to use this Finder</h3>" +
    "".join(f"<div class='step'><div class='step-num'>{i}</div><div class='step-text'>{t}</div></div>"
            for i, t in enumerate(guide_steps, 1)) +
    "</div>",
    unsafe_allow_html=True
)
st.markdown("### &nbsp;")  # spacer

# 4. Instructions for All Boards
# ─────────────────────────────────────────────
st.markdown("### 📘 Instructions for Entering Board Percentages")

with st.expander("📋 How to calculate your percentage (Board-wise)?"):
    st.markdown("""
    <style>
        /* General Styles for both modes */
        .instruction-box {
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            margin-bottom: 12px;
            font-size: 16px;
            background-color: #ffffff; /* White background to ensure readability */
            color: #000000; /* Set text color to black for high contrast */
        }
        .formula {
            background-color: #f4f4f4;
            border: 1px solid #ccc;
            padding: 8px 12px;
            border-radius: 5px;
            font-family: monospace;
            display: inline-block;
            margin: 6px 0 6px 0;
            color: #000000; /* Ensure formula text is black */
        }
        .note {
            font-size: 14px;
            color: #555555; /* Set note text color to a dark grey for better visibility */
            margin-top: 10px;
        }
    </style>

    <div class="instruction-box">
        <strong>📌 CBSE / ICSE / State Board</strong><br>
        ➤ Enter the percentage exactly as mentioned in your marksheet (Class 9 to 12).
    </div>

    <div class="instruction-box">
        <strong>📌 IB (International Baccalaureate)</strong><br>
        ➤ Use the following formula to convert your final score to percentage:<br>
        <div class="formula">Percentage = (Your Score ÷ 45) × 100</div><br>
        ➤ Example: If you scored 36 out of 45 → <div class="formula">(36 ÷ 45) × 100 = 80%</div><br>
        ✅ If your school provides a conversion certificate or percentage, use that instead.
    </div>

    <div class="instruction-box">
        <strong>📌 IGCSE</strong><br>
        ➤ If your school provides a percentage, use it directly.<br>
        ➤ Otherwise, estimate using:<br>
        <div class="formula">Estimated % = Your Grade × 2.5</div>
    </div>


    <div class="note">
       <br> ⚠️ <em>Note: These are general guidelines. Always follow the official conversion rules provided by your target university or school.<br></em><br>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# 4. Load & tidy data
# ─────────────────────────────────────────────
EXCEL_PATH = "College Finder UG New.xlsx"
profile_df = pd.read_excel(EXCEL_PATH, sheet_name="College_Finder")
uni_df     = pd.read_excel(EXCEL_PATH, sheet_name="University")

# Normalise headers
profile_df.columns = profile_df.columns.str.strip()
uni_df.columns     = uni_df.columns.str.strip()
rename_uni = {}
for col in uni_df.columns:
    key = col.lower().replace(" ", "")
    if key.startswith("requiredprofile"):
        rename_uni[col] = "Required Profile Score"
    elif key in {"qsranking", "qsrank", "rankqs"}:
        rename_uni[col] = "QS Ranking"
uni_df.rename(columns=rename_uni, inplace=True)

profile_df.rename(columns={
    "CC (Max 3)": "CC",
    "EC (Max 3)": "EC",
    "Internship (Max 2)": "Internship",
}, inplace=True)

num_cols_profile = [
    "Class 9","Class 10","Class 11","Class 12","SAT","AP",
    "CC","EC","Internship","Community","Research","LOR",
]
profile_df[num_cols_profile] = (
    profile_df[num_cols_profile].apply(pd.to_numeric, errors="coerce").fillna(0)
)
uni_df["Required Profile Score"] = pd.to_numeric(
    uni_df["Required Profile Score"], errors="coerce"
)
profile_df["Country"] = profile_df["Country"].astype(str).str.strip()
profile_df = profile_df[profile_df["Country"].str.lower() != "nan"]

# ─────────────────────────────────────────────
# 5. User inputs
# ─────────────────────────────────────────────
countries = sorted(profile_df["Country"].unique())
sel = st.multiselect("🌐 Choose Countries", ["All"] + countries, default=["All"])
filtered_profile = profile_df if "All" in sel else profile_df[profile_df["Country"].isin(sel)]

left, right = st.columns(2)

with left:
    st.header("📘 Academic")
    c9  = st.number_input("Class 9 %",  0, 100) / 100
    c10 = st.number_input("Class 10 %", 0, 100) / 100
    c11 = st.number_input("Class 11 %", 0, 100) / 100
    c12 = st.number_input("Class 12 %", 0, 100) / 100
    sat = st.number_input("SAT/ACT (400-1600)", 400, 1600) / 1600

    st.subheader("📘 AP Tests")
    n_ap = st.number_input("Number of APs", 0, 5, step=1)
    ap_scores = [st.number_input(f"AP{i+1} score", 0.0, 5.0, step=0.1)
                 for i in range(int(n_ap))]
    avg_ap = sum(ap_scores) / (n_ap * 5) if n_ap else 0.0

with right:
    st.header("🏅 Activities & Extras")
    cc   = st.number_input("Co-curricular (0-3)", 0, 3, step=1)
    ec   = st.number_input("Extra-curricular (0-3)", 0, 3, step=1)
    intr = st.number_input("Internships (0-2)", 0, 2, step=1)
    community = 1.0 if st.checkbox("Community Service") else 0.0
    research  = 1.0 if st.checkbox("Research Project") else 0.0

    st.header("📄 LORs")
    n_lor = st.number_input("Number of LORs (0-3)", 0, 3, step=1)

user_profile = {
    "Class 9": c9, "Class 10": c10, "Class 11": c11, "Class 12": c12,
    "SAT": sat, "AP": avg_ap,
    "CC": cc/3, "EC": ec/3, "Internship": intr/2,
    "Community": community, "Research": research, "LOR": n_lor/3,
}

# ─────────────────────────────────────────────
# 6. Helper functions
# ─────────────────────────────────────────────
acad_keys = ["Class 9","Class 10","Class 11","Class 12","SAT","AP"]
act_keys  = ["CC","EC","Internship","Community","Research"]

def country_score(row):
    total = (sum(user_profile[k] * row[k] for k in acad_keys + act_keys)
             + user_profile["LOR"] * row["LOR"])
    return round(total * 100, 1)

def render_cards(title, df, colour):
    st.markdown(f"## {title}")
    for i in range(0, len(df), 3):
        cols = st.columns(3)
        for col, (_, r) in zip(cols, df.iloc[i:i+3].iterrows()):
            with col:
                st.markdown(f"""
                <div class='uni-card' style='border-top:4px solid {colour};'>
                  <h4>{r['University']}</h4>
                  <div style='font-size:.8rem;margin-bottom:.4rem;'>
                    {r['Country']} · QS #{int(r['QS Ranking']) if pd.notna(r['QS Ranking']) else '–'}
                  </div>
                  <div style='font-size:.85rem;line-height:1.35rem;'>
                    <strong>Required:</strong> {int(r['Required Profile Score'])}<br>
                    <strong>Your score:</strong> {r['Your Profile %']}
                  </div>
                </div>
                """, unsafe_allow_html=True)

def build_pdf(country_scores, gap_view, amb, tgt, safe):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=30, rightMargin=30,
                            topMargin=30, bottomMargin=30)
    page_w, _ = landscape(A4)
    styles = getSampleStyleSheet()
    elems  = [Paragraph("Yocket Study-Abroad | Personalised University Report",
                        styles['Title']), Spacer(1, 12)]

    def add_table(df, hdr):
        elems.append(Paragraph(hdr, styles['Heading2']))
        data = [df.columns.tolist()] + df.astype(str).values.tolist()
        if 'University' in df.columns:
            uni_w   = (page_w-60)*0.35
            other_w = (page_w-60-uni_w)/(len(df.columns)-1)
            widths  = [uni_w if c=='University' else other_w for c in df.columns]
        else:
            widths = [(page_w-60)/len(df.columns)]*len(df.columns)
        tbl = Table(data, repeatRows=1, colWidths=widths)
        tbl.setStyle(TableStyle([
            ('GRID',(0,0),(-1,-1),0.25,colors.grey),
            ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        elems.extend([tbl, Spacer(1, 12)])

    add_table(country_scores, "Country-wise Profile Score")
    add_table(gap_view,        "University Gap Analysis")
    if not amb.empty:  add_table(amb,  "Ambitious Universities")
    if not tgt.empty:  add_table(tgt,  "Target Universities")
    if not safe.empty: add_table(safe, "Safe Universities")

    doc.build(elems)
    buf.seek(0)
    return buf

# ─────────────────────────────────────────────
# 7. Main action
# ─────────────────────────────────────────────
if st.button("🔍 Find My Universities"):
    # Country scores
    country_scores = filtered_profile[["Country"]].copy()
    country_scores["Total Profile %"] = filtered_profile.apply(country_score, axis=1)
    st.subheader("🌎 Country-wise Profile Breakdown")
    st.dataframe(country_scores.sort_values("Total Profile %", ascending=False)
                              .reset_index(drop=True), use_container_width=True)

    # University gap (hidden on-screen)
    score_map = dict(zip(country_scores["Country"], country_scores["Total Profile %"]))
    uni = uni_df.copy()
    uni["Your Profile %"] = uni["Country"].map(score_map)
    uni = uni[uni["Your Profile %"].notna()]
    uni["Gap %"] = (uni["Required Profile Score"] - uni["Your Profile %"]).round(1)
    gap_view = uni[["Country","University","QS Ranking",
                    "Required Profile Score","Your Profile %","Gap %"]]\
               .sort_values("Gap %", ascending=False).reset_index(drop=True)

    st.markdown("*(A detailed university gap analysis is included in your downloadable PDF.)*")

    # Categorise
    pos   = gap_view["Gap %"] > 0
    anchor = gap_view[pos]["Gap %"].idxmin() if pos.any() else gap_view["Gap %"].abs().idxmin()
    target_df = gap_view.iloc[max(0, anchor-5): anchor+1]
    ambitious_df = gap_view.iloc[max(0, anchor-11): max(0, anchor-5)]
    safe_df = gap_view.iloc[anchor+1: anchor+7]

    if not ambitious_df.empty: render_cards("🚀 Ambitious Universities", ambitious_df, RED)
    if not target_df.empty:    render_cards("🎯 Target Universities",    target_df,   BLUE)
    if not safe_df.empty:      render_cards("🛡️ Safe Universities",     safe_df,     GREEN)

    st.markdown("---")
    st.markdown("### 📄 Download your full report")
    
    # Add the "Book a Free 1:1 Counselling" Button beside the existing button
    col1, col2 = st.columns([2, 1])  # Create two columns
    with col1:
        pdf = build_pdf(country_scores, gap_view, ambitious_df, target_df, safe_df)
        st.download_button("📄 Download Detailed PDF Report", pdf, file_name="university_report.pdf", mime="application/pdf")
    with col2:
        st.markdown("""
        <a href="https://calendly.com/ugadmissions-yocket/university-readiness-counselling-booking" target="_blank">
            <button style="background-color: #1E88E5; color: white; padding: 10px 20px; border-radius: 5px; border: none; cursor: pointer;">
                Book a Free 1:1 Counselling
            </button>
        </a>
        """, unsafe_allow_html=True)

else:
    st.info("Enter your details above and click **Find My Universities** to generate personalised recommendations.")
