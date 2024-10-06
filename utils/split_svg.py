#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 - 2024 Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam
# @Email  : sepinetam@gmail.com
# @File   : split_svg.py

import re
import os


def separate_svg_and_text(input_file, output_folder, custom_prompt=""):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式分离SVG和文本
    svg_pattern = r'<svg.*?</svg>'
    svgs = re.findall(svg_pattern, content, re.DOTALL)

    # 分离演讲者注释
    notes_pattern = r'Speaker Notes:[^\n]*\n(.*?)(?=\n<svg|\Z)'
    notes = re.findall(notes_pattern, content, re.DOTALL)

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 写入SVG文件
    for i, svg in enumerate(svgs):
        with open(os.path.join(output_folder, f'slide_{i + 1}.svg'), 'w', encoding='utf-8') as f:
            f.write(svg)

    # 写入演讲者注释文件（英文和中文）
    with open(os.path.join(output_folder, 'speaker_notes_en.txt'), 'w', encoding='utf-8') as f_en, \
            open(os.path.join(output_folder, 'speaker_notes_cn.txt'), 'w', encoding='utf-8') as f_cn:

        f_en.write(f"Custom Prompt: {custom_prompt}\n\n")
        f_cn.write(f"自定义提示词：{custom_prompt}\n\n")

        for i, note in enumerate(notes):
            f_en.write(f"Slide {i + 1} Speaker Notes:\n{note.strip()}\n\n")

            # 为中文版本添加翻译提示
            f_cn.write(f"幻灯片 {i + 1} 演讲者注释：\n[请在此处添加中文翻译]\n\n")

    print(f"分离完成。SVG文件和演讲者注释已保存到 {output_folder} 文件夹中。")
    print("请在 speaker_notes_cn.txt 文件中添加中文翻译。")


if __name__ == '__main__':
    input_file = '../src/missing_women.txt'  # 包含SVG和文本的输入文件
    output_folder = '../src/key/missing_women'  # 输出文件夹
    separate_svg_and_text(input_file, output_folder)
