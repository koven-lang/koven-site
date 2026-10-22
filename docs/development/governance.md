# 网站里程碑与 Spec 治理

> 性质：工作规则；状态：current；读取时机：网站新能力立项；真源：本页的网站治理。

生态总规划由 [Koven 主仓库](https://github.com/Halckon/koven)的 `docs/development/ecosystem/README.md` 管理。
本次与主仓库文档分别交付；在主仓库合入后核实提交，不把未合入路径当成已发布契约。
本仓库只维护前端、导航、呈现和内容生成；Guide、教程源码及执行合同保持上游真源。

## 流程

先仓库里程碑，再单一 Goal 的 Spec，再分支实施与联合验收。生态规划不能替代已批准语义或生产方接口。
每个 Spec 归属一个 SITE-V1-M*；可引用其他仓库真实 ID 和固定提交，不复制生产方状态。
2026-10-22 用户追加按里程碑持续实施，覆盖范围内且依赖完备的 Spec 及分支／PR 交付；
不自动授权修改语言来源版本、上线新服务或开放执行未经隔离的源码。

Spec 编号本仓库独立，首次正式立项从未占用编号开始；当前只登记候选主题，不建占位编号。
生命周期 draft → approved → in-progress → done；done／superseded 归档到 docs/archive/specs。
草案、active 分别放 docs/specs/drafts、docs/specs/active；索引随路径变化更新，不删除历史失败证据。
里程碑 draft／approved／in-progress／completed，取消或延期保留理由与后继归属。
近期里程碑统一记录在索引正文；拆页时迁移链接，不维护重复状态账本。

## 必填合同

里程碑：目标、非目标、基线、优先级、必需子 Spec／候选项、依赖、联合验收、完成条件、证据。
Spec：主里程碑、单一目标、行为、接口／版本、失败场景、依赖、测试、完成标准与证据。
前置接口未就绪可用显式 fixture 验 UI，但不算服务联合验收通过。

实施 Spec 从 main 建 feature/spec-<id> 或 fix/spec-<id>；审查、定向测试、PR、CI 通过后归档。
逻辑、协议、共享代码修改须独立审查。现有内容生成脚本继续复用，不并行维护另一份语言 JSON。
纯文案和规划不建空功能 Spec；修改实现前补齐正式合同。

## 验证

内容生成相关修改运行 npm test；页面实现运行 npm run build，交互另验移动端、键盘、深链接、深色及 reduced-motion。
文档修改检查所有本地链接与 git diff --check。当前尚无网站 Spec 生命周期自动门禁；
正式增加／迁移 Spec 时先在对应治理 Spec 建立检查，不能声称本页已提供机器执行保护。
里程碑只在所有必需子项完成且真实联合验收通过后 completed。
