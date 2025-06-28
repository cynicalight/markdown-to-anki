#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to Anki Converter
将Markdown文档中的标记内容转换为Anki闪卡的脚本

功能：
1. 提取加粗文本（生词）- 调用API翻译并生成闪卡
2. 提取斜体文本（词组）- 调用API翻译并生成闪卡  
3. 提取高亮文本（好句子）- 调用API翻译并生成闪卡

Author: Assistant
Date: 2025-06-28
"""

import re
import os
import sys
import json
import time
from typing import List, Dict, Tuple, Optional
import requests
from pathlib import Path


class DeepSeekAPI:
    """DeepSeek API客户端"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def translate_word(self, word: str, context: str) -> Dict[str, str]:
        """翻译生词，返回含义和例句"""
        prompt = f"""请翻译英文单词"{word}"在以下句子中的含义：

            句子：{context}

            请按以下JSON格式回复：
            {{
                "meaning": "该单词在此句子中的中文含义",
                "example": "原句子"
            }}

            只返回JSON，不要其他内容。"""

        try:
            response = self._make_request(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"翻译单词 '{word}' 时出错: {e}")
            return {
                "meaning": f"翻译失败: {word}",
                "example": context
            }

    def translate_phrase(self, phrase: str, context: str) -> Dict[str, str]:
        """翻译词组，返回含义和例句"""
        prompt = f"""请翻译英文词组"{phrase}"在以下句子中的含义：

            句子：{context}

            请按以下JSON格式回复：
            {{
                "meaning": "该词组在此句子中的中文含义",
                "example": "原句子"
            }}

            只返回JSON，不要其他内容。"""

        try:
            response = self._make_request(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"翻译词组 '{phrase}' 时出错: {e}")
            return {
                "meaning": f"翻译失败: {phrase}",
                "example": context
            }

    def translate_sentence(self, sentence: str) -> str:
        """翻译句子"""
        prompt = f"""请将以下英文句子翻译成中文，要求翻译准确、自然：

            {sentence}

            只返回中文翻译，不要其他内容。"""

        try:
            response = self._make_request(prompt)
            return response.strip()
        except Exception as e:
            print(f"翻译句子时出错: {e}")
            return f"翻译失败: {sentence}"

    def _make_request(self, prompt: str) -> str:
        """发送API请求"""
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }

        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(
                f"API请求失败: {response.status_code}, {response.text}")


class MarkdownParser:
    """Markdown文档解析器"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = self._read_file()

    def _read_file(self) -> str:
        """读取Markdown文件"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            sys.exit(1)

    def extract_bold_text(self) -> List[Tuple[str, str]]:
        """提取加粗文本和其所在句子"""
        # 匹配 **text** 格式的加粗文本
        pattern = r'\*\*([^*]+)\*\*'
        matches = []

        for match in re.finditer(pattern, self.content):
            bold_text = match.group(1)
            # 获取句子上下文
            sentence = self._get_sentence_context(match.start(), match.end())
            matches.append((bold_text, sentence))

        return matches

    def extract_italic_text(self) -> List[Tuple[str, str]]:
        """提取斜体文本和其所在句子"""
        # 匹配 *text* 格式的斜体文本（排除加粗）
        pattern = r'(?<!\*)\*([^*]+)\*(?!\*)'
        matches = []

        for match in re.finditer(pattern, self.content):
            italic_text = match.group(1)
            # 获取句子上下文
            sentence = self._get_sentence_context(match.start(), match.end())
            matches.append((italic_text, sentence))

        return matches

    def extract_highlighted_text(self) -> List[str]:
        """提取高亮文本（假设使用 ==text== 格式）"""
        pattern = r'==([^=]+)=='
        matches = []

        for match in re.finditer(pattern, self.content):
            highlighted_text = match.group(1).strip()
            matches.append(highlighted_text)

        return matches

    def _get_sentence_context(self, start_pos: int, end_pos: int) -> str:
        """获取指定位置的句子上下文"""
        # 向前查找句子开始
        sentence_start = start_pos
        while sentence_start > 0 and self.content[sentence_start] not in '.!?':
            sentence_start -= 1
        if sentence_start > 0:
            sentence_start += 1

        # 向后查找句子结束
        sentence_end = end_pos
        while sentence_end < len(self.content) and self.content[sentence_end] not in '.!?':
            sentence_end += 1
        if sentence_end < len(self.content):
            sentence_end += 1

        sentence = self.content[sentence_start:sentence_end].strip()
        # 清理markdown标记
        sentence = re.sub(r'\*\*([^*]+)\*\*', r'\1', sentence)
        sentence = re.sub(r'\*([^*]+)\*', r'\1', sentence)
        sentence = re.sub(r'==([^=]+)==', r'\1', sentence)

        return sentence


class AnkiCardGenerator:
    """Anki闪卡生成器"""

    def __init__(self, api_client: DeepSeekAPI):
        self.api_client = api_client
        self.cards = []

    def process_bold_words(self, bold_words: List[Tuple[str, str]]):
        """处理加粗文本（生词）"""
        print("正在处理加粗文本（生词）...")

        for i, (word, sentence) in enumerate(bold_words, 1):
            print(f"处理生词 {i}/{len(bold_words)}: {word}")

            # 调用API翻译
            translation = self.api_client.translate_word(word, sentence)

            # 生成闪卡
            front = word
            back = f"{translation['meaning']}<br><br>{translation['example']}"

            self.cards.append((front, back))

            # 避免API频率限制
            time.sleep(1)

    def process_italic_phrases(self, italic_phrases: List[Tuple[str, str]]):
        """处理斜体文本（词组）"""
        print("正在处理斜体文本（词组）...")

        for i, (phrase, sentence) in enumerate(italic_phrases, 1):
            print(f"处理词组 {i}/{len(italic_phrases)}: {phrase}")

            # 调用API翻译
            translation = self.api_client.translate_phrase(phrase, sentence)

            # 生成闪卡
            front = phrase
            back = f"{translation['meaning']}<br><br>{translation['example']}"

            self.cards.append((front, back))

            # 避免API频率限制
            time.sleep(1)

    def process_highlighted_sentences(self, sentences: List[str]):
        """处理高亮文本（好句子）"""
        print("正在处理高亮文本（好句子）...")

        for i, sentence in enumerate(sentences, 1):
            print(f"处理句子 {i}/{len(sentences)}: {sentence[:50]}...")

            # 调用API翻译
            translation = self.api_client.translate_sentence(sentence)

            # 生成闪卡
            front = sentence
            back = translation

            self.cards.append((front, back))

            # 避免API频率限制
            time.sleep(1)

    def export_to_anki(self, output_file: str):
        """导出为Anki可导入的txt文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # 写入Anki格式头部
                f.write("#separator:tab\n")
                f.write("#html:true\n\n")

                # 写入闪卡数据
                for front, back in self.cards:
                    f.write(f"{front}\t{back}\n")

            print(f"成功导出 {len(self.cards)} 张闪卡到文件: {output_file}")

        except Exception as e:
            print(f"导出文件失败: {e}")


def main():
    """主函数"""
    print("Markdown to Anki Converter")
    print("=" * 40)

    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python3 md_to_anki.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]

    # 检查文件是否存在
    if not os.path.exists(markdown_file):
        print(f"文件不存在: {markdown_file}")
        sys.exit(1)

    # 获取API密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("错误: 请设置环境变量 DEEPSEEK_API_KEY")
        print("示例: export DEEPSEEK_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        # 初始化组件
        print("初始化API客户端...")
        api_client = DeepSeekAPI(api_key)

        print(f"解析Markdown文件: {markdown_file}")
        parser = MarkdownParser(markdown_file)

        print("提取标记文本...")
        bold_words = parser.extract_bold_text()
        italic_phrases = parser.extract_italic_text()
        highlighted_sentences = parser.extract_highlighted_text()

        print(f"找到 {len(bold_words)} 个生词")
        print(f"找到 {len(italic_phrases)} 个词组")
        print(f"找到 {len(highlighted_sentences)} 个好句子")

        # 生成闪卡
        generator = AnkiCardGenerator(api_client)

        if bold_words:
            generator.process_bold_words(bold_words)

        if italic_phrases:
            generator.process_italic_phrases(italic_phrases)

        if highlighted_sentences:
            generator.process_highlighted_sentences(highlighted_sentences)

        # 导出文件
        output_file = Path(markdown_file).stem + "_anki_cards.txt"
        generator.export_to_anki(output_file)

        print("转换完成!")

    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
