# Mookee Brand - Quick Reference Cheat Sheet

## Colors (Most Used)

### Primary
- **Mookee Teal**: `#83ADA4` - Buttons, Links, Key UI
- **Deep Teal**: `#62837C` - Text, Hover States
- **Charcoal**: `#48625C` - Body Text, Headings

### Backgrounds
- **Off-White**: `#F5F5F5` - Main Background
- **White**: `#FFFFFF` - Cards, Surfaces
- **Light Gray**: `#EAEAEA` - Borders, Dividers

### Accents
- **Light Teal**: `#AEE9DC` - Highlights, Soft Backgrounds
- **Success**: `#4CAF50` - Success Messages
- **Error**: `#F44336` - Error Messages

---

## Typography

### Font Families
```css
/* Primary Font (UI & Body) */
font-family: 'Inter', sans-serif;

/* Display Font (Headlines) */
font-family: 'Poppins', sans-serif;

/* Code Font */
font-family: 'JetBrains Mono', monospace;
```

### Font Sizes
- H1: 48px / 3rem - Bold
- H2: 36px / 2.25rem - Bold
- H3: 28px / 1.75rem - SemiBold
- Body: 16px / 1rem - Regular
- Small: 14px / 0.875rem - Regular

---

## Component Patterns

### Primary Button
```css
background: #83ADA4;
color: white;
padding: 12px 24px;
border-radius: 8px;
font-weight: 500;

hover: background #62837C;
```

### Secondary Button
```css
background: transparent;
color: #62837C;
border: 2px solid #83ADA4;
padding: 10px 22px; /* 2px less for border */
border-radius: 8px;

hover: background #AEE9DC;
```

### Card
```css
background: white;
border: 1px solid #EAEAEA;
border-radius: 12px;
padding: 24px;
box-shadow: 0 2px 8px rgba(72, 98, 92, 0.08);

hover: box-shadow 0 4px 16px rgba(72, 98, 92, 0.12);
```

### Input Field
```css
border: 2px solid #EAEAEA;
border-radius: 8px;
padding: 12px 16px;
font-size: 16px;

focus: border-color #83ADA4;
error: border-color #F44336;
```

---

## Spacing Scale (8px base)

- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px

---

## Border Radius

- sm: 4px - Small elements
- md: 8px - Buttons, inputs
- lg: 12px - Cards
- xl: 16px - Large cards
- full: 9999px - Pills, avatars

---

## Shadows

```css
/* Small */
box-shadow: 0 1px 2px rgba(72, 98, 92, 0.05);

/* Medium (Default) */
box-shadow: 0 2px 8px rgba(72, 98, 92, 0.08);

/* Large */
box-shadow: 0 4px 16px rgba(72, 98, 92, 0.12);

/* Extra Large */
box-shadow: 0 8px 32px rgba(72, 98, 92, 0.16);
```

---

## Transitions

```css
/* Fast - Micro-interactions */
transition: all 150ms cubic-bezier(0.4, 0.0, 0.2, 1);

/* Base - Default */
transition: all 250ms cubic-bezier(0.4, 0.0, 0.2, 1);

/* Slow - Complex animations */
transition: all 400ms cubic-bezier(0.4, 0.0, 0.2, 1);
```

---

## Breakpoints

- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px - 1439px
- Large: 1440px+

---

## CSS Variables Quick Copy

```css
:root {
  /* Colors */
  --mookee-teal: #83ADA4;
  --mookee-deep-teal: #62837C;
  --mookee-charcoal: #48625C;
  --mookee-off-white: #F5F5F5;
  --mookee-white: #FFFFFF;
  
  /* Typography */
  --font-primary: 'Inter', sans-serif;
  --font-display: 'Poppins', sans-serif;
  
  /* Spacing */
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  
  /* Borders */
  --radius-md: 8px;
  --radius-lg: 12px;
}
```

---

## Tailwind Classes Quick Reference

```jsx
/* Primary Button */
className="bg-[#83ADA4] text-white px-6 py-3 rounded-lg font-medium hover:bg-[#62837C]"

/* Card */
className="bg-white rounded-xl p-6 border border-[#EAEAEA] shadow-md"

/* Input */
className="w-full px-4 py-3 rounded-lg border-2 border-[#EAEAEA] focus:border-[#83ADA4]"

/* Heading */
className="text-3xl font-bold text-[#48625C]"

/* Body Text */
className="text-base text-[#48625C]"
```

---

## Common Color Combinations

### Light Theme (Default)
- Background: `#F5F5F5`
- Surface: `#FFFFFF`
- Text: `#48625C`
- Primary: `#83ADA4`

### Dark Theme
- Background: `#48625C`
- Surface: `#32403D`
- Text: `#FFFFFF`
- Primary: `#83ADA4`

### Hover States
- Button: `#83ADA4` → `#62837C`
- Link: `#62837C` → `#83ADA4`
- Card: increase shadow

---

## Accessibility Checklist

✅ Charcoal on Off-White = 7.8:1 (AAA)
✅ Deep Teal on Off-White = 5.2:1 (AA)
✅ White on Charcoal = 7.8:1 (AAA)
⚠️ Mookee Teal on White = 2.9:1 (Large text only)
⚠️ Light Teal on White = Insufficient (Don't use for text)

### Focus States
- Always show focus indicators
- Use: `outline: 2px solid #83ADA4; outline-offset: 2px;`

### Touch Targets
- Minimum 44×44px for mobile
- 48×48px preferred

---

## Logo Usage

### Variations
1. Full logo (with wordmark) - Primary
2. Icon in circle - App icons
3. Icon only - Favicons
4. Wordmark only - Text contexts

### Clear Space
- Minimum clear space = height of "M" in "MOOKEE"

### Minimum Sizes
- Digital: 32px height
- Print: 0.5 inches height

---

## File Exports Checklist

### Logo
- [ ] SVG (vector)
- [ ] PNG 512px, 256px, 128px, 64px, 32px
- [ ] Favicon ICO (32×32, 16×16)

### Brand Assets
- [ ] CSS variables file
- [ ] Color JSON
- [ ] Style guide PDF
- [ ] Component library

---

## Don'ts

❌ Don't use Light Teal for body text (insufficient contrast)
❌ Don't stretch or distort the logo
❌ Don't use colors outside the brand palette
❌ Don't use font sizes smaller than 14px for body text
❌ Don't remove focus indicators
❌ Don't use Mookee Teal text on Off-White backgrounds (use Deep Teal)

---

## Quick Start Commands

### Install Fonts (Web)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Import CSS Variables
```css
@import url('./mookee-variables.css');
```

### Import SCSS Variables
```scss
@import './mookee-variables.scss';
```

---

## Brand Personality

- **Approachable**: Friendly, never intimidating
- **Smart**: Intelligent without pretension
- **Reliable**: Dependable and trustworthy
- **Adaptable**: Flexible to user needs
- **Clear**: Simple, direct communication

---

## Support

For questions or additional brand assets:
- Refer to the full brand guide PDF
- Check mookee-colors.json for exact values
- See mookee-react-components for code examples

Version 1.0 | October 2025
