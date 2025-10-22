/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Mookee Brand Colors
        mookee: {
          teal: '#83ADA4',
          'deep-teal': '#62837C',
          charcoal: '#48625C',
          'light-teal': '#AEE9DC',
          mint: '#7AA79D',
          'dark-gray': '#32403D',
        },
        // Semantic colors
        primary: {
          DEFAULT: '#83ADA4',
          dark: '#62837C',
          light: '#AEE9DC',
        },
        secondary: {
          DEFAULT: '#7AA79D',
          dark: '#62837C',
        },
        neutral: {
          50: '#F5F5F5',
          100: '#EAEAEA',
          400: '#9B9B9B',
          700: '#48625C',
          900: '#32403D',
        },
        // Override default grays to match brand
        gray: {
          50: '#F5F5F5',
          100: '#EAEAEA',
          200: '#D5D5D5',
          300: '#B0B0B0',
          400: '#9B9B9B',
          500: '#7A7A7A',
          600: '#5A5A5A',
          700: '#48625C',
          800: '#32403D',
          900: '#1A1A1A',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
        display: ['Poppins', 'Arial', 'sans-serif'],
        mono: ['JetBrains Mono', 'Courier New', 'Courier', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1.4' }],      // 12px
        'sm': ['0.875rem', { lineHeight: '1.5' }],     // 14px
        'base': ['1rem', { lineHeight: '1.6' }],       // 16px
        'lg': ['1.125rem', { lineHeight: '1.6' }],     // 18px
        'xl': ['1.25rem', { lineHeight: '1.5' }],      // 20px
        '2xl': ['1.5rem', { lineHeight: '1.3' }],      // 24px
        '3xl': ['1.75rem', { lineHeight: '1.3' }],     // 28px
        '4xl': ['2.25rem', { lineHeight: '1.25' }],    // 36px
        '5xl': ['3rem', { lineHeight: '1.2' }],        // 48px
        '6xl': ['3.75rem', { lineHeight: '1.1' }],     // 60px
        '7xl': ['4.5rem', { lineHeight: '1.1' }],      // 72px
      },
      spacing: {
        '18': '4.5rem',   // 72px
        '88': '22rem',    // 352px
        '128': '32rem',   // 512px
      },
      borderRadius: {
        'sm': '4px',
        'DEFAULT': '8px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        '2xl': '20px',
        '3xl': '24px',
      },
      boxShadow: {
        'sm': '0 1px 2px rgba(72, 98, 92, 0.05)',
        'DEFAULT': '0 2px 8px rgba(72, 98, 92, 0.08)',
        'md': '0 2px 8px rgba(72, 98, 92, 0.08)',
        'lg': '0 4px 16px rgba(72, 98, 92, 0.12)',
        'xl': '0 8px 32px rgba(72, 98, 92, 0.16)',
        '2xl': '0 12px 48px rgba(72, 98, 92, 0.20)',
        'inner': 'inset 0 2px 4px rgba(72, 98, 92, 0.06)',
        'none': 'none',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
      transitionDuration: {
        '150': '150ms',
        '250': '250ms',
        '400': '400ms',
      },
      transitionTimingFunction: {
        'in-out': 'cubic-bezier(0.4, 0.0, 0.2, 1)',
        'out': 'cubic-bezier(0.0, 0.0, 0.2, 1)',
        'in': 'cubic-bezier(0.4, 0.0, 1, 1)',
      },
      maxWidth: {
        'container': '1200px',
        'narrow': '760px',
      },
      zIndex: {
        'base': '1',
        'dropdown': '100',
        'sticky': '200',
        'fixed': '300',
        'modal-backdrop': '400',
        'modal': '500',
        'popover': '600',
        'tooltip': '700',
      },
    },
  },
  plugins: [
    // Add custom utilities
    function({ addUtilities }) {
      const newUtilities = {
        '.text-balance': {
          'text-wrap': 'balance',
        },
        '.container-narrow': {
          'max-width': '760px',
          'margin-left': 'auto',
          'margin-right': 'auto',
          'padding-left': '1.5rem',
          'padding-right': '1.5rem',
        },
      }
      addUtilities(newUtilities)
    },
  ],
}
