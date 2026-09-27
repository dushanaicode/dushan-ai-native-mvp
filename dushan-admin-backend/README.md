# DuShan AI Native MVP 后端

Python 3.12 + FastAPI，基于 Native 0.0.0。依赖版本由各包 `pyproject.toml` 与根 `poetry.lock` 固定；不在业务启动时安装或猜测依赖。

## 运行

完整首次启动见 [根 README](../README.md#快速启动)。默认部署启用 `framework`、`system`、`infra`，使用一个 MySQL 主库和一个独立 Redis 实例。

本地开发需要 Python 3.12 和 Poetry 2.2.1。在本目录执行：

```bash
mkdir -p Temp/setup
export TEMP="$PWD/Temp/setup" TMP="$PWD/Temp/setup" TMPDIR="$PWD/Temp/setup"
export POETRY_CACHE_DIR="$PWD/Temp/poetry" PIP_CACHE_DIR="$PWD/Temp/pip"
export POETRY_VIRTUALENVS_PATH="$PWD/Temp/venvs" POETRY_VIRTUALENVS_IN_PROJECT=false
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1
poetry env use python3.12
poetry install --only main,core
```

开发配置放在 `Temp/dev-config/`。可从 Docker 生成的 `application/` 复制配置，沿用已初始化数据库的密码和应用密钥，将数据库地址改为 `127.0.0.1:23306`，Redis 改为 `127.0.0.1:26379`，并把 `system.allowed_origins` 配成开发前端的实际站点源。

```bash
export DUSHAN_CONFIG_DIR="$PWD/Temp/dev-config"
export SERVER_ENV=dev SERVER_PORT=48081
poetry run python -B app.py
```

数据库和 Redis 的地址必须与实际启动资源一致。不要同时启动使用相同雪花机器号的两个应用实例；本地开发使用独立机器号。默认 `application.yaml` 仅开启 framework，不会用隐式凭据连接数据库。

## 目录与接入

- `framework/`：通用能力与各 Starter。
- `server/`：应用工厂、配置、装配和生命周期。
- `module_system/`：认证、权限及系统业务。
- `module_infra/`：配置、文件、数据库工具、代码生成、任务和消息管理。
- `sql/mysql/`：MVP 新安装基线。完整版历史升级脚本不适用于该基线。

新增模块沿用 `module.toml`、本模块 `pyproject.toml` 及 API/Controller/Service/Mapper/DO 的组织方式，并在根依赖和模块配置中显式启用。DI、Scanner、SPI 的使用方式与完整版保持一致。

DO 继承 `BaseDO`。每个持久模型明确使用 `@public_data()` 或 `@data_permission(...)` 声明访问范围；后者继续支持用户及部门归属。路由声明身份与权限，客户端参数不能决定授权范围。应用没有租户基类、默认租户或租户占位提供器。

HTTP 沿用 `code/message/data/error` 响应，分页参数为 `page/pageSize`；Python 内部 ID 为整数，HTTP 雪花 ID 使用字符串。后端错误采用声明的消息，前端语言资源独立保留。

## 数据库与可选能力

`database.sources` 只能配置一个 `primary`。连接参数变更后重启应用；没有动态源注册和副本路由。事务传播、回滚、提交回调、锁、软删除、审计及数据权限保持。

Infra 的数据源管理用于外部查询和代码生成，不会替换应用主库。成熟数据库驱动保留；国产专用驱动仍通过 `database-domestic` 可选组安装。

Logging、Cache、DI 等完整能力保留。MQ 默认使用 Redis，RabbitMQ/Kafka、监控导出、社交及云验证码等按业务显式配置；关闭可选功能不会把受保护接口变成公开接口。

数据库备份任务默认关闭；启用前提供可执行的 MySQL `mysqldump` 并配置输出目录。容器部署的备份也可直接使用 MySQL 容器中的客户端，见 [Docker 说明](../docker/README.md)。

测试统一在 [dushan-test](../dushan-test/README.md)，后端目录不重复维护测试。
