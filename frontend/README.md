# Crypto Analytics Frontend

Mocked React + Vite + TypeScript experience for Iteration 1 of the Crypto Analytics Platform.

## Run

1. `npm install`
2. `npm run dev`
3. Open `http://localhost:5173`

Use `npm run build` to verify production readiness and `npm run preview` to inspect the compiled bundle.

## Stack Highlights

- **Tailwind CSS 4** configured via `tailwind.config.ts` + `@tailwindcss/postcss`.
- **Highcharts** renders the price (line) and volume (column) series.
- **Delay + errors**: mocks intentionally wait 500 ms and fail 1/8th of the time so the UI can show loading and error states.
- **Hooks**: `useAnalyticsState` centralizes the selected pair, date range, status, metrics, and points for the chart.

## Structure

- `src/pages/AnalyticsPage.tsx` — single-page layout with sidebar filters and the chart canvas.
- `src/components/*` — lightweight pair selector, date range picker, metrics cards, and chart wrapper.
- `src/mocks/analytics.ts` — deterministic data generator plus helper to compute metrics.
- `src/hooks/useAnalyticsState.ts` — glue between the mock API and the UI.
- `src/types/analytics.ts` — shared shapes for points, range, and metrics.

## Notes

- Replace `fetchAnalyticsMock` with real API calls when moving to Iteration 2.5.
- The “Track pair” button toggles a local flag for now; in later iterations it will hit `/api/pairs`.
- Use `npm run lint` to validate TypeScript + ESLint files (optional but recommended before commits).
# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
