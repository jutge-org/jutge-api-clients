/* eslint-disable  @typescript-eslint/no-explicit-any */

import type { ApiDir, ApiEndpointDir, ApiInfo, ApiModuleDir } from '@/types'
import { withTmpDir } from '@/utilities'
import { $ } from 'bun'
import path from 'path'

export async function genCppClient(dir: ApiDir): Promise<string> {
    const preamble = genPreamble(dir.info)
    const skeleton1 = await genSkeleton1()
    const skeleton2 = await genSkeleton2()
    const models = genModels(dir)
    const serializers = genSerializers(dir)
    const modules = genModule(dir.root, '', true)
    const source = `${preamble}

#ifndef JUTGE_API_CLIENT_H
#define JUTGE_API_CLIENT_H

${skeleton1}

// client

namespace jutge_api_client {

// models

${models}

// serializers

${serializers}

// modules

${modules}

// utilities

${skeleton2}

} // end namespace jutge_api_client

#endif

`
    return await format(source)
}

async function format(source: string): Promise<string> {
    if (!Bun.which('clang-format')) {
        console.error('clang-format command not found, skipping C++ formatting')
        return source
    }
    return withTmpDir(async (tmp) => {
        const path = `${tmp}/client.cpp`
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

function genPreamble(info: ApiInfo): string {
    return `
/**

This file has been automatically generated at ${new Date().toISOString()}

Name:       ${info.name}
Version:    ${info.version}

Description:

${info.description}

Dependencies:

https://github.com/nlohmann/json
https://github.com/yhirose/cpp-httplib

Compilation:

g++ -std=c++20 program.cpp -l ssl -l crypto
g++ -I/opt/homebrew/include -std=c++20 program.cpp -l ssl -l crypto

**/

`
}

async function genSkeleton1() {
    const packageRoot = path.resolve(__dirname, '../../..')
    return await Bun.file(`${packageRoot}/src/clients/cpp/skeleton1.cpp`).text()
}

async function genSkeleton2() {
    const packageRoot = path.resolve(__dirname, '../../..')
    return await Bun.file(`${packageRoot}/src/clients/cpp/skeleton2.cpp`).text()
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

    let input_parameters: string
    if (input.type == 'void') {
        input_parameters = ''
    } else {
        if ('$ref' in input) {
            const formal_parameter = input.param || 'data'
            input_parameters = `const ${typify(input, undefined)}& ${formal_parameter}`
        } else {
            if (input.type === 'object') {
                input_parameters = `${typify(input, undefined)}`
            } else {
                input_parameters = `const ${typify(input, undefined)}& ${input.param || 'data'}`
            }
        }
    }

    let ifiles_parameter: string
    if (endpoint.ifiles == 'none') {
        ifiles_parameter = ''
    } else if (endpoint.ifiles == 'one') {
        ifiles_parameter = 'const Blob& ifile'
    } else {
        ifiles_parameter = 'const std::vector<Blob>& ifiles'
    }

    let parameters: string
    if (input.type !== 'void' && endpoint.ifiles !== 'none') {
        parameters = `${input_parameters}, ${ifiles_parameter}`
    } else if (input.type !== 'void' && endpoint.ifiles === 'none') {
        parameters = input_parameters
    } else if (input.type === 'void' && endpoint.ifiles !== 'none') {
        parameters = ifiles_parameter
    } else {
        parameters = ''
    }

    const result_type_1 = typify(output, undefined)

    let result_type_2
    if (endpoint.ofiles === 'none') {
        result_type_2 = ''
    } else if (endpoint.ofiles === 'one') {
        result_type_2 = 'Download'
    } else {
        result_type_2 = 'std::vector<Download>'
    }

    let result_type
    if (endpoint.ofiles === 'none') {
        result_type = result_type_1
    } else if (result_type_1 === 'void') {
        result_type = result_type_2
    } else {
        result_type = `std::tuple<${result_type_1}, ${result_type_2}>`
    }

    let ijson
    if (input.type === 'void') {
        ijson = '{}'
    } else if ('$ref' in input) {
        ijson = 'data'
    } else {
        if (input.type === 'object') {
            ijson =
                '{ ' +
                Object.entries(input.properties)
                    .map(([key, value]: [string, any]) => `{"${key}", ${key}}`)
                    .join(', ') +
                ' }'
        } else {
            ijson = input.param || 'data'
        }
    }

    let result_1
    if (result_type_1 === 'void') {
        result_1 = ''
    } else {
        result_1 = 'ojson'
    }

    let result_2
    if (endpoint.ofiles === 'none') {
        result_2 = ''
    } else if (endpoint.ofiles === 'one') {
        result_2 = 'ofiles[0]'
    } else {
        result_2 = 'ofiles'
    }

    let result
    if (result_1 !== '' && endpoint.ofiles !== 'none') {
        result = `{${result_1}, ${result_2}}`
    } else if (result_1 === '' && endpoint.ofiles === 'none') {
        result = ''
    } else if (result_1 === '' && endpoint.ofiles !== 'none') {
        result = result_2
    } else {
        result = result_1
    }

    let ifiles
    if (endpoint.ifiles === 'none') {
        ifiles = '{}'
    } else if (endpoint.ifiles === 'one') {
        ifiles = '{ifile}'
    } else {
        ifiles = 'ifiles'
    }

    const code = `
    const json ijson = ${ijson};
    const auto [ojson, ofiles] = execute("${root ? '' : path + '.'}${name}", ijson, ${ifiles});
    return ${result};`

    const function_name = camelToSnakeCase(name)

    const header = `${result_type} ${function_name}(${parameters})`

    const documentation = `/**
    ${summary || 'No summary'}${actor ? '\n\n    🔐 Authenticated' : ''}    ${status ? `\n    ❌ Warning: ${status}` : ''}    ${description ? '\n\n    ' + description : ''}
    **/`

    return `
${header} {
    ${documentation}
    ${code}
}`
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
namespace ${mod.name} {

${module}

}`
}

function genModels(mod: ApiDir): string {
    return mod.models.map(([name, model]) => genModel(name, model)).join('\n')
}

function genModel(name: string, model: any): string {
    if (model.type === 'object' && 'properties' in model) {
        return `struct ${name} ${typify(model, name)}` + ';\n'
    } else {
        return `using ${name} = ${typify(model, name)};\n`
    }
}

function genSerializers(mod: ApiDir): string {
    return mod.models.map(([name, model]) => serializers(model, name)).join('\n')
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

function camelToSnakeCase(s: string) {
    return s.replace(/[/:-]/g, '_').replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`)
}

function typify(model: any, name?: string): string {
    if (Object.keys(model).length == 0) {
        return 'json'
    } else if ('$ref' in model) {
        return model.$ref
    } else if ('anyOf' in model) {
        if (model.anyOf.length == 2 && model.anyOf[1].type === 'null') {
            return `std::optional<${typify(model.anyOf[0], name)}>`
        } else if (model.anyOf.length == 4 && model.anyOf[0].type === 'Date') {
            return `std::string`
        } else {
            return `std::variant<${model.anyOf.map(typify).join(', ')}>`
        }
    } else if (model.type === 'object') {
        if ('properties' in model) {
            const props = Object.entries(model.properties)
                .map(([key, value]: [string, any]) => `${namify(key)}: ${typify(value)} `)
                .join(', ')
            if (name) {
                const props = Object.entries(model.properties)
                    .map(([key, value]: [string, any]) => `    ${typify(value)} ${namify(key)};`)
                    .join('\n')
                const fields = Object.entries(model.properties)
                    .map(([key, value]: [string, any]) => namify(key))
                    .join(', ')
                return `{\n${props}\n}`
            } else {
                return Object.entries(model.properties)
                    .map(([key, value]: [string, any]) => `const ${typify(value)}& ${namify(key)}`)
                    .join(', ')
            }
        } else if ('patternProperties' in model) {
            return `std::map<std::string, ${typify(model.patternProperties['^(.*)$'])}>`
        } else {
            throw new Error(`I do not know this type yet`)
        }
    } else if (model.type === 'array') {
        return `std::vector<${typify(model.items)}>`
    } else if (model.type === 'string') {
        return 'std::string'
    } else if (model.type === 'number') {
        return 'float'
    } else if (model.type === 'integer') {
        return 'int'
    } else if (model.type === 'boolean') {
        return 'bool'
    } else if (model.type === 'void') {
        return 'void'
    } else if (model.type === 'null') {
        return 'null'
    } else if (model.type === 'Date') {
        return 'std::string' // TODO: use better type? In fact, this generates a triple of strings???
    } else if (model.type === 'file') {
        return 'Uint8Array' // TODO: what to use???
    }

    /* We do not have this type :-( */
    console.error(model)
    return 'UNKNOWN'
}

function namify(name: string): string {
    if (name === 'public') return 'pub' // public is a reserved word in C++
    return name
}

function serializers(model: any, name: string): string {
    if (model.type === 'object' && 'properties' in model) {
        const props = Object.entries(model.properties)
            .map(([key, value]: [string, any]) => `    ${typify(value)} ${namify(key)};`)
            .join('\n')

        const to_json = `
            void to_json(json& j, const ${name}& x) {
                j = json{
            ${Object.entries(model.properties)
                .map(([key, value]: [string, any]) => `{"${key}", x.${namify(key)}}`)
                .join(',\n')}
                };
            }`
        const from_json = `
            void from_json(const json& j, ${name}& x) {
                ${Object.entries(model.properties)
                .map(([key, value]: [string, any]) => `j.at("${key}").get_to(x.${namify(key)});`)
                .join('\n    ')}
            }`

        return `${to_json}\n${from_json}`
    } else {
        return ''
    }
}
