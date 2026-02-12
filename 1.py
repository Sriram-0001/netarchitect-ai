import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time
import os
from dotenv import load_dotenv

from models.llm_handler import LLMHandler
from agents.system_pipeline import run_full_pipeline

# ============================================================
# INITIALIZATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"

llm = LLMHandler(API_KEY, MODEL)

st.set_page_config(layout="wide")

# ============================================================
# HEADER
# ============================================================

st.title("🚀 NetArchitect AI")
st.caption("Enterprise Infrastructure Intelligence Platform")

st.divider()

# ============================================================
# INPUT SECTION
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    employees = st.slider("Employees", 10, 1000, 120)
    office_size = st.slider("Office Size (sqft)", 1000, 50000, 6000)

with col2:
    growth = st.slider("Growth Rate (%)", 0, 50, 10)
    security = st.selectbox("Security Level", ["Low", "Medium", "High"])

with col3:
    deployment = st.selectbox("Deployment Model", ["Cloud", "On-Prem", "Hybrid"])
    budget = st.slider("Budget (₹)", 100000, 5000000, 700000)

st.divider()

# ============================================================
# RUN PIPELINE
# ============================================================

if st.button("Run Optimization"):

    user_input = {
        "num_employees": employees,
        "office_size_sqft": office_size,
        "security_level": security,
        "growth_rate_percent": growth,
        "cloud_preference": deployment,
        "budget": budget,
    }

    result = run_full_pipeline(user_input, llm)

    # ========================================================
    # TOP METRICS SECTION
    # ========================================================

    st.subheader("Executive Summary")

    m1, m2, m3 = st.columns(3)

    m1.metric("Cisco Cost", f"₹ {result['cost']['cisco_total_cost']:,}")
    m2.metric("TP-Link Cost", f"₹ {result['cost']['tplink_total_cost']:,}")
    m3.metric(
        "Optimization Needed",
        result["optimization_decision"]["optimization_needed"],
    )

    st.divider()

    # ========================================================
    # MAIN TABS
    # ========================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Vendor Comparison",
            "Deep Analysis",
            "Deployment Plan",
            "AI Insights",
        ]
    )




    # ========================================================
    # TAB 1 — VENDOR COMPARISON
    # ========================================================

    with tab1:

        st.subheader("Vendor Comparison Dashboard")

        vendors = ["Cisco", "TP-Link"]

        # ----------------------------------------------------
        # Compact Static Charts (Side-by-Side)
        # ----------------------------------------------------

        colA, colB, colC = st.columns(3)

        # Cost Chart
        with colA:
            fig_cost, ax_cost = plt.subplots(figsize=(3.5, 2.2), dpi=90)
            ax_cost.bar(vendors, [
                result["cost"]["cisco_total_cost"],
                result["cost"]["tplink_total_cost"]
            ])
            ax_cost.set_title("Cost", fontsize=9)
            ax_cost.tick_params(labelsize=8)
            plt.tight_layout()
            st.pyplot(fig_cost, use_container_width=False)

        # Performance Chart
        with colB:
            fig_perf, ax_perf = plt.subplots(figsize=(3.5, 2.2), dpi=90)
            ax_perf.bar(vendors, [
                result["performance"]["cisco"],
                result["performance"]["tplink"]
            ])
            ax_perf.set_title("Performance", fontsize=9)
            ax_perf.tick_params(labelsize=8)
            plt.tight_layout()
            st.pyplot(fig_perf, use_container_width=False)

        # Risk Chart
        with colC:
            fig_risk, ax_risk = plt.subplots(figsize=(3.5, 2.2), dpi=90)
            ax_risk.bar(vendors, [
                result["security"]["cisco"],
                result["security"]["tplink"]
            ])
            ax_risk.set_title("Risk", fontsize=9)
            ax_risk.tick_params(labelsize=8)
            plt.tight_layout()
            st.pyplot(fig_risk, use_container_width=False)

        st.divider()

        # ----------------------------------------------------
        # INTERACTIVE SLIDER VIEW (Carousel)
        # ----------------------------------------------------

        st.subheader("Interactive Comparison View")

        if "slide_index" not in st.session_state:
            st.session_state.slide_index = 0

        graph_types = ["Cost", "Performance", "Risk"]

        left, mid, right = st.columns([1, 6, 1])

        with left:
            if st.button("⬅", key="left_slide"):
                st.session_state.slide_index = (
                    st.session_state.slide_index - 1
                ) % len(graph_types)

        with right:
            if st.button("➡", key="right_slide"):
                st.session_state.slide_index = (
                    st.session_state.slide_index + 1
                ) % len(graph_types)

        current_graph = graph_types[st.session_state.slide_index]

        fig_slide, ax_slide = plt.subplots(figsize=(4, 2.5), dpi=90)

        if current_graph == "Cost":
            values = [
                result["cost"]["cisco_total_cost"],
                result["cost"]["tplink_total_cost"]
            ]
            ax_slide.set_ylabel("₹", fontsize=8)

        elif current_graph == "Performance":
            values = [
                result["performance"]["cisco"],
                result["performance"]["tplink"]
            ]
            ax_slide.set_ylabel("Score", fontsize=8)

        else:
            values = [
                result["security"]["cisco"],
                result["security"]["tplink"]
            ]
            ax_slide.set_ylabel("Risk", fontsize=8)

        ax_slide.bar(vendors, values)
        ax_slide.set_title(current_graph, fontsize=9)
        ax_slide.tick_params(labelsize=8)

        plt.tight_layout()
        st.pyplot(fig_slide, use_container_width=False)

    # ========================================================
    # TAB 2 — DEEP ANALYSIS
    # ========================================================

    with tab2:

        st.subheader("Deep Vendor Analysis")

        vendor_choice = st.selectbox(
            "Select Vendor",
            ["Cisco", "TP-Link"]
        )

        key = vendor_choice.lower().replace("-", "").replace(" ", "")

        # ----------------------------------------------------
        # Component Breakdown
        # ----------------------------------------------------

        st.markdown("### Component Cost Breakdown")

        breakdown = result["cost"][f"{key}_breakdown"]

        st.json(breakdown)

        # Pie Chart Distribution
        labels = [item["model"] for item in breakdown.values()]
        values = [item["total"] for item in breakdown.values()]

        fig_pie, ax_pie = plt.subplots(figsize=(3.5, 2.5), dpi=90)
        ax_pie.pie(values, labels=labels, autopct="%1.1f%%")
        ax_pie.set_title("Cost Distribution", fontsize=9)

        plt.tight_layout()
        st.pyplot(fig_pie, use_container_width=False)

        st.divider()

        # ----------------------------------------------------
        # Performance + Risk Metrics
        # ----------------------------------------------------

        colX, colY = st.columns(2)

        colX.metric("Performance Score", result["performance"][key])
        colY.metric("Risk Score", result["security"][key])

    # ========================================================
    # TAB 3 — DEPLOYMENT PLAN
    # ========================================================

    with tab3:

        st.subheader("Deployment Strategy Overview")

        st.json(result["deployment"])

        st.divider()

        st.subheader("Deployment Metrics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Cable Length (m)",
                result["deployment"]["cable_length_meters"]
            )
            st.metric(
                "Labour Hours",
                result["deployment"]["estimated_labour_hours"]
            )
            st.metric(
                "Labour Cost",
                f"₹ {result['deployment']['labour_cost']:,}"
            )

        with col2:
            st.metric(
                "Rack Units",
                result["deployment"]["rack_units_required"]
            )
            st.metric(
                "Power Estimate (kW)",
                result["deployment"]["estimated_power_kw"]
            )
            st.metric(
                "Total Project Cost",
                f"₹ {result['deployment']['total_project_cost_estimate']:,}"
            )

        st.divider()

        st.subheader("Network Architecture Diagram")
        st.image(result["diagram"])

    with tab4:
        st.subheader("Executive AI Insights")

        insights = result["insights"]

        st.markdown("### Executive Summary")
        st.write(insights["executive_summary"])

        st.markdown("### Cost Analysis Insight")
        st.write(insights["cost_analysis_insight"])

        st.markdown("### Performance Insight")
        st.write(insights["performance_insight"])

        st.markdown("### Risk Insight")
        st.write(insights["risk_insight"])

        st.markdown("### Scalability Outlook")
        st.write(insights["scalability_insight"])

        st.markdown("### Deployment Intelligence")
        st.write(insights["deployment_insight"])

        st.markdown("### Final Recommendation")
        st.success(insights["final_recommendation"])

    # ========================================================
    # PDF DOWNLOAD SECTION
    # ========================================================

    st.divider()

    st.subheader("Export Executive Report")

    st.download_button(
        "Download Full Executive Report (PDF)",
        result["pdf"],
        file_name="NetArchitect_Report.pdf"
    )
