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
        print("=" * 50)
        print("开始启动医疗知识图谱爬虫...")
        print("=" * 50)
        print(f"项目根目录: {project_root}")
        
        # 检查必要的依赖
        required_modules = ['scrapy', 'pymongo', 'py2neo']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
                print(f"✓ {module} 已安装")
            except ImportError:
                print(f"✗ {module} 未安装")
                missing_modules.append(module)
        
        if missing_modules:
            print("\n" + "=" * 50)
            print("错误：缺少以下依赖模块:")
            for module in missing_modules:
                print(f"  - {module}")
            print("\n请执行以下命令安装:")
            print(f"  pip install {' '.join(missing_modules)}")
            print("=" * 50)
            sys.exit(1)
        
        # 更改到项目目录
        os.chdir(project_root)
        
        # 运行 scrapy 爬虫
        print("\n" + "=" * 50)
        print("开始爬取百度百科医疗数据...")
        print("=" * 50)
        
        cmd = [
            sys.executable, 
            '-m', 
            'scrapy', 
            'crawl', 
            'BaikeMedical'
        ]
        
        print(f"执行命令: {' '.join(cmd)}\n")
        result = subprocess.run(cmd, cwd=project_root)
        
        if result.returncode == 0:
            print("\n" + "=" * 50)
            print("爬虫执行完成！")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print(f"爬虫执行失败，返回码: {result.returncode}")
            print("=" * 50)
        
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
