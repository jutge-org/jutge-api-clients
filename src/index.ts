import { genCppClient } from '@/clients/cpp/generator'
import { genJavaClient } from '@/clients/java/generator'
import { genJavaScriptClient } from '@/clients/javascript/generator'
import { genPhpClient } from '@/clients/php/generator'
import { genPythonClient } from '@/clients/python/generator'
import { genTypeScriptClient } from '@/clients/typescript/generator'

const url = 'https://api.jutge.org/api/dir'
const destination = 'out'

const request = await fetch(url)
const directory = await request.json()

await Bun.write(destination + '/jutge_api_client.py', await genPythonClient(directory))
await Bun.write(destination + '/jutge_api_client.ts', await genTypeScriptClient(directory))
await Bun.write(destination + '/jutge_api_client.js', await genJavaScriptClient(directory))
await Bun.write(destination + '/jutge_api_client.cpp', await genCppClient(directory))
await Bun.write(destination + '/jutge_api_client.php', await genPhpClient(directory))
await Bun.write(destination + '/JutgeApiClient.java', await genJavaClient(directory))
