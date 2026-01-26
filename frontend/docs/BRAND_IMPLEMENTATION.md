# Aura Brand Implementation Guide

This guide provides specific implementation details for maintaining brand consistency in the Aura frontend codebase.

## 📁 File Structure

```
frontend/
├── docs/
│   ├── BRAND_GUIDELINES.md      # Comprehensive brand guidelines
│   └── BRAND_IMPLEMENTATION.md  # Implementation specifics (this file)
├── tailwind.config.ts           # Tailwind configuration with brand colors
├── src/
│   ├── app/
│   │   └── globals.css          # Global styles and brand utilities
│   └── components/
│       ├── ui/                 # UI component library
│       └── AgentConsole.tsx    # Main application component
```

## 🎨 Color Implementation

### Tailwind Configuration

All brand colors are defined in `tailwind.config.ts`:

```typescript
colors: {
  // Primary Brand Colors
  'cyberpunk-blue': '#00f2ff',
  'cyberpunk-purple': '#a855f7',
  'cyberpunk-pink': '#ec4899',
  
  // Neutral Colors
  'dark-bg': '#0a0a0a',
  'card-bg': '#1a1a1a',
  'gray-800': '#1f1f1f',
  'gray-700': '#373737',
  'gray-600': '#4b4b4b',
  'gray-500': '#6b6b6b',
  'gray-400': '#9ca3af',
  'gray-300': '#d1d5db',
  
  // Semantic Colors
  'success': '#10b981',
  'warning': '#f59e0b',
  'error': '#ef4444',
  'info': '#3b82f6',
}
```

### Usage Examples

**Primary CTA Button:**
```jsx
<Button className="bg-cyberpunk-blue hover:bg-cyberpunk-blue/90 text-white">
  Submit
</Button>
```

**Secondary Button:**
```jsx
<Button className="bg-cyberpunk-purple hover:bg-cyberpunk-purple/90 text-white">
  Cancel
</Button>
```

**Error State:**
```jsx
<Alert className="bg-error/20 border-error">
  <AlertTitle className="text-error">Error</AlertTitle>
  <AlertDescription>Something went wrong</AlertDescription>
</Alert>
```

## 📐 Typography Implementation

### Font Families

The Inter font family is used as the primary typeface:

```css
@layer base {
  body {
    @apply font-sans; /* Uses Inter font stack */
  }
}
```

### Typography Classes

Custom typography classes are defined in `globals.css`:

```css
/* Heading Styles */
h1, .h1 { @apply text-h1 font-bold text-white; }
h2, .h2 { @apply text-h2 font-semibold text-white; }
h3, .h3 { @apply text-h3 font-semibold text-white; }
h4, .h4 { @apply text-h4 font-semibold text-white; }

/* Body Text */
p, .body-text { @apply text-body text-gray-300; }
.body-text-sm { @apply text-body-sm text-gray-400; }
.caption-text { @apply text-caption text-gray-500; }
```

### Usage Examples

**Main Heading:**
```jsx
<h1 className="h1">Aura Agent Console</h1>
```

**Section Heading:**
```jsx
<h3 className="h3 text-cyberpunk-blue">Search Inventory</h3>
```

**Body Text:**
```jsx
<p className="body-text">Find items to negotiate</p>
```

**Caption:**
```jsx
<span className="caption-text">ID: {item.itemId}</span>
```

## 🎯 Component Styles

### Card Component

Use the `card-brand` class for consistent card styling:

```jsx
<Card className="card-brand">
  {/* Card content */}
</Card>
```

This applies:
- Background: `card-bg` (#1a1a1a)
- Border: 1px solid `gray-700` (#373737)
- Border Radius: 0.5rem (8px)
- Shadow: subtle card shadow

### Input Component

Use the `input-brand` class for consistent input styling:

```jsx
<Input className="input-brand" />
```

This applies:
- Background: `gray-800` (#1f1f1f)
- Border: 1px solid `gray-600` (#4b4b4b)
- Text: white
- Focus: cyberpunk-blue ring

### Button Components

Use the predefined button classes:

```jsx
// Primary button
<Button className="btn-primary">Submit</Button>

// Secondary button
<Button className="btn-secondary">Cancel</Button>

// Destructive button
<Button className="btn-destructive">Delete</Button>
```

## 🎭 Animations & Transitions

### Brand Transitions

Use `transition-brand` for consistent transitions:

```jsx
<div className="transition-brand">
  {/* Content with smooth transitions */}
</div>
```

### Fade-in Animation

Use `animate-fade-in` for fade-in effects:

```jsx
<div className="animate-fade-in">
  {/* Content that fades in */}
</div>
```

### Custom Animations

Define custom animations in `globals.css`:

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## 🌙 Dark Mode Implementation

Aura uses a dark-first approach with Tailwind's dark mode:

```javascript
// tailwind.config.ts
darkMode: 'class',
```

```html
<!-- In your layout -->
<html className="dark">
  <body className="bg-dark-bg text-white">
    {/* Content */}
  </body>
</html>
```

## 📱 Responsive Design

### Breakpoints

Use Tailwind's built-in breakpoints:

```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

### Container Sizing

```jsx
<div className="max-w-7xl mx-auto px-4">
  {/* Content with proper max-width and padding */}
</div>
```

## 🔒 Accessibility

### Focus Styles

Brand focus styles are defined in `globals.css`:

```css
*:focus {
  @apply outline-none ring-2 ring-cyberpunk-blue ring-offset-2 ring-offset-dark-bg;
}
```

### Semantic HTML

Always use semantic HTML elements:

```jsx
// Good
<button onClick={handleClick}>Click me</button>

// Bad
<div onClick={handleClick}>Click me</div>
```

### ARIA Attributes

Use proper ARIA attributes:

```jsx
<button aria-label="Search" aria-disabled={isLoading}>
  <SearchIcon />
</button>
```

## 📋 Component Checklist

### Creating New Components

1. **Color**: Use brand colors from Tailwind config
2. **Typography**: Use defined typography classes
3. **Spacing**: Use consistent spacing scale (4px increments)
4. **Borders**: Use `gray-700` for standard borders
5. **Transitions**: Add `transition-brand` for interactive elements
6. **Accessibility**: Ensure proper focus states and ARIA attributes
7. **Responsive**: Test on all breakpoints
8. **Dark Mode**: Verify dark mode compatibility

### Component Review

- [ ] Uses brand colors correctly
- [ ] Follows typography guidelines
- [ ] Has proper spacing
- [ ] Includes hover/focus states
- [ ] Is accessible (keyboard, screen reader)
- [ ] Works on mobile devices
- [ ] Supports dark mode
- [ ] Has consistent transitions

## 🔧 Development Workflow

### Adding New Colors

1. Add to `tailwind.config.ts`
2. Document in `BRAND_GUIDELINES.md`
3. Update `BRAND_IMPLEMENTATION.md` with usage examples
4. Test contrast ratios

### Adding New Typography

1. Define in `globals.css`
2. Add to typography table in guidelines
3. Document usage patterns

### Creating New Components

1. Follow existing patterns
2. Use brand utility classes
3. Add to component library if reusable
4. Document component usage

## 🧪 Testing Brand Consistency

### Visual Regression Testing

Use tools like:
- Storybook for component isolation
- Chromatic for visual regression testing
- BrowserStack for cross-browser testing

### Automated Checks

```javascript
// Example: Color contrast check (pseudo-code)
const checkContrast = (foreground, background) => {
  const contrastRatio = calculateContrast(foreground, background);
  if (contrastRatio < 4.5) {
    console.warn(`Low contrast: ${contrastRatio}`);
  }
}
```

## 📝 Common Patterns

### Gradient Backgrounds

```jsx
<div className="bg-brand-gradient">
  {/* Content with cyberpunk gradient */}
</div>
```

### Status Badges

```jsx
<Badge variant={score > 0.8 ? 'default' : 'secondary'}>
  {score}%
</Badge>
```

### Loading States

```jsx
<Button disabled={isLoading}>
  {isLoading ? 'Processing...' : 'Submit'}
</Button>
```

## 🔗 Integration with Design Tools

### Figma to Code

1. Use Figma's Tailwind plugin
2. Map Figma styles to Tailwind classes
3. Export assets with proper naming
4. Use Figma variables for brand colors

### Design Token Management

```json
// Example design tokens (conceptual)
{
  "colors": {
    "primary": {
      "value": "#00f2ff",
      "name": "cyberpunk-blue"
    }
  },
  "typography": {
    "h1": {
      "fontSize": "3rem",
      "fontWeight": "700",
      "lineHeight": "1.2"
    }
  }
}
```

## 📋 Maintenance

### Updating Brand Guidelines

1. Update `BRAND_GUIDELINES.md`
2. Update `BRAND_IMPLEMENTATION.md`
3. Update Tailwind config
4. Update global CSS
5. Create migration guide if needed
6. Update all components

### Versioning

Follow semantic versioning for brand changes:
- **Patch**: Minor tweaks, bug fixes
- **Minor**: New components, non-breaking changes
- **Major**: Complete redesign, breaking changes

## 🤝 Contributing

### Reporting Brand Issues

1. Open GitHub issue
2. Tag with `brand` label
3. Include screenshots
4. Specify location
5. Suggest fix if possible

### Brand Review Process

1. Design team review
2. Engineering team implementation
3. QA testing
4. Stakeholder approval
5. Documentation update

---

*© 2024 Aura Platform. All rights reserved.*