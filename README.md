# DuShan AI Native MVP

面向快速验证产品、能够独立部署的通用前后端底座，与 [DuShan AI Native](https://github.com/dushanaicode/dushan-ai-native) 完整版配套。

MVP 保留业务开发和上线所需的基础能力，重点简化数据库拓扑与部署，移除多租户及后端国际化组件。业务模块目录、DI、SPI、接口响应、分页和雪花 ID 约定继续沿用完整版，方便后续迁移业务。

## 当前基线

来自 Native **0.0.0**，提交 `cd21ddf29ea8d3f7134c31eca1b903cac959da75`。Python 包版本继续为 **0.0.0**；前端根版本 **5.7.0**、web-ele **5.8.0** 是上游各自的版本号，不作为 MVP 产品版本。

完整来源、各包版本及原始锁文件哈希见 [UPSTREAM.json](UPSTREAM.json)。更新基座时先选择明确的上游提交，再迁入适用修复并验证，不自动覆盖业务代码。

## 能力范围

| 部分 | MVP 保留的能力 |
| --- | --- |
| 基础框架 | Common、模块与扫描、DI、配置、日志、Redis 缓存、Excel、验证码、IP |
| 数据访问 | 单主库、事务传播、回滚、提交回调、软删除、审计、雪花 ID、分页和数据权限 |
| 身份与权限 | 密码与短信登录、注册与找回、社交登录、扫码登录、角色菜单、部门岗位、会话撤销 |
| 数据范围 | 全部、自定义部门、本部门、部门及子部门、本人；支持多角色规则合并 |
| 通用业务 | 用户、字典、业务配置、通知、短信与邮件、操作审计、文件管理和代码生成 |
| 实时与异步 | WebSocket、定时任务、消息队列、Outbox、重试、签名与防重放 |
| 部署 | 默认 MySQL + Redis，前后端 Docker 镜像、健康检查、持久化文件卷；可选 S3/MinIO 与其他适配器 |

已移除应用多租户、租户套餐、租户切换、租户任务分发、后端 `starter_i18n`，以及业务数据库的动态多源和读写分离。前端语言资源保留。外部数据库连接管理仍供数据库工具和代码生成使用，修改它不会切换应用主库。

## 快速启动

需要 Docker Engine 和支持 `include` 的 Docker Compose。下面在仓库根目录使用 Bash 执行；Windows 可在 WSL 中执行。

```bash
mkdir -p Temp
docker build -t dushan-mvp-backend:local dushan-admin-backend

docker run --rm --user "$(id -u):$(id -g)" \
  --mount "type=bind,source=$PWD,target=/workspace" \
  --workdir /workspace \
  --env TEMP=/workspace/Temp --env TMP=/workspace/Temp --env TMPDIR=/workspace/Temp \
  --entrypoint python dushan-mvp-backend:local \
  -B docker/prepare.py --output Temp/docker-runtime --origin http://localhost:28080

export MVP_RUNTIME_DIR="$PWD/Temp/docker-runtime"
export MVP_PUBLIC_ORIGIN=http://localhost:28080
docker compose -f docker/app/compose.yaml up -d --build
```

打开 **http://localhost:28080**。初始账号为 `admin`，随机密码在 `Temp/docker-runtime/credentials.json` 的 `admin` 字段中。公共 SQL 不含可用默认密码。

生成目录不能覆盖重建。已有数据库再次部署时，继续使用原配置和密钥；SQL 初始化只用于空数据卷。`Temp/` 与 `.docs/` 都不进入版本库。

默认端口：前端 `28080`、MySQL `23306`、Redis `26379`，均绑定本机回环。对外部署、HTTPS、存储及备份见 [Docker 说明](docker/README.md)。

## 开发与维护

- [后端](dushan-admin-backend/README.md)：目录、配置和业务接入约定。
- [前端](dushan-admin-frontend/README.md)：Node/pnpm 版本、应用与请求约定。
- [测试](dushan-test/README.md)：测试入口、隔离资源与验证范围。

每个产品基于此底座维护自己的业务仓库。迁入完整版时，需要明确用户、数据与目标租户的归属映射；本项目不承诺任意业务的一键无损升级。

项目采用 [MIT License](LICENSE)。前端及字体、IP 数据等随包资源保留其原始来源与许可证。
