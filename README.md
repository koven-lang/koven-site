# Koven 门户与 Tour

独立的 Vue 3 + TypeScript + Vite 站点。门户提供学习入口；Tour 分为 v0.46 设计与动手入门；
规范全文和路线图来自主仓库。页面没有在线编译器；输出均明确标为主仓库合同中的预期输出。

## 本地开发

要求 Node 22、Python 3.12+ 和 Git。使用已有主仓库 checkout：

```bash
npm ci
npm run sync-content -- --source /path/to/Koven --ref acfacca31a5f43d9999c018bcb1f29d3bd786c6f
KOVEN_SOURCE=/path/to/Koven KOVEN_REF=acfacca31a5f43d9999c018bcb1f29d3bd786c6f npm test
npm run build
npm run dev -- --host 127.0.0.1
```

提交的 `generated.json` 是可离线预览的生成快照，带完整来源 SHA 和各文件 SHA256；CI 每次重新生成，
失败就停止，不回退旧快照。来源只读取 Git 中已提交的内容，不包含工作树未提交修改，不执行来源仓库脚本。
`npm run check-content -- --source /path/to/Koven --ref <相同ref>` 可检查快照是否一致。

## 内容归属

| 内容 | 真源 |
|---|---|
| 教程源码与说明 | 主仓库 `docs/tutorials/koven-tour.md` 的具名 fence |
| 输出、argv、完整诊断与 planned 状态 | 主仓库 `docs/tutorials/examples.json` |
| 语言设计与规范全文 | 主仓库 `docs/guide/` |
| 实施阶段与任务状态 | 主仓库 `docs/roadmap/v1.json` |
| Hero、导航、章节显示名称、布局 | 本站 `src/` |

主仓库已有真实 CLI build / artifact / run 门禁，复用它，不另造 `examples/tour/` 副本。
新增语义示例先修改主仓库合同。站点测试不替代编译器测试。

## 独立部署

在 GitHub 创建独立站点仓库并推送本目录；Pages Source 选择 **GitHub Actions**。
工作流位于 `.github/workflows/deploy.yml`，无嵌套 working-directory 和站点路径过滤：

- 站点 main push、手动执行或 `repository_dispatch: koven-content-updated` 构建并部署。
- PR 只测试和上传构建产物，不部署。
- 按 `content-source.json` 检出主仓库并生成内容，不接受 dispatch payload 提供的任意仓库/ref。nightly 固定通知 SHA，额外确认该提交在 main 且有成功的上游 push CI；手动/main-push 构建同样检查实际 checkout SHA。
- 当前固定 v0.46 设计提交；v0.46 合入 main 后把 ref 改为 `main` 即为 nightly。
- 稳定版将 ref 改成真实 tag；一次构建始终只使用一个 revision，不混用版本。当前没有虚构的稳定版选择器。
- 主仓库通知工作流使用变量 `KOVEN_SITE_REPOSITORY=owner/repo` 与 secret `KOVEN_SITE_DISPATCH_TOKEN`。
  使用只对站点仓库具有 Contents write 的细粒度 token，保存在主仓库 Actions secrets，不能放入源码。

hash 路由与相对资源路径支持根域名和 GitHub Pages 子路径。确定自定义域名后在 Pages 配置，
当前不写入虚构域名或 CNAME。迁移旧 URL 时应在旧站保留跳转；本轮没有删除旧远端站点。

## 设计与验证

参照 [Gleam 门户](https://gleam.run/) 的清晰学习入口与 [Gleam Tour](https://tour.gleam.run/) 的
目录/前后导航。对照标准是学习入口可发现、章节切换顺畅、代码可读和移动端无横向页面溢出；
不把 Gleam 的浏览器执行能力作为本项目已提供功能。

详见 [交付说明](docs/delivery.md)。
