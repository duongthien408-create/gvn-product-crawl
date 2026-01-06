# Dashboard Performance Optimization

## Data Loading Strategy

```javascript
// GOOD: Load pre-aggregated data
const queryAggregated = async () => {
  // Backend returns: 100 rows (monthly summaries)
  const response = await api.get("/metrics/revenue_by_month");
  return response.data; // Light, fast
};

// BAD: Load raw data, aggregate frontend
const queryRaw = async () => {
  // Backend returns: 1M+ rows
  const response = await api.get("/orders");
  // Frontend aggregates (slow, memory-heavy)
  return aggregateData(response.data);
};
```

---

## Caching Strategy

```javascript
// Implement SWR (Stale-While-Revalidate)
import useSWR from "swr";

const useDashboardData = (filters) => {
  const key = JSON.stringify({ endpoint: "/metrics", filters });

  return useSWR(key, fetcher, {
    revalidateOnFocus: false,
    dedupingInterval: 60000, // 1 minute cache
  });
};

// Memoize expensive computations
const selectChartData = useMemo(() => {
  return processData(rawData, filters);
}, [rawData, filters]);
```

---

## Debouncing Filter Updates

```javascript
const handleFilterChange = useCallback(
  debounce((newFilters) => {
    setFilters(newFilters);
    // Triggers data refetch
  }, 500), // Wait 500ms after user stops typing
  []
);
```

---

## React Chart Libraries Comparison

| Library            | Use Case                             | Ease       | Customization | Performance |
| ------------------ | ------------------------------------ | ---------- | ------------- | ----------- |
| **Recharts**       | Standard charts (line, bar, area)    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐      | ⭐⭐⭐⭐    |
| **Victory**        | Complex, animated charts             | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐    | ⭐⭐⭐⭐    |
| **D3.js**          | Highly custom, unique visualizations | ⭐⭐       | ⭐⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐  |
| **Visx**           | Low-level, React-friendly D3         | ⭐⭐⭐     | ⭐⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐  |
| **Plotly.js**      | Interactive, statistical charts      | ⭐⭐⭐⭐   | ⭐⭐⭐        | ⭐⭐⭐      |
| **Apache ECharts** | Large datasets, real-time            | ⭐⭐⭐⭐   | ⭐⭐⭐⭐      | ⭐⭐⭐⭐⭐  |

### Recommended Stack

```javascript
// Frontend Stack
{
  framework: 'React 18+',
  charting: 'Recharts or Victory',
  stateManagement: 'Zustand or Redux Toolkit',
  dataFetching: 'React Query / SWR',
  styling: 'Tailwind CSS or Styled Components',
  responsiveness: 'CSS Grid + Media Queries'
}

// Backend Optimization
{
  preAggregation: 'SQL aggregation tables',
  caching: 'Redis (5-10 min TTL)',
  queryOptimization: 'Indexes on dimensions',
}
```

---

## Quick Selection Guide

```javascript
// ✅ RECOMMENDED: Recharts + Zustand + React Query
import { LineChart, BarChart, PieChart } from "recharts";
import useSWR from "swr";
import { useDashboardFilters } from "./store";

<LineChart data={dashboardData}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="date" />
  <YAxis />
  <Tooltip />
  <Legend />
  <Line type="monotone" dataKey="revenue" stroke="#3B82F6" dot={false} />
</LineChart>
```

---

## Performance Rules

| Metric | Target |
|--------|--------|
| Data load | < 1 second (or show spinner) |
| Chart render | < 500ms |
| Filter response | < 300ms (debounced) |
| Max data points | 50-500 frontend |

**Optimization Checklist:**
- [ ] Data aggregated at backend
- [ ] SWR/React Query configured
- [ ] useMemo for expensive computations
- [ ] Debounced filter updates
- [ ] Lazy load below-fold charts
