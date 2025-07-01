module.exports = {
  content: [
    "./index.html",
    "./index.jsx",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      boxShadow: {
        neumorphism:
          '10px 10px 30px #d1d9e6, -10px -10px 30px #ffffff',
        'neumorphism-dark':
          '10px 10px 30px #1c1f2a, -10px -10px 30px #2a2e3c',
      },
    },
  },
  plugins: [],
};
