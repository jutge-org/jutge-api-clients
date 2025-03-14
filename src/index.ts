import { genCppClient } from '@/clients/cpp/generator'
import { genJavaClient } from '@/clients/java/generator'
import { genJavaScriptClient } from '@/clients/javascript/generator'
import { genPhpClient } from '@/clients/php/generator'
import { genPythonClient } from '@/clients/python/generator'
import { genTypeScriptClient } from '@/clients/typescript/generator'
import chalk from 'chalk'
import { exec as syncExec } from 'child_process'
import { promises as fs } from 'fs'
import path from 'path'
import util from 'util'
const exec = util.promisify(syncExec)

type Language = 'cpp' | 'java' | 'javascript' | 'php' | 'python' | 'typescript'

const API_URL = 'https://api.jutge.org/api/dir'
const DESTINATION_DIR = 'out'

export const generateClient = async (language: Language) => {
    const request = await fetch(API_URL)
    const directory = await request.json()
    switch (language) {
        case 'cpp':
            return await genCppClient(directory)
        case 'java':
            return await genJavaClient(directory)
        case 'javascript':
            return await genJavaScriptClient(directory)
        case 'php':
            return await genPhpClient(directory)
        case 'python':
            return await genPythonClient(directory)
        case 'typescript':
            return await genTypeScriptClient(directory)
        default:
            throw new Error(`Language ${language} not supported`)
    }
}

const clients = [
    { name: 'Python', lang: 'python', ext: '.py' },
    { name: 'TypeScript', lang: 'typescript', ext: '.ts' },
    { name: 'JavaScript', lang: 'javascript', ext: '.js' },
    { name: 'PHP', lang: 'php', ext: '.php' },
    { name: 'C++', lang: 'cpp', ext: '.cpp' },
]

for (const { name, lang, ext } of clients) {
    console.log(chalk.blue(name))
    await Bun.write(`${DESTINATION_DIR}/jutge_api_client${ext}`, await generateClient(lang as Language))
}

// NOTE: Java needs some extra steps
console.log(chalk.blue('Java'))

const javaDestination = path.join(DESTINATION_DIR, 'com', 'jutge', 'api')
const gsonPath = 'src/lib/java/gson-2.12.1.jar'
await fs.mkdir(javaDestination, { recursive: true })

await Bun.write(javaDestination + '/JutgeApiClient.java', await generateClient('java'))

await exec(`javac -cp ../../../../` + gsonPath + ` *.java`, { cwd: javaDestination })
await exec(`mkdir -p gson-temp`, { cwd: DESTINATION_DIR })
await exec(`jar xf ../../` + gsonPath, { cwd: DESTINATION_DIR + `/gson-temp` })
await exec(`jar cf JutgeApiClient-fat.jar -C . com/jutge/api -C gson-temp .`, { cwd: DESTINATION_DIR })

await exec(`rm -r com/ gson-temp/`, { cwd: DESTINATION_DIR })
