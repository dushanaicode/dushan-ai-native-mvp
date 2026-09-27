# MVP Docker 部署

默认组合是 MySQL、Redis、后端与 web-ele。首次部署按 [根 README](../README.md#快速启动) 生成配置后启动。项目名、镜像标签与环境变量使用 `dushan-mvp` / `MVP_`，与完整版区分。

## 配置和端口

`prepare.py` 从源码默认配置生成 `application/`、随机凭据、Redis 配置和仅供空 MySQL 数据卷使用的 SQL。默认管理员 `admin` 的随机密码只在生成目录的 `credentials.json` 中；其他种子账号关闭。部署 Cookie 为 `mvp_refresh`。

| 变量 | 默认值 | 用途 |
| --- | --- | --- |
| `MVP_RUNTIME_DIR` | `Temp/docker-runtime` | 生成配置的 Linux 可见绝对路径，建议显式设置 |
| `MVP_PUBLIC_ORIGIN` | `http://localhost:28080` | 前端扫码地址，必须与 prepare 的 origin 和浏览器地址一致 |
| `MVP_APP_ENV` | `staging` | 正式环境使用 `prod`，关闭交互 API 文档 |
| `MVP_HTTP_PORT` | `28080` | 本机 HTTP 入口 |
| `MVP_MYSQL_PORT` | `23306` | 本机数据库映射端口 |
| `MVP_REDIS_PORT` | `26379` | 本机缓存映射端口 |

后端 48080 只在容器网络内部开放。HTTP、MySQL、Redis 默认绑定回环地址。普通重启沿用同一 runtime 和数据卷，不重新生成密码或再次执行初始化 SQL。

```bash
export MVP_RUNTIME_DIR="$PWD/Temp/docker-runtime"
export MVP_PUBLIC_ORIGIN=http://localhost:28080
docker compose -f docker/app/compose.yaml config --quiet
docker compose -f docker/app/compose.yaml up -d --build
docker compose -f docker/app/compose.yaml ps
docker compose -f docker/app/compose.yaml logs --tail 100 backend
```

应用 `/api/health` 可从前端入口访问；内部后端健康地址为 `/health`。前后端镜像及基础服务均声明健康检查。MySQL 初始化脚本成功结束才写就绪标记，失败时不能跳过初始化或手工伪造标记。

临时验证应使用数据根也位于本项目 `Temp/` 的独立 Docker Engine；仅设置 `DOCKER_CONFIG` 不能隔离容器数据。生产数据卷属于部署数据，应按运行环境独立管理。

## HTTPS 与上线

生成配置时使用真实的 `--origin https://域名[:端口]`，这会开启 Secure 刷新 Cookie。配置 `MVP_PUBLIC_ORIGIN` 为同一站点源，重新构建前端。

将证书放入部署方管理的目录，包含 `fullchain.pem` 和 `privkey.pem`：

```bash
export MVP_APP_ENV=prod
export MVP_SERVER_NAME=admin.example.com
export MVP_TLS_DIR=/absolute/path/to/certificates
export MVP_HTTPS_BIND=0.0.0.0
export MVP_HTTPS_PORT=443
# MVP_RUNTIME_DIR、MVP_PUBLIC_ORIGIN 应已设置为本次 HTTPS 部署值。
docker compose -f docker/app/compose.yaml -f docker/app/compose.https.yaml config --quiet
docker compose -f docker/app/compose.yaml -f docker/app/compose.https.yaml up -d --build
```

HTTPS 入口直接代理 API/WebSocket 到后端，并保留 Host、协议和客户端地址。后端默认不信任转发头；按实际反向代理 IP/CIDR 设置 `trusted_proxy_cidrs`。不要把任意请求提供的转发头当成真实客户端地址。

只使用一个业务主库。多实例部署时分配不同雪花机器号，并使用已经保留的共享缓存、Job owner 和所选消息/实时传输能力；默认配方是单个后端 worker。

## 文件和可选服务

默认本地文件持久化到 `backend-files` 数据卷。S3 兼容对象存储可在文件配置管理中接入。

- [MinIO](storage/minio/compose.yaml)：本地对象存储联调，默认端口 29000/29001。镜像从固定上游源码构建；该历史社区版本沿用上游定位，不作为持续维护的云存储服务承诺。
- [RabbitMQ](mq/rabbitmq/compose.yaml)、[Kafka](mq/kafka/compose.yaml)：显式选择相应 MQ 后端时启用，默认使用 Redis。
- [邮件测试](mailpit/compose.yaml)、[FTP](storage/ftp/compose.yaml)、[SFTP](storage/sftp/compose.yaml)：供需要这些协议的场景使用。
- [监控](monitor/README.md)：按需求启用追踪导出及可视化，默认应用不依赖监控服务才能启动。
- `db/` 其他配方用于保留的数据库适配器；厂商镜像仍需按自身许可提供。应用一次只选择一个业务主库。

可选服务单独启动时，应明确连接地址、端口和网络。若与完整版同时运行，为可选服务分配不同端口。镜像和随包资源遵循其各自许可证。

## 备份和恢复

在仓库根目录使用同一 Compose 配置；以下 Bash 示例读取容器内凭据文件，不把密码放到命令行参数中：

```bash
mkdir -p Temp/backups
docker compose -f docker/app/compose.yaml exec -T mysql sh -c \
  'MYSQL_PWD="$(cat /run/secrets/mysql_root_password)" mysqldump -u root --single-transaction --routines --triggers --events --set-gtid-purged=OFF --no-tablespaces dushan_mvp' \
  > Temp/backups/application.sql
```

同时备份 runtime 配置、密钥和文件数据卷。数据库备份包含业务数据及凭据，保存在私有位置，不进入公开仓库。

恢复先新建独立空库验证，不直接覆盖正在运行的库：

```bash
docker compose -f docker/app/compose.yaml exec -T mysql sh -c \
  'MYSQL_PWD="$(cat /run/secrets/mysql_root_password)" mysql -u root -e "CREATE DATABASE dushan_mvp_restore CHARACTER SET utf8mb4"'
docker compose -f docker/app/compose.yaml exec -T mysql sh -c \
  'MYSQL_PWD="$(cat /run/secrets/mysql_root_password)" mysql -u root dushan_mvp_restore' \
  < Temp/backups/application.sql
```

核对表、数据、登录和业务闭环后再安排切换。不要对已有卷重跑空库初始化目录，也不要用删除数据卷解决配置或健康检查错误。
