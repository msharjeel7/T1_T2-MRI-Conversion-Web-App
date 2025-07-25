// This file tells PostCSS which plugins to use
// Exporting the configuration object so PostCSS can read it
module.exports = 
{
    // 'plugins' key defines which PostCSS plugins will be used
    plugins:
    {
         // This plugin adds Tailwind CSS support
        '@tailwindcss/postcss': {},
         // This plugin adds vendor prefixes to CSS (for browser compatibility)
        autoprefixer: {},
    },
}
