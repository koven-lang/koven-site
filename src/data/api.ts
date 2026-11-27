import data from './generated.json'

export const api = data.api
export const entries = api.artifact.entries.map((entry, index) => ({
    ...entry,
    links: api.links[index],
    id: `${entry.example}/${entry.file}/${entry.function}`,
}))
