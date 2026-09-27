-- MVP 基础数据；账号初始禁用，无已知默认密码。请使用部署准备脚本生成管理员凭据。

SET NAMES utf8mb4;

SET FOREIGN_KEY_CHECKS=0;

INSERT INTO `infra_config_data` (`type_id`,`name`,`key`,`value`,`description`,`input_type`,`input_props`,`sort`,`visible`,`remark`,`id`,`creator`,`create_time`,`updater`,`update_time`,`deleted`) VALUES
(10300000010001,'应用名称','APP_NAME','DUSHAN-SERVER',NULL,NULL,NULL,10,1,'应用名称',10300000020001,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010001,'应用作者','APP_AUTHER','渡山',NULL,NULL,NULL,20,1,'应用作者',10300000020002,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010001,'应用版本号','APP_VERSION','1.0.0',NULL,NULL,NULL,30,1,'应用版本号',10300000020003,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010001,'访问日志','APP_ACCESS_LOG_ENABLE','true',NULL,NULL,NULL,40,1,'是否开启访问日志功能',10300000020004,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010001,'国际化开关','APP_I18N_ENABLED','true',NULL,NULL,NULL,50,1,'是否启用国际化翻译',10300000020005,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010001,'默认语言','APP_I18N_DEFAULT_LANG','zh-CN',NULL,NULL,NULL,60,1,'默认语言（zh-CN/en-US）',10300000020006,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010001,'允许修改系统角色','APP_ALLOW_MODIFY_SYSTEM_ROLE','true',NULL,NULL,NULL,70,1,'是否允许修改系统内置角色',10300000020007,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010002,'默认时区','DATETIME_TIMEZONE','Asia/Shanghai',NULL,NULL,NULL,10,1,'默认时区',10300000020009,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'文件日志总开关','LOG_ENABLE_FILE_OVERALL','true',NULL,NULL,NULL,10,1,'是否启用文件日志',10300000020010,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'JSON结构化日志','LOG_ENABLE_JSON_FORMAT','false',NULL,NULL,NULL,20,1,'是否启用JSON结构化日志',10300000020011,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'控制台日志级别','LOG_CONSOLE_LEVEL','DEBUG',NULL,NULL,NULL,30,1,'控制台输出的最低级别',10300000020012,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'日志轮转大小','LOG_ROTATION_SIZE','20 MB',NULL,NULL,NULL,40,1,'日志轮转大小',10300000020013,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'异步写入','LOG_ENQUEUE','true',NULL,NULL,NULL,50,1,'是否启用异步写入',10300000020014,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'日志压缩格式','LOG_COMPRESSION','zip',NULL,NULL,NULL,60,1,'日志压缩格式',10300000020015,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'Info日志级别','LOG_FILE_LEVEL_INFO','INFO',NULL,NULL,NULL,70,1,'Info日志文件的最低记录级别',10300000020016,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'Info日志保留时间','LOG_RETENTION_INFO','7 days',NULL,NULL,NULL,80,1,'Info日志保留时间',10300000020017,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'Warning日志级别','LOG_FILE_LEVEL_WARNING','WARNING',NULL,NULL,NULL,90,1,'Warning日志文件的最低记录级别',10300000020018,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'Warning日志保留时间','LOG_RETENTION_WARN','15 days',NULL,NULL,NULL,100,1,'Warning日志保留时间',10300000020019,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'Error日志级别','LOG_FILE_LEVEL_ERROR','ERROR',NULL,NULL,NULL,110,1,'Error日志文件的最低记录级别',10300000020020,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010003,'Error日志保留时间','LOG_RETENTION_ERROR','30 days',NULL,NULL,NULL,120,1,'Error日志保留时间',10300000020021,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010004,'API加解密开关','API_ENCRYPT_ENABLE','false',NULL,NULL,NULL,10,1,'是否启用API加解密',10300000020022,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010005,'XSS过滤器开关','XSS_XSS_FILTER_ENABLED','true',NULL,NULL,NULL,10,1,'是否启用XSS过滤器',10300000020023,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010006,'验证码开关','CAPTCHA_ENABLE','true',NULL,NULL,NULL,10,1,'是否开启验证码',10300000020024,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010006,'验证码过期时间','CAPTCHA_TIMING_CLEAR','180',NULL,NULL,NULL,20,1,'验证码过期时间(秒)',10300000020025,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010006,'频率限制开关','CAPTCHA_REQ_FREQUENCY_LIMIT_ENABLE','false',NULL,NULL,NULL,30,1,'是否启用频率限制',10300000020026,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010006,'验证失败最大次数','CAPTCHA_REQ_GET_LOCK_LIMIT','5',NULL,NULL,NULL,40,1,'验证失败最大次数',10300000020027,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010006,'锁定时间间隔','CAPTCHA_REQ_GET_LOCK_SECONDS','120',NULL,NULL,NULL,50,1,'锁定时间间隔(秒)',10300000020028,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010006,'Get接口请求限制','CAPTCHA_REQ_GET_MINUTE_LIMIT','30',NULL,NULL,NULL,60,1,'Get接口一分钟请求数',10300000020029,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010006,'Check接口请求限制','CAPTCHA_REQ_CHECK_MINUTE_LIMIT','60',NULL,NULL,NULL,70,1,'Check接口一分钟请求数',10300000020030,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'表头字体加粗','EXCEL_HEADER_FONT_BOLD','true',NULL,NULL,NULL,10,1,'表头字体是否加粗',10300000020031,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'表头字体大小','EXCEL_HEADER_FONT_SIZE','11',NULL,NULL,NULL,20,1,'表头字体大小',10300000020032,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'自动调整列宽','EXCEL_AUTO_ADJUST_COLUMN_WIDTH','true',NULL,NULL,NULL,30,1,'是否自动调整列宽',10300000020033,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'最大列宽','EXCEL_MAX_COLUMN_WIDTH','60',NULL,NULL,NULL,40,1,'最大列宽',10300000020034,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'最小列宽','EXCEL_MIN_COLUMN_WIDTH','10',NULL,NULL,NULL,50,1,'最小列宽',10300000020035,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'只读模式','EXCEL_READ_ONLY_MODE','true',NULL,NULL,NULL,60,1,'读取模式是否只读',10300000020036,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'数据模式','EXCEL_DATA_ONLY_MODE','true',NULL,NULL,NULL,70,1,'是否只读取数据（不读取公式）',10300000020037,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'最大导入行数','EXCEL_MAX_IMPORT_ROWS','10000',NULL,NULL,NULL,80,1,'最大导入行数',10300000020038,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010007,'金额小数位数','EXCEL_MONEY_DECIMAL_PLACES','2',NULL,NULL,NULL,90,1,'金额小数位数',10300000020039,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010008,'IP查询超时时间','IP_IP_QUERY_TIMEOUT','5.0',NULL,NULL,NULL,10,1,'IP查询超时时间(秒)',10300000020040,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
(10300000010008,'IP缓存大小','IP_IP_CACHE_SIZE','1024',NULL,NULL,NULL,20,1,'IP查询结果缓存大小',10300000020041,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0);

INSERT INTO `infra_config_type` (`module`,`name`,`code`,`status`,`remark`,`deleted_time`,`id`,`creator`,`create_time`,`updater`,`update_time`,`deleted`) VALUES
('system','应用配置','APP_SETTINGS',1,'AppSettings - 应用基础配置（名称/版本/业务开关）',NULL,10300000010001,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
('system','日期时间配置','DATETIME_SETTINGS',1,'DateTimeSettings - 时区配置',NULL,10300000010002,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
('system','日志配置','LOG_SETTINGS',1,'LogSettings - 日志级别/保留策略',NULL,10300000010003,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
('system','API加解密配置','API_ENCRYPT_SETTINGS',1,'ApiEncryptSettings - API加解密开关',NULL,10300000010004,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
('system','XSS配置','XSS_SETTINGS',1,'XssSettings - XSS过滤开关',NULL,10300000010005,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
('system','验证码配置','CAPTCHA_SETTINGS',1,'CaptchaSettings - 验证码开关/频率/过期时间',NULL,10300000010006,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
('system','Excel配置','EXCEL_SETTINGS',1,'ExcelSettings - 导入导出样式/行数限制',NULL,10300000010007,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0),
('system','IP配置','IP_SETTINGS',1,'IpSettings - IP查询超时/缓存配置',NULL,10300000010008,'admin','2026-09-27 12:12:41','admin','2026-09-27 12:12:41',0);

INSERT INTO `infra_file_config` (`name`,`storage`,`remark`,`status`,`master`,`config`,`id`,`creator`,`create_time`,`updater`,`update_time`,`deleted`) VALUES
('数据库',1,'文件内容存储到数据库 infra_file_content 表，适合小文件和开发环境',1,1,'{\"domain\":\"http://localhost:18081\"}',10300000040001,'10100000010001','2026-09-27 12:12:41','10100000010001','2026-09-27 12:12:41',0);

INSERT INTO `infra_job` (`name`,`status`,`handler_name`,`handler_param`,`cron_expression`,`retry_count`,`retry_interval`,`monitor_timeout`,`revision`,`effective_at`,`parameters`,`max_instances`,`timeout_seconds`,`retry_backoff`,`stop_after_failure`,`id`,`creator`,`create_time`,`updater`,`update_time`,`deleted`) VALUES
('任务日志清理任务',1,'infra.job.log.clean','{}','0 2 * * *',3,5000,60000,'seed-1','2026-09-27 12:12:41','{}',1,300.0e0,1.0e0,0,10300000050001,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0),
('访问日志清理任务',1,'infra.log.access.clean','{}','30 2 * * *',3,5000,60000,'seed-1','2026-09-27 12:12:41','{}',1,300.0e0,1.0e0,0,10300000050002,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0),
('错误日志清理任务',1,'infra.log.error.clean','{}','0 3 * * *',3,5000,60000,'seed-1','2026-09-27 12:12:41','{}',1,300.0e0,1.0e0,0,10300000050003,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0),
('公告定时任务',1,'system.announcement.publish','{}','* * * * *',3,5000,120000,'seed-1','2026-09-27 12:12:41','{}',1,300.0e0,1.0e0,0,10300000050004,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0),
('数据权限同步任务',1,'system.permission.sync','{}','0 4 * * *',3,5000,60000,'seed-1','2026-09-27 12:12:41','{}',1,300.0e0,1.0e0,0,10300000050005,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0),
('数据库主从延迟检查任务',1,'infra.database.health','{}','0 5 * * *',3,5000,60000,'seed-1','2026-09-27 12:12:41','{}',1,300.0e0,1.0e0,0,10300000050006,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0),
('数据库备份任务',2,'infra.database.backup','{}','0 2 * * *',1,300000,1800000,'seed-1','2026-09-27 12:12:41','{}',1,300.0e0,1.0e0,0,10300000050007,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0),
('数据库指标采集任务',1,'infra.database.metrics','{}','*/5 * * * *',0,0,30000,'seed-1','2026-09-27 12:12:41','{}',1,300.0e0,1.0e0,0,10300000050008,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0);

INSERT INTO `infra_job_signal` (`revision`,`id`,`creator`,`create_time`,`updater`,`update_time`,`deleted`) VALUES
(0,1,'','2026-09-27 12:12:41','','2026-09-27 12:12:41',0);

INSERT INTO `infra_mq` (`topic`,`consumer`,`retry_count`,`description`,`enabled`,`concurrency`,`prefetch`,`id`,`creator`,`create_time`,`updater`,`update_time`,`deleted`) VALUES
('sms:send','system.sms.send',3,'短信发送消息。由 SmsProducer 投递，SmsSendConsumer 消费。完整链路：模板校验 → 参数构建 → 日志记录 → MQ 投递 → 实际发送。',1,NULL,NULL,1891372849213450001,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0),
('mail:send','system.mail.send',3,'邮件发送消息。由 MailProducer 投递，MailSendConsumer 消费。支持单发、多收件人、批量发送模式。',1,NULL,NULL,1891372849213450002,'system','2026-09-27 12:12:41','system','2026-09-27 12:12:41',0);

SET FOREIGN_KEY_CHECKS=1;
