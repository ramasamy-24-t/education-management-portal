/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        public: "#dbeafe",
        academic: "#ffedd5",
        user: "#dcfce7",
        admin: "#ede9fe",
        reports: "#e5e7eb",
      },
    },
  },
  plugins: [],
};
