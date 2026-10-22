import {chapters, sourceUrl, source} from './tour'
export const features = [
  {number: '01', title: '从熟悉的语法开始', desc: '沿着常量、函数、分支和集合，逐步认识 Koven。', to: '/tour/hello?mode=practice'},
  {number: '02', title: '看清值的生命周期', desc: '通过共享借用、资源析构与错误示例，理解所有权。', to: '/tour/borrowing?mode=practice'},
  {number: '03', title: `走进 ${source.version} 设计`, desc: '阅读值语义协议、Result 与闭包捕获的新规则。', to: '/tour/overview?mode=design'},
]
export const snippets = ['hello', 'borrowing', 'iteration'].map(id => {
  const chapter = chapters.find(ch => ch.id === id)!
  return {id, title: chapter.title, code: chapter.example!.files[0].code, path: chapter.path}
})
export const gettingStarted = sourceUrl('README.md')
