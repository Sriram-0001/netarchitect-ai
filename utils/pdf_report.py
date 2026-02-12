import io
import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4


# ==========================================================
# Utility: Convert Matplotlib Figure to ReportLab Image
# ==========================================================

def generate_chart_image(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=150)
    buffer.seek(0)
    plt.close(fig)
    return buffer


# ==========================================================
# MAIN PDF GENERATOR
# ==========================================================

def generate_pdf(infra_package, analysis, deployment, insights, diagram_image):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    section_style = styles["Heading2"]
    normal_style = styles["Normal"]

    # ------------------------------------------------------
    # SAFE EXTRACTION
    # ------------------------------------------------------

    cost_output = analysis.get("cost_analysis", {})
    performance_output = analysis.get("performance_scores", {})
    security_output = analysis.get("security_scores", {})

    cisco_cost = cost_output.get("cisco_total_cost", 0)
    tplink_cost = cost_output.get("tplink_total_cost", 0)

    # ======================================================
    # COVER PAGE
    # ======================================================

    elements.append(Paragraph("NetArchitect AI", title_style))
    elements.append(Spacer(1, 12))
    elements.append(
        Paragraph(
            "Enterprise Infrastructure Intelligence Report",
            styles["Heading3"]
        )
    )
    elements.append(PageBreak())

    # ======================================================
    # EXECUTIVE SUMMARY
    # ======================================================

    elements.append(Paragraph("Executive Summary", section_style))
    elements.append(Spacer(1, 12))

    summary_text = f"""
    Cisco Total Cost: ₹{cisco_cost:,}<br/>
    TP-Link Total Cost: ₹{tplink_cost:,}<br/><br/>

    Cisco Performance Score: {performance_output.get('cisco', 'N/A')}<br/>
    TP-Link Performance Score: {performance_output.get('tplink', 'N/A')}<br/><br/>

    Cisco Risk Score: {security_output.get('cisco', 'N/A')}<br/>
    TP-Link Risk Score: {security_output.get('tplink', 'N/A')}
    """

    elements.append(Paragraph(summary_text, normal_style))
    elements.append(PageBreak())

    # ======================================================
    # VENDOR COMPARISON CHARTS
    # ======================================================

    vendors = ["Cisco", "TP-Link"]

    # Cost Chart
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.bar(vendors, [cisco_cost, tplink_cost])
    ax1.set_title("Cost Comparison")
    cost_chart = generate_chart_image(fig1)

    elements.append(Paragraph("Cost Comparison", section_style))
    elements.append(Spacer(1, 8))
    elements.append(Image(cost_chart, width=4 * inch, height=3 * inch))
    elements.append(Spacer(1, 16))

    # Performance Chart
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.bar(
        vendors,
        [
            performance_output.get("cisco", 0),
            performance_output.get("tplink", 0),
        ],
    )
    ax2.set_title("Performance Comparison")
    perf_chart = generate_chart_image(fig2)

    elements.append(Paragraph("Performance Comparison", section_style))
    elements.append(Spacer(1, 8))
    elements.append(Image(perf_chart, width=4 * inch, height=3 * inch))
    elements.append(Spacer(1, 16))

    # Risk Chart
    fig3, ax3 = plt.subplots(figsize=(4, 3))
    ax3.bar(
        vendors,
        [
            security_output.get("cisco", 0),
            security_output.get("tplink", 0),
        ],
    )
    ax3.set_title("Risk Comparison")
    risk_chart = generate_chart_image(fig3)

    elements.append(Paragraph("Risk Comparison", section_style))
    elements.append(Spacer(1, 8))
    elements.append(Image(risk_chart, width=4 * inch, height=3 * inch))
    elements.append(PageBreak())

    # ======================================================
    # DEPLOYMENT SECTION
    # ======================================================

    elements.append(Paragraph("Deployment Engineering Plan", section_style))
    elements.append(Spacer(1, 12))

    deployment_text = f"""
    Cable Length Required: {deployment.get('cable_length_meters', 0)} meters<br/>
    Estimated Labour Hours: {deployment.get('estimated_labour_hours', 0)} hours<br/>
    Labour Cost: ₹{deployment.get('labour_cost', 0):,}<br/>
    Rack Units Required: {deployment.get('rack_units_required', 0)}<br/>
    Estimated Power Load: {deployment.get('estimated_power_kw', 0)} kW<br/>
    Total Project Cost Estimate: ₹{deployment.get('total_project_cost_estimate', 0):,}
    """

    elements.append(Paragraph(deployment_text, normal_style))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Network Architecture Diagram", section_style))
    elements.append(Spacer(1, 8))
    elements.append(Image(diagram_image, width=5 * inch, height=3 * inch))
    elements.append(PageBreak())

    # ======================================================
    # AI EXECUTIVE INSIGHTS
    # ======================================================

    elements.append(Paragraph("AI Executive Insights", section_style))
    elements.append(Spacer(1, 12))

    insight_sections = [
        ("Executive Summary", "executive_summary"),
        ("Cost Insight", "cost_analysis_insight"),
        ("Performance Insight", "performance_insight"),
        ("Risk Insight", "risk_insight"),
        ("Scalability Outlook", "scalability_insight"),
        ("Deployment Insight", "deployment_insight"),
        ("Final Recommendation", "final_recommendation"),
    ]

    for title, key in insight_sections:
        elements.append(Paragraph(title, styles["Heading3"]))
        elements.append(Spacer(1, 6))
        elements.append(
            Paragraph(insights.get(key, "N/A"), normal_style)
        )
        elements.append(Spacer(1, 14))

    # ======================================================
    # BUILD DOCUMENT
    # ======================================================

    doc.build(elements)
    buffer.seek(0)

    return buffer
