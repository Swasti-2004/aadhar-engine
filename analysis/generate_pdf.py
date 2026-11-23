from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime
import os

# Create PDF
pdf_filename = "UIDAI_Hackathon_Submission.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=50)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2c3e50'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#34495e'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=12,
)

# COVER PAGE
elements.append(Spacer(1, 1*inch))  # REDUCED from 2*inch
elements.append(Paragraph("🇮🇳 Aadhaar Insight Engine", title_style))
elements.append(Spacer(1, 0.2*inch))  # REDUCED from 0.3*inch
elements.append(Paragraph("Geographic & Temporal Pattern Analysis", heading_style))
elements.append(Spacer(1, 0.3*inch))  # REDUCED from 0.5*inch
elements.append(Paragraph("UIDAI Data Hackathon 2026", normal_style))
elements.append(Spacer(1, 0.3*inch))

# Team Details
elements.append(Paragraph("<b>Team ID:</b> UIDAI_4568", normal_style))
elements.append(Paragraph("<b>Team Lead:</b> ASHISH", normal_style))
elements.append(Paragraph("<b>Email:</b> goyalashish2003@gmail.com", normal_style))
elements.append(Paragraph("<b>Mobile:</b> 7015728644", normal_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph(f"<b>Submission Date:</b> {datetime.now().strftime('%B %d, %Y')}", normal_style))
elements.append(PageBreak())


# PROBLEM STATEMENT
elements.append(Paragraph("Problem Statement", heading_style))
elements.append(Paragraph(
    "Identify meaningful patterns, trends, anomalies, or predictive indicators in Aadhaar "
    "enrolment and update datasets and translate them into clear insights or solution frameworks "
    "that can support informed decision-making and system improvements for UIDAI.",
    normal_style
))
elements.append(Spacer(1, 0.3*inch))

# APPROACH
elements.append(Paragraph("Our Approach", heading_style))
elements.append(Paragraph(
    "We conducted comprehensive analysis on 4.5+ million Aadhaar records across three datasets: "
    "Enrolment (1M records), Demographic Updates (2M records), and Biometric Updates (1.5M records). "
    "Our analysis combined statistical methods, temporal trend analysis, and geographic pattern recognition "
    "to extract actionable insights.",
    normal_style
))
elements.append(PageBreak())

# DATASETS USED
elements.append(Paragraph("Datasets Used", heading_style))

# Better formatted dataset info without table overflow
elements.append(Paragraph("<b>1. Aadhaar Enrolment Dataset</b>", normal_style))
elements.append(Paragraph(
    "• Records: 1,006,029<br/>"
    "• Columns: date, state, district, pincode, age_0_5, age_5_17, age_18_greater<br/>"
    "• Purpose: Analysis of new Aadhaar registrations across demographics",
    normal_style
))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>2. Demographic Updates Dataset</b>", normal_style))
elements.append(Paragraph(
    "• Records: 2,000,000<br/>"
    "• Columns: date, state, district, pincode, demo_age_5_17, demo_age_17_<br/>"
    "• Purpose: Tracking address, name, mobile number, and other demographic changes",
    normal_style
))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>3. Biometric Updates Dataset</b>", normal_style))
elements.append(Paragraph(
    "• Records: 1,500,000<br/>"
    "• Columns: date, state, district, pincode, bio_age_5_17, bio_age_17_<br/>"
    "• Purpose: Analysis of fingerprint, iris, and facial biometric update patterns",
    normal_style
))
elements.append(PageBreak())

# METHODOLOGY
elements.append(Paragraph("Methodology", heading_style))
elements.append(Paragraph("<b>1. Data Cleaning & Preprocessing:</b>", normal_style))
elements.append(Paragraph(
    "• Merged 12 CSV files (3 enrolment + 5 demographic + 4 biometric)<br/>"
    "• Verified data integrity - zero missing values found<br/>"
    "• Standardized date formats and numeric types<br/>"
    "• Total processing: 4,506,029 records",
    normal_style
))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>2. Statistical Analysis:</b>", normal_style))
elements.append(Paragraph(
    "• Univariate Analysis: Age group distributions, state-wise counts<br/>"
    "• Bivariate Analysis: State vs age groups, time vs enrollments<br/>"
    "• Trivariate Analysis: State vs age vs time patterns",
    normal_style
))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>3. Visualization & Dashboard:</b>", normal_style))
elements.append(Paragraph(
    "• Built interactive React dashboard with Recharts library<br/>"
    "• Created bar charts, pie charts, line graphs for pattern visualization<br/>"
    "• Implemented responsive design for clear data presentation",
    normal_style
))
elements.append(PageBreak())

# KEY FINDINGS
elements.append(Paragraph("Key Findings", heading_style))

elements.append(Paragraph("<b>Finding 1: Baby Enrollment Dominance</b>", normal_style))
elements.append(Paragraph(
    "65.3% of all enrollments are babies aged 0-5 years (3.5M out of 5.4M total). "
    "Only 3.1% are adults (168K), indicating near-complete adult coverage. "
    "This suggests UIDAI should prioritize birth-time enrollment programs.",
    normal_style
))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("<b>Finding 2: September Enrollment Spike</b>", normal_style))
elements.append(Paragraph(
    "September 2025 recorded 1.47 million enrollments - 2x the average monthly rate. "
    "This massive spike coincides with back-to-school season, suggesting strategic "
    "timing for enrollment campaigns can dramatically increase participation.",
    normal_style
))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("<b>Finding 3: Geographic Concentration</b>", normal_style))
elements.append(Paragraph(
    "Top 3 states (Uttar Pradesh: 1.02M, Bihar: 610K, Madhya Pradesh: 494K) account for "
    "42% of all enrollments. Urban districts like Thane and Bengaluru show high activity, "
    "but rural areas also demonstrate strong participation.",
    normal_style
))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("<b>Finding 4: Biometric Updates Exceed Demographic Updates</b>", normal_style))
elements.append(Paragraph(
    "Biometric updates (64.1M) are 1.33x more common than demographic updates (48.3M). "
    "This indicates people update fingerprints/photos more frequently than changing address/name.",
    normal_style
))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("<b>Finding 5: Age-Based Update Patterns</b>", normal_style))
elements.append(Paragraph(
    "Adults dominate demographic updates (90.1%) as they relocate and change addresses. "
    "However, biometric updates are nearly equal between children (48.7%) and adults (51.3%), "
    "reflecting the need for children to update biometrics as they grow.",
    normal_style
))
elements.append(PageBreak())

# STRATEGIC RECOMMENDATIONS
elements.append(Paragraph("Strategic Recommendations for UIDAI", heading_style))

elements.append(Paragraph("<b>HIGH PRIORITY:</b>", normal_style))
elements.append(Paragraph(
    "1. <b>Leverage September Momentum:</b> Investigate and replicate the factors that caused "
    "the September spike. Partner with schools for back-to-school enrollment drives.<br/><br/>"
    "2. <b>Birth-Time Enrollment Program:</b> Since 65% enrollments are babies, establish "
    "partnerships with hospitals and maternity centers for immediate newborn enrollment.",
    normal_style
))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>MEDIUM PRIORITY:</b>", normal_style))
elements.append(Paragraph(
    "3. <b>Expand Biometric Update Centers:</b> With 64M biometric updates vs 48M demographic "
    "updates, increase biometric service capacity in high-demand states.<br/><br/>"
    "4. <b>Children's Biometric Update Reminders:</b> Implement automated reminders at ages "
    "5, 10, and 15 when children's biometrics change significantly.",
    normal_style
))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>OPERATIONAL INSIGHTS:</b>", normal_style))
elements.append(Paragraph(
    "5. <b>Resource Reallocation:</b> With only 3.1% adult enrollments, shift focus from new "
    "adult registrations to improving update service quality.<br/><br/>"
    "6. <b>Best Practice Sharing:</b> Replicate successful strategies from top-performing "
    "districts (Thane, Sitamarhi, Bahraich) to underperforming areas.",
    normal_style
))
elements.append(PageBreak())



print("Adding dashboard screenshots...")

print("Adding dashboard screenshots...")

# ADD DASHBOARD SCREENSHOTS with better sizing
for i in range(1, 7):
    img_path = f'dashboard_part{i}.png'
    if os.path.exists(img_path):
        elements.append(Paragraph(f"Dashboard Visualization - Part {i}", heading_style))
        
        # Get image dimensions to maintain aspect ratio
        from PIL import Image as PILImage
        pil_img = PILImage.open(img_path)
        img_width, img_height = pil_img.size
        
        # Calculate proper scaling
        max_width = 6.5 * inch
        aspect_ratio = img_height / img_width
        new_height = max_width * aspect_ratio
        
        # Limit height to avoid stretching
        if new_height > 5 * inch:
            new_height = 5 * inch
            max_width = new_height / aspect_ratio
        
        img = Image(img_path, width=max_width, height=new_height)
        elements.append(img)
        elements.append(Spacer(1, 0.3*inch))
        
        if i % 2 == 0:  # Page break after every 2 images
            elements.append(PageBreak())

# elements.append(PageBreak())

# PYTHON CODE SECTION
elements.append(Paragraph("Technical Implementation - Python Code", heading_style))

elements.append(Paragraph("<b>Data Merging Script:</b>", normal_style))
code_style = ParagraphStyle(
    'Code',
    parent=styles['Code'],
    fontSize=8,
    leftIndent=20,
    fontName='Courier',
    backgroundColor=colors.HexColor('#f4f4f4'),
    borderPadding=10,
)

merge_code = """
import pandas as pd
import os

# Merge all ENROLLMENT files
enrolment_files = [
    'api_data_aadhar_enrolment_0_500000.csv',
    'api_data_aadhar_enrolment_500000_1000000.csv',
    'api_data_aadhar_enrolment_1000000_1006029.csv'
]
df_enrolment = pd.concat([pd.read_csv(f) for f in enrolment_files])
print(f"Total enrollment records: {len(df_enrolment)}")

# Merge DEMOGRAPHIC files
df_demographic = pd.concat([pd.read_csv(f) for f in demographic_files])
print(f"Total demographic records: {len(df_demographic)}")

# Merge BIOMETRIC files
df_biometric = pd.concat([pd.read_csv(f) for f in biometric_files])
print(f"Total biometric records: {len(df_biometric)}")
"""

elements.append(Paragraph(f"<font face='Courier' size='8'>{merge_code.replace('<', '&lt;').replace('>', '&gt;')}</font>", normal_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>Statistical Analysis Script:</b>", normal_style))

analysis_code = """
# TOP STATES ANALYSIS
state_enrol = df_enrol.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
state_enrol['total'] = state_enrol.sum(axis=1)
top_states = state_enrol.sort_values('total', ascending=False).head(10)

# AGE DISTRIBUTION
age_totals = {
    'Babies (0-5)': df_enrol['age_0_5'].sum(),
    'Children (5-17)': df_enrol['age_5_17'].sum(),
    'Adults (18+)': df_enrol['age_18_greater'].sum()
}

# MONTHLY TRENDS
df_enrol['date'] = pd.to_datetime(df_enrol['date'], format='%d-%m-%Y')
df_enrol['month'] = df_enrol['date'].dt.to_period('M')
monthly = df_enrol.groupby('month')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()

# UPDATE COMPARISON
demo_total = df_demo[['demo_age_5_17', 'demo_age_17_']].sum().sum()
bio_total = df_bio[['bio_age_5_17', 'bio_age_17_']].sum().sum()
print(f"Demographic Updates: {demo_total:,}")
print(f"Biometric Updates: {bio_total:,}")
"""

elements.append(Paragraph(f"<font face='Courier' size='8'>{analysis_code.replace('<', '&lt;').replace('>', '&gt;')}</font>", normal_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>Dashboard Technology Stack:</b>", normal_style))
elements.append(Paragraph(
    "• <b>Frontend:</b> React.js with Recharts for interactive visualizations<br/>"
    "• <b>Data Processing:</b> Python (Pandas, NumPy)<br/>"
    "• <b>CSV Parsing:</b> PapaParse library<br/>"
    "• <b>Charts:</b> Bar charts, Pie charts, Line graphs, Stacked charts<br/>"
    "• <b>Styling:</b> CSS3 with gradient backgrounds and responsive design",
    normal_style
))
elements.append(PageBreak())

# CONCLUSION
elements.append(Paragraph("Conclusion", heading_style))
elements.append(Paragraph(
    "Our comprehensive analysis of 4.5+ million Aadhaar records reveals critical insights for UIDAI's "
    "strategic planning. The dominance of baby enrollments (65.3%) presents an opportunity for birth-time "
    "registration programs. The September enrollment spike demonstrates the effectiveness of targeted campaigns. "
    "The higher frequency of biometric updates (64M vs 48M demographic) indicates the need for expanded "
    "biometric service infrastructure.",
    normal_style
))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph(
    "By implementing our recommendations - leveraging seasonal trends, partnering with healthcare facilities "
    "for newborn enrollment, expanding biometric update centers, and reallocating resources from adult enrollment "
    "to service quality - UIDAI can significantly improve coverage, efficiency, and citizen satisfaction.",
    normal_style
))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph(
    "This analysis demonstrates the power of data-driven decision making in large-scale government programs. "
    "The patterns we identified can guide policy decisions, resource allocation, and operational improvements "
    "for India's largest biometric identification system.",
    normal_style
))
elements.append(Spacer(1, 0.3*inch))

elements.append(Paragraph("Thank you for considering our submission.", normal_style))
elements.append(Spacer(1, 0.2*inch))
elements.append(Paragraph("<b>Team UIDAI_4568</b>", normal_style))
elements.append(Paragraph("Ashish - goyalashish2003@gmail.com", normal_style))

print("Building PDF...")

# Build PDF
doc.build(elements)
print(f"✅ PDF generated successfully: {pdf_filename}")