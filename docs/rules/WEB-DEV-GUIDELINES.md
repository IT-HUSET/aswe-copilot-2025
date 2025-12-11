# Web Development Guidelines (Simplified)

Core web standards and best practices for browser-based projects.

> For UI/UX specifics (touch targets, visual hierarchy, accessibility checklists), see `UX-UI-GUIDELINES.md`.

## HTML & Semantics

- Use semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`)
- Always include `alt` text for images (empty `alt=""` for decorative)
- Keep content (HTML), presentation (CSS), and behavior (JS) separate

## CSS & Styling

- Keep styles in external stylesheets
- Use consistent naming (BEM or utility-first)
- Use Flexbox/Grid for layout (not floats/tables)
- Mobile-first with relative units and media queries

## JavaScript

- Use `defer/async` to avoid blocking
- Prefer ES6+ (`let`, `const`, arrow functions, modules)
- Cache DOM elements, batch updates, debounce events
- Use `async`/`await` for async operations

## Performance

- Minify CSS/JS, compress images (WebP preferred)
- Use `loading="lazy"` for images
- Track Core Web Vitals (LCP, INP, CLS)

## Security

- HTTPS everywhere
- Validate/sanitize inputs (prevent XSS, SQLi)
- Use Content Security Policy
- Secure cookies: HttpOnly, Secure, SameSite
- Never commit secrets; use `.env` files (gitignored)

## Accessibility

- Follow WCAG: semantic HTML, alt text, keyboard support
- Ensure focus visibility and logical tab order
- Use ARIA only when native HTML isn't enough
- Test with axe, WAVE, or screen readers

## Testing & Quality

- Write clean, readable code with meaningful names
- Add unit and E2E tests
- Test across browsers and devices
