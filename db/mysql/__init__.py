# -*- coding:utf-8 -*-
"""
   一、mysql的存储引擎: 1.InnoDB、2.MyISAM、3.
      1.innodb支持外键, myisam不支持外键。对一个包含外键的InnoDB表转为MYISAM会失败。
      2.innodb支持事务, MyISAM不支持事务。对于InnoDB每一条SQL语言都默认封装成事务,自动提交,这样会影响速度,所以最好把多条SQL语言放在begin和commit之间,组成一个事务。
      3.innodb支持表级锁、行级锁(默认)。MyISAM只支持表级锁,不支持行锁定。
      4.Innodb不支持全文索引, 而MyISAM支持全文索引, 在涉及全文索引领域的查询效率上MyISAM速度更快高；PS：5.7以后的InnoDB支持全文索引了。
      5.MyISAM表格可以被压缩后进行查询操作。
      6.InnoDB表必须有唯一索引（如主键）（用户没有指定的话会自己找/生产一个隐藏列Row_id来充当默认主键），而Myisam可以没有
      7.没有where的count(*)使用MyISAM要比InnoDB快得多。
      8.Innodb存储文件有frm、ibd。而Myisam是frm、MYD、MYI
        Innodb: frm是表定义文件, ibd是数据文件
        Myisam: frm是表定义文件, myd是数据文件, myi是索引文件

   二、mysql的事务特性: 1.原子性、2.一致性、3.隔离性、4.持久性
      1.原子性: 指处于同一个事务中的多条语句是不可分割的。
      2.一致性: 事务必须使数据库从一个一致性状态变换到另外一个一致性状态。比如转账，转账前两个账户余额之和为2k，转账之后也应该是2K。
      3.隔离性: 指多线程环境下，一个线程中的事务不能被其他线程中的事务打扰。
      4.持久性: 事务一旦提交，就应该被永久保存起来。

   三、mysql的事务隔离级别:
      1.未提交读（Read uncommitted）	可能(脏读)	可能(不可重复读)	可能(幻读)
      2.已提交读（Read committed）  	不可能(脏读)	可能(不可重复读)	可能(幻读)
      3.可重复读（Repeatable read）	不可能(脏读)	不可能(不可重复读)	可能(幻读)
      4.可串行化（Serializable   ）	不可能(脏读)	不可能(不可重复读)	不可能(幻读)
      附加: 脏读：指一个线程中的事务读取到了另外一个线程中未提交的数据。
      附加: 虚读：指一个线程中的事务读取到了另外一个线程中提交的update的数据。（不可重复读）
      附加: 幻读：指一个线程中的事务读取到了另外一个线程中提交的insert的数据。

   四、mysql的索引类型: 1.普通索引、2.唯一索引、3.主键索引、4.组合索引、5.全文索引
      1.普通索引:
      2.唯一索引:
      3.主键索引:
      4.组合索引:
      5.全文索引:

   五、mysql的约束类型: 1.默认约束、2.非空约束、3.唯一约束、4.自增约束、5.主键约束、6.外键约束、7.检查约束

   六、join
"""

# https://blog.csdn.net/qq_35642036/article/details/82820178
# https://blog.csdn.net/weixin_42386014/article/details/81811129