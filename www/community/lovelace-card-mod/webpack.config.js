const path = require('path');

module.exports = {
  entry: './src/main.js',
  mode: 'production',
  output: {
    filename: 'card-mod.js',
    path: path.resolve(__dirname)
  }
};
