# Module 2: Frontend Development — Digital Nurture 5.0

Hands-On 5–10 (React, Angular, Vue, Accessibility, Advanced State Management).
Hands-On 1–4 (HTML/CSS/JS fundamentals) are not included in this submission.

All React/Vue/Angular apps in this package were installed and built
successfully during preparation (`npm install && npm run build` passed with
zero errors) — the code is verified working, not just written.

## Folder structure

```
Module2_FrontendDev/YourName/
├── HandsOn5/   student-portal-react/    # Components, props, state, hooks
├── HandsOn6/   student-portal-react/    # Router, Context API, Redux Toolkit
├── HandsOn7/   student-portal-angular/  # Components, services, DI, routing, reactive forms
├── HandsOn8/   student-portal-vue/      # Composition API, Vue Router, Pinia
├── HandsOn9/   index.html, styles.css,  # Accessibility fixes + audit doc
│               accessibility-audit.md
└── HandsOn10/  student-portal-react/,   # Centralized API layer, async thunks,
                state-management-comparison.md   # error boundary, framework comparison
```

## Prerequisites

- Node.js LTS + npm — https://nodejs.org/en/download/
- Angular CLI (for Hands-On 7 only): `npm install -g @angular/cli`

## Hands-On 5 — React Fundamentals

```bash
cd HandsOn5/student-portal-react
npm install
npm run dev        # opens at http://localhost:5173
```

## Hands-On 6 — React Router, Context API, Redux Toolkit

```bash
cd HandsOn6/student-portal-react
npm install
npm run dev
```
Visit `/`, `/courses`, `/courses/1`, `/profile`. Enrolling a course
dispatches a Redux action and redirects to `/profile`. Redux DevTools
(browser extension) will show `enroll`/`unenroll` actions.

## Hands-On 7 — Angular

```bash
cd HandsOn7/student-portal-angular
npm install
npx ng serve        # opens at http://localhost:4200
```
Routes: `/` (course list with search) and `/profile` (reactive form with
validation). Course data loads via `CourseService` (HttpClient + DI).

## Hands-On 8 — Vue.js

```bash
cd HandsOn8/student-portal-vue
npm install
npm run dev         # opens at http://localhost:5173
```
Routes: `/`, `/courses`, `/courses/:id`, `/profile`. Enrollment state is
managed by the Pinia store in `src/stores/enrollment.js`. Install the Vue
DevTools browser extension to inspect the Pinia state tab.

## Hands-On 9 — Accessibility

```bash
cd HandsOn9
open index.html      # or double-click in a file browser / Live Server
```
Read `accessibility-audit.md` for the full Lighthouse audit write-up
(baseline score, flagged issues, fixes, contrast table, cross-browser notes).
Re-run Chrome DevTools → Lighthouse → Accessibility on `index.html` to see
the improved score.

## Hands-On 10 — Centralized API Layer & Advanced State Management

```bash
cd HandsOn10/student-portal-react
npm install
npm run dev
```
- `src/api/apiClient.js` — single Axios instance with interceptors.
- `src/api/courseApi.js` — `getAllCourses`, `getCourseById`, `enrollStudent`.
- `src/store/enrollmentSlice.js` — `createAsyncThunk` + `extraReducers` for
  loading/error/data state, plus selectors.
- `src/components/ErrorBoundary.jsx` — global error handling, wraps the app
  in `main.jsx`.
- `state-management-comparison.md` — NgRx concept write-up, Pinia advanced
  patterns, and a React/Angular/Vue state-management comparison table.

## Push to GitHub

```bash
cd Module2_FrontendDev/YourName
git init
git add .
git commit -m "Digital Nurture 5.0 - Module 2 Frontend Development (Hands-On 5-10)"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

> Tip: add a `.gitignore` with `node_modules/`, `dist/`, and `.angular/` in
> each framework subfolder before committing, per the submission guidelines
> ("include the full project folder minus node_modules").
