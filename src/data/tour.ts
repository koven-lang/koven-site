import data from './generated.json'

export const source = data.source
export const specPages = data.specPages
export const roadmap = data.roadmap
export const sourceUrl = (path: string) => `${source.repository}/blob/${source.revision}/${path}`

const titles: Record<string, string> = {
  hello: 'Hello, Koven', strings: '字符串', branch: '条件分支', function: '函数与返回值',
  constant: '常量', iteration: '顺序遍历', arguments: '命令行参数', borrowing: '共享借用',
  'collections-and-borrow-results': '集合、借用返回与范围', 'root-replace-swap': '原地置换',
  deinit: '资源析构', 'cross-file': '第一个多文件工程', 'parameter-report': '参数报告工具',
  'numbers-bitwise': '数字与位运算', 'scope-cleanup': '作用域清理', 'unit-loop-cleanup': '循环与资源退出',
  'reject-immutable-place': '诊断：不可变位置', 'reject-iteration-move': '诊断：活跃借用',
  'reject-typed': '诊断：类型不匹配', 'reject-ownership': '诊断：移动后使用',
  'planned-thread': '线程示例的实施边界', 'gap-scope-branch': '分支资源清理',
  'argv-word-frequency': '实战：Map 词频统计',
}
export const chapters = data.chapters.map(ch => ({...ch, title: titles[ch.id] || ch.id,
  example: data.examples.find(ex => ex.id === ch.id)}))

export const designLessons = data.designLessons
