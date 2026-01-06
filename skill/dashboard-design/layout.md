# Dashboard Layout Rules

## Grid System & Responsive Behavior

```javascript
// Responsive Grid Sizes
const gridLayout = {
  desktop: { columns: 12, gap: 24, breakpoint: 1024 },
  tablet: { columns: 6, gap: 16, breakpoint: 768 },
  mobile: { columns: 1, gap: 12, breakpoint: 0 },
};

// Component Sizing
const componentSizes = {
  kpiCard: { width: 2, height: 1 },      // 2 cols, 1 row
  smallChart: { width: 3, height: 2 },   // 1/4 width
  mediumChart: { width: 6, height: 3 },  // 1/2 width
  largeChart: { width: 12, height: 4 },  // Full width
  detailTable: { width: 12, height: 5 }, // Full width + scrollable
};
```

---

## Mobile-first Dashboard Patterns

### Layout Transformation

```
Desktop (12 cols)           Mobile (1 col)
┌────┬────┬────┬────┐      ┌────────────┐
│KPI │KPI │KPI │KPI │  →   │    KPI 1   │
├────┴────┴────┴────┤      ├────────────┤
│   Main Chart      │      │    KPI 2   │
├─────────┬─────────┤      ├────────────┤
│ Chart A │ Chart B │      │    KPI 3   │
└─────────┴─────────┘      ├────────────┤
                           │ Main Chart │
                           ├────────────┤
                           │  Chart A   │
                           └────────────┘
```

### Mobile-specific Rules

| Aspect      | Desktop        | Mobile                         |
| ----------- | -------------- | ------------------------------ |
| Columns     | 12             | 1                              |
| KPI cards   | Horizontal row | Vertical stack                 |
| Charts      | Side-by-side   | Full-width stacked             |
| Data tables | Full table     | Card view or horizontal scroll |
| Filters     | Top bar        | Collapsible drawer             |

### Touch Interactions

```javascript
const mobileInteractions = {
  onChartClick: handleFilter,  // Tap instead of hover
  enablePinchZoom: true,       // Pinch-to-zoom for maps
  onPullRefresh: refetchData,  // Pull-to-refresh
  onSwipeLeft: nextChart,      // Swipe gestures
  onSwipeRight: prevChart,
};
```

### Mobile Performance

- Lazy load below-fold content
- Reduce data points (desktop: 500 → mobile: 100)
- Disable animations if `prefers-reduced-motion`
- Consider offline-first with Service Workers

---

## Content Hierarchy Order

```
1. KPI Cards (Top) - Single metric, big number
   └─ Target: Achievement, comparison to goal

2. Primary Chart (Main insight area)
   └─ Largest, most important visualization

3. Secondary Charts (Supporting insights)
   └─ Breakdown by dimension, correlation

4. Detail Table (Drill-down)
   └─ Raw data, sortable, filterable

5. Annotations & Context
   └─ Notes, forecasts, thresholds
```

---

## KPI Card Anatomy

Each KPI card must contain the following components:

```
┌─────────────────────────────────────┐
│  📊 Revenue                    ⓘ   │  ← Metric name + tooltip
│                                     │
│     $1,234,567                      │  ← Primary value (LARGEST)
│                                     │
│  ↑ 12.5% vs last month              │  ← Trend indicator
│  ▁▂▃▅▆▇█▆▅▃▂▁                      │  ← Sparkline (optional)
│                                     │
│  Jan 1 - Jan 31, 2025               │  ← Date period
└─────────────────────────────────────┘
```

### Required Elements

| #   | Element         | Description                            | Font Size         |
| --- | --------------- | -------------------------------------- | ----------------- |
| 1   | Metric name     | Metric name + tooltip with description | 14-16px           |
| 2   | Primary value   | Main number, most prominent            | **32-48px**       |
| 3   | Trend indicator | ↑↓ with semantic color (green/red)     | 14px              |
| 4   | Comparison      | vs target, vs last period, vs average  | 12-14px           |
| 5   | Sparkline       | Mini chart 7-30 data points (optional) | height: 24-32px   |
| 6   | Date period     | Time range of the metric               | 12px, muted color |

### Placement Rules

- Maximum **4 KPI cards** at top of dashboard
- **Top-left = most important** metric
- Group related KPIs together (Revenue + Cost + Profit)
- Consistent card sizes across dashboard

### Trend Color Coding

```javascript
const trendColors = {
  up_good: "#10B981",    // Green - Revenue up
  up_bad: "#EF4444",     // Red - Cost up
  down_good: "#10B981",  // Green - Churn down
  down_bad: "#EF4444",   // Red - Revenue down
  neutral: "#6B7280",    // Gray - No significant change
};
```

---

## Filter Placement Strategy

### Option A: Top Bar (Default)

```
┌─────────────────────────────────────┐
│  [Date] [Category] [Region] [Reset] │ ← Top bar (sticky)
├─────────────────────────────────────┤
│                                     │
│  MAIN CONTENT                       │
│  (Charts update on filter change)   │
│                                     │
└─────────────────────────────────────┘
```

### Option B: Side Panel (Complex dashboards)

```
┌────────────────┬───────────────────┐
│  FILTER PANEL  │                   │
│  [Date]        │  MAIN CONTENT     │
│  [Category]    │  (Charts)         │
│  [Region]      │                   │
│  [Reset]       │                   │
└────────────────┴───────────────────┘
```
