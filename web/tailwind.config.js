module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#1c1917",
        paper: "#f7f3eb",
        panel: "#fffdf8",
        rule: "#e7e0d4",
        accent: "#0f766e",
        warn: "#b45309",
      },
      fontFamily: {
        display: [
          '"Iowan Old Style"',
          '"Palatino Linotype"',
          "Palatino",
          "Georgia",
          "serif",
        ],
        body: ['"Source Sans 3"', '"Segoe UI"', "system-ui", "sans-serif"],
        mono: ['"IBM Plex Mono"', "ui-monospace", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};
