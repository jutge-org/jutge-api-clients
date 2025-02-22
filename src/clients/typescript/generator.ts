/* eslint-disable  @typescript-eslint/no-explicit-any */
import type { ApiDir, ApiEndpointDir, ApiInfo, ApiModuleDir } from '@/types'

export async function genTypeScriptClient(dir: ApiDir): Promise<string> {
    const skeleton = await Bun.file('src/clients/typescript/skeleton.ts').text()
    const preamble = genPreamble(dir.info)
    const models = genModels(dir)
    const modules = genModule(dir.root, [], true)
    const main = genMainModule(dir.root)
    const source = skeleton
        .replace('// PREAMBLE_HERE', preamble)
        .replace('// MODELS_HERE', models)
        .replace('// MODULES_HERE', modules)
        .replace('// MAIN_MODULE_HERE', main)
        .replaceAll(/ *?\n/g, '\n')
        .replaceAll('\n\n\n', '\n\n')
        .replaceAll('\n\n\n', '\n\n')
        .replaceAll('\n\n\n', '\n\n')
    return source
}

function genPreamble(info: ApiInfo): string {
    return `
/**
 * This file has been automatically generated at ${new Date().toISOString()}
 *
 * Name:    ${info.name}
 * Version: ${info.version}
 *
 * Description: ${info.description}
 */
`
}

function genClientTtls(module: ApiModuleDir) {
    const ttls: Map<string, number> = new Map()
    genClientTtlsRec(module, [], ttls)
    const values = []
    for (const [key, value] of ttls) {
        values.push(`        this.clientTTLs.set('${key}', ${value})`)
    }
    return values.join('\n')
}

function genClientTtlsRec(module: ApiModuleDir, path: string[], ttls: Map<string, number>) {
    path = path.concat(module.name)
    for (const endpoint of module.endpoints) {
        if (endpoint.clientTtl) {
            ttls.set(path.slice(1).concat(endpoint.name).join('.'), endpoint.clientTtl)
        }
    }
    for (const submodule of module.submodules) {
        genClientTtlsRec(submodule, path, ttls)
    }
}

function genModule(module: ApiModuleDir, path: string[], root: boolean = false): string {
    const name = root ? 'Module' : module.name

    const submodules_decls = module.submodules.map(
        (submodule) => `    readonly ${submodule.name}: ${path.join('_')}_${name}_${submodule.name}`,
    )

    const submodules_inits = module.submodules.map(
        (submodule) => `        this.${submodule.name} = new ${path.join('_')}_${name}_${submodule.name}(root)`,
    )

    const endpoints = module.endpoints.map((endpoint) => genEndpoint(endpoint, path.concat(module.name), root))

    const klass = `
/**
 *
 * ${module.description || 'No description yet'}
 *
 */
class ${path.join('_')}_${name} {

    private readonly root: JutgeApiClient

${submodules_decls.join('\n')}

    constructor(root: JutgeApiClient) {
        this.root = root
${submodules_inits.join('\n')}
    }

${indent(endpoints.join('\n'))}

}
`

    const submodules = module.submodules.map((submodule) => genModule(submodule, path.concat(name)))

    return `
${root ? '' : klass}
${submodules.join('\n')}
`
}

function genMainModule(module: ApiModuleDir): string {
    const clientTtls = genClientTtls(module)

    const submodules_decls = module.submodules.map(
        (submodule) => `    readonly ${submodule.name}: Module_${submodule.name}`,
    )

    const submodules_inits = module.submodules.map(
        (submodule) => `        this.${submodule.name} = new Module_${submodule.name}(this)`,
    )

    return `
${submodules_decls.join('\n')}

    constructor() {
${submodules_inits.join('\n')}

${clientTtls}
    }
`
}

function genEndpoint(endpoint: ApiEndpointDir, path: string[], root: boolean = false): string {
    const { name, input, output, summary, description, actor, status } = endpoint
    let params = ''
    let args = 'null'
    if (input.type !== 'void') {
        const param = input.param || 'data'
        params = `${param}: ${typify(input, undefined)}`
        args = `${input.param || 'data'}`
    }
    if (endpoint.ifiles == 'many') {
        params += (input.type !== 'void' ? ', ' : '') + 'ifiles: File[]'
        args += ', ifiles'
    } else if (endpoint.ifiles == 'one') {
        params += (input.type !== 'void' ? ', ' : '') + 'ifile: File'
        args += ', [ifile]'
    }

    let result = 'void'
    if (output.type !== 'void') {
        result = typify(output, undefined)
    }
    if (endpoint.ofiles === 'none') {
        // nothing
    } else if (endpoint.ofiles == 'one') {
        if (endpoint.output.type === 'void') {
            result = `Download`
        } else {
            result = `[${result}, Download]`
        }
    } else if (endpoint.ofiles == 'many') {
        if (endpoint.output.type === 'void') {
            result = `Download[]`
        } else {
            result = `[${result}, Download[]]`
        }
    }

    const with_ofiles = endpoint.ofiles !== 'none'
    const without_output = with_ofiles && endpoint.output.type === 'void'

    const code1 = `const [output, ofiles] = await this.root.execute('${root ? '' : path.splice(1).join('.') + '.'}${name}', ${args})`
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
 * ${summary || 'No summary'}
 *
 * ${actor ? `🔐 Authentication: ${actor.replace('Actor', '')}` : 'No authentication'}
 * ${status ? `❌ Warning: ${status}` : 'No warnings'}
 * ${description ? description : ''}
 */
async ${toCamelCase(name)}(${params}) : Promise<${result}> {
    ${code1}
    ${code2}
}
    `
}
function genModels(mod: ApiDir): string {
    return mod.models.map(([name, model]) => genModel(name, model)).join('\n')
}

function genModel(name: string, model: any): string {
    return `export type ${name} = ${typify(model, name)}` + '\n'
}

function indent(s: string): string {
    return s
        .split('\n')
        .map((line) => ' '.repeat(4) + line)
        .join('\n')
}

function typify(model: any, name?: string): string {
    if (Object.keys(model).length == 0) {
        return 'any'
    } else if ('$ref' in model) {
        return model.$ref
    } else if ('anyOf' in model) {
        return model.anyOf.map(typify).join(' | ')
    } else if (model.type === 'object') {
        if ('properties' in model) {
            const props = Object.entries(model.properties)
                .map(([key, value]: [string, any]) => `${key}: ${typify(value)} `)
                .join(', ')
            if (name) {
                const props = Object.entries(model.properties)
                    .map(([key, value]: [string, any]) => `    ${key}: ${typify(value)}`)
                    .join(',\n')
                return `{\n${props}\n}`
            } else {
                const props = Object.entries(model.properties)
                    .map(([key, value]: [string, any]) => `${key}: ${typify(value)}`)
                    .join(', ')
                return `{ ${props} } `
            }
        } else if ('patternProperties' in model) {
            return `Record<string, ${typify(model.patternProperties['^(.*)$'])}>`
        } else {
            throw new Error(`I do not know this type yet`)
        }
    } else if (model.type === 'array') {
        return `${typify(model.items)}[]`
    } else if (model.type === 'string') {
        return 'string'
    } else if (model.type === 'number') {
        return 'number'
    } else if (model.type === 'integer') {
        return 'number'
    } else if (model.type === 'boolean') {
        return 'boolean'
    } else if (model.type === 'void') {
        return 'null'
    } else if (model.type === 'null') {
        return 'null'
    } else if (model.type === 'Date') {
        return 'string'
    } else if (model.type === 'file') {
        return 'Uint8Array'
    }

    /* We do not have this type :-( */
    console.error(model)
    return 'UNKNOWN'
}

function capitalize(s: string): string {
    return s.charAt(0).toUpperCase() + s.slice(1)
}

function toCamelCase(s: string): string {
    if (s == 'throw') return 'throw_'
    return s.replace(/([-_][a-z])/g, (group) => group.toUpperCase().replace('-', '').replace('_', ''))
}
