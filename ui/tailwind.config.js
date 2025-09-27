/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: '#0d1117',                // deep space background
        panel: '#161b22',             // sidebar / panel contrast
        muted: '#1e293b',             // muted sections (code blocks, etc.)
        primary: '#14b8a6',             // turquoise highlight (buttons, links)
        'primary-foreground': '#eafdfc', // very light aqua/white for text on turquoise
        accent: '#10b981',            // constellation violet/indigo
        text: '#e5e7eb',
        'text-muted': '#9ca3af',    
        border: '#232a36', 
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

