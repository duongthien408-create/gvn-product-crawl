---
name: dashboard-design
description: "Kích hoạt khi user yêu cầu: Thiết kế dashboard, báo cáo, analytics, hoặc cần tư vấn về các loại chart, layout, filter, performance, accessibility phục vụ dashboard, ui thống kê và phân tích."
---

# Dashboard Design Skill

## Execution Process

### Step 1: Analyze Context

Before starting, AI MUST understand the current user context:

- **Source code**: Does user have existing dashboard code? Which framework (React, Vue, etc.)?
- **Data**: Does user provide data schema, API response, or sample data?
- **Existing charts**: Any existing charts? Need to add/modify/replace?
- **Specific issue**: Performance issue? Layout issue? Chart type selection?
- **Special requirements**: Mobile-first? Accessibility? Real-time?

### Step 2: Load Files by Intent

Based on context analysis, load appropriate files:

| Intent     | Keywords                                                    | Load file                       |
| ---------- | ----------------------------------------------------------- | ------------------------------- |
| **BUILD**  | "create dashboard", "build dashboard", "design", "new"      | `fundamentals.md` + `charts.md` |
| **CHART**  | "choose chart", "which chart", "visualize", "chart type"    | `charts.md`                     |
| **LAYOUT** | "KPI card", "layout", "responsive", "mobile", "grid"        | `layout.md`                     |
| **FILTER** | "filter", "cross-filter", "click to filter", "interactivity"| `interactions.md`               |
| **PERF**   | "slow", "optimize", "performance", "cache", "faster"        | `performance.md`                |
| **A11Y**   | "accessibility", "WCAG", "color blind", "screen reader"     | `accessibility.md`              |

**Mandatory files (ALWAYS LOAD):**
- `SKILL.md` (this file) - Color scheme + Checklist + Core rules

**Note:** Load multiple files if task is complex (e.g., BUILD needs fundamentals + charts + layout).

### Step 3: Execute Task

- Apply **Color Scheme** and **Core Rules** from this file
- Follow guidelines from loaded files
- **DO NOT skip any steps**

### Step 4: Verify Checklist

Before completion, **MUST verify** the **Final Checklist** at the end of this file.
Never skip checklist regardless of task size.

---

## Color Scheme (Always Apply)

```javascript
const colorScheme = {
  // Semantic colors
  positive: "#10B981", // Green - Growth, profit, success
  negative: "#EF4444", // Red - Decline, loss, error
  neutral: "#6B7280", // Gray - No change
  warning: "#F59E0B", // Amber - Caution needed
  info: "#3B82F6", // Blue - Information

  // Chart series (max 6)
  series: [
    "#3B82F6", // Blue
    "#10B981", // Green
    "#F59E0B", // Amber
    "#EF4444", // Red
    "#8B5CF6", // Purple
    "#EC4899", // Pink
  ],

  // Trend indicators
  trend: {
    up_good: "#10B981", // Revenue up
    up_bad: "#EF4444", // Cost up
    down_good: "#10B981", // Churn down
    down_bad: "#EF4444", // Revenue down
  },
};
```

---

## Dashboard Architecture (Always Reference)

```
┌─────────────────────────────────────────────────────┐
│                    DASHBOARD                         │
├─────────────────────────────────────────────────────┤
│ [Global Filters] [Date Range] [Search]             │
├──────────────┬──────────────┬──────────────────────│
│   KPI Cards  │  KPI Cards   │   KPI Cards         │
├─────────────────────────────────────────────────────┤
│                   ROW 1: Main Charts                 │
│  [Primary Chart]    [Secondary Chart]   [Tertiary]  │
├─────────────────────────────────────────────────────┤
│                   ROW 2: Drill-down                  │
│           [Detail Table / Heat Map]                  │
├─────────────────────────────────────────────────────┤
│              ROW 3: Supporting Insights              │
│    [Trend]      [Comparison]      [Forecast]        │
└─────────────────────────────────────────────────────┘
```

### Layer Cake Structure

```
┌─────────────────────────────────────────────────────┐
│  LAYER 1: EXECUTIVE SUMMARY (Top)                   │
│  • 3-5 KPI cards with green/red status indicators   │
│  • "5-second test": Know immediately if OK or not   │
├─────────────────────────────────────────────────────┤
│  LAYER 2: DEPARTMENTAL VIEW (Middle)                │
│  • Key charts with interactive filters              │
│  • Trend analysis (line/area charts)                │
├─────────────────────────────────────────────────────┤
│  LAYER 3: DEEP DIVE (Bottom)                        │
│  • Detailed data tables (sortable, searchable)      │
│  • Export options (CSV, PDF)                        │
└─────────────────────────────────────────────────────┘
```

**Audience per layer:**
- **Layer 1:** C-level executives (< 30 seconds)
- **Layer 2:** Department managers (2-5 minutes)
- **Layer 3:** Analysts/Specialists (deep exploration)

---

## Core Rules (Quick Reference)

| Rule                       | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| **Single Truth**           | 1 dashboard answers 1-3 main questions                  |
| **Layer Cake**             | Executive (top) → Department (middle) → Detail (bottom) |
| **Progressive Disclosure** | Overview → Detail → Actions                             |
| **Max 4 KPIs**             | Maximum 4 KPI cards at top                              |
| **Max 5-6 Series**         | Maximum 5-6 series per chart                            |
| **Aggregate Backend**      | Data > 10k rows → aggregate at backend                  |

---

## Data Size Rules (Critical)

| Data Size      | Approach                                            |
| -------------- | --------------------------------------------------- |
| **< 100 rows** | Any chart type                                      |
| **100-1000**   | Aggregation recommended, avoid scatter              |
| **1000-10k**   | Pre-aggregate, use heatmap/histogram                |
| **10k+**       | MUST aggregate backend, max 50-500 points frontend  |

**CRITICAL:** Always aggregate at backend if data > 10k rows. Frontend only filters pre-aggregated data.

---

## Quick Chart Selection

| Intent              | Chart Type                | Limit              |
| ------------------- | ------------------------- | ------------------ |
| **% of total**      | Pie/Donut                 | ≤ 5 segments       |
| **% by category**   | Stacked Bar (100%)        | ≤ 8 categories     |
| **Ranking**         | Bar Chart (sorted)        | ≤ 15 items         |
| **Trend over time** | Line Chart                | 5+ time periods    |
| **Comparison**      | Grouped Bar               | 2-5 groups         |
| **Distribution**    | Histogram / Box Plot      | 1000+ data points  |
| **Correlation**     | Scatter / Bubble          | 2-3 metrics        |
| **Geographic**      | Choropleth Map            | Regions by metric  |

**See `charts.md` for detailed selection matrix.**

---

## Final Checklist

Verify before completing dashboard:

### Layout & Structure

- [ ] Grid 12 cols desktop → 1 col mobile
- [ ] KPI cards on top (max 4)
- [ ] Primary chart largest
- [ ] Filter bar sticky at top
- [ ] Max 5 rows (don't scroll > 2x viewport)

### Data Quality

- [ ] All metrics aggregated (< 500 points frontend)
- [ ] No raw data > 10k rows
- [ ] Date formats consistent (YYYY-MM-DD)
- [ ] Numbers formatted (thousands separator)
- [ ] No null displayed (show "N/A" or "-")

### Chart Selection

- [ ] Chart type matches intent (see charts.md)
- [ ] Max 5-6 series per chart
- [ ] Max 15 categories for bar chart
- [ ] Pie charts ≤ 5 segments
- [ ] Tooltip adds context

### Interactivity

- [ ] Charts respond to global filters
- [ ] Click-to-filter works
- [ ] Reset filters button visible
- [ ] Drill-down breadcrumb if applicable

### Visual Design

- [ ] Colors from semantic palette
- [ ] Contrast ≥ 4.5:1 for text
- [ ] Consistent spacing (gap-4, gap-6, gap-8)
- [ ] Loading states during fetch

### Performance

- [ ] Data loads < 1 second
- [ ] Charts render < 500ms
- [ ] Filter response debounced
- [ ] useMemo for expensive computations

---

## Best Practices Summary

| Aspect            | Do's                              | Don'ts                      |
| ----------------- | --------------------------------- | --------------------------- |
| **Charts**        | Match intent to chart type        | Pie > 5 segments, 3D charts |
| **Data**          | Aggregate to 50-500 points        | Raw data > 10k rows         |
| **Dimensions**    | Filter by 2-3 dimensions          | 10+ simultaneous filters    |
| **Colors**        | Semantic palette (6 max)          | Rainbow gradients           |
| **Layout**        | Responsive, KPI → trends → detail | Fixed-width, cramped        |
| **Interaction**   | Click-to-filter, hover tooltips   | Animations > 300ms          |
| **Performance**   | Memoization, debouncing, caching  | Unoptimized re-renders      |
| **Accessibility** | Contrast, keyboard nav            | Color alone for meaning     |

---

## File Structure

```
.claude/skills/dashboard-design/
├── SKILL.md          # This file (entry + routing + checklist)
├── fundamentals.md   # Architecture + Design Rules + Data Handling
├── charts.md         # Chart Selection Matrix (6 types)
├── layout.md         # Grid + Mobile + KPI Cards
├── interactions.md   # Cross-filtering + Click/Hover
├── performance.md    # Caching + Libraries
└── accessibility.md  # WCAG Guidelines
```
