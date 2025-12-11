# UI/UX Guidelines (Simplified)

## Core Principle
**Users scan, don't read** - Every element must be instantly understandable.

## 5 Fundamental Laws

### 1. Don't Make Me Think
- Make every element self-evident within 5 seconds
- Use universally recognized icons and patterns
- **Test**: Can someone identify the primary action in 5 seconds?

### 2. Visual Hierarchy
- Primary action = largest and brightest element
- Use size ratios 3:2:1 for headline:subhead:body
- **Test**: Squint at screen - is the primary action obvious?

### 3. Touch/Click Targets
```yaml
Mobile:  44pt minimum, 8pt spacing
Desktop: 32px minimum, 8px spacing
```

### 4. Instant Feedback
```yaml
0-100ms:  No indicator needed
100ms-1s: Show spinner/skeleton
1-3s:     Show progress bar
>3s:      Add time estimate + cancel
```

### 5. Error Prevention
- Prevent errors with constraints (disable invalid actions)
- Use inline validation as user types
- Provide undo for destructive actions
- Error format: `[What happened] + [Why] + [How to fix]`

## Design Tokens

```yaml
Spacing (8px grid):
  xs: 4px | sm: 8px | md: 16px | lg: 24px | xl: 32px

Typography:
  Mobile min: 12pt | Desktop min: 14px | Body: 16px
  Max line width: 65ch

Contrast (WCAG AA):
  Regular text: 4.5:1 | Large text: 3:1
```

## Accessibility Essentials

- All text: 4.5:1 contrast minimum
- Focus indicators on all interactive elements
- Color never sole indicator (add icons)
- Tab order matches visual hierarchy
- All interactive elements keyboard accessible
- Semantic HTML with proper ARIA labels

## Performance Targets

```yaml
First Paint:   < 1 second
Interactive:   < 3 seconds
Animations:    60fps (use transform/opacity only)
```

## Quick Validation

Before completing UI work:
- [ ] Primary action obvious in 5 seconds
- [ ] Touch targets ≥ 44pt
- [ ] Loading states for async operations
- [ ] Error messages are helpful
- [ ] Keyboard navigable
- [ ] Contrast passes WCAG AA
- [ ] Works on mobile

**Remember**: The best interface is invisible.
