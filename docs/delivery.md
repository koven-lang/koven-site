# 本轮交付记录

2026-10-22。站点本地更新；尚未创建远端站点仓库、设置 Pages 或跨仓通知 secret，未提交、未发布。

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
