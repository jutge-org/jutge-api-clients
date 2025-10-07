/* eslint-disable  @typescript-eslint/no-explicit-any */

import type { ApiDir, ApiEndpointDir, ApiModuleDir } from '@/types'
import { withTmpDir } from '@/utilities'
import { $ } from 'bun'
import { pascal } from 'radash'
import path from 'path'


export async function genPythonClient(dir: ApiDir): Promise<string> {
    const packageRoot = path.resolve(__dirname, '../../..')
    const skeleton = await Bun.file(`${packageRoot}/src/clients/python/skeleton.py`).text()
    const preamble = genPreamble(dir.info)
    const models = genModels(dir.models)
    const modules = genModule(dir.root, [], true)
    const main = genMainModule(dir.root)
    const source = skeleton
        .replace('# PREAMBLE_HERE', preamble)
        .replace('# MODELS_HERE', models)
        .replace('# MODULES_HERE', modules)
        .replace('# MAIN_MODULE_HERE', main)
    const formatted = await format(source)
    await check(source)
    return formatted
}

async function format(source: string): Promise<string> {
    if (!Bun.which('ruff')) {
        console.error('ruff command not found, skipping python formatting')
        return source
    }

    return await withTmpDir(async (tmp) => {
        const path = `${tmp}/client.py`
        Bun.write(path, source)
        try {
            await $`ruff format --line-length=320 ${path}`.quiet()
            return await Bun.file(path).text()
        } catch (e) {
            console.error('Failed to format python code')
            return source
        }
    })
}

async function check(source: string): Promise<void> {
    if (!Bun.which('ruff')) {
        console.error('ruff command not found, skipping python checking')
        return
    }

    await withTmpDir(async (tmp) => {
        const path = `${tmp}/client.py`
        Bun.write(path, source)

        try {
            await $`ruff check ${path}`.quiet()
        } catch (e) {
            console.error('Failed to check python code')
            if (e instanceof Error && 'info' in e && e.info instanceof Object && 'stderr' in e.info && e.info.stderr) {
                console.error(e.info.stderr)
            } else {
                console.error(e)
            }
        }
    })
}

function genPreamble(info: any): string {
    return `
"""
This file has been automatically generated at ${new Date().toISOString()}

Name:    ${info.name}
Version: ${info.version}

Description:

${info.description}

"""
`
}

function genModels(models: [string, any][]): string {
    return models.map(([name, model]) => genModel(name, model)).join('\n\n')
}

function genModel(name: string, model: any): string {
    if (model.type === 'object' && 'properties' in model) {
        return `${typify(model, name, '', 0)}`
    } else {
        return `type ${name} = ${typify(model, name, '', 99)}` // 99 because we don't want to generate any more nested types
    }
}

function genModule(module: ApiModuleDir, path: string[], root: boolean = false): string {
    const name = root ? 'Module' : module.name

    const submodules_decls = module.submodules.map(
        (submodule) => `${submodule.name}: ${pascal(path.join('_') + '_' + name + '_' + submodule.name)}`,
    )

    const submodules_inits = module.submodules.map(
        (submodule) => `self.${submodule.name} = ${pascal(path.join('_') + '_' + name + '_' + submodule.name)}(root)`,
    )

    const endpoints = module.endpoints.map((endpoint) => genEndpoint(endpoint, path.concat(module.name), root))

    const klass = `
class ${pascal(path.join('_') + '_' + name)}:
    """
    ${module.description || 'No description yet'}
    """

    _root: JutgeApiClient

${indent(submodules_decls.join('\n'))}

    def __init__(self, root: JutgeApiClient):
        self._root = root
${indentTwice(submodules_inits.join('\n'))}


    ${indent(endpoints.join('\n'))}


`

    const submodules = module.submodules.map((submodule) => genModule(submodule, path.concat(name)))

    return `
${root ? '' : klass}
${submodules.join('\n')}
`
}

function genMainModule(module: ApiModuleDir): string {
    const submodules_decls = module.submodules.map(
        (submodule) => `${submodule.name}: ${pascal('Module_' + submodule.name)}`,
    )

    const submodules_inits = module.submodules.map(
        (submodule) => `self.${submodule.name} = ${pascal('Module_' + submodule.name)}(self)`,
    )

    return `
${indent(submodules_decls.join('\n'))}

    def __init__(self):
${indentTwice(submodules_inits.join('\n'))}

`
}

function genEndpoint(endpoint: ApiEndpointDir, path: string[], root: boolean = false): string {
    const { name, input, output, summary, description, actor, status } = endpoint
    let inlined = false
    let params = ''
    let args = 'None'

    if (input.type !== 'void') {
        if (isInlined(input)) {
            inlined = true
            params = typify(input, '', path.join('_'), 0)
        } else {
            const param = input.param || 'data'
            params = `${param}: ${typify(input, '', path.join('_'), 0)}`
        }
        args = `_debuild(${input.param || 'data'})`
    }

    if (endpoint.ifiles == 'many') {
        params += (input.type !== 'void' ? ', ' : '') + 'ifiles: list[BinaryIO]'
        args += ', ifiles'
    } else if (endpoint.ifiles == 'one') {
        params += (input.type !== 'void' ? ', ' : '') + 'ifile: BinaryIO'
        args += ', [ifile]'
    }

    let result = 'None'
    if (output.type !== 'void') {
        result = typify(output, '', path.join('_'), 0)
    }

    if (endpoint.ofiles === 'none') {
        // nothing
    } else if (endpoint.ofiles == 'one') {
        if (endpoint.output.type === 'void') {
            result = `Download`
        } else {
            result = `tuple[${result}, Download]`
        }
    } else if (endpoint.ofiles == 'many') {
        if (endpoint.output.type === 'void') {
            result = `list[Download]`
        } else {
            result = `tuple[${result}, list[Download]]`
        }
    }

    const with_ofiles = endpoint.ofiles !== 'none'
    const without_output = with_ofiles && endpoint.output.type === 'void'

    let code0 = ''
    if (inlined) {
        const content = Object.entries(input.properties)
            .map(([key, _]: [string, any]) => `'${key}': ${key}`)
            .join(', ')

        code0 = `data = { ${content} }`
    }

    const code1 = `output, ofiles = self._root.execute('${root ? '' : path.splice(1).join('.') + '.'}${name}', ${args})`

    let code2 = ''
    if (!without_output) {
        code2 = `result = _build(output, ${typify(endpoint.output, 'NAME', path.join('_'), 99)})`
    }

    let code3
    if (!with_ofiles) {
        code3 = `return result`
    } else if (without_output) {
        if (endpoint.ofiles === 'one') {
            code3 = `return ofiles[0]`
        } else {
            code3 = `return ofiles`
        }
    } else {
        if (endpoint.ofiles === 'one') {
            code3 = `return result, ofiles[0]`
        } else {
            code3 = `return result, ofiles`
        }
    }

    return `
def ${camelToSnakeCase(name)}(self ${params ? ',' : ''} ${params}) -> ${result}:
    """
    ${summary || 'No summary'}${actor ? '\n\n    🔐 Authenticated' : ''}    ${status ? `\n    ❌ Warning: ${status}` : ''}    ${description ? '\n\n' + description : ''}
    """

    ${code0}
    ${code1}
    ${code2}
    ${code3}
    `
}

function isInlined(model: any): boolean {
    return (
        Object.keys(model).length != 0 &&
        !('$ref' in model) &&
        !('$anyOf' in model) &&
        model.type === 'object' &&
        'properties' in model
    )
}

function typify(model: any, name: string, path: string, level: number): string {
    if (Object.keys(model).length == 0) {
        return 'Any'
    } else if ('$ref' in model) {
        return `${model.$ref}`
    } else if ('anyOf' in model) {
        return typifyAnyOf(model, name, path, level)
    } else if (model.type === 'object') {
        return typifyObject(model, name, path, level)
    } else if (model.type === 'array') {
        return `list[${typify(model.items, name, path, level + 1)}]`
    } else if (model.type === 'string') {
        return 'str'
    } else if (model.type === 'number') {
        return 'float'
    } else if (model.type === 'integer') {
        return 'int'
    } else if (model.type === 'boolean') {
        return 'bool'
    } else if (model.type === 'void') {
        return 'None'
    } else if (model.type === 'null') {
        return 'None'
    } else if (model.type === 'file') {
        return 'bytes'
    }

    console.error(model)
    return 'Any'
}

function typifyAnyOf(model: any, name: string, path: string, level: number): string {
    if (model.anyOf.length == 2 && model.anyOf[1].type === 'null') {
        let field = ''
        if (name && level <= 1) {
            let def = 'None'
            if (model.anyOf[0].default) def = valuefy(model.anyOf[0].default)
            field = `= Field(default=${def})`
        }
        return `Optional[${typify(model.anyOf[0], name, path, level + 1)}] ${field}`
    } else if (model.anyOf.length == 4 && model.anyOf[0].type === 'Date') {
        return 'str'
    } else {
        return 'Union[' + model.anyOf.map(typify).join(', ') + ']'
    }
}

function typifyObject(model: any, name: string, path: string, level: number): string {
    if ('properties' in model) {
        if (name) {
            const props = Object.entries(model.properties)
                .map(([key, value]: [string, any]) => {
                    let field = ''
                    if ('default' in value)
                        field = `= Field(default=${valuefy(value.default)} ${value.description ? `, description="${value.description}"` : ''})`
                    return `    ${key}: ${typify(value, name, path, level + 1)} ${field} ${!field && value.description ? `# ${value.description}` : ''}`
                })
                .join('\n')
            const description = `    """\n    ${model.description ? model.description : 'No description yet'}\n    """\n`
            return `class ${name}(BaseModel):\n${description}${props}\n`
        } else {
            return Object.entries(model.properties)
                .map(([key, value]: [string, any]) => `${key}: ${typify(value, name, path, level + 1)}`)
                .join(', ')
        }
    } else if ('patternProperties' in model) {
        return `dict[str, ${typify(model.patternProperties['^(.*)$'], name, path, level + 1)}]`
    } else {
        throw new Error(`I do not know this type yet`)
    }
}

function valuefy(value: any): string {
    if (typeof value === 'string') {
        return `'${value}'`
    } else if (value === null) {
        return 'None'
    } else if (value === undefined) {
        return 'None'
    } else if (typeof value === 'boolean') {
        return value ? 'True' : 'False'
    } else if (typeof value === 'object') {
        return JSON.stringify(value)
    } else {
        return value
    }
}

function camelToSnakeCase(s: string) {
    return s.replace(/[/:-]/g, '_').replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`)
}

function indent(s: string): string {
    return s
        .split('\n')
        .map((line) => ' '.repeat(4) + line)
        .join('\n')
}

function indentTwice(s: string): string {
    return indent(indent(s))
}
