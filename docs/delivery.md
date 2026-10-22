# 本轮交付记录

2026-10-22。本记录保留本地实现阶段的验证边界；下方联动验收补充发布后的真实结果。

## 输入与结果

- 源仓库：Halckon/koven，固定提交 `acfacca31a5f43d9999c018bcb1f29d3bd786c6f`。
- 该分支已启用 Guide v0.46；当时 main 仍为 v0.45。站点不把设计等同于实现完成。
- 10 个设计章节、23 个动手入门章节；导入 22 个执行合同（17 正例、4 诊断、1 planned）。
- 15 页规范全文、8 个路线图阶段均从该来源生成；未改教程源码和输出 oracle。
- 独立站点已初始化本地 Git；主仓库配套工作位于 `feature/spec-0344-site-content-sync`。

## 验证

- 带 `KOVEN_SOURCE` / `KOVEN_REF` 的 `npm test`：11 项全部通过，无跳过。
- `npm run check-content -- --source <checkout> --ref acfacca31a5f43d9999c018bcb1f29d3bd786c6f`：通过。
- `npm run build`：快照校验、vue-tsc 和生产构建通过；完整规范数据形成一个较大的共享 chunk，Vite 提示超过 500 kB，gzip 约 212 kB，非构建失败。
- 主仓库 `python3 scripts/check_docs.py`：732 篇文档结构检查通过；不证明语义等价。
- 两份 workflow 的 YAML 与 shell 语法通过；主仓库通知命令的已配置/未配置 mock 通过，未发网络请求。
- 浏览器：1440px 桌面与 375px 视口（可用内容宽 360px）检查；主导航、手机目录、前后翻章与 ArrowRight、诊断 L0131、多文件输入组合、规范深链接、8阶段路线图和深色主题实际核验。
- 计划示例没有运行命令或预期输出；源码代码框可局部横滚，页面无横向溢出。
- reduced-motion CSS 与路由行为保留并静态检查，未模拟操作系统减少动态效果设置。
- 独立上下文审查发现的标题变化导致浏览器异常、nightly通知提交与实际检出不一致问题均已修复并复审；复审独立重跑11测试通过。
- 视觉对照为 Gleam 门户与 Tour 的真实截图，学习入口、目录、代码阅读布局通过独立审查；不宣称提供其浏览器编译器，也不宣称优于未取证的 Gleam 手机端。
- Vite 保持6系列，升级安全补丁后 npm 安装审计为0漏洞；Markdown 使用 markdown-it（MIT），禁用原始HTML。

## 尚未验证

真实 GitHub Actions、repository_dispatch 送达、Pages 发布及自定义域名未执行。
本次未运行编译器 native 门禁；示例仍由主仓库既有 CI 验证，站点合同检查不替代 native 证据。
主仓库 SPEC-0344 保持 in-progress，待远端配置与交付闭环后归档。

## 远端发布与联动验收

- 公开仓库：`koven-lang/koven-site`；Pages：<https://koven-lang.github.io/koven-site/>。
- 主仓库通知工作流由 PR #124 合入 `Halckon/Koven` main，目标变量及专用 Repository secret 已配置。
- 主仓库手动通知运行 `39784467407` 成功，触发站点运行 `39784489466`，构建和部署均成功。
- 用户确认暂保留 v0.46 固定快照，合入 main 后再切换；主仓库更新会触发重建，但当前内容仍来自固定版本。
- 切换 main 消费策略前需增加过期通知防护，避免旧成功 CI 重跑发布旧提交。
