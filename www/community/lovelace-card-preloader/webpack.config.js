const path = require('path');

module.exports = {
  entry: './src/main.js',
  mode: 'production',
  devtool: false,
  output: {
    filename: 'lovelace-card-preloader.js',
    path: path.resolve(__dirname)
  }
};