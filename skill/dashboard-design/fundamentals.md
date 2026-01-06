# Dashboard Fundamentals

> **Note:** Core architecture, Layer Cake structure, and Data Size Rules are in `SKILL.md` or `dashboard-design.md` (always loaded).

---

## Multi-Dimensional Data Handling

### Dimension vs Metric Classification

```javascript
// DIMENSIONS: Categorical attributes (breakdowns)
const dimensions = {
  time: ["date", "week", "month", "quarter", "year"],
  geography: ["country", "state", "city", "region"],
  product: ["category", "product_name", "brand"],
  customer: ["segment", "tier", "cohort"],
  channel: ["source", "campaign", "device"],
};

// METRICS: Numeric values (aggregated)
const metrics = {
  count: ["impressions", "users", "orders"],
  revenue: ["total_revenue", "avg_order_value"],
  rate: ["conversion_rate", "bounce_rate", "ctr"],
  efficiency: ["cost_per_acquisition", "roi"],
};
```

### Aggregation Levels

```
FACT TABLE (Raw Data)
  ↓ Aggregate by: [Time, Geography, Product]
  ↓
AGGREGATE TABLES (Pre-computed)
  - revenue_by_date_product
  - revenue_by_country_date
  ↓ Apply Filters
  ↓
DASHBOARD QUERIES (Frontend)
  - Get revenue_by_date filtered by country='US'
  ↓
VISUALIZATION
```

### Drill-Down Navigation

```javascript
// Breadcrumb Navigation
[All Products] > [Electronics] > [Smartphones] > [iPhone 15]

// Associated Drill-Down:
├─ Level 0: Total Revenue = $1.2M
├─ Level 1: Revenue by Category (5 items)
│   └─ Click Electronics →
├─ Level 2: Revenue by Subcategory (12 items)
│   └─ Click Smartphones →
├─ Level 3: Revenue by Product (50 items)
│   └─ Click iPhone 15 →
└─ Level 4: Detail Table (Orders with details)
```

