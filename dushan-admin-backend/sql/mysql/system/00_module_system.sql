-- DuShan AI Native MVP 0.0.0; upstream cd21ddf29ea8d3f7134c31eca1b903cac959da75

-- 由无租户模型在 MySQL 8.4.11 上生成；普通业务、数据权限与审计能力保持。

SET NAMES utf8mb4;

SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE `system_announcement` (
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '公告标题',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '公告内容',
  `status` smallint NOT NULL COMMENT '公告状态（0-草稿，1-待发布，2-已发布，3-已过期）',
  `is_top` tinyint(1) NOT NULL COMMENT '是否置顶',
  `sort` int NOT NULL COMMENT '排序序号（数值越小越靠前）',
  `category` smallint NOT NULL COMMENT '公告类别，参见 AnnouncementCategoryEnum',
  `publish_time` datetime DEFAULT NULL COMMENT '发布时间',
  `expire_time` datetime DEFAULT NULL COMMENT '过期时间',
  `publisher` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发布人',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='公告表';

CREATE TABLE `system_authorization_revision` (
  `revision` bigint NOT NULL,
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统授权版本';

CREATE TABLE `system_dept` (
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '部门名称',
  `parent_id` bigint NOT NULL COMMENT '父部门id',
  `sort` int NOT NULL COMMENT '显示顺序',
  `leader_user_id` bigint DEFAULT NULL COMMENT '负责人',
  `phone` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话',
  `email` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）【StatusEnum】',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='部门信息表';

CREATE TABLE `system_dict_data` (
  `sort` int NOT NULL COMMENT '字典排序',
  `label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典标签',
  `value` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典键值',
  `dict_type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典类型',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `color_type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '颜色类型',
  `tag_style` json DEFAULT NULL COMMENT '按钮样式',
  `permission` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '权限标识（该选项所需的权限码，NULL表示无需权限）',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='字典数据表';

CREATE TABLE `system_dict_type` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典名称',
  `type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '字典类型',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `deleted_time` datetime DEFAULT NULL COMMENT '删除时间',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='字典类型表';

CREATE TABLE `system_login_log` (
  `log_type` smallint NOT NULL COMMENT '日志类型（枚举）【LoginLogTypeEnum】',
  `trace_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '链路追踪编号',
  `user_id` bigint NOT NULL COMMENT '用户编号',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户账号',
  `result` smallint NOT NULL COMMENT '登录结果（枚举）【LoggerLoginResultEnum】',
  `user_ip` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户IP',
  `user_agent` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '浏览器UA',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统访问记录';

CREATE TABLE `system_mail_account` (
  `mail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `host` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'SMTP 服务器域名',
  `port` int NOT NULL COMMENT 'SMTP 服务器端口',
  `ssl_enable` tinyint(1) NOT NULL COMMENT '是否开启 SSL',
  `starttls_enable` tinyint(1) NOT NULL COMMENT '是否开启 STARTTLS',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮箱账号表';

CREATE TABLE `system_mail_log` (
  `user_id` bigint DEFAULT NULL COMMENT '用户编号',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `to_mail` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '接收邮箱地址(多个逗号分隔)',
  `cc_mail` text COLLATE utf8mb4_unicode_ci COMMENT '抄送邮箱地址(多个逗号分隔)',
  `bcc_mail` text COLLATE utf8mb4_unicode_ci COMMENT '密送邮箱地址(多个逗号分隔)',
  `account_id` bigint NOT NULL COMMENT '邮箱账号编号',
  `from_mail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发送邮箱地址',
  `template_id` bigint NOT NULL COMMENT '模板编号',
  `template_code` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板编码',
  `template_nickname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '模版发送人名称',
  `template_title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮件标题',
  `template_content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮件内容',
  `template_params` json NOT NULL COMMENT '邮件参数',
  `send_status` smallint NOT NULL COMMENT '发送状态【MailSendStatusEnum】',
  `send_time` datetime DEFAULT NULL COMMENT '发送时间',
  `send_message_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发送返回的消息 ID',
  `send_exception` text COLLATE utf8mb4_unicode_ci COMMENT '发送异常',
  `send_claim_token` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '外发 claim 令牌',
  `send_claim_until` datetime DEFAULT NULL COMMENT '外发前 claim 到期时间',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件日志表';

CREATE TABLE `system_mail_template` (
  `name` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板名称',
  `code` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板编码',
  `account_id` bigint NOT NULL COMMENT '发送的邮箱账号编号',
  `nickname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发送人名称',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板标题',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板内容',
  `params` json NOT NULL COMMENT '参数数组',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件模版表';

CREATE TABLE `system_menu` (
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单名称',
  `permission` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限标识',
  `kind` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单种类：group/page/action/link/iframe',
  `data_permission` tinyint(1) NOT NULL COMMENT '是否为数据权限操作，承接源 DATA 类型',
  `url` varchar(2048) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '外链或内嵌页面地址',
  `sort` int NOT NULL COMMENT '显示顺序',
  `parent_id` bigint NOT NULL COMMENT '父菜单ID',
  `path` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '路由地址',
  `icon` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单图标',
  `component` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '组件路径',
  `component_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '组件名',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `visible` tinyint(1) NOT NULL COMMENT '是否可见',
  `keep_alive` tinyint(1) NOT NULL COMMENT '是否缓存',
  `always_show` tinyint(1) NOT NULL COMMENT '是否总是显示',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='菜单权限表';

CREATE TABLE `system_notification_message` (
  `user_id` bigint NOT NULL COMMENT '用户id',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `notice_id` bigint NOT NULL COMMENT '关联的通知编号',
  `notice_log_id` bigint DEFAULT NULL COMMENT '通知日志ID (system_notification_notice_log.id)',
  `notice_title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通知标题',
  `notice_content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通知内容',
  `notice_type` int NOT NULL COMMENT '通知类型',
  `publisher_info` json DEFAULT NULL COMMENT '发布者信息',
  `sent_channels` json NOT NULL COMMENT '实际发送的渠道,参见 NotificationChannelEnum',
  `read_status` tinyint(1) NOT NULL COMMENT '是否已读',
  `read_time` datetime DEFAULT NULL COMMENT '阅读时间',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='站内信消息表';

CREATE TABLE `system_notification_notice` (
  `code` varchar(63) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '通知编码',
  `builtin` smallint NOT NULL COMMENT '内置类型（1-内置 2-自定义）【BuiltinTypeEnum】',
  `title` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通知标题',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通知内容',
  `type` int NOT NULL COMMENT '通知类型【NoticeTypeEnum】',
  `user_type` smallint NOT NULL COMMENT '用户类型【UserTypeEnum】',
  `channels` json NOT NULL COMMENT '通知渠道,参见 NotificationChannelEnum',
  `sms_template_code` varchar(63) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信模板编码,选择SMS渠道时必填',
  `mail_account_id` bigint DEFAULT NULL COMMENT '邮箱账号编号,选择MAIL渠道时必填',
  `publisher` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发布人',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知表';

CREATE TABLE `system_notification_notice_log` (
  `notice_id` bigint NOT NULL COMMENT '关联的通知编号',
  `notice_title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通知标题(冗余快照)',
  `notice_type` int NOT NULL COMMENT '通知类型(冗余快照)',
  `push_target_type` smallint NOT NULL COMMENT '推送目标类型(NoticePushTargetTypeEnum): 1=按用户, 2=按部门, 3=混合',
  `target_user_ids` json DEFAULT NULL COMMENT '目标用户ID列表(原始选择)',
  `target_dept_ids` json DEFAULT NULL COMMENT '目标部门ID列表(原始选择)',
  `target_dept_names` json DEFAULT NULL COMMENT '目标部门名称列表(冗余快照)',
  `push_channels` json NOT NULL COMMENT '推送渠道',
  `total_count` int NOT NULL COMMENT '推送总人数',
  `success_count` int NOT NULL COMMENT '成功数',
  `fail_count` int NOT NULL COMMENT '失败数',
  `push_status` smallint NOT NULL COMMENT '推送状态(NoticePushStatusEnum): 0=推送中, 1=全部成功, 2=部分失败, 3=全部失败',
  `publisher_info` json DEFAULT NULL COMMENT '发布者信息',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知日志表';

CREATE TABLE `system_oauth2_access_token` (
  `user_id` bigint NOT NULL COMMENT '用户编号',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `user_info` json NOT NULL COMMENT '用户信息 (JSON 格式)',
  `scopes` json DEFAULT NULL COMMENT '授权范围 (JSON 数组格式)',
  `token_digest` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '访问令牌 SHA-256 摘要',
  `refresh_token_id` bigint DEFAULT NULL COMMENT '刷新令牌记录编号',
  `client_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户端编号',
  `expires_time` datetime NOT NULL COMMENT '过期时间',
  `family_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会话族编号',
  `credential_revision` int NOT NULL COMMENT '签发时的凭据版本',
  `revoked` tinyint(1) NOT NULL COMMENT '是否撤销',
  `application_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '应用标识',
  `domain` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '认证域',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_oauth2_access_token_digest` (`token_digest`),
  KEY `fk_system_oauth2_access_token_refresh_token_id` (`refresh_token_id`),
  KEY `ix_system_oauth2_access_token_family` (`family_id`),
  KEY `ix_system_oauth2_access_token_lookup` (`application_id`,`domain`,`token_digest`),
  CONSTRAINT `fk_system_oauth2_access_token_refresh_token_id` FOREIGN KEY (`refresh_token_id`) REFERENCES `system_oauth2_refresh_token` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='OAuth2 访问令牌';

CREATE TABLE `system_oauth2_approve` (
  `user_id` bigint NOT NULL COMMENT '用户编号',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `client_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户端编号',
  `scope` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '授权范围',
  `approved` tinyint(1) NOT NULL COMMENT '是否接受',
  `expires_time` datetime NOT NULL COMMENT '过期时间',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='OAuth2 批准表';

CREATE TABLE `system_oauth2_client` (
  `client_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户端编号',
  `secret` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户端密钥',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '应用名',
  `logo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '应用图标',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '应用描述',
  `status` smallint NOT NULL COMMENT '状态',
  `user_type` smallint DEFAULT NULL COMMENT '绑定的用户类型',
  `access_token_validity_seconds` int NOT NULL COMMENT '访问令牌的有效期',
  `refresh_token_validity_seconds` int NOT NULL COMMENT '刷新令牌的有效期',
  `redirect_uris` json NOT NULL COMMENT '可重定向的 URI 地址 (JSON 数组)',
  `authorized_grant_types` json NOT NULL COMMENT '授权类型 (JSON 数组)',
  `scopes` json NOT NULL COMMENT '授权范围 (JSON 数组)',
  `auto_approve_scopes` json DEFAULT NULL COMMENT '自动通过的授权范围 (JSON 数组)',
  `authorities` json DEFAULT NULL COMMENT '权限 (JSON 数组)',
  `resource_ids` json DEFAULT NULL COMMENT '资源 (JSON 数组)',
  `additional_information` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '附加信息',
  `credential_revision` int NOT NULL COMMENT '客户端密钥版本',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_id` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='OAuth2 客户端表';

CREATE TABLE `system_oauth2_code` (
  `user_id` bigint NOT NULL COMMENT '用户编号',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `code_digest` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '授权码 SHA-256 摘要',
  `client_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户端编号',
  `scopes` json DEFAULT NULL COMMENT '授权范围 (JSON 数组)',
  `expires_time` datetime NOT NULL COMMENT '过期时间',
  `redirect_uri` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '可重定向的 URI 地址',
  `state` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '状态',
  `consumed` tinyint(1) NOT NULL COMMENT '授权码是否已消费',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_oauth2_code_digest` (`code_digest`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='OAuth2 授权码表';

CREATE TABLE `system_oauth2_refresh_token` (
  `user_id` bigint NOT NULL COMMENT '用户编号',
  `token_digest` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '刷新令牌 SHA-256 摘要',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `client_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户端编号',
  `scopes` json DEFAULT NULL COMMENT '授权范围 (存储为JSON)',
  `expires_time` datetime NOT NULL COMMENT '过期时间',
  `family_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会话族编号',
  `credential_revision` int NOT NULL COMMENT '签发时的凭据版本',
  `revoked` tinyint(1) NOT NULL COMMENT '是否撤销',
  `consumed_time` datetime DEFAULT NULL COMMENT '轮换消费时间，保留记录用于重放检测',
  `application_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '应用标识',
  `domain` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '认证域',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_oauth2_refresh_token_digest` (`token_digest`),
  KEY `ix_system_oauth2_refresh_token_lookup` (`application_id`,`domain`,`token_digest`),
  KEY `ix_system_oauth2_refresh_token_family` (`family_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='OAuth2 刷新令牌';

CREATE TABLE `system_operate_log` (
  `trace_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '链路追踪编号',
  `user_id` bigint NOT NULL COMMENT '用户编号',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作模块类型',
  `sub_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作名',
  `biz_id` bigint NOT NULL COMMENT '操作数据模块编号',
  `action` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作内容',
  `extra` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '拓展字段',
  `request_method` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '请求方法名',
  `request_url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '请求地址',
  `user_ip` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户 IP',
  `user_agent` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '浏览器 UA',
  `user_info` json NOT NULL COMMENT '用户信息 (JSON 格式)',
  `event_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '审计预留编号',
  `result` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'pending/success/failure/cancelled',
  `duration_ms` float DEFAULT NULL COMMENT '操作耗时毫秒',
  `lease_until` datetime DEFAULT NULL COMMENT '审计预留有效期',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志记录';

CREATE TABLE `system_post` (
  `code` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '岗位编码',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '岗位名称',
  `sort` int NOT NULL COMMENT '显示顺序',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）【StatusEnum】',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_post_active_0` (`code`,`active_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='岗位信息表';

CREATE TABLE `system_role` (
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名称',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色权限字符串',
  `sort` int NOT NULL COMMENT '显示顺序',
  `data_scope` smallint NOT NULL COMMENT '数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限 5：本人数据）',
  `data_scope_dept_ids` json NOT NULL COMMENT '数据范围(指定部门数组)',
  `builtin` smallint NOT NULL COMMENT '内置类型（1-内置 2-自定义）【BuiltinTypeEnum】',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_role_active_0` (`code`,`active_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色信息表';

CREATE TABLE `system_role_menu` (
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `menu_id` bigint NOT NULL COMMENT '菜单ID',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_role_menu_active_0` (`role_id`,`menu_id`,`active_key`),
  CONSTRAINT `fk_system_role_menu_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色和菜单关联表';

CREATE TABLE `system_sms_channel` (
  `signature` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '短信签名',
  `code` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '渠道编码【SmsChannelEnum】',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `api_key` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '短信 API 的账号',
  `api_secret` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信 API 的秘钥',
  `callback_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信发送回调 URL',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='短信渠道信息表';

CREATE TABLE `system_sms_code` (
  `mobile` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `code` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '验证码',
  `create_ip` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '创建 IP',
  `scene` smallint NOT NULL COMMENT '发送场景',
  `today_index` smallint NOT NULL COMMENT '今日发送的第几条',
  `used` tinyint(1) NOT NULL COMMENT '是否使用',
  `used_time` datetime DEFAULT NULL COMMENT '使用时间',
  `used_ip` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '使用 IP',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='手机验证码表';

CREATE TABLE `system_sms_log` (
  `channel_id` bigint NOT NULL COMMENT '短信渠道编号',
  `channel_code` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '短信渠道编码',
  `template_id` bigint NOT NULL COMMENT '模板编号',
  `template_code` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板编码',
  `template_type` smallint NOT NULL COMMENT '短信类型【SmsTemplateTypeEnum】',
  `template_content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '短信内容',
  `template_params` json NOT NULL COMMENT '短信参数',
  `api_template_id` varchar(63) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信 API 的模板编号',
  `mobile` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `user_id` bigint DEFAULT NULL COMMENT '用户编号',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `send_status` smallint NOT NULL COMMENT '发送状态',
  `send_time` datetime DEFAULT NULL COMMENT '发送时间',
  `api_send_code` varchar(63) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信 API 发送结果的编码',
  `api_send_msg` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信 API 发送失败的提示',
  `api_request_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信 API 发送返回的唯一请求 ID',
  `api_serial_no` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '短信 API 发送返回的序号',
  `receive_status` smallint NOT NULL COMMENT '接收状态',
  `receive_time` datetime DEFAULT NULL COMMENT '接收时间',
  `api_receive_code` varchar(63) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'API 接收结果的编码',
  `api_receive_msg` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'API 接收结果的说明',
  `send_claim_token` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '外发 claim 令牌',
  `send_claim_until` datetime DEFAULT NULL COMMENT '外发前 claim 到期时间',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='短信日志表';

CREATE TABLE `system_sms_template` (
  `type` smallint NOT NULL COMMENT '短信类型【SmsTemplateTypeEnum】',
  `builtin` smallint NOT NULL COMMENT '内置类型（1-内置 2-自定义）【BuiltinTypeEnum】',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）【StatusEnum】',
  `code` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板编码',
  `name` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板名称',
  `content` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板内容',
  `params` json NOT NULL COMMENT '参数数组',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `api_template_id` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '短信 API 的模板编号',
  `channel_id` bigint NOT NULL COMMENT '短信渠道编号',
  `channel_code` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '短信渠道编码',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_sms_template_active_0` (`code`,`active_key`),
  KEY `fk_system_sms_template_channel_id` (`channel_id`),
  CONSTRAINT `fk_system_sms_template_channel_id` FOREIGN KEY (`channel_id`) REFERENCES `system_sms_channel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='短信模板表';

CREATE TABLE `system_social_client` (
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '应用名',
  `social_type` smallint NOT NULL COMMENT '社交平台的类型【SocialTypeEnum】',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `client_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户端编号',
  `client_secret` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户端密钥，支付宝等渠道存放 PEM 私钥',
  `agent_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '代理编号',
  `auth_config` json NOT NULL DEFAULT (_utf8mb4'{}') COMMENT '认证配置，JSON格式',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_social_client_active_0` (`social_type`,`user_type`,`active_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社交客户端表';

CREATE TABLE `system_social_user` (
  `type` smallint NOT NULL COMMENT '社交平台的类型【SocialTypeEnum】',
  `openid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '社交 openid',
  `token` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '社交 token',
  `raw_token_info` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '原始 Token 数据，一般是 JSON 格式',
  `nickname` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户昵称',
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户头像',
  `raw_user_info` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '原始用户数据，一般是 JSON 格式',
  `code` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '最后一次的认证 code',
  `state` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '最后一次的认证 state',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `client_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '第三方应用编号',
  `subject_type` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '第三方主体类型',
  `application_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '本站社交应用标识',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_social_user_active_0` (`type`,`openid`,`client_id`,`subject_type`,`application_id`,`active_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社交用户表';

CREATE TABLE `system_social_user_bind` (
  `user_id` bigint NOT NULL COMMENT '用户编号',
  `user_type` smallint NOT NULL COMMENT '用户类型（枚举）【UserTypeEnum】',
  `social_type` smallint NOT NULL COMMENT '社交平台的类型【SocialTypeEnum】',
  `social_user_id` bigint NOT NULL COMMENT '社交用户的编号',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_social_user_bind_active_0` (`user_type`,`social_type`,`social_user_id`,`active_key`),
  UNIQUE KEY `uq_system_social_user_bind_active_1` (`user_type`,`social_type`,`user_id`,`active_key`),
  KEY `fk_system_social_user_bind_social_user_id` (`social_user_id`),
  CONSTRAINT `fk_system_social_user_bind_social_user_id` FOREIGN KEY (`social_user_id`) REFERENCES `system_social_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社交绑定表';

CREATE TABLE `system_user_post` (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `post_id` bigint NOT NULL COMMENT '岗位ID',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_user_post_active_0` (`user_id`,`post_id`,`active_key`),
  KEY `fk_system_user_post_post_id` (`post_id`),
  CONSTRAINT `fk_system_user_post_post_id` FOREIGN KEY (`post_id`) REFERENCES `system_post` (`id`),
  CONSTRAINT `fk_system_user_post_user_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户岗位表';

CREATE TABLE `system_user_profiles` (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `bio` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '个人简介',
  `tags` json DEFAULT NULL COMMENT '用户标签',
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '地址',
  `skills` json DEFAULT NULL COMMENT '技能标签',
  `work_scope` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '工作职责描述',
  `expertise` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '专业领域',
  `communication_style` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '沟通风格（formal/casual/technical）',
  `ai_preference` json DEFAULT NULL COMMENT 'AI 交互偏好（用户主动设置）',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_user_profiles_active_0` (`user_id`,`active_key`),
  KEY `ix_system_user_profiles_user_id` (`user_id`),
  CONSTRAINT `fk_system_user_profiles_user_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户详情表';

CREATE TABLE `system_user_role` (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_user_role_active_0` (`user_id`,`role_id`,`active_key`),
  KEY `fk_system_user_role_role_id` (`role_id`),
  CONSTRAINT `fk_system_user_role_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`),
  CONSTRAINT `fk_system_user_role_user_id` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

CREATE TABLE `system_users` (
  `username` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户账号',
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `nickname` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户昵称',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `dept_id` bigint DEFAULT NULL COMMENT '部门ID',
  `post_ids` json DEFAULT NULL COMMENT '岗位编号列表（JSON 格式）',
  `email` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户邮箱',
  `mobile` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号码',
  `sex` smallint DEFAULT NULL COMMENT '用户性别',
  `avatar` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像地址',
  `status` smallint NOT NULL COMMENT '开启状态（1-启用，0-禁用）',
  `login_ip` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后登录IP',
  `login_date` datetime DEFAULT NULL COMMENT '最后登录时间',
  `active_key` smallint GENERATED ALWAYS AS ((case when (`deleted` = 0) then 1 else NULL end)) VIRTUAL COMMENT '仅有效记录参与业务唯一约束',
  `credential_revision` int NOT NULL COMMENT '凭据版本，改密或账号状态变化时递增',
  `authorization_revision` int NOT NULL COMMENT '权限版本，与授权变化原子提交',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_time` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_system_users_active_0` (`username`,`active_key`),
  KEY `fk_system_users_dept_id` (`dept_id`),
  CONSTRAINT `fk_system_users_dept_id` FOREIGN KEY (`dept_id`) REFERENCES `system_dept` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息表';

SET FOREIGN_KEY_CHECKS=1;
