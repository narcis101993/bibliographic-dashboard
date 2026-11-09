// Custom Chart.js bundle entry — only what dashboard/app.js uses.
//
// The dashboard draws exactly two chart types: "bar" (3 charts) and
// "doughnut" (2 charts), with the legend and tooltip plugins. The stock
// chart.umd.min.js also ships line/pie/polar/radar/scatter/bubble
// controllers, logarithmic/time scales, decimation, filler and title
// plugins that are never executed (Lighthouse "Reduce unused JavaScript").
// Bundling just the used pieces keeps the same global `Chart` API
// (new Chart(ctx, config), chart.resize(), chart.destroy()) in a
// much smaller file. See docs/lighthouse-fixes-2026-11-09.md.
//
// Build: python3 scripts/build_chart_bundle.py  (esbuild, MIT-licensed
// Chart.js 4.4.7 — see dashboard/vendor/CHARTJS-LICENSE.md)
import {
  Chart,
  BarController,
  DoughnutController,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js";

Chart.register(
  BarController,
  DoughnutController,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

// dashboard/app.js expects a browser global named `Chart`.
window.Chart = Chart;
export default Chart;
