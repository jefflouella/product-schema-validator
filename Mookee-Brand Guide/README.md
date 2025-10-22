# Mookee Brand Style Guide Package

Welcome to your complete Mookee brand style guide! This package contains everything you need to maintain consistent branding across all your applications.

## 📦 What's Included

### Documentation Files
1. **mookee-brand-guide.md** (11KB)
   - Comprehensive brand guidelines
   - Logo system, colors, typography, components
   - Voice & tone, accessibility guidelines
   - Photography, motion, and layout principles

2. **QUICK-REFERENCE.md** (6KB)
   - Quick lookup cheat sheet
   - Most commonly used values
   - Code snippets and examples
   - Perfect for developers

3. **IMPLEMENTATION-GUIDE.md** (11KB)
   - Step-by-step implementation instructions
   - Framework-specific examples (CSS, Tailwind, React)
   - Migration guide from existing brands
   - Troubleshooting tips

### Implementation Files
4. **mookee-variables.css** (8.4KB)
   - CSS custom properties (CSS variables)
   - Ready to use in any web project
   - Includes utility classes

5. **mookee-variables.scss** (5.8KB)
   - SCSS/SASS variables and mixins
   - For projects using Sass preprocessor
   - Includes helpful mixins

6. **mookee-colors.json** (4.3KB)
   - Color definitions in multiple formats
   - Import into Figma, Sketch, Adobe XD
   - Includes RGB, HEX, HSL, CMYK values

7. **mookee-tailwind-config.js** (4.8KB)
   - Tailwind CSS configuration
   - Drop-in replacement for your config
   - Custom Mookee theme

8. **mookee-react-components.txt** (851B)
   - React component examples
   - Copy-paste ready components
   - Styled with Mookee brand

---

## 🚀 Quick Start (Choose Your Path)

### Path 1: CSS Variables (Easiest)
Perfect for: Any web project, WordPress, static sites

1. Link the CSS file:
```html
<link rel="stylesheet" href="mookee-variables.css">
```

2. Use the variables:
```css
.button {
  background: var(--mookee-teal);
  color: white;
  padding: var(--space-md);
}
```

### Path 2: Tailwind CSS
Perfect for: React, Next.js, Vue projects using Tailwind

1. Replace your `tailwind.config.js` with `mookee-tailwind-config.js`
2. Use Mookee classes:
```jsx
<button className="bg-mookee-teal text-white px-6 py-3 rounded-lg">
  Click Me
</button>
```

### Path 3: SCSS/SASS
Perfect for: Projects already using Sass

1. Import variables:
```scss
@import './mookee-variables.scss';
```

2. Use variables and mixins:
```scss
.button {
  @include button-base;
  background: $mookee-teal;
}
```

---

## 🎨 Brand Essentials

### Primary Colors
- **Mookee Teal**: `#83ADA4` - Your primary brand color
- **Deep Teal**: `#62837C` - Text and hover states
- **Charcoal**: `#48625C` - Body text

### Typography
- **Primary Font**: Inter (body text, UI)
- **Display Font**: Poppins (headlines)

### Logo
- Your pigeon logo represents adaptability, intelligence, and reliability
- Use the full logo with wordmark for primary branding
- Icon-only version for app icons and favicons

---

## 📖 Where to Start

### 1. Designers
Start here → **mookee-brand-guide.md**
- Read the complete brand guidelines
- Import **mookee-colors.json** into your design tool
- Reference for all design decisions

### 2. Developers
Start here → **IMPLEMENTATION-GUIDE.md**
- Choose your framework (CSS, Tailwind, or SCSS)
- Follow step-by-step implementation
- Use **QUICK-REFERENCE.md** for daily lookups

### 3. Product Managers
Start here → **QUICK-REFERENCE.md**
- Understand brand personality and voice
- Review component patterns
- Reference for product decisions

---

## 🛠️ Design Tool Setup

### Figma
1. Import colors from **mookee-colors.json**
2. Install Inter and Poppins fonts
3. Create components matching the style guide
4. Share library with your team

### Adobe XD / Photoshop / Illustrator
1. Create color swatches from **mookee-colors.json**
2. Install fonts on your system
3. Reference typography scale from brand guide

### Sketch
1. Add colors as document colors
2. Create text and layer styles
3. Build symbol library

---

## ✅ Implementation Checklist

### Week 1: Setup
- [ ] Read the brand guide
- [ ] Choose implementation method
- [ ] Install fonts
- [ ] Set up color variables
- [ ] Create first branded component (button)

### Week 2: Core Components
- [ ] Implement buttons (primary, secondary, ghost)
- [ ] Create card components
- [ ] Build form elements (inputs, selects)
- [ ] Design navigation components
- [ ] Test accessibility

### Week 3: Refinement
- [ ] Apply to all existing components
- [ ] Test responsive behavior
- [ ] Verify color contrast
- [ ] Get stakeholder approval
- [ ] Document any customizations

### Week 4: Rollout
- [ ] Deploy to production
- [ ] Update all applications
- [ ] Train team members
- [ ] Create internal documentation
- [ ] Monitor for issues

---

## 🎯 Key Principles

### Consistency
Use the brand guidelines consistently across all applications. Don't deviate from the color palette or typography scale.

### Accessibility
- Maintain 4.5:1 contrast ratio for text
- Use semantic HTML
- Include focus states
- Ensure 44×44px touch targets on mobile

### Simplicity
Keep designs clean and uncluttered. The Mookee brand is about smart simplicity.

### Adaptability
The brand should feel at home on web, mobile, and any platform. Use the responsive guidelines.

---

## 📚 File Usage Guide

| File | When to Use |
|------|-------------|
| **mookee-brand-guide.md** | Complete reference, design decisions, new team members |
| **QUICK-REFERENCE.md** | Daily development, quick lookups, common patterns |
| **IMPLEMENTATION-GUIDE.md** | Initial setup, migration, troubleshooting |
| **mookee-variables.css** | HTML/CSS projects, WordPress, static sites |
| **mookee-variables.scss** | Sass/SCSS projects, custom build processes |
| **mookee-tailwind-config.js** | Tailwind CSS projects (React, Next.js, Vue) |
| **mookee-colors.json** | Design tools (Figma, Sketch, XD), documentation |
| **mookee-react-components.txt** | React projects, component library creation |

---

## 💡 Pro Tips

### For Developers
- Always use the spacing scale (4px, 8px, 16px, 24px...)
- Keep the QUICK-REFERENCE.md open while coding
- Use CSS variables for easy theme changes
- Test on mobile devices early and often

### For Designers
- Start with the logo and color palette
- Use the typography scale consistently
- Design with accessibility in mind
- Create reusable components

### For Teams
- Share the brand guide with everyone
- Use consistent naming (e.g., "Mookee Teal" not "teal")
- Review new designs against the guidelines
- Update the guide as the brand evolves

---

## 🔍 Common Questions

**Q: Can I add new colors to the palette?**
A: Try to work within the existing palette first. If you need a new color, ensure it complements the existing palette and maintains accessibility standards.

**Q: What if the fonts aren't loading?**
A: Check that you've included the Google Fonts link in your HTML head. For local fonts, ensure the font files are properly referenced.

**Q: How do I handle dark mode?**
A: See the "Dark Mode Implementation" section in IMPLEMENTATION-GUIDE.md for CSS variables and Tailwind approaches.

**Q: Can I use these files with [framework]?**
A: Yes! The CSS variables work with any framework. React, Vue, Angular, Svelte - all work great with these files.

**Q: What about mobile apps (iOS/Android)?**
A: Use the color values from mookee-colors.json. The spacing scale and typography principles apply to native apps too.

---

## 📞 Support

### Need Help?
1. Check **IMPLEMENTATION-GUIDE.md** for troubleshooting
2. Review **mookee-brand-guide.md** for design questions
3. Search **QUICK-REFERENCE.md** for specific values

### Found an Issue?
Document any inconsistencies or problems and discuss with your team to update the guidelines.

### Want to Contribute?
If you create new components or patterns that follow the brand guidelines, consider adding them to your internal component library.

---

## 🎉 You're Ready!

You now have everything you need to implement the Mookee brand consistently across all your applications. Start with the IMPLEMENTATION-GUIDE.md and you'll be up and running in no time.

**Remember**: Consistency is key. When in doubt, refer back to these guidelines.

---

**Mookee Brand Style Guide v1.0**
Created: October 22, 2025

*Building reliable, approachable, and smart experiences.*
