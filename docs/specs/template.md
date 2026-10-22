# Spec 模板

复制到 drafts/NNNN.md，首行用实际 metadata 替换本标题。先申请未占用编号并登记库存，不直接使用占位身份。

```json
{"id":"SPEC-NNNN","kind":"spec","status":"draft","milestone":"SITE-V1-M0","depends_on":[],"blockers":[],"evidence":[]}
```

metadata 形式为 `<!-- metadata: JSON -->`；正文包含下列非空章节：
目标、范围、非目标、行为合同、接口变化、失败场景、依赖、测试与验收、完成条件、验收证据。
每项用二级标题。范围写基线和授权；本地 depends_on 只用真实 Spec ID，外部依赖写正文和 blocker。
只有前置 done 且无 blocker 才能 approved／in-progress；归档必须更新路径、库存、链接和证据。
