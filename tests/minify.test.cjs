const test = require('node:test');
const assert = require('node:assert/strict');
const { minify } = require('html-minifier-terser');
const { options } = require('../scripts/minify_html.cjs');

test('保留 calc 运算符空格、CSS 文本、预格式文本和脚本', async () => {
  const script = 'const text = "a  b"; // 保留脚本\n';
  const html = '<style>.x { width: calc(100% + 10px); } .x::before { content: "a  b"; }</style>' +
    '<pre>a  b\n c</pre><textarea>a  b\n c</textarea><script>' + script + '</script>';
  const result = await minify(html, options);
  assert.ok(result.includes('calc(100% + 10px)'));
  assert.ok(result.includes('"a  b"'));
  assert.ok(result.includes('<pre>a  b\n c</pre>'));
  assert.ok(result.includes('<textarea>a  b\n c</textarea>'));
  assert.equal(result.match(/<script>([\s\S]*?)<\/script>/)[1].trim(), script.trim());
});

test('保留标记注释以及行内元素之间的空格', async () => {
  const result = await minify('<!-- PROTO_MARKER --><span>甲</span>  <span>乙</span>', options);
  assert.ok(result.includes('<!-- PROTO_MARKER -->'));
  assert.ok(result.includes('</span> <span>'));
});
