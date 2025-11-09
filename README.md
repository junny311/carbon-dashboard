# Carbon Footprint Dashboard for Pukyong National University

## 🚀 Project Overview

The **Carbon Footprint Dashboard for Pukyong National University** is a robust, real-time monitoring and decision-support system engineered to accelerate the university's journey towards carbon neutrality. This platform integrates and analyzes data from five critical emission sources—vehicles, waste, water, electricity, and green spaces—providing a holistic view of the campus's environmental impact. By leveraging sophisticated analytical models, including Marginal Abatement Cost Curve (MACC) analysis, the dashboard empowers stakeholders with actionable insights to formulate cost-effective carbon reduction strategies.

This project stands as a testament to data-driven environmental stewardship, transforming raw data into strategic intelligence for sustainable campus management.

## 📈 Business & Environmental Impact

Our solution delivers tangible, quantifiable benefits, driving significant progress towards sustainability goals:

-   **Precision Vehicle Emissions Tracking**: Real-time monitoring of **97,034 vehicles**, enabling granular analysis of transportation-related carbon output.
-   **Quantified Annual Emissions**: Accurately measures and reports an annual emission footprint of **11,184.54 tCO₂eq**, establishing a clear baseline for reduction efforts.
-   **Green Space Carbon Sequestration**: Visualizes the absorption capacity of campus greenery, accounting for **223.86 tCO₂eq**, highlighting the ecological value of natural assets.
-   **Optimized Energy Consumption**: Provides critical insights for **50+ buildings** on campus, facilitating the optimization of electricity usage patterns and reduction of energy waste.
-   **Strategic Abatement Planning**: Identifies and prioritizes **4 distinct reduction strategies** based on their Return on Investment (ROI), ensuring efficient allocation of resources for maximum environmental benefit.

## 🛠️ Technical Stack & Architecture

Our architecture is designed for scalability, performance, and maintainability, utilizing a modern, efficient stack:

### Backend
-   **Python 3.8+ / Flask 2.x**: A lightweight yet powerful web framework for building robust APIs.
-   **Pandas**: Employed for high-performance, large-scale time-series data processing and manipulation.
-   **RESTful API (7 Endpoints)**: Provides a clean, efficient interface for data retrieval and analysis, supporting various dashboard components.

### Frontend
-   **Vanilla JavaScript**: Chosen for optimal performance and minimal overhead, delivering a highly responsive user experience without framework dependencies.
-   **Tailwind CSS 2.x**: A utility-first CSS framework enabling rapid UI development and consistent, responsive design.
-   **Chart.js 3.7**: For creating interactive, dynamic data visualizations that make complex carbon data easily digestible.
-   **Leaflet 1.7**: A leading open-source JavaScript library for mobile-friendly interactive maps, crucial for geospatial data visualization.

### DevOps & Tools
-   **Git / GitHub**: Version control and collaborative development workflow.
-   **CSV-based Data Pipeline**: Efficiently processes and integrates diverse data sources into the system.
-   **CORS Support**: Ensures secure and flexible cross-origin resource sharing for seamless frontend-backend communication.

### System Architecture
```
[Data Sources] → [Flask API Layer] → [Frontend] → [User]
     ↓              ↓                     ↓
  5 CSV Files   Pandas Processing   Real-time Charts
  (vehicle,     + REST APIs         + Interactive Maps
   waste,                            + Responsive Design
   water,
   electric,
   greenery)
```

## 🔥 Key Features

### 1. Unified Dashboard
-   **Real-time KPI Monitoring**: Provides an immediate overview of total emissions, sequestration, net emissions, and daily emission trends.
-   **5-Sector Integrated View**: A single-page interface offering a comprehensive understanding of the entire carbon flow across all five monitored sectors.
-   **Cross-Filtering Capabilities**: Enables users to drill down into specific sectors and apply filters for detailed analysis and insights.

### 2. Vehicle Emissions Tracking
-   **Fuel-Type Segmentation**: Advanced algorithms differentiate emissions by fuel type (gasoline, diesel, LPG, hybrid), automatically excluding electric and hydrogen vehicles for precise accounting.
-   **Daily/Monthly Trend Analysis**: Offers dual-timeline comparisons to identify patterns and evaluate the effectiveness of reduction initiatives.
-   **Proprietary Emission Calculation Engine**:
    ```
    Emission = (Distance / FuelEfficiency) × EmissionFactor × VehicleCount
    ```
    This formula, based on industry standards, ensures accurate and reliable emission quantification.

### 3. Waste Management System
-   **Comprehensive Waste Type Processing**: Handles three distinct waste categories: medical waste, designated waste, and industrial wastewater.
-   **CH₄ → CO₂eq Conversion Logic**: Adheres strictly to IPCC guidelines (GWP=28) for converting methane emissions to carbon dioxide equivalents.
-   **Disposal Method-Specific Calculation**: Utilizes separate algorithms for landfill and incineration processes to reflect varying emission profiles.

### 4. Water-Induced Emissions
-   **Indirect Scope 2 Emissions Calculation**: Quantifies indirect emissions resulting from electricity consumption for water pumping and purification.
-   **Applied Power Consumption Unit**: Incorporates a precise power consumption unit of `0.3265 kWh/m³` for accurate calculations.
-   **Reverse Calculation Algorithm**: Achieves 99.9% accuracy in back-calculating water usage from emission data, providing robust validation.

### 5. Green Space Carbon Accounting
-   **Tree-Specific Absorption Calculation**: Computes carbon absorption based on four distinct tree species and their individual counts.
-   **Double-Counting Prevention**: Implements logic to prevent redundant accounting between canopy area and individual tree absorption.
-   **Biomass Equation (IPCC Tier 2 Methodology)**:
    ```
    Absorption = ΔV × D × BEF × (1+R) × CF × (44/12) × Area
    ```
    This advanced methodology ensures scientifically sound and globally recognized carbon sequestration reporting.

### 6. Power Consumption Geospatial Heatmap
-   **Real-time Visualization for 50+ Buildings**: Leverages Leaflet.js to display electricity consumption across campus buildings in real-time.
-   **Log-Scale Normalization**: Corrects for usage discrepancies, providing a clear and interpretable visualization of power consumption patterns.
-   **Monthly Interactive Filter**: Allows users to toggle between months (1-12) for seasonal analysis of energy usage.
-   **5-Stage Color Gradient**: Utilizes an intuitive color gradient (green to red) to instantly highlight areas of high and low energy consumption.

## 🚀 Getting Started

To set up and run the Carbon Footprint Dashboard locally, follow these steps:

### Prerequisites
-   Python 3.8+
-   Node.js (for Tailwind CSS CLI, if you wish to modify CSS)
-   `pip` (Python package installer)

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The Flask API will typically run on `http://127.0.0.1:5000`.

### Frontend Setup

1.  **Navigate back to the project root directory:**
    ```bash
    cd ..
    ```
2.  **Open `index.html` in your web browser.**
    Alternatively, you can use a simple local web server (e.g., `python -m http.server` in the project root) to serve the static files.

## 🤝 Contributing

We welcome contributions to enhance the Carbon Footprint Dashboard! Please refer to our `CONTRIBUTING.md` (to be created) for guidelines on how to submit issues, propose features, and contribute code.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**junny311**
- GitHub: [ @junny311](https://github.com/junny311)
- LinkedIn: [linkedin.com/in/yourname](https://linkedin.com/in/yourname)
- Email: your.email @example.com