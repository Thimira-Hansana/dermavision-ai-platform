/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0E1A24",
        sand: "#F4EDE1",
        ember: "#D1683F",
        sage: "#88A17A",
        mist: "#DCE8EE",
        slate: "#35506B",
      },
      fontFamily: {
        display: ["Fraunces", "Georgia", "serif"],
        body: ["Space Grotesk", "Segoe UI", "sans-serif"],
      },
      boxShadow: {
        panel: "0 20px 60px rgba(15, 22, 34, 0.14)",
      },
      backgroundImage: {
        halo: "radial-gradient(circle at top left, rgba(209,104,63,0.24), transparent 35%), radial-gradient(circle at bottom right, rgba(136,161,122,0.24), transparent 30%)",
      },
    },
  },
  plugins: [],
};
