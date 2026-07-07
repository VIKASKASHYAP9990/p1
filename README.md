# Premium Sales Data Analysis Dashboard

A comprehensive, dual-stack Sales Analytics project featuring a **Python Data Analysis Pipeline** and a **Web-based Interactive Dashboard**. This project explores and visualizes retail sales data (based on the Superstore dataset format) to provide actionable insights into revenue, profitability, category distributions, and regional performance.

---

## 🌟 Features

### 1. Interactive Web Dashboard
An elegant, browser-based dashboard built with vanilla web technologies, featuring:
*   **Modern Aesthetics**: Dark-mode glassmorphism design with responsive grid layout and micro-animations.
*   **Dynamic Visualizations**: Powered by **Chart.js**, showing:
    *   **KPI Summary Cards**: Total Sales, Total Profit, Profit Margin, and Order Count.
    *   **Sales & Profit Trends**: Monthly timeline chart.
    *   **Category Distribution**: Interactive donut chart.
    *   **Regional Performance**: Horizontal bar chart comparing regions.
    *   **Top 10 Products**: Top selling products sorted dynamically.
*   **Interactive Filters**: Filter entire dashboard views dynamically by **Region**, **Category**, and **Year**.

### 2. Python Data Analysis & Visualizations
A robust data analysis script (`dashboard.py`) leveraging standard Python data science libraries to:
*   **Data Processing**: Manage data loading, cleaning, and transformation using **Pandas** and **NumPy**.
*   **Static Graphics**: Generate advanced charts utilizing **Matplotlib** and **Seaborn** (such as discount-vs-profit correlations).
*   **Interactive Plots**: Render dynamic HTML figures using **Plotly**.

---

## 📂 Repository Structure

The project is structured as follows:

```
├── index.html                   # Main web page shell
├── style.css                    # Dark glassmorphism design stylesheet
├── dashboard.js                 # Javascript logic for web data processing & Chart.js rendering
├── data.js                      # Embedded Superstore-style dataset (500+ records)
├── dashboard.py                 # Python script for local data analysis & visualization
├── README.md                    # Project documentation (this file)
├── implementation_plan.md       # Original implementation and component architecture plan
├── discount_vs_profit.png       # Generated chart: correlation between discounts and profit margins
└── superstore_dashboard_static.png # Static dashboard collage image
```

---

## 🚀 How to Run

### Web Dashboard
No external build tools or libraries are required to run the frontend. You can open it in three ways:

1.  **Online (Recommended for Mobile/Other Devices)**:
    Access the live deployed site directly on any device:
    👉 **[https://vikaskashyap9990.github.io/p1/](https://vikaskashyap9990.github.io/p1/)**

2.  **Directly in Browser**: Double-click `index.html` or open it with any web browser.
3.  **Using a Local HTTP Server** (For local development):
    ```bash
    # Run the server on port 8001 (or another port if 8000 is already in use by another project):
    python -m http.server 8001
    ```
    *   **To access on this computer**: Open [http://localhost:8001](http://localhost:8001) in your browser.
    *   **Note on Mobile Access**: Accessing via local IP (e.g., `http://192.168.1.4:8001`) can sometimes fail if your computer's firewall blocks incoming connections or your Wi-Fi router has access point isolation enabled. If this occurs, use the online GitHub Pages link above.

### Python Data Analysis
To run the analytical script and generate plots:

1.  **Install dependencies**:
    ```bash
    pip install pandas numpy matplotlib seaborn plotly
    ```
2.  **Run the script**:
    ```bash
    python dashboard.py
    ```
    This will process the data, output command-line metrics, and generate/display plots.

---

## 📊 Sample Visualizations
*   **Web Design**: Modern dark theme with CSS styling.
*   **Discount vs Profitability Analysis**: Visualized in `discount_vs_profit.png` showing how excessive discounts negatively impact margins.
*   **Static Overview**: Collage of static metrics in `superstore_dashboard_static.png`.
