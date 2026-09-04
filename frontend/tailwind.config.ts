import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0b1120",
        surface: "#1e293b",
        "surface-light": "#334155",
        primary: {
          50: "#ecfeff",
          500: "#06b6d4",
          600: "#0891b2",
          700: "#0e7490",
        },
        clinical: {
          nodr: "#10b981",
          mild: "#06b6d4",
          moderate: "#f59e0b",
          severe: "#f97316",
          pdr: "#ef4444",
        }
      },
    },
  },
  plugins: [],
};

export default config;
