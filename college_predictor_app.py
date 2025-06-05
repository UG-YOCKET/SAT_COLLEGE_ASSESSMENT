import streamlit as stAdd commentMore actions
import pandas as pd
import io
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# ─────────────────────────────────────────────
# 0. Page config (must be first Streamlit call)
# CONFIG & THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Yocket Study‑Abroad | University Finder",
    page_icon="🎓",
    layout="wide"
)
st.set_page_config(page_title="Yocket Study‑Abroad | University Finder", page_icon="🎓", layout="wide")

ORANGE = "#FF6B00"  # Brand accent
RED    = "#E53935"  # Ambitious
BLUE   = "#1E88E5"  # Target
GREEN  = "#43A047"  # Safe

st.markdown(f"""
<style>
#MainMenu, footer {{visibility:hidden;}}
body{{background:#f5f6f7;color:#212121;font-family:'Segoe UI',sans-serif;}}
.hero-title{{font-size:2.4rem;font-weight:800;color:{ORANGE};margin:0;}}
.hero-sub{{font-size:1.4rem;font-weight:600;margin-top:.3rem;}}
.hero-divider{{height:2px;background:{ORANGE};margin:1.6rem 0 2.4rem;}}
.card{{background:#fff;border-radius:14px;max-width:900px;margin:0 auto;padding:2.1rem 2.6rem;box-shadow:0 4px 16px rgba(0,0,0,.06);}}
.card h3{{font-size:1.65rem;margin-bottom:.9rem;}}
.step{{display:flex;margin:.65rem 0;}}
.step-num{{min-width:30px;height:30px;border-radius:50%;background:{ORANGE}33;color:#000;font-weight:700;font-size:.85rem;display:flex;align-items:center;justify-content:center;margin-right:.6rem;}}
.step-text{{line-height:1.45rem;}}
@media(max-width:480px){{.card{{padding:1.5rem 1.2rem;}}.hero-title{{font-size:2rem;}}.hero-sub{{font-size:1.2rem;}}}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 1. Global styling & helpers
# HERO & GUIDE
# ─────────────────────────────────────────────
ORANGE = "#FF6B00"  # Yocket brand

st.markdown(
    f"""
    <style>
    /* Hide default Streamlit chrome */
    #MainMenu, footer {{visibility:hidden;}}

    body{{background:#f5f6f7;color:#212121;font-family:'Segoe UI',sans-serif;}}
    .hero-title{{font-size:2.4rem;font-weight:800;color:{ORANGE};margin:0;}}
    .hero-sub  {{font-size:1.4rem;font-weight:600;margin-top:.3rem;}}
    .hero-divider{{height:2px;background:{ORANGE};margin:1.6rem 0 2.4rem;}}

    .card{{background:#fff;border-radius:14px;max-width:900px;margin:0 auto;
          padding:2.1rem 2.6rem;box-shadow:0 4px 16px rgba(0,0,0,.06);color:#000;}}
    .card h3{{font-size:1.65rem;margin-bottom:.9rem;}}

    .step{{display:flex;margin:.65rem 0;}}
    .step-num{{min-width:30px;height:30px;border-radius:50%;background:{ORANGE}33;
              color:#000;font-weight:700;font-size:.85rem;display:flex;align-items:center;
              justify-content:center;margin-right:.6rem;}}
    .step-text{{line-height:1.45rem;}}

    @media(max-width:480px){{
      .card{{padding:1.5rem 1.2rem;}}
      .hero-title{{font-size:2rem;}}
      .hero-sub{{font-size:1.2rem;}}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("""
<div style='text-align:center'>
  <div class='hero-title'>YOCKET STUDY‑ABROAD 🎓</div>
  <div class='hero-sub'>University Finder 2025</div>
</div>
<div class='hero-divider'></div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='card'>
  <h3>How to use this Finder</h3>
  <div class='step'><div class='step-num'>1</div><div class='step-text'>Choose <strong>countries</strong>.</div></div>
  <div class='step'><div class='step-num'>2</div><div class='step-text'>Fill in <strong>academic</strong> & <strong>test</strong> scores.</div></div>
  <div class='step'><div class='step-num'>3</div><div class='step-text'>Add <strong>activities</strong>, internships, LORs.</div></div>
  <div class='step'><div class='step-num'>4</div><div class='step-text'>Hit <strong>Find My Universities</strong> ↴</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("### &nbsp;")

# ─────────────────────────────────────────────
# 2. Hero banner & quick guide
# ─────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center">
      <div class="hero-title">YOCKET STUDY‑ABROAD 🎓</div>
      <div class="hero-sub">University Finder 2025</div>
    </div>
    <div class="hero-divider"></div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card">
      <h3>How to use this Finder</h3>
      <div class="step"><div class="step-num">1</div><div class="step-text">Choose one or more <strong>countries</strong>.</div></div>
      <div class="step"><div class="step-num">2</div><div class="step-text">Enter <strong>academic scores</strong> (Class 9‑12 + SAT/ACT).</div></div>
      <div class="step"><div class="step-num">3</div><div class="step-text">Add <strong>AP</strong> test data (optional).</div></div>
      <div class="step"><div class="step-num">4</div><div class="step-text">Add <strong>activities</strong>, internships & extras.</div></div>
      <div class="step"><div class="step-num">5</div><div class="step-text">Enter number of <strong>LORs</strong>.</div></div>
      <div class="step"><div class="step-num">6</div><div class="step-text">Click <strong>Find My Universities</strong> for Ambitious‑Target‑Safe lists.</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### &nbsp;")  # spacer

# ─────────────────────────────────────────────
# 3. Load data (Excel has two sheets)
# LOAD DATA
# ─────────────────────────────────────────────
EXCEL_PATH = "College Finder UG New.xlsx"
profile_df = pd.read_excel(EXCEL_PATH, sheet_name="College_Finder")
uni_df     = pd.read_excel(EXCEL_PATH, sheet_name="University")
uni_df = pd.read_excel(EXCEL_PATH, sheet_name="University")

profile_df["Country"] = profile_df["Country"].astype(str).str.strip()
profile_df = profile_df[profile_df["Country"].str.lower() != "nan"]
profile_df.rename(columns={
    "CC (Max 3)": "CC",
    "EC (Max 3)": "EC",
    "Internship (Max 2)": "Internship",
}, inplace=True)

numeric_cols = [
    "Class 9","Class 10","Class 11","Class 12","SAT","AP",
    "CC","EC","Internship","Community","Research","LOR",
]
profile_df[numeric_cols] = profile_df[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
profile_df.rename(columns={"CC (Max 3)":"CC","EC (Max 3)":"EC","Internship (Max 2)":"Internship"}, inplace=True)

num_cols = ["Class 9","Class 10","Class 11","Class 12","SAT","AP","CC","EC","Internship","Community","Research","LOR"]
profile_df[num_cols] = profile_df[num_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

uni_df.rename(columns=str.strip, inplace=True)
uni_df["Required Profile Score"] = pd.to_numeric(uni_df["Required Profile Score"], errors="coerce")

# ─────────────────────────────────────────────
# 4. Country selector & inputs
# INPUT SECTION
# ─────────────────────────────────────────────
countries = sorted(profile_df["Country"].unique())
sel = st.multiselect("🌐 Choose Countries", ["All"] + countries, default=["All"])
filtered_profile = profile_df if "All" in sel else profile_df[profile_df["Country"].isin(sel)]

left, right = st.columns(2)

with left:
    st.header("📘 Academic")
    class9  = st.number_input("Class 9 %", 0, 100) / 100
    class10 = st.number_input("Class 10 %", 0, 100) / 100
    class11 = st.number_input("Class 11 %", 0, 100) / 100
    class12 = st.number_input("Class 12 %", 0, 100) / 100
    sat     = st.number_input("SAT/ACT (400‑1600)", 400, 1600) / 1600

    c9 = st.number_input("Class 9 %", 0, 100) / 100
    c10 = st.number_input("Class 10 %", 0, 100) / 100
    c11 = st.number_input("Class 11 %", 0, 100) / 100
    c12 = st.number_input("Class 12 %", 0, 100) / 100
    sat = st.number_input("SAT/ACT (400‑1600)", 400, 1600) / 1600
    st.subheader("📘 AP Tests")
    num_ap = st.number_input("Number of APs", 0, 5, step=1)
    ap_scores = [st.number_input(f"AP{i+1} score", 0.0, 5.0, step=0.1) for i in range(int(num_ap))]
    avg_ap = sum(ap_scores) / (num_ap * 5) if num_ap > 0 else 0.0
    n_ap = st.number_input("Number of APs", 0, 5, step=1)
    ap_scores = [st.number_input(f"AP{i+1} score", 0.0, 5.0, step=0.1) for i in range(int(n_ap))]
    avg_ap = sum(ap_scores) / (n_ap * 5) if n_ap else 0.0

with right:
    st.header("🏅 Activities & Extras")
    cc_cnt     = st.number_input("Co‑curricular (0‑3)", 0, 3, step=1)
    ec_cnt     = st.number_input("Extra‑curricular (0‑3)", 0, 3, step=1)
    intern_cnt = st.number_input("Internships (0‑2)", 0, 2, step=1)
    community  = 1.0 if st.checkbox("Community Service") else 0.0
    research   = 1.0 if st.checkbox("Research Project") else 0.0

    cc = st.number_input("Co‑curricular (0‑3)", 0, 3, step=1)
    ec = st.number_input("Extra‑curricular (0‑3)", 0, 3, step=1)
    intern = st.number_input("Internships (0‑2)", 0, 2, step=1)
    community = 1.0 if st.checkbox("Community Service") else 0.0
    research = 1.0 if st.checkbox("Research Project") else 0.0
    st.header("📄 LORs")
    num_lor  = st.number_input("Number of LORs (0‑3)", 0, 3, step=1)
    lor_frac = num_lor / 3
    n_lor = st.number_input("Number of LORs (0‑3)", 0, 3, step=1)

user_profile = {
    "Class 9": class9,
    "Class 10": class10,
    "Class 11": class11,
    "Class 12": class12,
    "SAT": sat,
    "AP": avg_ap,
    "CC": cc_cnt / 3,
    "EC": ec_cnt / 3,
    "Internship": intern_cnt / 2,
    "Community": community,
    "Research": research,
    "LOR": lor_frac,
    "Class 9": c9, "Class 10": c10, "Class 11": c11, "Class 12": c12,
    "SAT": sat, "AP": avg_ap,
    "CC": cc / 3, "EC": ec / 3, "Internship": intern / 2,
    "Community": community, "Research": research, "LOR": n_lor / 3,
}

# ─────────────────────────────────────────────
# 5. Compute & display on button click
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
if st.button("🔍 Find My Universities", help="Generate recommendations"):
    acad_keys     = ["Class 9","Class 10","Class 11","Class 12","SAT","AP"]
    activity_keys = ["CC","EC","Internship","Community","Research"]

    def score_row(row):
        raw_acad = sum(user_profile[k] * row[k] for k in acad_keys)
        raw_act  = sum(user_profile[k] * row[k] for k in activity_keys)
        raw_lor  = user_profile["LOR"] * row["LOR"]
        total    = raw_acad + raw_act + raw_lor
        max_acad = sum(row[k] for k in acad_keys) or 1
        max_act  = sum(row[k] for k in activity_keys) or 1
        acad_pct = raw_acad / max_acad * 100
        act_pct  = raw_act  / max_act  * 100
        lor_pct  = raw_lor  / (row["LOR"] or 1) * 100
        return pd.Series({
            "Academic %": round(acad_pct, 1),
            "Activity %": round(act_pct, 1),
            "LOR %":      round(lor_pct, 1),
            "Total Profile %": round(total * 100, 1),
        })

    country_scores = filtered_profile.apply(score_row, axis=1)
    country_scores.insert(0, "Country", filtered_profile["Country"].values)

    st.subheader("🌎 Country‑wise Profile Breakdown")
    st.dataframe(
        country_scores.sort_values("Total Profile %", ascending=False).reset_index(drop=True),
        use_container_width=True,
    )

    # ---- University gap analysis ----
    score_map = dict(zip(country_scores["Country"], country_scores["Total Profile %"]))
    uni_df_filtered = uni_df.copy()
    uni_df_filtered["Your Profile %"] = uni_df_filtered["Country"].map(score_map)
    uni_df_filtered = uni_df_filtered[uni_df_filtered["Your Profile %"].notna()]

    if uni_df_filtered.empty:
        st.warning("No universities match the selected countries.")
        st.stop()

    uni_df_filtered["Gap %"] = (uni_df_filtered["Required Profile Score"] - uni_df_filtered["Your Profile %"]).round(1)

    gap_view = (
        uni_df_filtered[[
            "Country","University","QS Ranking","Required Profile Score","Your Profile %","Gap %",
        ]]
        .sort_values("Gap %", ascending=False)
        .reset_index(drop=True)
    )

    # Anchor = smallest positive gap (or closest to zero if no positive)
    pos_mask = gap_view["Gap %"] > 0
    anchor_idx = gap_view[pos_mask]["Gap %"].idxmin() if pos_mask.any() else gap_view["Gap %"].abs().idxmin()
def render_cards(title: str, df: pd.DataFrame, color: str):
    """Render a section of cards, 3 per row."""
    st.markdown(f"## {title}")
    for i in range(0, len(df), 3):
        cols = st.columns(3)
        for col, (_, row) in zip(cols, df.iloc[i:i+3].iterrows()):
            with col:
                st.markdown(
                    f"""
                    <div style='background:#fff;border-top:4px solid {color};border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.04);padding:1rem 1.2rem;margin-bottom:1.2rem;'>
                      <h4 style='margin:0 0 .3rem 0;font-size:1rem;'>{row['University']}</h4>
                      <div style='font-size:.8rem;color:#555;margin-bottom:.4rem;'>
                         {row['Country']} · QS #{int(row['QS Ranking']) if pd.notna(row['QS Ranking']) else '–'}
                      </div>
                      <div style='font-size:.85rem;line-height:1.35rem;'>
                         <span><strong>Required Score:</strong> {int(row['Required Profile Score'])}</span><br>
                         <span><strong>Your Score:</strong> {round(row['Your Profile %'],1)}</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def build_pdf(country_scores: pd.DataFrame, gap_view: pd.DataFrame, ambitious: pd.DataFrame, target: pd.DataFrame, safe: pd.DataFrame) -> io.BytesIO:
    """Create landscape PDF with uniform, wrapped tables."""
    buf = io.BytesIO()
    page_w, _ = landscape(A4)
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elems = [Paragraph("Yocket Study-Abroad | Personalised University Report", styles['Title']), Spacer(1, 12)]

    def add_table(df: pd.DataFrame, heading: str):
        elems.append(Paragraph(heading, styles['Heading2']))
        data = [df.columns.tolist()]
        for _, r in df.iterrows():
            data.append([Paragraph(str(r[c]), styles['BodyText']) for c in df.columns])
        # column widths
        if 'University' in df.columns:
            uni_w = (page_w - 60) * 0.35
            other_w = (page_w - 60 - uni_w) / (len(df.columns) - 1)
            widths = [uni_w if c == 'University' else other_w for c in df.columns]
        elif len(df.columns) == 2:
            widths = [(page_w - 60) * 0.4, (page_w - 60) * 0.6]
        else:
            widths = [(page_w - 60) / len(df.columns)] * len(df.columns)
        tbl = Table(data, repeatRows=1, colWidths=widths)
        tbl.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 12))

    add_table(country_scores, "Country-wise Profile Score")
    add_table(gap_view, "University Gap Analysis")
    if not ambitious.empty:
        add_table(ambitious, "Ambitious Universities")
    if not target.empty:
        add_table(target, "Target Universities")
    if not safe.empty:
        add_table(safe, "Safe Universities")

    doc.build(elems)
    buf.seek(0)
    return buf

    gap_view.insert(0, "Anchor", "")
    gap_view.loc[anchor_idx, "Anchor"] = "⬅️"

    st.subheader("🗺️ University Gap Analysis (positive gap = profile below requirement)")

    def highlight(row):
        style = f"background-color:{ORANGE}22;font-weight:600;"
        return [style if row["Anchor"] == "⬅️" else "" for _ in row]

    styled_gap = gap_view.style.apply(highlight, axis=1).hide(axis="columns", subset=["Anchor"])
    st.write(styled_gap.to_html(index=False, escape=False), unsafe_allow_html=True)

    # ---- Category lists ----
    target_start = max(0, anchor_idx - 5)
    target_end   = anchor_idx + 1  # exclusive
    target_list  = gap_view.iloc[target_start:target_end]

    ambitious_start = max(0, target_start - 6)
    ambitious_list  = gap_view.iloc[ambitious_start:target_start]

    safe_start = anchor_idx + 1
    safe_end   = safe_start + 6
    safe_list  = gap_view.iloc[safe_start:safe_end]

    tabs = st.tabs(["🚀 Ambitious", "🎯 Target", "🛡️ Safe"])
# ─────────────────────────────────────────────
# MAIN BUTTON ACTION
# ─────────────────────────────────────────────
if st.button("🔍 Find My Universities"):
    acad_keys = ["Class 9","Class 10","Class 11","Class 12","SAT","AP"]
    act_keys = ["CC","EC","Internship","Community","Research"]

    with tabs[0]:
        st.markdown("#### Universities that will stretch your profile")
        st.dataframe(ambitious_list.reset_index(drop=True), use_container_width=True)
    def calc_score(row):
        total = sum(user_profile[k] * row[k] for k in acad_keys + act_keys) + user_profile["LOR"] * row["LOR"]
        return round(total * 100, 1)

    with tabs[1]:
        st.markdown("#### Best‑fit options (Target)")
        st.dataframe(target_list.reset_index(drop=True), use_container_width=True)
    country_scores = filtered_profile[["Country"]].copy()
    country_scores["Total Profile %"] = filtered_profile.apply(calc_score, axis=1)

    with tabs[2]:
        st.markdown("#### Safer admits consistent with your profile")
        st.dataframe(safe_list.reset_index(drop=True), use_container_width=True)
    # display country scores
    st.markdown("## Country-wise Profile Score")
    st.dataframe(country_scores, use_container_width=True)

    # map profile to universities
    score_map = dict(zip(country_scores["Country"], country_scores["Total Profile %"]))
    uni = uni_df.copy()
    uni["Your Profile %"] = uni["Country"].map(score_map)
    uni = uni[uni["Your Profile %"].notna()]
    uni["Gap %"] = (uni["Required Profile Score"] - uni["Your Profile %"]).round(1)
    gap_view = uni[["Country","University","QS Ranking","Required Profile Score","Your Profile %","Gap %"]].sort_values("Gap %", ascending=False).reset_index(drop=True)

    st.markdown("*(Detailed gap analysis is included in the downloadable PDF.)*")

    # categorise
    pos = gap_view["Gap %"] > 0
    anchor_idx = gap_view[pos]["Gap %"].idxmin() if pos.any() else gap_view["Gap %"].abs().idxmin()
    target_df = gap_view.iloc[max(0, anchor_idx-5): anchor_idx+1]
    ambitious_df = gap_view.iloc[max(0, anchor_idx-11): max(0, anchor_idx-5)]
    safe_df = gap_view.iloc[anchor_idx+1: anchor_idx+7]

    if not ambitious_df.empty:
        render_cards("Ambitious Universities", ambitious_df, RED)
    if not target_df.empty:
        render_cards("Target Universities", target_df, BLUE)
    if not safe_df.empty:
        render_cards("Safe Universities", safe_df, GREEN)

    st.markdown("---")
    st.markdown("### 📄 Download your full report")
    pdf_file = build_pdf(country_scores, gap_view, ambitious_df, target_df, safe_df)
    st.download_button("📄 Download Detailed PDF Report", pdf_file, file_name="university_report.pdf", mime="application/pdf")
else:
    st.info("Enter your details above and click the button to generate recommendations.")
    st.info("Fill in your details and click the button to generate recommendations and download the PDF report.")
