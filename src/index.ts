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

const url = 'https://api.jutge.org/api/dir'
const destination = 'out'

const request = await fetch(url)
const directory = await request.json()

console.log(chalk.blue('Python'))
await Bun.write(destination + '/jutge_api_client.py', await genPythonClient(directory))

console.log(chalk.blue('TypeScript'))
await Bun.write(destination + '/jutge_api_client.ts', await genTypeScriptClient(directory))

console.log(chalk.blue('C++'))
await Bun.write(destination + '/jutge_api_client.cpp', await genCppClient(directory))

console.log(chalk.blue('JavaScript'))
await Bun.write(destination + '/jutge_api_client.js', await genJavaScriptClient(directory))

console.log(chalk.blue('PHP'))
await Bun.write(destination + '/jutge_api_client.php', await genPhpClient(directory))



console.log(chalk.blue('Java'))

const javaDestination = path.join(destination, 'com', 'jutge', 'api')
const gsonPath = "src/lib/java/gson-2.12.1.jar"
await fs.mkdir(javaDestination, { recursive: true })

await Bun.write(javaDestination + '/JutgeApiClient.java', await genJavaClient(directory))

await exec(`javac -cp ../../../../` + gsonPath + ` *.java`, { cwd: javaDestination })
await exec(`mkdir -p gson-temp`, { cwd: destination })
await exec(`jar xf ../../` + gsonPath, { cwd: destination + `/gson-temp` })
await exec(`jar cf JutgeApiClient-fat.jar -C . com/jutge/api -C gson-temp .`, { cwd: destination })

await exec(`rm -r com/ gson-temp/`, { cwd: destination })
