# ============================================================
# DHANVI Healthcare Ecosystem - PowerPoint Generator
# ============================================================
# Requirements:
#   pip install python-pptx
#
# Run:
#   python generate_pptx.py
# ============================================================

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os
import sys

# Force UTF-8 output so Unicode symbols print correctly on Windows cp1252 terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ── Output path ──────────────────────────────────────────────
OUTPUT_PATH = r"C:\Users\admin\.gemini\antigravity\scratch\dhanvi\DHANVI_Presentation.pptx"

# ── Theme colours (Classic Medical by default, dark with --dark) ──
is_classic = "--dark" not in sys.argv

if is_classic:
    CLR_BG          = RGBColor(0xf8, 0xfa, 0xfc)   # Clean medical white/slate #f8fafc
    CLR_WHITE       = RGBColor(0x0f, 0x17, 0x2a)   # Title: Deep navy  #0f172a
    CLR_TEAL        = RGBColor(0x02, 0x84, 0xc7)   # Medical Blue #0284c7
    CLR_TEAL_DARK   = RGBColor(0xe0, 0xf2, 0xfe)   # Badge fill: Soft sky #e0f2fe
    CLR_LIGHT_GRAY  = RGBColor(0x33, 0x41, 0x55)   # Body text: Charcoal slate #334155
    CLR_MID_GRAY    = RGBColor(0x64, 0x74, 0x8b)   # Mid gray    #64748b
    CLR_ACCENT_BAR  = RGBColor(0x02, 0x84, 0xc7)   # Classic Blue
else:
    CLR_BG          = RGBColor(0x0f, 0x17, 0x2a)   # Dark slate  #0f172a
    CLR_WHITE       = RGBColor(0xff, 0xff, 0xff)   # Pure white  #ffffff
    CLR_TEAL        = RGBColor(0x14, 0xb8, 0xa6)   # Teal        #14b8a6
    CLR_TEAL_DARK   = RGBColor(0x0f, 0x76, 0x6e)   # Dark teal   #0f766e
    CLR_LIGHT_GRAY  = RGBColor(0xcb, 0xd5, 0xe1)   # Light gray  #cbd5e1
    CLR_MID_GRAY    = RGBColor(0x64, 0x74, 0x8b)   # Mid gray    #64748b
    CLR_ACCENT_BAR  = RGBColor(0x14, 0xb8, 0xa6)   # Same as teal

# ── Slide dimensions (13.33 × 7.5 in widescreen 16:9) ───────
SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.50)

# ── Footer text ──────────────────────────────────────────────
FOOTER_TEXT = "DHANVI Healthcare Ecosystem  •  Team Epic Engineers  •  WHO & ABDM Aligned"

# ── Slide data ───────────────────────────────────────────────
SLIDES = [
    {
        "title":    "DHANVI",
        "subtitle": "Smart Healthcare Access for Everyone",
        "tagline":  "Right Care. Right Time. Right Place.",
        "badge":    "Healthcare & MedTech | Software & Hardware",
        "bullets":  [
            "Developed by Team Epic Engineers: Engineering the Future, Inspiring Legacies",
            "A unified digital healthcare ecosystem bringing instant care access to every citizen",
            "Featuring the Dual-Format Emergency Health ID Card & AI-powered triage guidance",
        ],
    },
    {
        "title":    "The Healthcare Challenge",
        "subtitle": "Fragmented Data & Costly Delays in Critical Moments",
        "badge":    "Problem Statement",
        "bullets":  [
            "Information Fragmentation: Scattered records cause critical delays.",
            "Wasted OPD Hours: Patients spend hours checking availability and booking.",
            "Emergency Gaps: Locating ICU beds and ambulances is chaotic.",
            "Economic Burden: 45.11% of Indian healthcare is paid out-of-pocket.",
            "Impact: Lost time, travel expenses, and risk in the Golden Hour.",
        ],
    },
    {
        "title":    "DHANVI - The Solution",
        "subtitle": "Instant Discovery, Transparent Appointments & Emergency Dispatch",
        "badge":    "Solution Overview",
        "bullets":  [
            "Hospital & Doctor Discovery: Instant search for accredited specialists.",
            "Real-Time OPD Booking: Live slot visibility and upfront fees.",
            "One-Tap Emergency Response: Geolocated trauma care and ambulance dispatch.",
            "AI Clinical Triage: Symptom-checking guiding users to the right department.",
            "Universal Health Pass: Smart ID carrying vital parameters everywhere.",
        ],
    },
    {
        "title":    "Emergency Health ID Card",
        "subtitle": "Dual-Format (Physical PVC NFC + Digital Wallet Pass)",
        "badge":    "Hardware & Security Innovation",
        "bullets":  [
            "Instant Emergency Profile: Blood group, chronic conditions, drug allergies.",
            "Paramedic SOS Contact: One-tap next-of-kin contact during unconscious trauma.",
            "Two-Tier Privacy: Level 1 (instant vitals) vs. Level 2 (OTP-locked EHR).",
            "Zero-Connectivity Support: NFC chip stores critical parameters offline.",
        ],
    },
    {
        "title":    "WHO Digital Health Compliance",
        "subtitle": "Adhering to Global Standards",
        "badge":    "Global Compliance",
        "bullets":  [
            "Universal Access & Equity: Optimized for low-bandwidth environments.",
            "Patient Safety & Governance: AI as clinical recommendation support.",
            "Data Privacy & Minimization: End-to-end encryption with consent controls.",
            "Interoperability: Complies with ABDM, UHI, and international protocols.",
        ],
    },
    {
        "title":    "Architecture & Multi-Layer Framework",
        "subtitle": "3-Tier Scalable Stack",
        "badge":    "System Architecture",
        "bullets":  [
            "Top Layer (Govt & Policy): ABDM, NHA, and MOHFW compliance.",
            "Middle Layer (Research): WHO guidelines & NLP triage algorithms.",
            "Bottom Layer (Technology): React.js, Node/Express, Supabase/PostgreSQL, NTAG NFC.",
        ],
    },
]


# ─────────────────────────────────────────────────────────────
# Helper utilities
# ─────────────────────────────────────────────────────────────

def set_bg(slide, color: RGBColor):
    """Fill slide background with a solid colour."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill_color, line_color=None, line_width_pt=0):
    """Add a coloured rectangle shape to the slide."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width_pt)
    else:
        shape.line.fill.background()   # no border
    return shape


def add_textbox(slide, left, top, width, height, text, font_size,
                bold=False, color=None, align=PP_ALIGN.LEFT, italic=False):
    """Add a text box and return the run so caller can style further."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return txBox


def add_badge(slide, text: str, left, top):
    """Draw a small badge box with teal border and dark-teal fill."""
    width  = Inches(3.8)
    height = Inches(0.32)
    box = add_rect(slide, left, top, width, height,
                   fill_color=CLR_TEAL_DARK,
                   line_color=CLR_TEAL, line_width_pt=1.2)
    tf = box.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text.upper()
    run.font.size = Pt(9)
    run.font.bold = True
    run.font.color.rgb = CLR_TEAL
    # Vertical centering via margin tweak
    tf.margin_top    = Pt(4)
    tf.margin_bottom = Pt(4)
    tf.margin_left   = Pt(6)
    tf.margin_right  = Pt(6)


def add_accent_bar(slide):
    """Add the thin teal vertical bar on the left edge."""
    add_rect(slide,
             left=Inches(0), top=Inches(0),
             width=Inches(0.08), height=SLIDE_H,
             fill_color=CLR_ACCENT_BAR)


def add_footer(slide, slide_number: int, total: int):
    """Add footer text (centered) and slide number (right)."""
    # Footer label
    add_textbox(slide,
                left=Inches(0.15), top=Inches(7.1),
                width=Inches(11.5), height=Inches(0.3),
                text=FOOTER_TEXT,
                font_size=8,
                color=CLR_MID_GRAY,
                align=PP_ALIGN.CENTER)

    # Slide number
    add_textbox(slide,
                left=Inches(12.3), top=Inches(7.1),
                width=Inches(0.9), height=Inches(0.3),
                text=f"{slide_number} / {total}",
                font_size=8,
                color=CLR_MID_GRAY,
                align=PP_ALIGN.RIGHT)


def add_bullet_list(slide, bullets: list[str], left, top, width, height):
    """Add a bullet list with teal ▸ markers and light-gray text."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, bullet_text in enumerate(bullets):
        # Reuse first paragraph, add new ones after
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(5)
        p.space_after  = Pt(2)

        # Teal bullet character
        run_bullet = p.add_run()
        run_bullet.text = "▸  "
        run_bullet.font.size = Pt(14)
        run_bullet.font.color.rgb = CLR_TEAL
        run_bullet.font.bold = True

        # Bullet content
        run_text = p.add_run()
        run_text.text = bullet_text
        run_text.font.size = Pt(13)
        run_text.font.color.rgb = CLR_LIGHT_GRAY


# ─────────────────────────────────────────────────────────────
# Per-slide builders
# ─────────────────────────────────────────────────────────────

def build_slide_1(slide, data: dict, slide_num: int, total: int):
    """Title / Hero slide with extra tagline."""
    set_bg(slide, CLR_BG)
    add_accent_bar(slide)

    # Badge – top-left
    add_badge(slide, data["badge"], left=Inches(0.18), top=Inches(0.22))

    # Hero title – large, centred
    add_textbox(slide,
                left=Inches(0.15), top=Inches(1.0),
                width=Inches(13.0), height=Inches(1.3),
                text=data["title"],
                font_size=64,
                bold=True,
                color=CLR_WHITE,
                align=PP_ALIGN.CENTER)

    # Subtitle
    add_textbox(slide,
                left=Inches(0.15), top=Inches(2.2),
                width=Inches(13.0), height=Inches(0.5),
                text=data["subtitle"],
                font_size=20,
                color=CLR_TEAL,
                align=PP_ALIGN.CENTER)

    # Tagline
    add_textbox(slide,
                left=Inches(0.15), top=Inches(2.75),
                width=Inches(13.0), height=Inches(0.4),
                text=data.get("tagline", ""),
                font_size=14,
                italic=True,
                color=CLR_MID_GRAY,
                align=PP_ALIGN.CENTER)

    # Horizontal divider (teal line)
    add_rect(slide,
             left=Inches(1.5), top=Inches(3.25),
             width=Inches(10.33), height=Pt(1.5),
             fill_color=CLR_TEAL)

    # Bullet list
    add_bullet_list(slide, data["bullets"],
                    left=Inches(1.0), top=Inches(3.45),
                    width=Inches(11.2), height=Inches(3.2))

    add_footer(slide, slide_num, total)


def build_slide_standard(slide, data: dict, slide_num: int, total: int):
    """Standard content slide layout."""
    set_bg(slide, CLR_BG)
    add_accent_bar(slide)

    # Badge – top-left
    add_badge(slide, data["badge"], left=Inches(0.18), top=Inches(0.22))

    # Title
    add_textbox(slide,
                left=Inches(0.18), top=Inches(0.65),
                width=Inches(12.9), height=Inches(0.85),
                text=data["title"],
                font_size=38,
                bold=True,
                color=CLR_WHITE,
                align=PP_ALIGN.LEFT)

    # Subtitle
    add_textbox(slide,
                left=Inches(0.18), top=Inches(1.45),
                width=Inches(12.9), height=Inches(0.4),
                text=data["subtitle"],
                font_size=16,
                color=CLR_TEAL,
                align=PP_ALIGN.LEFT)

    # Thin separator line
    add_rect(slide,
             left=Inches(0.18), top=Inches(1.92),
             width=Inches(12.9), height=Pt(1.2),
             fill_color=CLR_TEAL_DARK)

    # Bullet list
    add_bullet_list(slide, data["bullets"],
                    left=Inches(0.25), top=Inches(2.05),
                    width=Inches(12.8), height=Inches(4.6))

    add_footer(slide, slide_num, total)


# ─────────────────────────────────────────────────────────────
# Main builder
# ─────────────────────────────────────────────────────────────

def build_presentation():
    prs = Presentation()

    # Set widescreen dimensions
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H

    # Use a completely blank layout (index 6 = blank in default theme)
    blank_layout = prs.slide_layouts[6]

    total = len(SLIDES)

    for idx, data in enumerate(SLIDES):
        slide = prs.slides.add_slide(blank_layout)
        slide_num = idx + 1

        if slide_num == 1:
            build_slide_1(slide, data, slide_num, total)
        else:
            build_slide_standard(slide, data, slide_num, total)

        print(f"  ✔ Slide {slide_num}/{total}: {data['title']}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    prs.save(OUTPUT_PATH)
    print(f"\n✅ Presentation saved to:\n   {OUTPUT_PATH}")


if __name__ == "__main__":
    print("=" * 60)
    print("  DHANVI Healthcare Ecosystem — Presentation Generator")
    print("=" * 60)
    print(f"  Slides  : {len(SLIDES)}")
    print(f"  Theme   : Dark Slate / Teal (#0f172a / #14b8a6)")
    print(f"  Output  : {OUTPUT_PATH}")
    print("-" * 60)
    build_presentation()
    print("=" * 60)
