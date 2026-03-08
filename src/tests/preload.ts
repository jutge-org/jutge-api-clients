import { generateClientFromDir, getAPIDirectory } from '@/clients'

const API_URL = (process.env.JUTGE_API_URL ?? 'https://api.jutge.org/api') + '/dir'
const OUT_DIR = `${import.meta.dir}/../../out`

const dir = await getAPIDirectory(API_URL)
await generateClientFromDir(dir, 'typescript', OUT_DIR)
await generateClientFromDir(dir, 'javascript', OUT_DIR)
