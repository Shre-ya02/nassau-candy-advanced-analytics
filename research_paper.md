# Internship Project Report: Product Profitability & Margin Optimization
**Organization**: Nassau Candy Distributor  
**Project Title**: Product Line Profitability & Margin Performance Analysis  
**Student Name**: Shreya Halder  
**Internship Period**: 20/1/2026 to 20/3/2026 

---

## Executive Summary
This report details the analysis of Nassau Candy Distributor’s product profitability, focusing on identifying high-margin drivers and operational inefficiencies. Over the course of this internship project, I processed over 10,000 transaction records to build a strategic decision-making dashboard. Key findings highlight that 80% of organization profit is concentrated in top-tier products, while regional logistical shifts significantly impact the bottom line.

## 1. Introduction & Business Context
For high-volume distributors like Nassau Candy, sales revenue can often mask underlying margin risks. This project was initiated to move the organization from a "Volume-First" approach to a "Margin-First" strategy. The goal was to provide transparent visibility into which products, regions, and customers truly drive the company’s financial health.

## 2. Problem Statement
The organization previously lacked granular visibility into:
*   **True Profitability**: Which products remain profitable after manufacturing and shipping costs.
*   **Geographic Variance**: How logistical distances from factories (e.g., Arizona vs. Georgia) affect regional margins.
*   **Risk Exposure**: Identifying "low-margin traps" where high sales volume does not translate to profit.

## 3. Project Objectives
1.  **Metric Standardization**: Calculate Gross Margin (%), Profit per Unit, and Revenue Contribution for the entire portfolio.
2.  **Operational Intelligence**: Map product lines to manufacturing facilities to measure factory output efficiency.
3.  **Strategic Visualization**: Develop an interactive Streamlit dashboard for real-time performance monitoring.

## 4. Methodology & Tools
*   **Data Source**: Nassau Candy Distributor Transaction Dataset (10,194 records).
*   **Processing**: Python (Pandas) for data cleaning, metric calculation, and factory-to-product correlation.
*   **Analytics Framework**: 
    *   **Pareto Analysis (80/20)** for profit concentration.
    *   **Choropleth Heatmaps** for geographic intelligence.
    *   **Scatter Diagnostics** for cost vs. sales risk assessment.
*   **Visual Interface**: Streamlit & Plotly (for interactive industry-grade reporting).

*   **Visual Interface**: Streamlit & Plotly (for interactive industry-grade reporting).

## 5. Metric Standardization & Methodology
To ensure financial accuracy, the following standardized formulas were implemented across the dataset:
-   **Gross Margin (%)**: $\frac{\text{Sales} - \text{Cost}}{\text{Sales}} \times 100$
-   **Profit per Unit**: $\frac{\text{Gross Profit}}{\text{Units Sold}}$
-   **Revenue Contribution**: $\frac{\text{Product Sales}}{\text{Total Organization Sales}}$

> [!NOTE]
> The average global margin for the analyzed period is **66.51%**, which serves as the benchmark for identifying "underperforming" lines.

## 6. Key Business Insights

### 6.1 Geographic & Logistical Performance
*   **The Logistical Compression**: Profitability varies significantly by region. Products shipped to the Pacific region from eastern factories (like Georgia-based Wicked Choccy’s) show lower net margins due to increased logistical friction.
*   **Regional Strength**: The Interior and Gulf regions represent the most stable margin profiles.

### 6.2 Product Performance Leaderboard
The analysis identified the "Crown Jewels" of the Nassau Candy portfolio—products that consistently deliver over 65% margin:

| Product Name | Gross Profit ($) | Gross Margin (%) |
| :--- | :--- | :--- |
| Wonka Bar - Nutty Crunch Surprise | $16,819.95 | **71.35%** |
| Wonka Bar -Scrumdiddlyumptious | $19,357.50 | **69.44%** |
| Wonka Bar - Fudge Mallows | $16,593.60 | 66.67% |
| Wonka Bar - Triple Dazzle Caramel | $18,610.20 | 65.33% |
| Wonka Bar - Milk Chocolate | $17,443.37 | 64.92% |

### 6.3 Factory Diagnostics
*   **Factory Benchmarks**: Facilities like 'Lot's O' Nuts' (AZ) and 'Sugar Shack' (MN/ND) demonstrate the highest manufacturing efficiency ratios.
*   **Risk Area**: The Georgia facility ('Wicked Choccy's') shows higher average costs, suggesting potential for sourcing optimization or process automation.

### 6.4 Customer & Selection Strategy
*   **Customer Value Tiers**: We identified a core group of high-contribution customers.
*   **Market Risk**: Several high-volume accounts currently over-index on "Other" low-margin lines, diluting the overall organization margin.

## 7. Strategic Recommendations
1.  **Implement Regional Pricing**: Introduce shipping-adjusted pricing tiers to protect margins in distant regions.
2.  **Product Portfolio Rationalization**: Repave or discontinue the bottom 10% of products that fall into the "High Cost / Low Sales" quadrant.
3.  **Incentive Realignment**: Shift sales team focus toward high-margin "Sugar-based" and "Chocolate" lines identified in the Pareto analysis.
4.  **Operational Best Practices**: Scale the cost-efficient manufacturing processes used in Arizona and Minnesota to other underperforming facilities.

## 8. Conclusion & Learning Outcomes
This project demonstrates that data-driven transparency is the first step toward profitability. By transitioning to a "Margin-First" culture, Nassau Candy can protect its most profitable assets while surgically addressing operational leaks. This internship provided deep hands-on experience in financial data modeling, operational logistics, and stakeholder-level reporting.

---
**Dashboard Link**: [Streamlit Analytics Dashboard](https://shreya-live-dashboard.streamlit.app/)
*(Please ensure the latest `requirements.txt` is pushed for the live link to be active)*
