CREATE TABLE `tb_task`(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `userid` INTEGER,
  `content` TEXT,
  `addtime` TEXT,
  `endtime` TEXT,
  `ctime` TEXT,
  `type` TEXT,
  `status` TEXT,
  `name` TEXT
);


CREATE TABLE IF NOT EXISTS `tb_backup` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `userid` INTEGER,
  `content` TEXT,
  `addtime` TEXT,
  `endtime` TEXT,
  `ctime` TEXT,
  `type` TEXT,
  `status` TEXT,
  `name` TEXT
);


-- CREATE TABLE IF NOT EXISTS `users` (
--   `id` INTEGER PRIMARY KEY AUTOINCREMENT,
--   `username` TEXT,
--   `password` TEXT,
--   `login_ip` TEXT,
--   `login_time` TEXT,
--   `phone` TEXT,
--   `email` TEXT
-- );
-- INSERT INTO `users` (`id`, `username`, `password`, `login_ip`, `login_time`, `phone`, `email`) VALUES
-- (1, 'admin', '21232f297a57a5a743894a0e4a801fc3', '192.168.0.10', '2016-12-10 15:12:56', 0, '287962566@qq.com');