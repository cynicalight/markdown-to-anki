# Markdown to Anki Converter

将Markdown文档中的标记内容转换为Anki闪卡的工具集，包含命令行版本和Obsidian插件版本。

## 🎯 两种使用方式

### 1. 命令行脚本版本
- [markdown-to-anki](https://github.com/cynicalight/markdown-to-anki)
- **文件**: `md_to_anki.py`
- **功能**: 独立的Python脚本，可处理任意Markdown文件
- **优势**: 无需依赖特定编辑器，适合批处理

### 2. Obsidian插件版本 (TypeScript)
- [markdown-to-anki-converter](https://github.com/cynicalight/Markdown-to-Anki-Converter)
- **功能**: 直接在Obsidian中处理当前文档

### 2. Obsidian插件版本  
直接在Obsidian中使用，无需切换应用，一键处理当前文档。

## 开发目的

在**英语学习**过程中，我们经常会在阅读材料中标记重要的生词、词组和好句子并尝试记忆。本项目旨在自动化将这些标记内容转换为Anki闪卡，提高学习效率，让知识积累更加系统化。

- 不止英语学习，可以根据需要自行修改prompt，生成其他类型的闪卡，比如名词解释等。

主要解决的问题：
- 手动制作闪卡效率低下
- 标记的学习内容容易遗忘
- 缺乏系统化的复习机制
- 翻译查询重复性工作耗时

## 基本功能

### 1. 标记内容识别
- **加粗文本** (`**word**`) - 识别为生词
- *斜体文本* (`*phrase*`) - 识别为词组
- ==高亮文本== (`==sentence==`) - 识别为句子

### 2. 智能翻译
- 集成DeepSeek API，提供上下文相关的翻译
- 生词翻译：提供在特定句子中的含义
- 词组翻译：考虑上下文语境的准确翻译
- 句子翻译：自然流畅的中文翻译

### 3. Anki闪卡生成
- 生词闪卡：正面显示单词，背面显示含义+例句
- 词组闪卡：正面显示词组，背面显示含义+例句  
- 句子闪卡：正面显示英文句子，背面显示中文翻译
- 支持HTML格式，美观的卡片布局

### 4. 批量处理
- 一次性处理整个Markdown文档
- 自动去重，避免重复内容
- 进度显示，实时了解处理状态

## 文件结构

```
md-to-anki/
├── md_to_anki.py          # 主程序脚本（命令行版本）
├── requirements.txt       # Python依赖包
├── README.md             # 项目说明文档
├── Getting girlhood right.md  # 示例Markdown文档
├── obsidian-plugin/       # Obsidian插件版本
│   ├── main.ts           # 插件主代码
│   ├── manifest.json     # 插件清单
│   ├── package.json      # 依赖配置
│   ├── README.md         # 插件说明
│   └── INSTALL.md        # 安装指南
└── output/               # 输出文件目录（生成）
    └── *.txt            # 生成的Anki闪卡文件
```

### 核心模块说明

#### `DeepSeekAPI` 类
- **功能**: 封装DeepSeek API调用
- **主要方法**:
  - `translate_word()`: 翻译生词，返回含义和例句
  - `translate_phrase()`: 翻译词组，考虑上下文
  - `translate_sentence()`: 翻译完整句子
  - `_make_request()`: 统一的API请求处理

#### `MarkdownParser` 类  
- **功能**: 解析Markdown文档，提取标记内容
- **主要方法**:
  - `extract_bold_text()`: 提取加粗文本及其句子上下文
  - `extract_italic_text()`: 提取斜体文本及其句子上下文
  - `extract_highlighted_text()`: 提取高亮文本
  - `_get_sentence_context()`: 智能获取词汇所在的完整句子

#### `AnkiCardGenerator` 类
- **功能**: 生成Anki闪卡并导出
- **主要方法**:
  - `process_bold_words()`: 处理生词，生成词汇卡片
  - `process_italic_phrases()`: 处理词组，生成短语卡片
  - `process_highlighted_sentences()`: 处理句子，生成翻译卡片
  - `export_to_anki()`: 导出为Anki可导入的txt格式

## 安装和使用

### 命令行版本

#### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd md-to-anki

# 安装依赖
pip install -r requirements.txt
```

#### 2. 配置API密钥

获取DeepSeek API密钥并设置环境变量：

```bash
# macOS/Linux
export DEEPSEEK_API_KEY="your_api_key_here"

# Windows
set DEEPSEEK_API_KEY=your_api_key_here
```

#### 3. 准备Markdown文档

在Markdown文档中使用以下格式标记学习内容：

```markdown
# 英语学习材料

这是一个**important**的*key phrase*。

==This is a good sentence that I want to remember.==

另一个**vocabulary**出现在这个句子中。
```

#### 4. 运行脚本

```bash
python3 md_to_anki.py your_document.md
```

### Obsidian插件版本

#### 1. 安装插件

详细安装步骤请查看：[obsidian-plugin/INSTALL.md](obsidian-plugin/INSTALL.md)

#### 2. 配置和使用

1. 在Obsidian设置中配置DeepSeek API密钥
2. 在Markdown文档中标记学习内容
3. 使用命令面板搜索"转换当前文件为Anki闪卡"
4. 等待处理完成

### 5. 导入Anki（通用步骤）

1. 打开Anki桌面版
2. 选择"文件" → "导入"
3. 选择生成的 `*_anki_cards.txt` 文件
4. 确认导入设置（分隔符：制表符，允许HTML）
5. 完成导入

## 输出格式示例

生成的Anki闪卡文件格式：

```
#separator:tab
#html:true

subordinate	adj. 下级的，次要的<br><br><i>Or, at best, subordinate people, required to obey their fathers.</i>
vaccine	n. 疫苗<br><br><i>Even fewer imagined that a girl could grow up to govern Germany, run the IMF or invent a vaccine.</i>
in field after field	在各个领域<br><br><i>In field after field girls have caught up with boys.</i>
Fifty years ago only 49% of primary-school-age girls in lower-middle-income countries were in school, compared with 71% of boys; today the share of both is about 90%.	50年前，中低收入国家小学学龄女孩的入学率仅为49%，而男孩为71%；如今，两者的比例都达到了90%左右。
```

## 注意事项

1. **API调用频率**: 脚本在API调用间加入了1秒延迟，避免触发频率限制
2. **网络连接**: 需要稳定的网络连接以调用翻译API
3. **文件编码**: 确保Markdown文件使用UTF-8编码
4. **标记格式**: 严格按照指定格式标记内容（`**bold**`, `*italic*`, `==highlight==`）

## 常见问题

### Q: API调用失败怎么办？
A: 检查API密钥是否正确设置，网络连接是否正常，API余额是否充足。

### Q: 生成的翻译不准确？
A: 可以手动编辑生成的txt文件，或调整API的提示词以获得更好的翻译质量。

### Q: 如何处理大文档？
A: 脚本支持大文档处理，但建议分段处理以避免API超时。

### Q: 闪卡重复怎么办？
A: Anki导入时会自动检测重复内容，可以选择跳过或更新。

## 开发计划

- [ ] 支持更多标记格式（如下划线、删除线）
- [ ] 添加GUI界面
- [ ] 支持批量处理多个文件
- [ ] 集成更多翻译API选项
- [ ] 添加闪卡模板自定义功能
- [ ] 支持音频文件生成（TTS）

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License
