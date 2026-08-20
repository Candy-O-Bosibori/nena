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
      colors: {
        'primary':'#F25019',
        'secondary':'#FFEEE3',
        'read':'#BBC53B',
        'read':'#FFC107',
        'read':'#F25019'// 39%
      },
      fontFamily:{
        'body':"Open Sans"
      }
    },
  },
  plugins: [],
}