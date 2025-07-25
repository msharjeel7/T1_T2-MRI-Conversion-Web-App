/** 
 * This line is a TypeScript type annotation (used even in JS files) 
 * that tells your editor (like VS Code) to use Tailwind CSS's config type definition.
 * It enables IntelliSense (auto-complete & validation) for the Tailwind config object.
 */

/** @type {import('tailwindcss').Config} */

// This file tells Tailwind where the content files are and how to extend the theme
// Exporting the Tailwind configuration object
module.exports = 
{
    // Tell Tailwind which files to scan for class names
    content: ["./src/**/*.{js, jsx, ts, tsx,}"],

    // Customize the default Tailwind theme here
    theme:
    {
        // 'extend' is used to add (not override) custom styles like colors, fonts, spacing, etc.
        extend: {},
    },

    // Add Tailwind plugins here if needed (like forms, typography, etc.)
    plugins: [],
}
