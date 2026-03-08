import { generateClientFromDir, getAPIDirectory } from '@/clients'

const API_BASE = process.env.JUTGE_API_URL ?? 'http://localhost:8012/api'

try {
  await fetch(API_BASE)
} catch {
  console.error(
    `\nThe Jutge API is not reachable at ${API_BASE}.\n` +
    `Please run the tests with the development version of the API running on ${API_BASE}.\n`
  )
  process.exit(1)
}

const API_URL = API_BASE + '/dir'
const OUT_DIR = `${import.meta.dir}/../../out`

const dir = await getAPIDirectory(API_URL)
await generateClientFromDir(dir, 'typescript', OUT_DIR)
await generateClientFromDir(dir, 'javascript', OUT_DIR)
