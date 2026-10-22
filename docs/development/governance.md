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

Spec 编号本仓库独立；正式合同在 docs/inventory.json 登记 ID→路径，正文首行 metadata 是状态真源。
候选主题不分配编号，不建空占位 Spec。
生命周期 draft → approved → in-progress → done；done／superseded 归档到 docs/archive/specs。
草案、active 分别放 docs/specs/drafts、docs/specs/active；索引随路径变化更新，不删除历史失败证据。
里程碑 draft／approved／in-progress／completed，取消或延期保留理由与后继归属。
正式里程碑放 docs/milestones/drafts 或 active，完成／取消归入 docs/archive/milestones；
只在正文 metadata 维护状态，索引链接正文。尚未细化的远期规划保留在索引，不充当正式合同。
渐进立项可以先登记一份 Spec；关闭里程碑时至少两份真实 Spec 且全部完成，不能以空占位合同凑数。

## 必填合同

里程碑：目标、非目标、基线、优先级、必需子 Spec／候选项、依赖、联合验收、完成条件、证据。
Spec：主里程碑、单一目标、行为、接口／版本、失败场景、依赖、测试、完成标准与证据。
前置接口未就绪可用显式 fixture 验 UI，但不算服务联合验收通过。

实施 Spec 从 main 建 feature/spec-<id> 或 fix/spec-<id>；审查、定向测试、PR、CI 通过后归档。
逻辑、协议、共享代码修改须独立审查。现有内容生成脚本继续复用，不并行维护另一份语言 JSON。
纯文案和规划不建空功能 Spec；修改实现前补齐正式合同。

## 验证

内容生成相关修改运行 npm test；页面实现运行 npm run build，交互另验移动端、键盘、深链接、深色及 reduced-motion。
文档修改运行 npm run check-docs 与 git diff --check。检查器核库存双向覆盖、唯一身份／路径、状态目录、
归属、无环同类依赖、存在的证据与本地链接／锚点；检查器不访问外部仓库，也不证明证据内容真实。
approved／in-progress Spec 必须无 blocker 且本地前置 done；跨仓库前置按原规则人工核实。
检查器复用编辑器仓库固定提交 17f0f1b2 的标准库实现，网站只适配 ID、渐进立项和活动前置检查。
实现边界与命令见 [文档门禁架构](../architecture/documentation-gate.md)；来源声明见
[内容来源仓库身份](../architecture/source-identity.md)。
里程碑只在所有必需子项完成且真实联合验收通过后 completed。
