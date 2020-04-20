# encoding:utf-8
CREATE_TABLE_USER = '''CREATE TABLE IF NOT EXISTS `tb_user` (
                              `username` varchar(255) NOT NULL,
                              `password` varchar(255) NOT NULL,
                              `password_encode` varchar(255) NOT NULL,
                              `full_name` varchar(255) NOT NULL,
                              `is_admin` tinyint(1) NOT NULL DEFAULT 0,
                              `maildir` varchar(255) NOT NULL,
                              `quota` bigint(20) NOT NULL DEFAULT 0,
                              `local_part` varchar(255) NOT NULL,
                              `domain` varchar(255) NOT NULL,
                              `created` datetime NOT NULL,
                              `modified` datetime NOT NULL,
                              `active` tinyint(1) NOT NULL DEFAULT 1,
                               PRIMARY KEY (`username`)
                       );'''


# 修改字段名称：alter table 表名 change 旧字段名 新字段名 新数据类型;
update_field_name = "alter table tb_login_record change createdat logtime timestamp;"
