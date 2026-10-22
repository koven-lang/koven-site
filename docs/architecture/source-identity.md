# 内容来源仓库身份

> 性质：当前实现；状态：current；读取时机：修改内容来源或生成器；真源：scripts/resolve_source.py 与 scripts/sync_content.py。

`content-source.json` 的 repository 同时决定 CI checkout 与生成内容的来源链接。
`resolve_source.repository_url` 统一检查 owner/repository 并形成 GitHub HTTPS URL。
`sync_content.source_repository` 在读取源文件之前查询实际 checkout 的 origin，接受
GitHub HTTPS、scp SSH、ssh URL 和可选 `.git` 后缀，按不区分大小写的仓库名比较。
缺失、不支持或不匹配时失败；诊断不回显可能含凭据的 remote。

内容仍由一个精确 Git commit 读取，当前 ref、Guide 版本、教程合同和生成 JSON 保持原状。
离线 `--validate-snapshot` 另外要求 source.repository 与当前配置一致，防止构建已改配置但
未同步来源身份的旧快照。其他内容完整性继续由既有 Guide 摘要、设计章节和 `--check` 负责。

该检查证明的是配置／checkout／声明的一致性，不是签名、仓库所有权认证、main 成员资格、
已发布工具链或网站／编译器兼容性证明；nightly 的 main CI 门禁仍由原工作流单独执行。
合同与验收见 [SPEC-0002](../archive/specs/0002.md)。
