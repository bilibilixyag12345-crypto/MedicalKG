#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗知识图谱构建工具
从 MongoDB 读取数据，构建 neo4j 知识图谱
"""

import logging
import sys
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def check_databases():
    """检查数据库连接"""
    logger.info("=" * 60)
    logger.info("检查数据库连接...")
    logger.info("=" * 60)
    
    # 检查 MongoDB
    try:
        from pymongo import MongoClient
        mongo_client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        mongo_client.server_info()
        logger.info("✓ MongoDB 连接成功")
        mongo_connected = True
    except Exception as e:
        logger.error(f"✗ MongoDB 连接失败: {e}")
        mongo_connected = False
    
    # 检查 neo4j
    try:
        from py2neo import Graph
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
        graph.run("RETURN 1")
        logger.info("✓ neo4j 连接成功")
        neo4j_connected = True
    except Exception as e:
        logger.error(f"✗ neo4j 连接失败: {e}")
        logger.info("  如果密码错误，请修改脚本中的密码")
        neo4j_connected = False
    
    return mongo_connected, neo4j_connected

def migrate_data_mongodb_to_neo4j():
    """从 MongoDB 迁移数据到 neo4j"""
    try:
        from pymongo import MongoClient
        from py2neo import Graph, Node, Relationship
        
        logger.info("\n" + "=" * 60)
        logger.info("开始从 MongoDB 迁移数据到 neo4j...")
        logger.info("=" * 60)
        
        # 连接数据库
        mongo_client = MongoClient('mongodb://localhost:27017/')
        mongo_db = mongo_client['MedicalKG']
        mongo_collection = mongo_db['MedicalKG']
        
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
        
        # 清空 neo4j 中的旧数据（可选）
        logger.info("清空 neo4j 中的旧数据...")
        graph.run("MATCH (n) DETACH DELETE n")
        
        # 从 MongoDB 读取数据
        logger.info("从 MongoDB 读取数据...")
        documents = list(mongo_collection.find())
        logger.info(f"找到 {len(documents)} 条数据")
        
        if len(documents) == 0:
            logger.warning("MongoDB 中没有数据！")
            logger.info("请先运行爬虫或导入测试数据")
            return False
        
        # 创建节点和关系
        logger.info("开始创建知识图谱...")
        
        nodes_created = 0
        relations_created = 0
        
        for i, doc in enumerate(documents):
            try:
                head = doc.get('head', '').strip()
                relation = doc.get('relation', '').strip()
                tail = doc.get('tail', '').strip()
                
                if not head or not relation or not tail:
                    continue
                
                # 创建节点
                head_node = Node("Disease", name=head)
                tail_node = Node("Attribute", name=tail)
                
                # 创建关系
                rel = Relationship(head_node, relation, tail_node)
                
                # 保存到 neo4j
                graph.create(rel)
                
                nodes_created += 2
                relations_created += 1
                
                if (i + 1) % 100 == 0:
                    logger.info(f"已处理 {i + 1} / {len(documents)} 条数据...")
            
            except Exception as e:
                logger.warning(f"处理数据时出错: {e}")
                continue
        
        logger.info("=" * 60)
        logger.info("数据迁移完成！")
        logger.info(f"创建节点数: {nodes_created}")
        logger.info(f"创建关系数: {relations_created}")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"数据迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def query_neo4j_examples():
    """查询 neo4j 中的数据示例"""
    try:
        from py2neo import Graph
        
        logger.info("\n" + "=" * 60)
        logger.info("neo4j 查询示例:")
        logger.info("=" * 60)
        
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
        
        # 查询 1：统计节点和关系
        logger.info("\n1. 统计数据:")
        result = graph.run("MATCH (n) RETURN COUNT(n) as node_count").data()
        logger.info(f"   节点总数: {result[0]['node_count'] if result else 0}")
        
        result = graph.run("MATCH ()-[r]-() RETURN COUNT(r) as rel_count").data()
        logger.info(f"   关系总数: {result[0]['rel_count'] if result else 0}")
        
        # 查询 2：显示前 5 条关系
        logger.info("\n2. 前 5 条知识三元组:")
        result = graph.run(
            "MATCH (a)-[r]->(b) RETURN a.name as head, type(r) as relation, b.name as tail LIMIT 5"
        ).data()
        
        for row in result:
            logger.info(f"   {row['head']} --[{row['relation']}]--> {row['tail']}")
        
        # 查询 3：查找某个疾病的属性
        logger.info("\n3. 查询示例（查找疾病的症状）:")
        result = graph.run(
            "MATCH (d:Disease)-[r]->(a) RETURN DISTINCT d.name as disease LIMIT 3"
        ).data()
        
        if result:
            disease_name = result[0]['disease']
            logger.info(f"   疾病: {disease_name}")
            
            attrs = graph.run(
                f"MATCH (d:Disease {{name: '{disease_name}'}})-[r]->(a) RETURN type(r) as relation, a.name as attr LIMIT 10"
            ).data()
            
            for attr in attrs:
                logger.info(f"     - {attr['relation']}: {attr['attr']}")
        
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"查询失败: {e}")

def import_sample_data():
    """导入示例数据到 MongoDB（如果为空）"""
    try:
        from pymongo import MongoClient
        
        logger.info("\n" + "=" * 60)
        logger.info("检查 MongoDB 中是否有数据...")
        logger.info("=" * 60)
        
        mongo_client = MongoClient('mongodb://localhost:27017/')
        mongo_db = mongo_client['MedicalKG']
        mongo_collection = mongo_db['MedicalKG']
        
        count = mongo_collection.count_documents({})
        
        if count > 0:
            logger.info(f"✓ MongoDB 中已有 {count} 条数据")
            return True
        
        logger.info("MongoDB 中没有数据，导入示例数据...")
        
        # 示例数据
        sample_data = [
            {'head': '高血压', 'relation': '症状', 'tail': '头晕'},
            {'head': '高血压', 'relation': '症状', 'tail': '头痛'},
            {'head': '高血压', 'relation': '症状', 'tail': '疲劳'},
            {'head': '高血压', 'relation': '治疗', 'tail': '药物治疗'},
            {'head': '高血压', 'relation': '治疗', 'tail': '饮食调理'},
            {'head': '糖尿病', 'relation': '症状', 'tail': '口渴'},
            {'head': '糖尿病', 'relation': '症状', 'tail': '乏力'},
            {'head': '糖尿病', 'relation': '症状', 'tail': '多尿'},
            {'head': '糖尿病', 'relation': '类型', 'tail': '1型糖尿病'},
            {'head': '糖尿病', 'relation': '类型', 'tail': '2型糖尿病'},
            {'head': '感冒', 'relation': '症状', 'tail': '咳嗽'},
            {'head': '感冒', 'relation': '症状', 'tail': '流鼻涕'},
            {'head': '感冒', 'relation': '症状', 'tail': '喉咙痛'},
            {'head': '感冒', 'relation': '病因', 'tail': '病毒感染'},
        ]
        
        mongo_collection.insert_many(sample_data)
        logger.info(f"✓ 已导入 {len(sample_data)} 条示例数据")
        
        return True
        
    except Exception as e:
        logger.error(f"导入示例数据失败: {e}")
        return False

def main():
    """主程序"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 12 + "医疗知识图谱构建工具 v1.0" + " " * 20 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    # 检查数据库
    mongo_ok, neo4j_ok = check_databases()
    
    if not mongo_ok:
        logger.error("\n✗ MongoDB 未运行！")
        logger.info("  请先启动 MongoDB 服务")
        sys.exit(1)
    
    if not neo4j_ok:
        logger.error("\n✗ neo4j 未运行或密码错误！")
        logger.info("  请先启动 neo4j 服务")
        logger.info("  如果密码不是 'password'，请修改脚本")
        sys.exit(1)
    
    # 导入示例数据
    import_sample_data()
    
    # 迁移数据
    success = migrate_data_mongodb_to_neo4j()
    
    if success:
        # 查询示例
        query_neo4j_examples()
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ 知识图谱构建完成！")
        logger.info("=" * 60)
        logger.info("\n你可以现在访问 neo4j 浏览器:")
        logger.info("  http://localhost:7474")
        logger.info("\n或者使用以下 Cypher 查询:")
        logger.info("  MATCH (a)-[r]->(b) RETURN a.name, type(r), b.name LIMIT 50")
        
        sys.exit(0)
    else:
        logger.error("\n✗ 知识图谱构建失败！")
        sys.exit(1)

if __name__ == '__main__':
    main()
