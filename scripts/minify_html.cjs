const fs = require('node:fs');
const { minify } = require('html-minifier-terser');

const options = {
  collapseWhitespace: true,
  conservativeCollapse: true,
  removeComments: false,
  removeAttributeQuotes: false,
  removeOptionalTags: false,
  minifyCSS: { level: 1, rebase: false },
  minifyJS: false,
  minifyURLs: false,
};

if (require.main === module) {
  minify(fs.readFileSync(0, 'utf8'), options)
    .then(output => process.stdout.write(output))
    .catch(error => {
      process.stderr.write(error.message + '\n');
      process.exitCode = 1;
    });
}

module.exports = { options };
