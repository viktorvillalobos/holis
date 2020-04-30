const BundleTracker = require('webpack-bundle-tracker')


const webpackFile = process.env.NODE_ENV === 'production' ? '../webapp/webpack-stats-prod.json' : '../webapp/webpack-stats.json'

module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/static/webapp/' : 'http://127.0.0.1:8080/',
  outputDir: './assets/webapp/',
  assetsDir: './',

  chainWebpack: config => {
    config.optimization
      .splitChunks(false)

    config
      .plugin('BundleTracker')
      .use(BundleTracker, [{ filename: webpackFile}])

    config.resolve.alias
      .set('__STATIC__', 'static')

    config.devServer
      .public('http://127.0.0.1:8080')
      .host('127.0.0.1')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['\*'] })

    if (config.plugins.has('extract-css')) {
      const extractCSSPlugin = config.plugin('extract-css')
      extractCSSPlugin && extractCSSPlugin.tap(() => [{
        filename: '[name].[hash].css',
        chunkFilename: '[name].[hash].css'
      }])
    }
  },
  configureWebpack: {
    output: {
      filename: '[name].[hash].js',
      chunkFilename: '[name].[hash].js'
    }
  }
}
