# Dashboard Interactions

## Cross-Filtering Architecture

### Filter State Management

```javascript
// RECOMMENDED: Zustand (lightweight) or Redux Toolkit
import create from "zustand";

const useDashboardFilters = create((set) => ({
  // Core filters
  dateRange: { start: null, end: null },
  selectedDimensions: {}, // {dimensionName: [values]}
  searchQuery: "",

  // Actions
  setDateRange: (range) => set({ dateRange: range }),
  setDimension: (name, values) =>
    set((state) => ({
      selectedDimensions: {
        ...state.selectedDimensions,
        [name]: values,
      },
    })),
  resetFilters: () =>
    set({
      dateRange: { start: null, end: null },
      selectedDimensions: {},
      searchQuery: "",
    }),
}));
```

---

## Cross-Filtering Patterns

### Pattern A: Click-to-Filter (Recommended)

```
User clicks element in Chart A
  ↓
Update global filter state
  ↓
Query engine filters aggregated data
  ↓
All charts update automatically
```

**Advantages:**
- Intuitive, easy to understand
- No need to precompute all combinations
- Flexible for arbitrary dimensions

### Pattern B: Multi-Select Filters

```
User selects multiple values from filter panel
  ↓
Boolean logic (AND/OR) applied
  ↓
Charts aggregate based on selection
```

### Pattern C: Range Sliders

```
User drags slider
  ↓
Continuous update (debounced)
  ↓
Charts update in real-time
```

---

## Data Flow Architecture

```
Raw Data (API)
    ↓
Data Aggregation Layer (Backend)
    ↓ [Cached aggregations per dimension]
    ↓
Filter Application (Frontend)
    ↓
Selector/Memoization (React)
    ↓
Chart Components (Recharts/Visx)
    ↓
Visual Output
```

**CRITICAL:** Always aggregate at backend if data > 10k rows.

---

## Click-to-Filter Implementation

```javascript
// User clicks bar in chart → Filter applied
const handleChartClick = (data, index) => {
  const filters = useDashboardFilters();
  filters.setDimension('category', [data.category]);
};

// In Recharts:
<BarChart onClick={(state) => {
  if (state.activeTooltipIndex) {
    const clickedData = chartData[state.activeTooltipIndex];
    handleChartClick(clickedData);
  }
}}>
```

---

## Tooltip Customization

```javascript
// Rich tooltips with additional context
<Tooltip
  content={({ active, payload }) => {
    if (!active || !payload?.length) return null;

    const data = payload[0].payload;
    return (
      <div className="bg-white p-3 rounded shadow-lg border">
        <p className="font-semibold">{data.date}</p>
        <p className="text-blue-600">
          Revenue: ${data.revenue.toLocaleString()}
        </p>
        <p className="text-gray-600">vs Last Year: {data.yoy_change}%</p>
      </div>
    );
  }}
/>
```

---

## Hover Highlight

```javascript
// Highlight related data when hovering
const [hoveredCategory, setHoveredCategory] = useState(null);

<BarChart
  data={data}
  onMouseMove={(state) => {
    if (state.activeTooltipIndex !== undefined) {
      setHoveredCategory(data[state.activeTooltipIndex].category);
    }
  }}
  onMouseLeave={() => setHoveredCategory(null)}
>
  <Bar
    dataKey="revenue"
    fill={(entry) =>
      hoveredCategory === entry.category ? "#3B82F6" : "#A3E9D7"
    }
  />
</BarChart>
```

---

## Interaction Best Practices

| Do's | Don'ts |
|------|--------|
| Click-to-filter | 3D charts |
| Hover tooltips with context | Animations > 300ms |
| Clear reset button | Auto-play animations |
| Breadcrumb for drill-down | Hidden interactions |
| Debounced filter updates | Instant refresh on every keystroke |
