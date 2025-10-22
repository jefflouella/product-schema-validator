# Mookee Brand Implementation Guide

## Overview
This guide will help you implement the Mookee brand across your applications quickly and consistently.

---

## Files Included

1. **mookee-brand-guide.md** - Complete brand style guide (reference document)
2. **QUICK-REFERENCE.md** - Quick lookup for common values and patterns
3. **mookee-variables.css** - CSS custom properties (CSS variables)
4. **mookee-variables.scss** - SCSS variables and mixins
5. **mookee-colors.json** - Color values in multiple formats for design tools
6. **mookee-tailwind-config.js** - Tailwind CSS configuration
7. **mookee-react-components.txt** - React component examples

---

## Quick Start (5 minutes)

### Option 1: CSS Variables (Recommended for most projects)

1. Add the CSS variables file to your project:
```html
<link rel="stylesheet" href="path/to/mookee-variables.css">
```

2. Use the variables in your CSS:
```css
.my-button {
  background-color: var(--mookee-teal);
  color: var(--mookee-white);
  padding: var(--space-md) var(--space-lg);
  border-radius: var(--radius-md);
}
```

3. Install brand fonts (Google Fonts):
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Done!** You're now using Mookee brand colors, typography, and spacing.

---

### Option 2: Tailwind CSS

1. Replace your `tailwind.config.js` with `mookee-tailwind-config.js`

2. Use Tailwind classes with Mookee colors:
```jsx
<button className="bg-mookee-teal text-white px-6 py-3 rounded-lg hover:bg-mookee-deep-teal">
  Click Me
</button>
```

---

### Option 3: SCSS/SASS

1. Import the SCSS variables:
```scss
@import './mookee-variables.scss';
```

2. Use variables and mixins:
```scss
.my-button {
  @include button-base;
  background-color: $mookee-teal;
  
  &:hover {
    background-color: $mookee-deep-teal;
  }
}
```

---

## Design Tool Setup

### Figma

1. Create a new color style for each color in `mookee-colors.json`
2. Import Inter and Poppins fonts
3. Create text styles matching the typography scale
4. Create component variants for buttons, cards, inputs

### Adobe XD / Illustrator / Photoshop

1. Import colors from `mookee-colors.json` (or create swatches manually)
2. Load the included color palette (.ase format if you create one)
3. Install Inter and Poppins fonts on your system

### Sketch

1. Add colors as document colors from `mookee-colors.json`
2. Create shared text styles
3. Create symbol library for common components

---

## Component Implementation

### Primary Button

**HTML/CSS:**
```html
<button class="btn-primary">Click Me</button>
```

**React:**
```jsx
<PrimaryButton onClick={handleClick}>
  Click Me
</PrimaryButton>
```

**Tailwind:**
```jsx
<button className="bg-mookee-teal text-white px-6 py-3 rounded-lg font-medium hover:bg-mookee-deep-teal transition-colors">
  Click Me
</button>
```

---

### Card

**HTML/CSS:**
```html
<div class="card">
  <h2>Card Title</h2>
  <p>Card content goes here.</p>
</div>
```

**React:**
```jsx
<Card>
  <h2>Card Title</h2>
  <p>Card content goes here.</p>
</Card>
```

**Tailwind:**
```jsx
<div className="bg-white rounded-xl p-6 border border-gray-100 shadow-md hover:shadow-lg transition-shadow">
  <h2>Card Title</h2>
  <p>Card content goes here.</p>
</div>
```

---

### Input Field

**HTML/CSS:**
```html
<div>
  <label for="email">Email</label>
  <input type="email" id="email" class="input" placeholder="Enter your email">
</div>
```

**React:**
```jsx
<Input 
  label="Email"
  type="email"
  placeholder="Enter your email"
/>
```

**Tailwind:**
```jsx
<div>
  <label className="block mb-2 text-sm font-medium text-mookee-charcoal">
    Email
  </label>
  <input 
    type="email"
    className="w-full px-4 py-3 rounded-lg border-2 border-gray-100 focus:border-mookee-teal focus:outline-none"
    placeholder="Enter your email"
  />
</div>
```

---

## Responsive Implementation

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1023px
- Desktop: 1024px+

### Example (CSS):
```css
/* Mobile First */
.container {
  padding: var(--space-md);
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: var(--space-lg);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: var(--space-xl);
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### Example (Tailwind):
```jsx
<div className="p-4 md:p-6 lg:p-8 lg:max-w-screen-xl lg:mx-auto">
  {/* Content */}
</div>
```

---

## Common Patterns

### Page Layout
```jsx
<div className="min-h-screen bg-mookee-off-white">
  <header className="bg-white border-b border-gray-100">
    {/* Header content */}
  </header>
  
  <main className="max-w-screen-xl mx-auto px-6 py-8">
    {/* Main content */}
  </main>
  
  <footer className="bg-mookee-charcoal text-white mt-16">
    {/* Footer content */}
  </footer>
</div>
```

### Navigation
```jsx
<nav className="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-100">
  <img src="logo.svg" alt="Mookee" className="h-8" />
  
  <div className="flex items-center gap-6">
    <a href="#" className="text-mookee-deep-teal hover:text-mookee-teal">
      Features
    </a>
    <a href="#" className="text-mookee-deep-teal hover:text-mookee-teal">
      Pricing
    </a>
    <button className="bg-mookee-teal text-white px-6 py-2 rounded-lg hover:bg-mookee-deep-teal">
      Sign Up
    </button>
  </div>
</nav>
```

### Hero Section
```jsx
<section className="bg-gradient-to-br from-mookee-light-teal to-white py-20">
  <div className="max-w-screen-lg mx-auto px-6 text-center">
    <h1 className="text-5xl font-bold text-mookee-charcoal mb-4">
      Welcome to Mookee
    </h1>
    <p className="text-xl text-mookee-deep-teal mb-8">
      Your reliable platform for smart solutions
    </p>
    <button className="bg-mookee-teal text-white px-8 py-4 rounded-lg text-lg font-medium hover:bg-mookee-deep-teal">
      Get Started
    </button>
  </div>
</section>
```

---

## Dark Mode Implementation

### CSS Variables Approach
```css
/* Light mode (default) */
:root {
  --bg-primary: #F5F5F5;
  --bg-surface: #FFFFFF;
  --text-primary: #48625C;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #48625C;
    --bg-surface: #32403D;
    --text-primary: #FFFFFF;
  }
}

/* Or use a class-based approach */
.dark {
  --bg-primary: #48625C;
  --bg-surface: #32403D;
  --text-primary: #FFFFFF;
}
```

### Tailwind Dark Mode
```jsx
// Enable dark mode in tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media'
  // ... rest of config
}

// Use dark: prefix
<div className="bg-white dark:bg-mookee-charcoal text-mookee-charcoal dark:text-white">
  Content
</div>
```

---

## Accessibility Checklist

### Color Contrast
- ✅ Use Charcoal (#48625C) or Deep Teal (#62837C) for body text on light backgrounds
- ⚠️ Avoid using Mookee Teal (#83ADA4) for small text (contrast too low)
- ✅ Light Teal should only be used for backgrounds, not text

### Focus States
Always include visible focus indicators:
```css
button:focus-visible {
  outline: 2px solid var(--mookee-teal);
  outline-offset: 2px;
}
```

### Touch Targets
Ensure interactive elements are at least 44×44px on mobile:
```css
@media (max-width: 767px) {
  button, a {
    min-height: 44px;
    min-width: 44px;
  }
}
```

### Semantic HTML
Use proper HTML elements:
```html
<!-- Good -->
<button type="button">Click</button>
<nav><a href="#">Link</a></nav>

<!-- Bad -->
<div onclick="...">Click</div>
<span class="link">Link</span>
```

---

## Testing Your Implementation

### Visual Checklist
- [ ] Logo displays correctly at all sizes
- [ ] Colors match the brand palette exactly
- [ ] Fonts load properly (Inter for body, Poppins for headings)
- [ ] Spacing follows the 8px grid
- [ ] Border radius is consistent
- [ ] Shadows match the design system

### Accessibility Checklist
- [ ] All text has sufficient contrast (4.5:1 minimum)
- [ ] Focus states are visible
- [ ] Touch targets are at least 44×44px on mobile
- [ ] Semantic HTML is used throughout
- [ ] Alt text provided for images
- [ ] Keyboard navigation works

### Responsive Checklist
- [ ] Layouts adapt at 768px and 1024px breakpoints
- [ ] Text remains readable at all sizes
- [ ] Touch targets are appropriately sized on mobile
- [ ] No horizontal scrolling at any breakpoint

---

## Migration from Existing Brand

### Step 1: Audit Current Colors
1. List all colors used in your current app
2. Map each color to the closest Mookee color
3. Update color variables/constants

### Step 2: Update Typography
1. Replace fonts with Inter and Poppins
2. Update font sizes to match the type scale
3. Adjust line heights and letter spacing

### Step 3: Component Updates
1. Start with buttons (most visible)
2. Update cards and containers
3. Refresh form elements
4. Update navigation components

### Step 4: Test & Refine
1. Test on multiple devices and browsers
2. Check accessibility
3. Get stakeholder approval
4. Roll out gradually (feature by feature)

---

## Troubleshooting

### Fonts Not Loading
**Problem:** Fonts appear as system defaults
**Solution:** 
- Check if Google Fonts link is in `<head>`
- Verify font names match exactly: 'Inter' and 'Poppins'
- Check browser console for network errors

### Colors Look Different
**Problem:** Colors don't match the brand guide
**Solution:**
- Verify hex codes match exactly
- Check if browser is applying color profiles
- Ensure no CSS overrides are interfering

### Spacing Feels Off
**Problem:** Elements are too close or too far apart
**Solution:**
- Stick to the 8px spacing scale (4px, 8px, 16px, 24px, 32px...)
- Use spacing variables consistently
- Check if inherited margins are interfering

---

## Support & Resources

### Documentation
- **Full Brand Guide**: See mookee-brand-guide.md
- **Quick Reference**: See QUICK-REFERENCE.md
- **Color Values**: See mookee-colors.json

### Online Resources
- Inter Font: https://fonts.google.com/specimen/Inter
- Poppins Font: https://fonts.google.com/specimen/Poppins
- Color Contrast Checker: https://webaim.org/resources/contrastchecker/

### Community
- Share implementations and get feedback
- Request additional components or variants
- Report issues or inconsistencies

---

## Next Steps

1. ✅ Choose your implementation method (CSS Variables, Tailwind, or SCSS)
2. ✅ Install the Mookee brand files in your project
3. ✅ Set up fonts (Google Fonts or local)
4. ✅ Create your first branded component (start with a button)
5. ✅ Test for accessibility and responsiveness
6. ✅ Expand to other components
7. ✅ Get stakeholder approval
8. ✅ Roll out across all applications

---

**Version 1.0** | October 2025 | Mookee Brand System

For questions or additional support, refer to the main brand guide or reach out to your design team.
