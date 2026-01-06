# Dashboard Accessibility Guidelines (WCAG)

## Why Accessibility Matters

- **Legal requirements:** ADA (US), EAA (EU) are increasingly strict
- **Inclusive design:** 15% of the population has a disability
- **Better UX for all:** Accessible dashboards are easier to use for everyone

---

## Color & Contrast

### WCAG 1.4.1 - Use of Color

> Color must not be the only means of conveying information

```javascript
// ❌ BAD: Color only
<Bar fill={value > 0 ? "green" : "red"} />

// ✅ GOOD: Color + Pattern + Label
<Bar
  fill={value > 0 ? "green" : "red"}
  pattern={value > 0 ? "solid" : "striped"}
  label={`${value > 0 ? "↑" : "↓"} ${value}%`}
/>
```

### WCAG 1.4.3 - Contrast Ratio

- Text thường: **4.5:1** minimum
- Large text (18px+): **3:1** minimum
- Non-text elements: **3:1** minimum

### Color-blind Safe Palettes

```javascript
// Thay vì Red-Green (problematic)
const colorBlindSafe = {
  positive: "#0072B2", // Blue
  negative: "#D55E00", // Orange-Red
  neutral: "#6B7280",  // Gray
  warning: "#F0E442",  // Yellow

  // Sequential palette
  series: [
    "#0072B2", // Blue
    "#E69F00", // Orange
    "#009E73", // Teal
    "#CC79A7", // Pink
    "#F0E442", // Yellow
  ],
};
```

---

## Screen Reader Support

### Alt Text cho Charts

```javascript
<BarChart
  aria-label="Bar chart showing revenue by region"
  aria-describedby="chart-description"
>
  {/* Chart content */}
</BarChart>

<div id="chart-description" className="sr-only">
  Revenue by region: North America $1.2M (highest),
  Europe $800K, APAC $600K, LATAM $200K (lowest)
</div>
```

### Data Tables as Alternative

```javascript
// Always provide data table for screen readers
<details>
  <summary>View data as table</summary>
  <table>
    <caption>Revenue by Region Q4 2024</caption>
    <thead>
      <tr>
        <th scope="col">Region</th>
        <th scope="col">Revenue</th>
      </tr>
    </thead>
    <tbody>
      {data.map((row) => (
        <tr key={row.region}>
          <td>{row.region}</td>
          <td>${row.revenue.toLocaleString()}</td>
        </tr>
      ))}
    </tbody>
  </table>
</details>
```

---

## Keyboard Navigation

```javascript
const AccessibleChart = () => {
  const [focusedIndex, setFocusedIndex] = useState(0);

  const handleKeyDown = (e) => {
    switch (e.key) {
      case "ArrowRight":
        setFocusedIndex((i) => Math.min(i + 1, data.length - 1));
        break;
      case "ArrowLeft":
        setFocusedIndex((i) => Math.max(i - 1, 0));
        break;
      case "Enter":
      case " ":
        handleBarClick(data[focusedIndex]);
        break;
    }
  };

  return (
    <div
      role="img"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      aria-label="Interactive bar chart"
    >
      {/* Chart with focus indicators */}
    </div>
  );
};
```

---

## React Accessibility Hook

```javascript
const useAccessibleChart = (chartRef, data) => {
  useEffect(() => {
    const announcement = `Chart updated with ${data.length} data points`;
    announceToScreenReader(announcement);
  }, [data]);

  const prefersReducedMotion = useMediaQuery(
    "(prefers-reduced-motion: reduce)"
  );

  return {
    animationDuration: prefersReducedMotion ? 0 : 300,
    shouldAnimate: !prefersReducedMotion,
  };
};
```

---

## Accessibility Checklist

### Color & Contrast
- [ ] Text contrast ≥ 4.5:1
- [ ] Non-text elements contrast ≥ 3:1
- [ ] Color is not the only indicator
- [ ] Color-blind safe palette used
- [ ] Patterns/textures supplement colors

### Screen Readers
- [ ] All charts have aria-label
- [ ] Complex charts have aria-describedby
- [ ] Data tables provided as alternative
- [ ] Logical reading order (tabindex)
- [ ] Live regions for dynamic updates

### Keyboard Navigation
- [ ] All interactive elements focusable
- [ ] Focus indicators visible (outline)
- [ ] Keyboard shortcuts documented
- [ ] No keyboard traps
- [ ] Skip links for main content

### Motion & Animation
- [ ] Respect prefers-reduced-motion
- [ ] Animations < 5 seconds or pausable
- [ ] No flashing content > 3Hz

---

## Testing Tools

- **WebAIM Contrast Checker** - Check color contrast ratios
- **NoCoffee Vision Simulator** - Simulate vision impairments
- **Colorblindly Chrome Extension** - Test color blindness
- **axe DevTools** - Automated accessibility testing
- **NVDA/VoiceOver** - Screen reader testing
