const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const isDev = process.env.NODE_ENV === 'development';

module.exports = [
  // Main process (Electron)
  {
    mode: isDev ? 'development' : 'production',
    entry: './main.js',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: 'main.js',
      pathinfo: false
    },
    devtool: isDev ? 'source-map' : false,
    target: 'electron-main',
    resolve: {
      extensions: ['.ts', '.js', '.json']
    },
    externals: {
      'electron': 'commonjs electron'
    }
  },
  // Renderer process (React)
  {
    mode: isDev ? 'development' : 'production',
    entry: {
      renderer: './src/renderer/index.tsx'
    },
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: '[name].js',
      publicPath: './' // Use relative paths for file:// protocol
    },
    devtool: isDev ? 'source-map' : false,
    target: 'web',
    module: {
      rules: [
        {
          test: /\.tsx?$/,
          use: 'ts-loader',
          exclude: /node_modules/
        },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader']
        }
      ]
    },
    resolve: {
      extensions: ['.ts', '.tsx', '.js', '.json'],
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: './src/renderer/index.html',
        chunks: ['renderer'],
        minify: !isDev
      })
    ],
    devServer: {
      port: 3000,
      hot: true,
      historyApiFallback: true,
      client: {
        overlay: true
      }
    }
  }
];
