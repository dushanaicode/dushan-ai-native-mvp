# DuShan AI Native MVP 前端

默认应用为 `apps/web-ele`，使用 Vue、TypeScript、Vben 与 Element Plus。沿用上游工作区依赖及锁文件，保留登录、布局、权限路由、请求封装和通用业务页面；移除租户管理、套餐、登录选择器及租户请求参数。

## 版本与启动

- Node **24.16.0**，见 [.node-version](.node-version)。
- pnpm **11.16.0**，以 [package.json](package.json) 的 `packageManager` 为准。
- 工作区根版本 **5.7.0**，web-ele **5.8.0**；这些是来源组件版本。

整体运行优先使用 [根目录 Docker 启动方式](../README.md#快速启动)。独立开发时，在本目录使用锁定工具：

```bash
mkdir -p Temp/dev
export TEMP="$PWD/Temp/dev" TMP="$PWD/Temp/dev" TMPDIR="$PWD/Temp/dev"
export COREPACK_HOME="$PWD/Temp/corepack" npm_config_cache="$PWD/Temp/npm"
pnpm install --frozen-lockfile --store-dir "$PWD/Temp/pnpm-store"
pnpm --filter @vben/web-ele dev
```

后端代理和开发端口由 `apps/web-ele/.env.development` 配置。并行运行完整版时，为本项目分配独立端口。部署构建使用 `pnpm build:ele`，对应正式 [Dockerfile](scripts/deploy/Dockerfile)。

## 接口与业务页面

请求沿用 `apps/web-ele/src/api/request.ts` 与会话协调器。登录后由权限接口装配用户、角色、菜单和权限码；刷新、退出及跨标签页会话变化仍由统一会话逻辑处理。

前端以字符串传递雪花 ID；分页使用 `page` / `pageSize`。新增页面与 API 分别放入 `src/views/`、`src/api/` 的业务目录。公共包保持应用无关，不从 `#/api` 等应用入口反向导入。

注册、社交登录、扫码登录等入口仍使用各自的明确开关；前后端开启条件必须一致。生产构建中的 `VITE_APP_QR_LOGIN_ORIGIN` 应与浏览器实际访问的站点源一致。

## 检查

```bash
pnpm --filter @vben/web-ele typecheck
pnpm test:native
pnpm build:ele
```

业务前端测试统一位于 [dushan-test/frontend](../dushan-test/frontend)。原有 Vben 版权与许可证保留；其他应用及公共包作为既有工作区内容保留，默认 Docker 仅构建 web-ele 及其依赖。
