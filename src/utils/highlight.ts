const KW = /\b(fun|val|var|class|value|enum|interface|object|companion|override|if|else|when|is|in|for|while|loop|return|break|continue|move|own|borrow|inout|const|this|super|as|null|true|false|by)\b/
export const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
const re = new RegExp('(\\/\\/.*)|("(?:[^"\\\\]|\\\\.)*")|' + KW.source + '|\\b([A-Z][A-Za-z0-9_]*)\\b|\\b(\\d[\\d_.]*)\\b|\\b([a-z_][A-Za-z0-9_]*)(?=\\()', 'g')

export function highlight(src: string): string {
    return esc(src).replace(re, (m, c?: string, s?: string, k?: string, t?: string, n?: string, f?: string) =>
        c ? `<span class="c">${c}</span>` : s ? `<span class="s">${s}</span>` : k ? `<span class="k">${k}</span>`
            : t ? `<span class="t">${t}</span>` : n ? `<span class="n">${n}</span>` : f ? `<span class="f">${f}</span>` : m)
}
