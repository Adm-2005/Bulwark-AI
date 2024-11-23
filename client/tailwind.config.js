/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  safelist: [
    'bg-primary',
    'bg-secondary',
    'bg-accent',
    'border-primary',
    'border-secondary',
    'border-accent'
  ],
  theme: {
    extend: {
      colors: {
        primary: "#536FFF",
        secondary: "#FFAE52",
        accent: "#53FFD6"
      },
      fontFamily: {
        poppins: ["Poppins", "sans-serif"]
      }
    },
  },
  plugins: [],
}

