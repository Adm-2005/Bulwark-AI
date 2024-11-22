/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
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

