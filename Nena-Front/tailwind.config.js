/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      boxShadow: {
        'md': '0 0 10px rgba(0, 0, 0, 0.1)',
      },
      // Color and font tokens now live in src/index.css via @theme (Tailwind v4).
      // Nena is single-hue: #DC9750 (--color-primary-500) plus its tints/shades,
      // with --color-danger as the one deliberate exception for destructive/
      // warning states.
    },
  },
  plugins: [],
}