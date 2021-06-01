const BundleTracker = require('webpack-bundle-tracker')

const webpackFile = process.env.NODE_ENV === 'production' ? '../webapp/webpack-stats-prod.json' : 'webpack-stats.json'

module.exports = {
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production' ? '/static/bundle_webapp/' : 'http://holis.local:8080/',
  outputDir: './assets/bundle_webapp/',
  assetsDir: 'assets/',

  css: {
    loaderOptions: {
      scss: {
        prependData: '@import "~@/_import.scss";'
      }
    }
  },

  devServer: {
    disableHostCheck: true,
    overlay: {
      warnings: true,
      errors: true
    }
  },

  chainWebpack: config => {
    config.optimization
      .splitChunks(false)

    config
      .plugin('BundleTracker')
      .use(BundleTracker, [{ filename: webpackFile }])

    config.resolve.alias
      .set('__STATIC__', 'static')

    config.devServer
      .public('http://0.0.0.0:8080')
      .host('0.0.0.0')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['*'] })

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
  },

  lintOnSave: false
}
