/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: '#0b0f14',
        panel: '#12171f',
        muted: '#1a2130',
        primary: '#2f6feb',
        'primary-foreground': '#eaf1ff',
        accent: '#e95c5c',
        text: '#e6e9ef',
        'text-muted': '#b8c0cc',
        border: '#232a36',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

