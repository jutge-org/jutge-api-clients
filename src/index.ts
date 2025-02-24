import { genCppClient } from '@/clients/cpp/generator'
import { genJavaClient } from '@/clients/java/generator'
import { genJavaScriptClient } from '@/clients/javascript/generator'
import { genPhpClient } from '@/clients/php/generator'
import { genPythonClient } from '@/clients/python/generator'
import { genTypeScriptClient } from '@/clients/typescript/generator'
import chalk from 'chalk'

const url = 'https://api.jutge.org/api/dir'
const destination = 'out'

const request = await fetch(url)
const directory = await request.json()

console.log(chalk.blue('Python'))
await Bun.write(destination + '/jutge_api_client.py', await genPythonClient(directory))

console.log(chalk.blue('TypeScript'))
await Bun.write(destination + '/jutge_api_client.ts', await genTypeScriptClient(directory))

console.log(chalk.blue('Java'))
await Bun.write(destination + '/JutgeApiClient.java', await genJavaClient(directory))

console.log(chalk.blue('C++'))
await Bun.write(destination + '/jutge_api_client.cpp', await genCppClient(directory))

console.log(chalk.blue('JavaScript'))
await Bun.write(destination + '/jutge_api_client.js', await genJavaScriptClient(directory))

console.log(chalk.blue('PHP'))
await Bun.write(destination + '/jutge_api_client.php', await genPhpClient(directory))
