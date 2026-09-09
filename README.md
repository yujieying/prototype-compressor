# Prototype Compressor

将单文件 HTML 原型压缩为同目录的 `*.min.html`，用于发送同事或上传预览。原文件保留，重复执行会刷新压缩副本，不生成版本号。

## 功能

- 压缩 HTML/CSS 注释和格式空白。
- 内嵌 PNG/JPEG 转为质量 80 的 WebP，仅在图片变小时替换。
- 保留图片尺寸及 SVG，不引入外部资源文件。
- 输出压缩前后字节数、压缩比例和图片转换数量。
- 不进行重复图片引用去重，不压缩 JavaScript 代码。

## 环境与运行

需要 Python 3.10+；默认图片转换还需要 `cwebp` 在 PATH 中。macOS 可以通过 Homebrew 安装：

```bash
brew install webp
git clone https://github.com/yujieying/prototype-compressor.git
cd prototype-compressor
python3 scripts/compress_prototype.py /absolute/path/to/PROTO.html
```

其他运行方式：

```bash
# 提高图片质量
python3 scripts/compress_prototype.py --webp-quality 90 /absolute/path/to/PROTO.html

# 仅压缩 HTML/CSS，不转换图片，无需 cwebp
python3 scripts/compress_prototype.py --no-webp /absolute/path/to/PROTO.html
```

## 作为 Skill 使用

仓库根目录就是 Skill 目录，包含 `SKILL.md`、`scripts/` 和 `agents/`。将仓库克隆到个人 Skills 目录中的 `prototype-compressor` 子目录即可，例如：

```bash
git clone https://github.com/yujieying/prototype-compressor.git ~/.codex/skills/prototype-compressor
```

目标目录已经存在时，应先核对现有 Skill，再决定同步方式。也可以让 AI 直接读取本仓库的 `SKILL.md` 后执行。原型生成流程在保存 HTML 后调用此 Skill 即可。

## 使用边界

WebP 质量 80 为有损压缩，输出应抽查图片和交互。当前 HTML/CSS 压缩使用正则处理，并非完整语法解析器，特殊 CSS 字符串、空白语义等场景仍可能受影响，不能保证任意 HTML 的渲染完全一致。需求变更应继续修改原文件，再重新压缩。

上传服务若扫描所有 `*.html`，需明确选择压缩副本，避免同时上传原版。`html.md` 附件命名由上传流程处理，本工具不负责上传或改名。
