# Chart Type Selection Guide

> **Note:** Quick Chart Selection table is in `SKILL.md` or `dashboard-design.md` (always loaded). This file contains detailed selection matrix.

## Decision Matrix: Metric × Intent

Based on **metric type** + **question being asked**, select chart type:

---

## A. COMPOSITION (Percentage, breakdown)

| Question               | Chart Type         | When to Use               | Stack Limit  |
| ---------------------- | ------------------ | ------------------------- | ------------ |
| "% of total?"          | Pie/Donut          | ≤ 5 segments              | Max 5        |
| "% by category?"       | Stacked Bar (100%) | ≤ 8 categories            | Max 8        |
| "% breakdown + trend?" | Stacked Area       | Time series, 3-5 segments | Max 5        |
| "Hierarchical %"       | Treemap/Sunburst   | Nested categories         | Max 3 levels |

**⚠️ Avoid:** Pie charts > 5 segments, 3D charts

```javascript
<CompositionChart
  data={salesByRegion}
  dimensions={["region"]}
  metric="revenue"
  type="stacked_bar_100"
/>
```

---

## B. COMPARISON (Compare between groups)

| Question              | Chart Type         | When                        | Performance |
| --------------------- | ------------------ | --------------------------- | ----------- |
| "Value ranking?"      | Bar Chart (sorted) | ≤ 15 items                  | O(n log n)  |
| "Grouped comparison?" | Grouped Bar        | 2-5 groups, ≤ 10 categories | O(n²)       |
| "Many categories?"    | Dot Plot           | > 10 categories, need space | O(n)        |
| "2D comparison?"      | Scatter Plot       | 2 numeric + 1 categorical   | O(n)        |
| "Relationship?"       | Bubble Chart       | 3 metrics + 1 categorical   | O(n)        |

```javascript
<ComparisonChart
  data={salesByRegionByProduct}
  dimensions={["region", "product"]}
  metric="revenue"
  type="grouped_bar"
  limit={15}
/>
```

---

## C. TRENDS (Over time)

| Question             | Chart Type             | When                   | Best For             |
| -------------------- | ---------------------- | ---------------------- | -------------------- |
| "Trend direction?"   | Line Chart             | 5+ time periods        | Smooth trends        |
| "Cumulative growth?" | Area Chart             | Starting from 0        | Cumulative view      |
| "Month-to-month?"    | Column Chart           | Distinct periods       | Period comparison    |
| "Multiple trends?"   | Multi-line             | 3-5 metrics over time  | Correlation analysis |
| "Forecast?"          | Line + Confidence Band | Historical + Predicted | Future planning      |

```javascript
<TrendChart
  data={revenueOverTime}
  dimensions={['date']}
  metrics=['revenue', 'forecast']
  type='line_with_area'
  interval='day'
/>
```

---

## D. DISTRIBUTION (Data distribution)

| Question         | Chart Type       | When                       | Use Case              |
| ---------------- | ---------------- | -------------------------- | --------------------- |
| "Data spread?"   | Histogram        | Numeric data, 1000+ points | Revenue distribution  |
| "Quartile view?" | Box Plot         | Statistical summary        | Compare spreads       |
| "Density curve?" | Violin Plot      | Compare distributions      | Complex distributions |
| "Outliers?"      | Strip Plot + Box | Identify anomalies         | QA/Fraud detection    |

```javascript
<DistributionChart
  data={customerOrders}
  metric="order_value"
  type="histogram_with_box_plot"
  bins={50}
/>
```

---

## E. CORRELATION & RELATIONSHIP

| Question               | Chart Type        | When              | 2D/3D |
| ---------------------- | ----------------- | ----------------- | ----- |
| "X vs Y relationship?" | Scatter Plot      | 2 numeric metrics | 2D    |
| "3 metrics + size?"    | Bubble Chart      | 3 metrics         | 2D    |
| "Matrix correlation?"  | Heatmap           | M × N dimensions  | 2D    |
| "Network graph?"       | Node-Link Diagram | Connections       | 2D/3D |

```javascript
<CorrelationChart
  data={customerMetrics}
  xAxis="customer_lifetime_value"
  yAxis="monthly_spending"
  sizeAxis="engagement_score"
  type="bubble_chart"
/>
```

---

## F. GEOGRAPHICAL (Location-based)

| Question                | Chart Type     | When                      | Interactivity        |
| ----------------------- | -------------- | ------------------------- | -------------------- |
| "Regional performance?" | Choropleth Map | Regions colored by metric | Click → Drill-down   |
| "Location heatmap?"     | Heatmap on Map | Point density             | Tooltip with details |
| "City comparisons?"     | Symbol Map     | Locations marked by size  | Click → Detail       |

```javascript
<GeographicChart
  data={salesByCountry}
  dimension="country"
  metric="revenue"
  type="choropleth"
  onRegionClick={handleRegionFilter}
/>
```

---

## Chart Complexity vs Data Size

```
Complexity
    ↑
    │     Sunburst/Treemap
    │         Heatmap
    │     Box Plot
    │     Violin Plot
    │        ╱─────╱
    │       ╱     ╱  Scatter
    │      ╱     ╱     Bubble
    │ Line──Area  Stacked
    │Bar─Pie─Donut
    └─────────────────→ Data Points
       100    1000   10k   100k+
```

## Quick Selection Rules

| # Data Points | Recommended Charts |
|---------------|-------------------|
| < 100 | Any chart type |
| 100-1000 | Line, Bar, Pie, Area |
| 1000-10k | Heatmap, Histogram |
| 10k+ | Pre-aggregated summaries only |

**Golden Rules:**
- Max **5-6 series** per chart
- Max **15 categories** for bar charts
- Pie charts: **≤ 5 segments** (else use stacked bar)
- Tooltip **adds context** (not just numbers)
