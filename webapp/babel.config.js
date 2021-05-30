module.exports = api => {
  const babelEnv = api.env()

  const plugins = []

  if (babelEnv === 'production') {
    plugins.push(['transform-remove-console', { exclude: ['error', 'warn'] }])
  }

  return {
    presets: [
      '@vue/cli-plugin-babel/preset'
    ],
    plugins: plugins
  }
}
