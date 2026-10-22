# koven-site 工作入口

- 本仓库只维护 Vue 门户、导航、呈现组件和内容生成脚本。
- 语言规范、教程源码与执行合同位于 `content-source.json` 指定的 Koven 主仓库版本。
- 不手改 `src/data/generated.json`；使用 `npm run sync-content -- --source <checkout> --ref <revision>`。
- 新语言示例须先进入主仓库教程库存与真实 CLI 合同，再同步到站点。
- 设计说明、预期输出和本次实际执行结果必须分开；不得暗示浏览器执行代码。
- `npm test` 验生成器；指定 `KOVEN_SOURCE` 与 `KOVEN_REF` 时核真实库存。`npm run build` 验类型与产物。
- 修改交互后验证手机宽度、键盘导航、深链接、深色主题与 reduced-motion。
- 不提交缓存、依赖目录、截图、日志或本地路径；不将语言规则复制到站点文案。

## 里程碑与 Spec

生态功能先读 [治理](docs/development/governance.md)、[里程碑](docs/milestones/README.md)和 [Spec 入口](docs/specs/README.md)。
各 Spec 只有一个主里程碑；上游合同只引用，不复制状态。必需子项与真实联合验收完成后才能关闭里程碑。

正式文档状态只写正文 metadata，docs/inventory.json 只登记 ID 与路径；文档变更运行 `npm run check-docs`。
Spec／里程碑归档必须同步库存和本地引用；机器门禁不代替跨仓库真实验收。
