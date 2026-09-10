# Prototype Compressor

让包含大量内嵌图片的 HTML 原型显著瘦身。将 PNG/JPEG 转为 WebP，保留单文件结构，默认保留原始文件，仅依赖 Python 和 cwebp。

## 压缩效果

在一份内嵌图片占比约 98.3% 的 HTML 原型上实测：

| 版本 | 文件体积 | 相比原文件减少 |
| --- | ---: | ---: |
| 原文件 | 64.46 MB | — |
| WebP 质量 80 | 7.30 MB | 88.7% |
| WebP 质量 75 | 6.12 MB | 90.5% |

质量 75 相比质量 80 再减少约 1.18 MB（16.1%）。主要收益来自图片编码转换，无需压缩或重写页面代码。

默认质量为 **78**，可按图片细节需求调整。上表为质量 80 和 75 的历史实测，体积按十进制 MB 计算；实际收益取决于图片数量、格式和内容，不代表所有原型都能达到同样比例。

## 功能

- 保留 HTML/CSS/JS 文本、注释和空白，仅压缩内嵌图片。
- 内嵌 PNG/JPEG 转为质量 78 的 WebP，仅在图片变小时替换。
- 保留图片尺寸及 SVG，不引入外部资源文件。
- 输出压缩前后字节数、压缩比例和图片转换数量。
- 不进行重复图片引用去重，不压缩 JavaScript 代码。

默认质量为 78，输出为原文件同目录的 `*.min.html`。重复执行刷新该压缩副本，不追加版本号；默认保留原文件。使用 `--overwrite` 可直接覆盖源文件，此模式不生成副本或备份，原始图片数据将被替换；已有的 `*.min.html` 不会同步更新。

## 环境与运行

需要 Python 3.10+ 和 PATH 中的 `cwebp`，无需 Node.js/npm 依赖。macOS 可以通过 Homebrew 安装：

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

# 使用默认质量 78，直接覆盖源文件
python3 scripts/compress_prototype.py --overwrite /absolute/path/to/PROTO.html

# 生成不做图片转换的原样副本，用于对比，无需 cwebp
python3 scripts/compress_prototype.py --no-webp /absolute/path/to/PROTO.html
```

## 作为 Skill 使用

仓库根目录就是 Skill 目录，包含 `SKILL.md`、`scripts/` 和 `agents/`。将仓库克隆到个人 Skills 目录中的 `prototype-compressor` 子目录即可，例如：

```bash
git clone https://github.com/yujieying/prototype-compressor.git ~/.codex/skills/prototype-compressor
cd ~/.codex/skills/prototype-compressor
```

目标目录已经存在时，应先核对现有 Skill，再决定同步方式。也可以让 AI 直接读取本仓库的 `SKILL.md` 后执行。原型生成流程在保存 HTML 后调用此 Skill 即可。

## 使用边界

WebP 转换为有损压缩，建议抽查截图中的文字、细线和图片细节。工具保留图片尺寸，HTML/CSS/JS 除内嵌图片 data URI 外保持原样。需要更高保真度时可提高质量参数；需求变更后，继续修改原文件并重新压缩。

外链图片、SVG 和已有 WebP 不参与转换。以文本或已压缩资源为主的原型，体积下降可能有限。
