const path = require('path');

module.exports = {
  entry: './src/main.js',
  mode: 'production',
  output: {
    filename: 'hui-element.js',
    path: path.resolve(__dirname)
  }
};
