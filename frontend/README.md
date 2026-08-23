# Eclipse Analyst Dashboard

React + TypeScript + Tailwind + Vite.

## Run

```bash
npm install
npm run dev
```

Proxies `/api` → `http://localhost:8000`.

## Structure

- `src/pages/` – Dashboard, Alerts, Entities, Cases, Reports
- `src/components/Layout.tsx` – sidebar navigation
- Ready for React Query + Axios integration against FastAPI

## Next steps

1. Auth context + protected routes
2. Real data fetching from `/api/v1/*`
3. Interactive network graph (e.g. react-force-graph or vis.js)
4. Risk score visualizations and SHAP factor breakdowns
5. Case annotation UI and SAR export
