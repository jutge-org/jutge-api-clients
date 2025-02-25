/* eslint-disable  @typescript-eslint/no-explicit-any */
import type { ApiDir, ApiEndpointDir, ApiInfo, ApiModuleDir } from '@/types'

// @ts-expect-error: foo
import skeleton from './skeleton.php' with { type: 'text' }

export async function genPhpClient(dir: ApiDir): Promise<string> {
    const preamble = genPreamble(dir.info)
    const skeleton = await genSkeleton()
    const modules = genModule(dir.root, '', true)
    const source = `<?php\n\n${preamble}\n\n${skeleton}\n\n${modules}\n\n`
    return source
}

function genPreamble(info: ApiInfo): string {
    return `/*

This file has been automatically generated at ${new Date().toISOString()}

Name:    ${info.name}
Version: ${info.version}

Description:

${info.description}

RERMARK:

This version does not yet support uploading and downloading files.
Endpoints that require file upload/download will not work.

*/

`
}

async function genSkeleton() {
    // remove the first line, which is the <php> tag
    const lines = skeleton.split('\n')
    lines.shift()
    return lines.join('\n')
}

function genModule(module: ApiModuleDir, path: string, root: boolean = false): string {
    const endpoints = module.endpoints.map((endpoint) => genEndpoint(endpoint, path, root))
    const modules = module.submodules.map((module) =>
        genSubModule(module, path == '' ? module.name : `${path}.${module.name}`),
    )
    return endpoints.join('\n') + modules.join('\n')
}

function genEndpoint(func: ApiEndpointDir, path: string, root: boolean = false): string {
    const { name, input, output, summary, description, actor, status } = func

    let parameter = ''
    let argument = 'null'
    if (input.type !== 'void') {
        const param = input.param || 'data'
        parameter = `${dolar}${param}`
        argument = dolar + (input.param || 'data')
    }

    const code = `return \\jutge\\execute('${root ? '' : path + '.'}${name}', ${argument});`

    return `
/*
    ${summary || 'No summary'}${actor ? '\n\n    🔐 Authenticated' : ''}    ${status ? `\n    ❌ Warning: ${status}` : ''}    ${description ? '\n\n    ' + description : ''}
*/
function ${camelToSnakeCase(name)}(${parameter}) {
    ${code}
}
    `
}

function genSubModule(mod: ApiModuleDir, path: string): string {
    const module = genModule(mod, path)

    let description = ''
    if (mod.description) {
        description = `
/*
    ${mod.description}
*/`
    }

    return `
${description}
namespace jutge\\${path.replace(/\./g, '\\')};

${module}

    `
}

function indent(s: string): string {
    return s
        .split('\n')
        .map((line) => ' '.repeat(4) + line)
        .join('\n')
}

function capitalize(s: string): string {
    return s.charAt(0).toUpperCase() + s.slice(1)
}

function toCamelCase(s: string): string {
    if (s == 'throw') return 'throw_'
    return s.replace(/([-_][a-z])/g, (group) => group.toUpperCase().replace('-', '').replace('_', ''))
}

function camelToSnakeCase(s: string) {
    return s.replace(/[/:-]/g, '_').replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`)
}

const dolar = '$'
