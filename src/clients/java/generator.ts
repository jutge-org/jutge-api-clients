/* eslint-disable  @typescript-eslint/no-explicit-any */

import type { ApiDir, ApiEndpointDir, ApiModuleDir } from '@/types'
import { $ } from 'bun'
import { pascal } from 'radash'
import { withTmpDir } from '../../utilities'

export async function genJavaClient(dir: ApiDir): Promise<string> {
    return await format(await new JavaGenerator(dir).generate())
}

class JavaGenerator {
    private aliases: Map<string, string> = new Map()

    constructor(private dir: ApiDir) {}

    async generate(): Promise<string> {
        const preamble = this.genPreamble()
        const skeleton = await this.genSkeleton()
        const models = this.genModels()
        const modules = this.genModule(this.dir.root, [], true)
        const main = this.genMainModule(this.dir.root)
        const source = skeleton
            .replace('// PREAMBLE_HERE', preamble)
            .replace('// MODELS_HERE', models)
            .replace('// MODULES_HERE', modules)
            .replace('// MAIN_MODULE_HERE', main)
        return source
    }

    private genPreamble(): string {
        const info = this.dir.info
        return `
/**
This file has been automatically generated at ${new Date().toISOString()}

Name:    ${info.name}
Version: ${info.version}

Description:

${info.description}

Notes:

    - functions that return files are not supported yet.
    - ifiles are implemented as byte[].
    - whatch out for optionals and nulls.

*/
`
    }

    private async genSkeleton(): Promise<string> {
        return await Bun.file('src/clients/java/JutgeApiClient.java').text()
    }

    private genModels(): string {
        return this.dir.models.map(([name, model]) => this.genModel(name, model)).join('\n\n')
    }

    private genModel(name: string, model: any): string {
        if (model.type === 'object' && 'properties' in model) {
            return `${this.typify(model, name, '', 0)}`
        } else {
            const t = this.typify(model, name, '', 99) // 99 because we don't want to generate any more nested types
            this.aliases.set(name, t)
            return `// type ${name} = ${t};`
        }
    }

    private genModule(module: ApiModuleDir, path: string[], root: boolean = false): string {
        const name = root ? 'Module' : module.name

        const submodules_decls = module.submodules.map(
            (submodule) => `public ${pascal(path.join('_') + '_' + name + '_' + submodule.name)} ${submodule.name};`,
        )

        const submodules_inits = module.submodules.map(
            (submodule) =>
                `this.${submodule.name} = new ${pascal(path.join('_') + '_' + name + '_' + submodule.name)}(root);`,
        )

        const endpoints = module.endpoints.map((endpoint) => this.genEndpoint(endpoint, path.concat(module.name), root))

        const klass = `
/**
${module.description || 'No description yet'}
*/
@SuppressWarnings("unused")
public static class ${pascal(path.join('_') + '_' + name)} {

    private JutgeApiClient root;

${indent(submodules_decls.join('\n'))}

    public ${pascal(path.join('_') + '_' + name)}(JutgeApiClient root) {
        this.root = root;
${indent2(submodules_inits.join('\n'))}
    }

    ${indent(endpoints.join('\n'))}
}

`

        const submodules = module.submodules
            .filter(this.accept_module)
            .map((submodule) => this.genModule(submodule, path.concat(name)))

        return `
${root ? '' : klass}
${submodules.join('\n')}
`
    }

    genMainModule(module: ApiModuleDir): string {
        const submodules_decls = module.submodules
            .filter(this.accept_module)
            .map((submodule) => `public ${pascal('Module_' + submodule.name)} ${submodule.name};`)

        const submodules_inits = module.submodules
            .filter(this.accept_module)
            .map((submodule) => `this.${submodule.name} = new ${pascal('Module_' + submodule.name)}(this);`)

        return `
${indent(submodules_decls.join('\n'))}

    public JutgeApiClient() {
${indent2(submodules_inits.join('\n'))}
    }
`
    }

    private genEndpoint(endpoint: ApiEndpointDir, path: string[], root: boolean = false): string {
        const { name, input, output, summary, description, actor, status } = endpoint

        let inlined = false
        let params = ''
        let args = 'null'
        if (input.type !== 'void') {
            if (this.isInlined(input)) {
                inlined = true
                params = this.typify(input, '', path.join('_'), 0)
            } else {
                const param = input.param || 'data'
                params = `${this.typify(input, '', path.join('_'), 0)} ${param}`
            }
            args = input.param || 'data'
        }
        let ifiles_decl
        if (endpoint.ifiles == 'many') {
            ifiles_decl = 'byte[][] the_ifiles = ifiles;'
        } else if (endpoint.ifiles == 'one') {
            ifiles_decl = 'byte[][] the_ifiles = new byte[][]{ifile};'
        } else {
            ifiles_decl = 'byte[][] the_ifiles = new byte[0][0];'
        }

        let result = 'void'
        if (output.type !== 'void') {
            result = this.typify(output, '', path.join('_'), 0)
        }
        if (endpoint.ofiles === 'none') {
            // nothing
        } else if (endpoint.ofiles == 'one') {
            if (endpoint.output.type === 'void') {
                result = `Download`
            } else {
                result = `Tuple<${result}, Download>`
            }
        } else if (endpoint.ofiles == 'many') {
            if (endpoint.output.type === 'void') {
                result = `Download[]`
            } else {
                result = `Tuple<${result}, Download[]]>`
            }
        }

        let ifiles_parameter: string
        if (endpoint.ifiles == 'none') {
            ifiles_parameter = ''
        } else if (endpoint.ifiles == 'one') {
            ifiles_parameter = (input.type !== 'void' ? ', ' : '') + 'byte[] ifile'
        } else {
            ifiles_parameter = (input.type !== 'void' ? ', ' : '') + 'byte[][] ifiles'
        }

        const with_ofiles = endpoint.ofiles !== 'none'
        const without_output = with_ofiles && endpoint.output.type === 'void'

        let code0 = ''
        if (inlined) {
            const content = Object.entries(input.properties)
                .map(
                    ([key, _]: [string, any]) =>
                        `    ijson.add("${key}", new Gson().toJsonTree(${key}).getAsJsonObject());`,
                )
                .join('\n')

            code0 = `JsonObject ijson = new JsonObject();\n${content}`
        }

        let init
        if (input.type === 'void') init = 'null'
        else init = `new Gson().toJsonTree(${args}).getAsJsonObject()`

        const code1 = `${inlined ? '' : `JsonElement ijson = ${init};\n`}Execution execution = root.execute("${root ? '' : path.splice(1).join('.') + '.'}${name}", ijson, the_ifiles);`

        let code2 = ''
        if (!without_output) {
            const t = this.typify(endpoint.output, 'NAME', path.join('_'), 99)
            let t2 = t
            if (t == 'int') t2 = 'Integer'
            else if (t == 'double') t2 = 'Double'
            if (endpoint.output.type !== 'void') {
                code2 = `${t} result = new Gson().fromJson(execution.output, new TypeToken<${t2}>(){}.getType());`
            }
        }

        let code3 = ''
        if (!with_ofiles) {
            if (endpoint.output.type !== 'void') code3 = `return result;`
        } else if (without_output) {
            if (endpoint.ofiles === 'one') {
                code3 = `return execution.ofiles[0];`
            } else {
                code3 = `return execution.ofiles;`
            }
        } else {
            if (endpoint.ofiles === 'one') {
                code3 = `return new ${result}(result, execution.ofiles[0]);`
            } else {
                code3 = `return new ${result}(result, execution.ofiles);`
            }
        }

        if (this.aliases.has(result)) result = this.aliases.get(result)!

        return `
/**
${summary || 'No summary'}${actor ? '\n\n    🔐 Authenticated' : ''}    ${status ? `\n    ❌ Warning: ${status}` : ''}    ${description ? '\n\n' + description : ''}
*/
public ${result} ${name}(${params} ${ifiles_parameter}) throws Exception {

    ${code0}
    ${ifiles_decl}
    ${code1}
    ${code2}
    ${code3}
}
    `
    }

    private genSubModule(mod: ApiModuleDir, path: string): string {
        const module = this.genModule(mod, path.split('_'))

        let description = ''
        if (mod.description) {
            description = `
/**
${mod.description}
*/`
        }

        return `
${description}
@SuppressWarnings("unused")
public static class ${mod.name} {

${this.indent(module)}
}
    `
    }

    private indent(s: string): string {
        return s
            .split('\n')
            .map((line) => ' '.repeat(4) + line)
            .join('\n')
    }

    private camelToSnakeCase(s: string) {
        // use radash snake?
        return s.replace(/[/:-]/g, '_').replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`)
    }

    private accept_module(module: ApiModuleDir) {
        return !module.hideFromDoc // && module.name != 'admin'
    }

    private isInlined(model: any): boolean {
        return (
            Object.keys(model).length != 0 &&
            !('$ref' in model) &&
            !('$anyOf' in model) &&
            model.type === 'object' &&
            'properties' in model
        )
    }

    private typify(model: any, name: string, path: string, level: number): string {
        if (Object.keys(model).length == 0) {
            return 'Object'
        } else if ('$ref' in model) {
            if (level != 0) {
                if (this.aliases.has(model.$ref)) return this.aliases.get(model.$ref)!
                else return model.$ref
            } else {
                return model.$ref
            }
        } else if ('anyOf' in model) {
            if (model.anyOf.length == 2 && model.anyOf[1].type === 'null') {
                const base = this.typify(model.anyOf[0], name, path, level + 1)
                return objectify(base)
                // return `Optional<${objectify(base)}>`
            } else if (model.anyOf.length == 4 && model.anyOf[0].type === 'Date') {
                return 'String'
            } else {
                return (
                    'Union<' +
                    model.anyOf.map((x: any) => objectify(this.typify(x, 'fakename', 'fakepath', 99))).join(', ') +
                    '>'
                )
            }
        } else if (model.type === 'object') {
            if ('properties' in model) {
                if (name) {
                    const props = Object.entries(model.properties)
                        .map(([key, value]: [string, any]) => {
                            return `    public ${this.typify(value, name, path, level + 1)} ${namify(key)};`
                        })
                        .join('\n')
                    const description = '/** ' + (model.description ? model.description : 'No description yet') + ' */'
                    return `${description}\npublic static class ${name} {\n${props}\n}\n`
                } else {
                    return Object.entries(model.properties)
                        .map(([key, value]: [string, any]) => `${this.typify(value, name, path, level + 1)} ${key}`)
                        .join(', ')
                }
            } else if ('patternProperties' in model) {
                let base = this.typify(model.patternProperties['^(.*)$'], name, path, level + 1)
                base = objectify(base)
                return `HashMap<String, ${base}>`
            } else {
                throw new Error(`I do not know this type yet`)
            }
        } else if (model.type === 'array') {
            let base = this.typify(model.items, name, path, level + 1)
            base = objectify(base)
            return `Vector<${base}>`
        } else if (model.type === 'string') {
            return 'String'
        } else if (model.type === 'number') {
            return 'double'
        } else if (model.type === 'integer') {
            return 'int'
        } else if (model.type === 'boolean') {
            return 'boolean'
        } else if (model.type === 'void') {
            return 'Void'
        } else if (model.type === 'null') {
            return 'null'
        } else if (model.type === 'file') {
            return 'bytes'
        }

        console.error(model)
        return 'Object'
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

function indent(s: string): string {
    return s
        .split('\n')
        .map((line) => ' '.repeat(4) + line)
        .join('\n')
}

function indent2(s: string): string {
    return indent(indent(s))
}

function namify(name: string): string {
    if (name === 'public') return 'pub' // public is a reserved word in Java
    return name
}

function objectify(t: string): string {
    if (t == 'int') return 'Integer'
    if (t == 'boolean') return 'Boolean'
    if (t == 'double') return 'Double'
    return t
}

async function format(source: string): Promise<string> {
    if (!Bun.which('clang-format')) {
        console.error('clang-format command not found, skipping Java formatting')
        return source
    }
    return withTmpDir(async (tmp) => {
        const path = `${tmp}/JutgeApiClient.java`
        Bun.write(path, source)
        try {
            await $`clang-format -i --style=WebKit ${path}`
        } catch (e) {
            console.error(e)
            return source
        }
        return await Bun.file(path).text()
    })
}
