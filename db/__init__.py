# -*- coding:utf-8 -*-
"""
   一、关系型数据库-MySQL
      优点: 1.数据一致性高，冗余度低，完整性好。
           2.技术成熟，可以使用外部链接等比较复杂的操作。
      缺点: 1.在海量数据处理的时候效率会显著变慢。不能很好的满足高并发需求，每次都需要进行sql语句的解析。
             高并发：同时有大量的客户端来操作访问数据库。针对海量数据的瞬间爆发读写性能不足，关系型数据库内部每步操作都需要加锁，保证操作的原子性。
           2.数据扩展普遍比非关系型困难。
           3.数据一致性高，有时会浪费大量空间
   二、非关系型数据库-MongoDB
   三、Mongodb、MySQL数据库的对比
      1.数据库模型:
        mysql: 关系型
        mongo: 非关系型
      2.存储方式:
        mysql: 不同的引擎有不同的存储方式。
        mongo: 虚拟内存+持久化。以类JSON的文档的格式存储。
      3.查询语句:
        mysql: 传统的sql语句
        mongo: 独特的mongodb查询方式
      4.数据处理方式
        mysql: 不同的引擎拥有其自己的特点。
        mongo: 基于内存, 将热数据存放在物理内存中, 从而达到高速读写。
      5.成熟度
        mysql: 成熟度较高, 拥有较为成熟的体系。
        mongo: 成熟度较低, 新兴数据库。
      6.广泛度
        mysql: 开源数据库，市场份额不断增长。
        mongo: NoSQL数据库中，比较完善且开源，使用人数在不断增长。
"""

# https://www.jianshu.com/p/56524b50b376
# https://www.cnblogs.com/1488boss/p/10754290.html
# https://blog.csdn.net/striner/article/details/81114621

