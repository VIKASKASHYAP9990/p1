/* =============================================
   dashboard.js — Data processing & chart logic
   ============================================= */

/* ─── Global Chart.js defaults ─── */
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(10,15,30,0.97)';
Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.08)';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.plugins.tooltip.cornerRadius = 8;
Chart.defaults.plugins.tooltip.titleFont = { family: "'Space Grotesk', sans-serif", size: 13, weight: '600' };
Chart.defaults.plugins.tooltip.bodyFont = { family: "'Inter', sans-serif", size: 12 };
Chart.defaults.plugins.tooltip.titleColor = '#e2e8f0';
Chart.defaults.plugins.tooltip.bodyColor = '#94a3b8';

// Store active chart instances so we can destroy/recreate on filter change
const chartInstances = {};

/* ─── Currency formatter ─── */
const fmt = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
const fmtK = v => v >= 1000 ? `$${(v/1000).toFixed(1)}K` : `$${v.toFixed(0)}`;
const fmtPct = v => `${v.toFixed(1)}%`;

/* ─── Month names ─── */
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

/* ─── Palette ─── */
const PALETTE = {
  blue:   { solid:'#4facfe', glow:'rgba(79,172,254,0.2)', light:'rgba(79,172,254,0.12)' },
  cyan:   { solid:'#00f2fe', glow:'rgba(0,242,254,0.2)',  light:'rgba(0,242,254,0.12)' },
  violet: { solid:'#a78bfa', glow:'rgba(167,139,250,0.2)',light:'rgba(167,139,250,0.12)' },
  pink:   { solid:'#f472b6', glow:'rgba(244,114,182,0.2)',light:'rgba(244,114,182,0.12)' },
  green:  { solid:'#34d399', glow:'rgba(52,211,153,0.2)', light:'rgba(52,211,153,0.12)' },
  amber:  { solid:'#fbbf24', glow:'rgba(251,191,36,0.2)', light:'rgba(251,191,36,0.12)' },
  orange: { solid:'#fb923c', glow:'rgba(251,146,60,0.2)', light:'rgba(251,146,60,0.12)' },
  red:    { solid:'#f87171', glow:'rgba(248,113,113,0.2)',light:'rgba(248,113,113,0.12)' },
};

// Category colors
const CAT_COLORS = {
  'Technology':     PALETTE.blue.solid,
  'Furniture':      PALETTE.violet.solid,
  'Office Supplies':PALETTE.green.solid,
};

const REGION_META = {
  'West':    { icon:'🏔️', color: PALETTE.blue.solid,   grad: 'linear-gradient(90deg,#4facfe,#00f2fe)' },
  'East':    { icon:'🗽', color: PALETTE.violet.solid, grad: 'linear-gradient(90deg,#a78bfa,#f472b6)' },
  'South':   { icon:'🌴', color: PALETTE.green.solid,  grad: 'linear-gradient(90deg,#34d399,#059669)' },
  'Central': { icon:'🌾', color: PALETTE.amber.solid,  grad: 'linear-gradient(90deg,#fbbf24,#f59e0b)' },
};

/* ─── Filter State ─── */
let currentFilters = { year: 'all', region: 'all', category: 'all' };

/* ─── Apply Filters ─── */
function applyFilters(data) {
  return data.filter(r => {
    const yOk = currentFilters.year     === 'all' || r.year     === +currentFilters.year;
    const rOk = currentFilters.region   === 'all' || r.region   === currentFilters.region;
    const cOk = currentFilters.category === 'all' || r.category === currentFilters.category;
    return yOk && rOk && cOk;
  });
}

/* ─── Aggregation helpers ─── */
function sumField(arr, field) { return arr.reduce((acc, r) => acc + r[field], 0); }

function groupBy(arr, keyFn) {
  const map = {};
  arr.forEach(r => {
    const k = keyFn(r);
    if (!map[k]) map[k] = [];
    map[k].push(r);
  });
  return map;
}

/* ─── Main render ─── */
function renderDashboard() {
  const filtered = applyFilters(SALES_DATA);

  // Summary stats
  const totalSales  = sumField(filtered, 'sales');
  const totalProfit = sumField(filtered, 'profit');
  const totalOrders = filtered.length;
  const margin      = totalSales > 0 ? (totalProfit / totalSales) * 100 : 0;

  // Compare with previous year for growth
  const years = [...new Set(SALES_DATA.map(r => r.year))].sort();
  let yoyGrowth = null;
  if (currentFilters.year !== 'all') {
    const prevYear = +currentFilters.year - 1;
    const prevData = applyFilters(SALES_DATA.map(r => r)).filter(r => r.year === prevYear);
    const prevSales = sumField(prevData, 'sales');
    if (prevSales > 0) yoyGrowth = ((totalSales - prevSales) / prevSales) * 100;
  } else {
    // Calculate 2024 vs 2023
    const s2024 = sumField(SALES_DATA.filter(r => r.year === 2024 && (currentFilters.region === 'all' || r.region === currentFilters.region) && (currentFilters.category === 'all' || r.category === currentFilters.category)), 'sales');
    const s2023 = sumField(SALES_DATA.filter(r => r.year === 2023 && (currentFilters.region === 'all' || r.region === currentFilters.region) && (currentFilters.category === 'all' || r.category === currentFilters.category)), 'sales');
    if (s2023 > 0) yoyGrowth = ((s2024 - s2023) / s2023) * 100;
  }

  // ── Update KPI cards ──
  animateValue('kpi-sales',  totalSales,  '$', true);
  animateValue('kpi-profit', totalProfit, '$', true);
  animateValue('kpi-orders', totalOrders, '',  false);
  animateValue('kpi-margin', margin,      '%', false, 1);

  // Growth badge
  const growthEl = document.getElementById('kpi-growth-badge');
  if (growthEl && yoyGrowth !== null) {
    growthEl.innerHTML = `${yoyGrowth >= 0 ? '▲' : '▼'} ${Math.abs(yoyGrowth).toFixed(1)}%`;
    growthEl.className = `kpi-change ${yoyGrowth >= 0 ? 'up' : 'down'}`;
  }

  // Summary pills
  const uniqueProducts = new Set(filtered.map(r => r.product)).size;
  const uniqueRegions  = new Set(filtered.map(r => r.region)).size;
  document.getElementById('pill-products').innerHTML  = `<strong>${uniqueProducts}</strong> Products`;
  document.getElementById('pill-regions').innerHTML   = `<strong>${uniqueRegions}</strong> Regions`;
  document.getElementById('pill-records').innerHTML   = `<strong>${filtered.length}</strong> Records`;

  // Render all charts
  renderTrendChart(filtered);
  renderCategoryDonut(filtered);
  renderTopProductsChart(filtered);
  renderRegionBar(filtered);
  renderTopProductsTable(filtered);
  renderMonthlyHeatmap(filtered);
}

/* ─── Animate KPI value ─── */
function animateValue(elId, target, prefix, isCurrency, decimals = 0) {
  const el = document.getElementById(elId);
  if (!el) return;
  const start = 0;
  const dur = 900;
  const startTime = performance.now();
  function step(now) {
    const pct = Math.min((now - startTime) / dur, 1);
    const ease = 1 - Math.pow(1 - pct, 3);
    const val = start + (target - start) * ease;
    if (isCurrency) {
      el.textContent = prefix === '$' ? fmtK(val) : (prefix + val.toFixed(decimals));
    } else if (prefix === '%') {
      el.textContent = fmtPct(val);
    } else {
      el.textContent = Math.round(val).toLocaleString();
    }
    if (pct < 1) requestAnimationFrame(step);
    else {
      if (isCurrency && prefix === '$') el.textContent = fmtK(target);
      else if (prefix === '%') el.textContent = fmtPct(target);
      else el.textContent = Math.round(target).toLocaleString();
    }
  }
  requestAnimationFrame(step);
}

/* ─── Chart: Monthly Sales & Profit Trend (Line) ─── */
function renderTrendChart(data) {
  const ctx = document.getElementById('trendChart');
  if (!ctx) return;

  // Build month buckets
  const monthMap = {};
  data.forEach(r => {
    const key = r.monthStr;
    if (!monthMap[key]) monthMap[key] = { sales: 0, profit: 0 };
    monthMap[key].sales  += r.sales;
    monthMap[key].profit += r.profit;
  });

  const sortedKeys = Object.keys(monthMap).sort();
  const labels  = sortedKeys.map(k => {
    const [y, m] = k.split('-');
    return MONTHS[+m - 1] + ' ' + y.slice(2);
  });
  const salesVals  = sortedKeys.map(k => monthMap[k].sales);
  const profitVals = sortedKeys.map(k => monthMap[k].profit);

  // Gradient fills
  const canvasCtx = ctx.getContext('2d');
  const gradSales  = canvasCtx.createLinearGradient(0, 0, 0, 300);
  gradSales.addColorStop(0, 'rgba(79,172,254,0.35)');
  gradSales.addColorStop(1, 'rgba(79,172,254,0)');
  const gradProfit = canvasCtx.createLinearGradient(0, 0, 0, 300);
  gradProfit.addColorStop(0, 'rgba(52,211,153,0.3)');
  gradProfit.addColorStop(1, 'rgba(52,211,153,0)');

  if (chartInstances.trend) chartInstances.trend.destroy();
  chartInstances.trend = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Sales',
          data: salesVals,
          borderColor: '#4facfe',
          backgroundColor: gradSales,
          borderWidth: 2.5,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#4facfe',
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBorderWidth: 0,
        },
        {
          label: 'Profit',
          data: profitVals,
          borderColor: '#34d399',
          backgroundColor: gradProfit,
          borderWidth: 2,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#34d399',
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBorderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.dataset.label}: ${fmt.format(ctx.parsed.y)}`,
          },
        },
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
          ticks: { maxRotation: 45, maxTicksLimit: 12 },
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
          ticks: { callback: v => fmtK(v) },
          beginAtZero: true,
        },
      },
    },
  });
}

/* ─── Chart: Category Donut ─── */
function renderCategoryDonut(data) {
  const ctx = document.getElementById('categoryChart');
  if (!ctx) return;

  const groups = groupBy(data, r => r.category);
  const cats   = Object.keys(CAT_COLORS).filter(c => groups[c]);
  const vals   = cats.map(c => sumField(groups[c] || [], 'sales'));
  const colors = cats.map(c => CAT_COLORS[c]);
  const backgrounds = cats.map(c => {
    const col = CAT_COLORS[c];
    return col;
  });

  if (chartInstances.category) chartInstances.category.destroy();
  chartInstances.category = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: cats,
      datasets: [{
        data: vals,
        backgroundColor: backgrounds,
        borderColor: 'rgba(10,15,30,0.8)',
        borderWidth: 3,
        hoverBorderWidth: 2,
        hoverOffset: 6,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      cutout: '70%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => {
              const total = ctx.chart.data.datasets[0].data.reduce((a,b) => a+b, 0);
              const pct   = ((ctx.parsed / total) * 100).toFixed(1);
              return ` ${ctx.label}: ${fmt.format(ctx.parsed)} (${pct}%)`;
            },
          },
        },
      },
    },
  });

  // Update legend
  const legendEl = document.getElementById('category-legend');
  if (legendEl) {
    const totalSales = vals.reduce((a,b)=>a+b,0);
    legendEl.innerHTML = cats.map((c, i) => {
      const pct = totalSales > 0 ? ((vals[i]/totalSales)*100).toFixed(1) : 0;
      return `<div class="legend-item">
        <div class="legend-dot" style="background:${colors[i]}"></div>
        <span>${c}</span>
        <span style="color:#e2e8f0;font-weight:600;margin-left:auto">${pct}%</span>
      </div>`;
    }).join('');
  }
}

/* ─── Chart: Top Products Bar ─── */
function renderTopProductsChart(data) {
  const ctx = document.getElementById('productsChart');
  if (!ctx) return;

  const groups = groupBy(data, r => r.product);
  const sorted = Object.entries(groups)
    .map(([p, rows]) => ({ name: p, sales: sumField(rows, 'sales'), profit: sumField(rows, 'profit') }))
    .sort((a,b) => b.sales - a.sales)
    .slice(0, 8);

  const labels  = sorted.map(p => p.name.length > 22 ? p.name.slice(0,22)+'…' : p.name);
  const salesV  = sorted.map(p => p.sales);
  const profitV = sorted.map(p => p.profit);

  if (chartInstances.products) chartInstances.products.destroy();
  chartInstances.products = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Sales',
          data: salesV,
          backgroundColor: 'rgba(79,172,254,0.75)',
          borderColor: '#4facfe',
          borderWidth: 1,
          borderRadius: 5,
          borderSkipped: false,
        },
        {
          label: 'Profit',
          data: profitV,
          backgroundColor: 'rgba(52,211,153,0.7)',
          borderColor: '#34d399',
          borderWidth: 1,
          borderRadius: 5,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.dataset.label}: ${fmt.format(ctx.parsed.y)}`,
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 10.5 }, maxRotation: 25 },
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
          ticks: { callback: v => fmtK(v) },
          beginAtZero: true,
        },
      },
    },
  });
}

/* ─── Region horizontal bars ─── */
function renderRegionBar(data) {
  const el = document.getElementById('region-list');
  if (!el) return;

  const groups = groupBy(data, r => r.region);
  const regions = Object.entries(groups)
    .map(([r, rows]) => ({ name: r, sales: sumField(rows, 'sales'), profit: sumField(rows, 'profit'), count: rows.length }))
    .sort((a,b) => b.sales - a.sales);

  const maxSales = Math.max(...regions.map(r => r.sales), 1);

  el.innerHTML = regions.map(r => {
    const meta = REGION_META[r.name] || { icon:'🌐', grad:'linear-gradient(90deg,#94a3b8,#475569)' };
    const pct  = (r.sales / maxSales * 100).toFixed(1);
    const margin = r.sales > 0 ? ((r.profit / r.sales)*100).toFixed(1) : 0;
    return `
      <div class="region-item">
        <div class="region-flag">${meta.icon}</div>
        <div class="region-info">
          <div class="region-name">${r.name} <span style="font-size:11px;color:var(--text-muted);font-weight:400">(${r.count} orders, ${margin}% margin)</span></div>
          <div class="region-bar-bg">
            <div class="region-bar" style="width:${pct}%;background:${meta.grad}"></div>
          </div>
        </div>
        <div class="region-value">${fmtK(r.sales)}</div>
      </div>`;
  }).join('');
}

/* ─── Top Products Table ─── */
function renderTopProductsTable(data) {
  const tbody = document.getElementById('products-tbody');
  if (!tbody) return;

  const groups = groupBy(data, r => r.product);
  const top10  = Object.entries(groups)
    .map(([p, rows]) => ({
      name: p,
      category: rows[0].category,
      sales:   sumField(rows, 'sales'),
      profit:  sumField(rows, 'profit'),
      orders:  rows.length,
      qty:     sumField(rows, 'quantity'),
    }))
    .sort((a,b) => b.sales - a.sales)
    .slice(0, 10);

  const maxProfit = Math.max(...top10.map(p => p.profit), 1);

  tbody.innerHTML = top10.map((p, i) => {
    const rankClass = i===0?'rank-1':i===1?'rank-2':i===2?'rank-3':'rank-other';
    const margin    = p.sales > 0 ? ((p.profit/p.sales)*100).toFixed(1) : 0;
    const barW      = (p.profit / maxProfit * 100).toFixed(1);
    const catColor  = CAT_COLORS[p.category] || '#94a3b8';
    return `<tr>
      <td><span class="rank-badge ${rankClass}">${i+1}</span></td>
      <td title="${p.name}">${p.name.length>30?p.name.slice(0,30)+'…':p.name}</td>
      <td><span style="color:${catColor};font-size:11px;font-weight:600">${p.category}</span></td>
      <td style="color:#e2e8f0;font-weight:600">${fmt.format(p.sales)}</td>
      <td style="color:#34d399;font-weight:600">${fmt.format(p.profit)}</td>
      <td style="color:#94a3b8">${margin}%</td>
      <td>
        <div class="profit-bar-bg"><div class="profit-bar" style="width:${barW}%"></div></div>
      </td>
    </tr>`;
  }).join('');
}

/* ─── Monthly Heatmap (Sub-category breakdown) ─── */
function renderMonthlyHeatmap(data) {
  const ctx = document.getElementById('heatmapChart');
  if (!ctx) return;

  // Quarterly breakdown by category
  const quarters = ['Q1', 'Q2', 'Q3', 'Q4'];
  const categories = ['Technology', 'Furniture', 'Office Supplies'];
  const catColors  = ['#4facfe', '#a78bfa', '#34d399'];

  const datasets = categories.map((cat, ci) => {
    const qData = quarters.map((q, qi) => {
      const months = [qi*3+1, qi*3+2, qi*3+3];
      return sumField(
        data.filter(r => r.category === cat && months.includes(r.month)),
        'sales'
      );
    });
    return {
      label: cat,
      data: qData,
      backgroundColor: catColors[ci] + 'bb',
      borderColor: catColors[ci],
      borderWidth: 1.5,
      borderRadius: 6,
      borderSkipped: false,
    };
  });

  if (chartInstances.heatmap) chartInstances.heatmap.destroy();
  chartInstances.heatmap = new Chart(ctx, {
    type: 'bar',
    data: { labels: quarters, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.dataset.label}: ${fmt.format(ctx.parsed.y)}`,
          },
        },
      },
      scales: {
        x: { grid: { display: false }, stacked: false },
        y: {
          grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
          ticks: { callback: v => fmtK(v) },
          beginAtZero: true,
        },
      },
    },
  });
}

/* ─── Filter initialization ─── */
function initFilters() {
  const years = [...new Set(SALES_DATA.map(r => r.year))].sort();
  const yearSel = document.getElementById('filter-year');
  yearSel.innerHTML = '<option value="all">All Years</option>';
  years.forEach(y => {
    yearSel.innerHTML += `<option value="${y}">${y}</option>`;
  });

  ['filter-year','filter-region','filter-category'].forEach(id => {
    document.getElementById(id).addEventListener('change', function() {
      currentFilters[id.replace('filter-','')] = this.value;
      renderDashboard();
    });
  });
}

/* ─── Boot ─── */
document.addEventListener('DOMContentLoaded', () => {
  initFilters();
  renderDashboard();
});
