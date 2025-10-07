import type { TSchema } from '@sinclair/typebox'

export type FilesOptions = 'none' | 'one' | 'many'

export type ApiModels = [string, TSchema][]

export type ApiDir = {
    info: ApiInfo
    root: ApiModuleDir
    models: ApiModels
}

export type ApiInfo = {
    name: string
    description: string
    version: string
    url: string
}

export type ApiModuleDir = {
    name: string
    description?: string
    hideFromDoc?: boolean
    endpoints: ApiEndpointDir[]
    submodules: ApiModuleDir[]
}

export type ApiEndpointDir = {
    status?: string
    name: string
    summary?: string
    description?: string
    actor: string
    domains: string[]
    input: TSchema
    output: TSchema
    ifiles?: FilesOptions
    ofiles?: FilesOptions
    clientTtl?: number
}
