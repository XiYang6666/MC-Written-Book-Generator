# MC 成书生成器

一个用于在 Minecraft 中使用文本文件生成成书的 Python 工具. 如果文本太长, 它会自动将成书分成多卷. 该工具支持各种自定义选项, 例如指定编码格式,成书名和作者.

[中文](README.md) | [English](docs/README-en.md)

## Roadmap

- [ ] 使用 Unifont 获取宽度而非硬编码.
- [ ] 更友好的操作逻辑.
- [ ] 支持浏览, 编辑排版.
- [ ] 提供更友好的代码库.

## 用法

### 方法 1：使用 UI 快捷方式

1.运行脚本 `install.bat`(Windows)或`install.sh`(类 Unix 系统) 以安装依赖项.

2.安装完成后, 运行脚本 `ui.bat` (Windows)或`ui.sh`(类 Unix 系统) 打开图形用户界面.

### 方法 2：手动使用命令行

#### 1. 通过执行以下命令创建并激活虚拟环境

Windows:

```bash
python-m venv.venv
.venv\Scripts\activate
```

类 Unix 系统:

```bash
python-m venv.venv
source.venv/bin/activate
```

#### 2.激活虚拟环境后, 使用以下 bash 命令来使用该工具

```bash
python main.py <text_file_path> [-e <encoding_format>] [-t <title>] [-a <author>]
```

- `<text_file_path>`：包含成书内容的文本文件的路径.
- `<encoding_format>`(可选)：文本文件的编码格式. 如果未指定, 则默认值为 utf-8. -`<title>`(可选)：成书的标题. 您可以在标题中使用占位符{volume}, 在生成过程中它将自动替换为卷号.
- `<author>`(可选)：成书的作者.

## 故障排除

如果在生成过程中遇到`ValueError: Width data without character“…”`, 则可以将该字符的宽度数据添加到**extended_Width.json**文件中.

## 自定义

可以通过导入此 Python 包, 并利用提供的接口自定义生成规则. 该包提供了以下类和方法:

- `create_book_collection`: 用于生成成书集合的方法.
- `Book`: 用于生成单个成书的类.
- `Page`: 用于生成书页的类.

你也可以随意使用此程序, 并根据您的需求定制生成过程.
