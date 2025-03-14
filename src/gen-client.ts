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
import type { ApiDir } from './types'

const exec = util.promisify(syncExec)

export type Language = 'cpp' | 'java' | 'javascript' | 'php' | 'python' | 'typescript'

const API_URL = 'https://api.jutge.org/api/dir'

type ClientInfo = {
    name: string
    ext: string
}

export const clients: Record<Language, ClientInfo> = {
    python: { name: 'Python', ext: '.py' },
    typescript: { name: 'TypeScript', ext: '.ts' },
    javascript: { name: 'JavaScript', ext: '.js' },
    java: { name: 'Java', ext: '.java' },
    cpp: { name: 'C++', ext: '.cpp' },
    php: { name: 'PHP', ext: '.php' },
}

export const getAPIDirectory = async () => {
    const request = await fetch(API_URL)
    return await request.json()
}

const _generate = async (lang: Language, dir: ApiDir) => {
    switch (lang) {
        case 'cpp':
            return await genCppClient(dir)
        case 'java':
            return await genJavaClient(dir)
        case 'javascript':
            return await genJavaScriptClient(dir)
        case 'php':
            return await genPhpClient(dir)
        case 'python':
            return await genPythonClient(dir)
        case 'typescript':
            return await genTypeScriptClient(dir)
        default:
            throw new Error(`${lang} not supported`)
    }
}

export const generateClient = async (lang: Language, destinationDir: string) => {
    const directory = await getAPIDirectory()
    const info = clients[lang]

    console.log(chalk.blue(info.name))

    if (lang === 'java') {
        const javaDestination = path.join(destinationDir, 'com', 'jutge', 'api')
        const gsonPath = 'src/lib/java/gson-2.12.1.jar'
        await fs.mkdir(javaDestination, { recursive: true })

        await Bun.write(javaDestination + '/JutgeApiClient.java', await _generate('java', directory))

        await exec(`javac -cp ../../../../` + gsonPath + ` *.java`, { cwd: javaDestination })
        await exec(`mkdir -p gson-temp`, { cwd: destinationDir })
        await exec(`jar xf ../../` + gsonPath, { cwd: destinationDir + `/gson-temp` })
        await exec(`jar cf JutgeApiClient-fat.jar -C . com/jutge/api -C gson-temp .`, { cwd: destinationDir })

        await exec(`rm -r com/ gson-temp/`, { cwd: destinationDir })
    } else {
        await Bun.write(`${destinationDir}/jutge_api_client${info.ext}`, await _generate(lang, directory))
    }
}
