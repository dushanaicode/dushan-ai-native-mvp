# MVP 测试

本目录跟随 Native 基线迁入，并按单数据库、无应用租户的接口同步。保留事务、权限、生命周期、消息、文件和业务回归；租户套餐、租户路由与旧数据库迁移的专属用例不再适用。

## 环境与运行

使用 Python 3.12，在已安装后端 `main,core` 锁定依赖的同一隔离环境中安装 [requirements.txt](requirements.txt)。解释器、pip 缓存及测试产物放在当前工作目录的 `Temp/`，不改写 HOME/USERPROFILE。

PowerShell 入口从仓库根目录执行，`-Python` 指向上述解释器：

```powershell
.\dushan-test\run-tests.ps1 -Python .\Temp\test-python\Scripts\python.exe -Paths framework/common
.\dushan-test\run-tests.ps1 -Python .\Temp\test-python\Scripts\python.exe -ResourcesFile .\Temp\test-resources.json -IncludeSmoke
```

每次运行生成独立 `Temp/dushan-tests/<时间>/`，包含 fixtures、缓存和 JUnit。脚本会恢复调用前的进程环境。Linux 也可直接使用 pytest，显式指定 `--basetemp`、`cache_dir`、JUnit 路径与 TEMP/TMP/TMPDIR。

## 真实资源

集成测试使用专用 Docker MySQL、Redis、MinIO。部分测试会制造连接故障，不能指向正在工作的产品实例。业务测试创建独立临时 schema，并使用专用 Redis DB 10/11；框架测试使用随机表名和缓存前缀。

`-ResourcesFile` 读取 JSON 清单，其结构如下；值填写实际隔离实例，不提交该文件：

```json
{
  "mysql": {
    "host": "127.0.0.1", "port": 3306, "database": "mvp_test",
    "username": "mvp_test", "password": "测试账号密码", "root_password": "测试实例管理密码",
    "server_uuid": "SELECT @@server_uuid 的结果"
  },
  "redis": {
    "host": "127.0.0.1", "port": 6379, "password": "测试实例密码",
    "run_id": "INFO server 中的 run_id"
  },
  "minio": {
    "host": "127.0.0.1", "port": 9000, "access_key": "测试访问键", "secret_key": "测试秘密键"
  }
}
```

清单必须位于仓库根 `Temp/`。MySQL 测试账号可操作 `database` 指定的测试库；业务建库使用该隔离实例的管理凭据。实例 UUID/run_id 用于核对连接目标。缺少外部服务的测试会明确跳过，跳过不代表该能力已验证。

细分入口 `run-database-tests.ps1`、`run-cache-tests.ps1` 接收专用目标文件，适合单组件回归。RabbitMQ/Kafka、厂商数据库和云服务按对应测试声明提供独立资源；不凭借其他项目的历史通过记录宣布本项目通过。

## 前端

在前端工作区安装锁定依赖后执行 `pnpm test:native`，用例位于 `frontend/`。代码生成、文件预览和 WebSocket 等包含额外的实际服务场景。隔离复制工作区时，可通过 `DUSHAN_FRONTEND_WORKSPACE` 指定包含前端与测试目录的工作区根。

## 浏览器烟测

`tools/browser-smoke.mjs` 验证真实部署中的登录、首页和用户表格，支持当前前端的 hash/history 路由。它使用新建的隔离 Chrome profile；截图及结果只写根 `Temp/`。

设置 `PLAYWRIGHT_ENTRY` 为已安装 Playwright 的 `index.mjs`，`DUSHAN_SMOKE_CREDENTIALS` 为本轮 `docker/prepare.py` 生成的凭据文件，再从仓库根运行：

```bash
node dushan-test/tools/browser-smoke.mjs
```

测试不读取个人浏览器配置。完整版本的历史一次性浏览器复审阶段脚本未带入 MVP；业务组件回归和可重复的当前烟测继续保留。
