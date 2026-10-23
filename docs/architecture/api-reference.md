# API 参考输入与呈现

SPEC-0003 在原 generated.json 中增加 api 字段，消费真实 koven.api-examples v1；不维护第二份教程源码或执行 oracle。
api-source.json 单独固定上游提交与规范化快照 SHA256，既有 content-source.json 继续管理 Guide/Tour。
两者版本在页面分别标明，页脚标明规范快照。

scripts/api_snapshot.py 复用来源仓库策略和教程代码围栏读取；对照固定 Git 提交核查 Guide、教程合同、源码摘要及声明范围，生成同版本 GitHub 行链接。
离线构建核固定快照摘要；CI 第二 checkout 再次核查真实源。同步可传 --api-source 和 --api-artifact，未提供新产物时保留并验证原产物，失败不回退。

/api 提供函数/签名/教程搜索，?symbol=<example>/<file>/<function> 提供详情深链接；参数模式直接呈现上游声明。
完整教程的真实执行证据不等于语法抽取具备类型检查，也不等于浏览器执行。
输入升级需重新生成真实产物、审阅固定提交与摘要，并重复联合验收。
