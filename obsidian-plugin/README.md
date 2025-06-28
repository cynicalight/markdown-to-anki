# Markdown to Anki Converter - Obsidian插件

将Obsidian中的Markdown文档标记内容自动转换为Anki闪卡的插件。

## 功能特点

### 🎯 智能识别标记内容
- **加粗文本** (`**单词**`) → 生词卡片
- *斜体文本* (`*词组*`) → 词组卡片  
- ==高亮文本== (`==句子==`) → 句子翻译卡片

### 🤖 AI驱动的翻译
- 集成DeepSeek API，提供上下文相关的准确翻译
- 生词翻译：考虑句子语境的精准含义
- 词组翻译：结合上下文的自然表达
- 句子翻译：流畅自然的中文翻译

### ⚡ 一键生成闪卡
- 直接在Obsidian中处理当前文件
- 实时显示处理进度
- 自动生成Anki可导入的txt文件
- 支持HTML格式的美观卡片布局

## 安装方法

### 方法一：手动安装（推荐）

1. 下载插件文件
   ```bash
   # 克隆仓库
   git clone <repository-url>
   cd md-to-anki/obsidian-plugin
   ```

2. 构建插件
   ```bash
   # 安装依赖
   npm install
   
   # 构建插件
   npm run build
   ```

3. 安装到Obsidian
   - 复制 `main.js`、`manifest.json`、`styles.css` 到 Obsidian 插件目录
   - 路径：`<Obsidian Vault>/.obsidian/plugins/md-to-anki-converter/`
   - 在Obsidian设置中启用插件

### 方法二：开发模式

1. 在插件目录中运行开发模式
   ```bash
   npm run dev
   ```

2. 插件会自动监听文件变化并重新构建

## 使用指南

### 1. 配置API密钥

首次使用需要配置DeepSeek API密钥：

1. 前往 [DeepSeek平台](https://platform.deepseek.com/) 获取API密钥
2. 在Obsidian设置 → 第三方插件 → Markdown to Anki Converter 中配置
3. 输入API密钥并保存

### 2. 标记学习内容

在Markdown文档中使用以下格式标记：

```markdown
# 英语学习笔记

这是一个**important**概念，它的*key phrase*很有用。

==This is a complete sentence that I want to remember.==

另一个**vocabulary**在这个句子中。

我想学习*in the meantime*这个词组。
```

### 3. 生成Anki卡片

1. 打开包含标记内容的Markdown文件
2. 使用命令面板（Ctrl/Cmd + P）搜索"转换当前文件为Anki闪卡"
3. 等待处理完成
4. 生成的txt文件会保存在指定目录

### 4. 导入Anki

1. 打开Anki桌面版
2. 选择"文件" → "导入"
3. 选择生成的 `*_anki_cards.txt` 文件
4. 确认导入设置：
   - 分隔符：制表符
   - 允许HTML：是
5. 完成导入

## 插件设置

### API配置
- **DeepSeek API密钥**：必填，用于调用翻译服务
- **输出文件路径**：可选，指定生成文件的保存位置

### 功能开关
- **生成生词卡片**：是否处理加粗文本
- **生成词组卡片**：是否处理斜体文本
- **生成句子卡片**：是否处理高亮文本

## 输出格式示例

生成的Anki闪卡文件格式：

```
#separator:tab
#html:true

important	adj. 重要的<br><br><i>这是一个important概念，它的key phrase很有用。</i>
key phrase	关键短语<br><br><i>这是一个important概念，它的key phrase很有用。</i>
This is a complete sentence that I want to remember.	这是一个我想记住的完整句子。
```

## 注意事项

1. **网络连接**：需要稳定的网络连接访问DeepSeek API
2. **API频率**：插件会自动在API调用间添加1秒延迟，避免频率限制
3. **文件编码**：确保Markdown文件使用UTF-8编码
4. **标记格式**：严格按照指定格式标记内容

## 常见问题

### Q: API调用失败怎么办？
A: 检查网络连接、API密钥是否正确、账户余额是否充足

### Q: 找不到标记内容？
A: 确认使用了正确的Markdown标记格式：`**bold**`、`*italic*`、`==highlight==`

### Q: 生成的翻译不准确？
A: 可以手动编辑生成的txt文件，或在设置中调整处理选项

### Q: 如何处理大文件？
A: 插件支持大文件处理，会显示实时进度。如遇超时，建议分段处理

## 技术架构

### 核心模块

1. **MarkdownParser**：解析Markdown内容，提取标记文本
2. **DeepSeekAPI**：封装API调用，处理翻译请求
3. **AnkiExporter**：生成Anki格式的输出文件
4. **ProcessingModal**：显示处理进度的模态框

### 工作流程

```
Markdown文档 → 解析标记 → API翻译 → 生成卡片 → 导出文件
```

## 开发计划

- [ ] 支持更多翻译API（OpenAI、Claude等）
- [ ] 添加自定义卡片模板
- [ ] 支持批量处理多个文件
- [ ] 添加缓存机制减少重复翻译
- [ ] 集成音频生成（TTS）功能

## 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置

```bash
# 安装依赖
npm install

# 开发模式（自动重新构建）
npm run dev

# 生产构建
npm run build
```

## 许可证

MIT License

## 致谢

- [Obsidian](https://obsidian.md/) - 强大的知识管理工具
- [DeepSeek](https://www.deepseek.com/) - 提供优秀的AI翻译服务
- [Anki](https://apps.ankiweb.net/) - 优秀的间隔重复学习软件
