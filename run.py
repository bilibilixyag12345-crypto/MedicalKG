#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

# 添加项目路径到 sys.path
sys.path.insert(0, project_root)

# 设置 PYTHONPATH
os.environ['PYTHONPATH'] = project_root

# 运行爬虫
if __name__ == '__main__':
    try:
        print("开始启动爬虫...")
        print(f"项目根目录: {project_root}")
        
        # 方法1: 直接使用 scrapy 命令
        cmd = [
            sys.executable, 
            '-m', 
            'scrapy', 
            'crawl', 
            'BaikeMedical'
        ]
        
        # 更改到项目目录
        os.chdir(project_root)
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=project_root)
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"错误: {e}")
        print("请确保已安装以下依赖:")
        print("  - scrapy")
        print("  - scrapy-splash")
        print("  - pymongo")
        print("  - py2neo")
        print("\n可以使用以下命令安装:")
        print("  pip install scrapy scrapy-splash pymongo py2neo")
        sys.exit(1)
