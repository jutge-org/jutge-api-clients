/* eslint-disable  @typescript-eslint/no-explicit-any */

import type { ApiDir, ApiEndpointDir, ApiInfo, ApiModuleDir } from '@/types'
import * as prettier from 'prettier'

export async function genJavaScriptClient(dir: ApiDir): Promise<string> {
    const skeleton = await genSkeleton()
    const preamble = genPreamble(dir.info)
    const modules = genModule(dir.root, '', true)
    const source = `

${preamble}

${skeleton}

jutge_api_client = {

    ...jutge_api_client,

${modules}

}
`
    const formatted = await format(source)
    return formatted
}

async function format(source: string): Promise<string> {
    return await prettier.format(source, {
        semi: false,
        parser: 'babel',
        tabWidth: 4,
        printWidth: 120,
    })
}

function genPreamble(info: ApiInfo): string {
    return `

/**

This file has been automatically generated at ${new Date().toISOString()}

Name:    ${info.name}
Version: ${info.version}

Description:

${info.description}

*/

`
}

async function genSkeleton() {
    return await Bun.file('src/clients/javascript/skeleton.js').text()
}

function genModule(module: ApiModuleDir, path: string, root: boolean = false): string {
    const endpoints = module.endpoints.map((endpoint) => genEndpoint(endpoint, path, root))
    const modules = module.submodules.map((module) =>
        genSubModule(module, path == '' ? module.name : `${path}.${module.name}`),
    )
    return endpoints.join('\n') + modules.join('\n')
}

function genEndpoint(endpoint: ApiEndpointDir, path: string, root: boolean = false): string {
    const { name, input, output, summary, description, actor, status } = endpoint
    let params = ''
    let args = 'null'
    if (input.type !== 'void') {
        const param = input.param || 'data'
        params = param
        args = `${input.param || 'data'}`
    }
    if (endpoint.ifiles == 'many') {
        params += (input.type !== 'void' ? ', ' : '') + 'ifiles'
        args += ', ifiles'
    } else if (endpoint.ifiles == 'one') {
        params += (input.type !== 'void' ? ', ' : '') + 'ifile'
        args += ', [ifile]'
    }

    const with_ofiles = endpoint.ofiles !== 'none'
    const without_output = with_ofiles && endpoint.output.type === 'void'

    const code1 = `const [output, ofiles] = await jutge_api_client.execute('${root ? '' : path + '.'}${name}', ${args})`
    let code2
    if (!with_ofiles) {
        code2 = `return output`
    } else if (without_output) {
        if (endpoint.ofiles === 'one') {
            code2 = `return ofiles[0]`
        } else {
            code2 = `return ofiles`
        }
    } else {
        if (endpoint.ofiles === 'one') {
            code2 = `return [output, ofiles[0]]`
        } else {
            code2 = `return [output, ofiles]`
        }
    }

    return `

    /**
    ${summary || 'No summary'}${actor ? '\n\n    🔐 Authenticated' : ''}    ${status ? `\n    ❌ Warning: ${status}` : ''}    ${description ? '\n\n    ' + description : ''}
    **/
${toCamelCase(name)}: async function (${params}) {

    ${code1}
    ${code2}
},
    `
}

function genSubModule(mod: ApiModuleDir, path: string): string {
    const module = genModule(mod, path)

    let description = ''
    if (mod.description) {
        description = `
/**
    ${mod.description}
*/`
    }

    return `
${description}
${mod.name}: {


${indent(module)}

},
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
