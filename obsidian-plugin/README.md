# Markdown to Anki - Obsidian Plugin

将Markdown文档中的标记内容（**加粗**、*斜体*、==高亮==）自动转换为Anki闪卡的Obsidian插件。

## ✨ 主要功能

- **生词提取**：识别加粗文本（`**word**`），调用API翻译并生成卡片
- **词组识别**：识别斜体文本（`*phrase*`），获取上下文翻译  
- **句子收集**：识别高亮文本（`==sentence==`），整句翻译
- **智能翻译**：集成DeepSeek API，提供准确的中英翻译
- **批量导出**：一键生成Anki可导入的txt格式文件
- **路径灵活**：支持相对路径和绝对路径输出

## 🚀 快速开始

### 安装

1. 下载最新release中的文件：
   - `main.js`
   - `manifest.json` 
   - `styles.css`

2. 在Obsidian vault中创建文件夹：`.obsidian/plugins/markdown-to-anki/`

3. 将下载的文件复制到该文件夹中

4. 重启Obsidian并在设置中启用插件

### 配置

1. 在插件设置中配置DeepSeek API密钥
2. 设置输出路径（可选）
3. 选择要处理的标记类型

### 使用方法

1. 在Markdown文档中使用标记：
   - `**生词**` - 加粗标记生词
   - `*词组*` - 斜体标记词组
   - `==好句子==` - 高亮标记句子

2. 打开命令面板（Ctrl/Cmd + P）

3. 运行命令："Generate Anki Cards"

4. 等待处理完成，获取生成的txt文件

5. 将txt文件导入Anki

## ⚙️ 设置选项

- **API密钥**：DeepSeek API密钥设置
- **输出路径**：自定义输出路径（支持绝对路径如 `/Users/username/Downloads`）
- **处理选项**：
  - 处理加粗文本（生词）
  - 处理斜体文本（词组）
  - 处理高亮文本（句子）

## 📝 示例

输入Markdown：
```markdown
The **algorithm** *runs efficiently* and ==produces accurate results==.
```

生成的Anki卡片：
1. 正面：`algorithm` | 反面：`算法<br><br>The algorithm runs efficiently and produces accurate results.`
2. 正面：`runs efficiently` | 反面：`高效运行<br><br>The algorithm runs efficiently and produces accurate results.`
3. 正面：`produces accurate results` | 反面：`产生准确的结果`

## 🔧 开发

### 构建插件

```bash
npm install
npm run build
```

### 开发模式

```bash
npm run dev
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issues和Pull Requests！

## 📞 支持

如有问题，请在GitHub Issues中反馈。
