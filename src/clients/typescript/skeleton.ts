// PREAMBLE_HERE

/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */

// Models

// MODELS_HERE

// Client types

export interface Meta {
    readonly token: string
    readonly exam: string | null
}

export interface Download {
    readonly data: Uint8Array
    readonly name: string
    readonly type: string
}

// Exceptions

export class UnauthorizedError extends Error {
    name: string = 'UnauthorizedError'
    constructor(public message: string = 'Unauthorized') {
        super(message)
    }
}

export class InfoError extends Error {
    name: string = 'InfoError'
    constructor(public message: string) {
        super(message)
    }
}

export class NotFoundError extends Error {
    name: string = 'NotFoundError'
    constructor(public message: string) {
        super(message)
    }
}

export class InputError extends Error {
    name: string = 'InputError'
    constructor(public message: string) {
        super(message)
    }
}

export class ProtocolError extends Error {
    name: string = 'ProtocolError'
    constructor(public message: string) {
        super(message)
    }
}

type CacheEntry = {
    output: any
    ofiles: any
    epoch: number
}

/**
 *
 * JutgeApiClient
 *
 */
export class JutgeApiClient {
    //

    /** Client TTL values (in seconds) */
    clientTTLs: Map<string, number> = new Map()

    /** Whether to use cache or not */
    useCache: boolean = true

    /** Whether to log cache or not */
    logCache: boolean = false

    /** The cache */
    private cache: Map<string, CacheEntry> = new Map()

    /** URL to talk with the API */
    JUTGE_API_URL = process.env.JUTGE_API_URL || 'https://api.jutge.org/api'

    /** Meta information */
    meta: Meta | null = null

    /** Function that sends a request to the API and returns the response. **/
    async execute(func: string, input: any, ifiles: File[] = []): Promise<[any, Download[]]> {
        //

        const caching = this.useCache && this.clientTTLs.has(func) && ifiles.length === 0

        // check cache
        if (caching) {
            const key = JSON.stringify({ func, input })
            const entry = this.cache.get(key)
            if (entry !== undefined) {
                if (this.logCache) console.log('found')
                const ttl = this.clientTTLs.get(func)!
                if (entry.epoch + ttl * 1000 > new Date().valueOf()) {
                    if (this.logCache) console.log('used')
                    return [entry.output, entry.ofiles]
                } else {
                    if (this.logCache) console.log('expired')
                    this.cache.delete(key)
                }
            }
        }
        if (this.logCache) console.log('fetch')

        // prepare form
        const iform = new FormData()
        const idata = { func, input, meta: this.meta }
        iform.append('data', JSON.stringify(idata))
        for (const index in ifiles) iform.append(`file_${index}`, ifiles[index])

        // send request
        const response = await fetch(this.JUTGE_API_URL, {
            method: 'POST',
            body: iform,
        })

        // process response
        const contentType = response.headers.get('content-type')?.split(';')[0].toLowerCase()
        if (contentType !== 'multipart/form-data') {
            throw new ProtocolError('The content type is not multipart/form-data')
        }

        const oform = await response.formData()
        const odata = oform.get('data')
        const { output, error, duration, operation_id, time } = JSON.parse(odata as string)

        if (error) {
            this.throwError(error, operation_id)
        }

        // extract ofiles
        const ofiles = []
        for (const [key, value] of oform.entries()) {
            if (value instanceof File) {
                ofiles.push({
                    data: new Uint8Array(await value.arrayBuffer()),
                    name: value.name,
                    type: value.type,
                })
            }
        }

        // update cache
        if (caching) {
            if (this.logCache) console.log('saved')
            const key = JSON.stringify({ func, input })
            this.cache.set(key, { output, ofiles, epoch: new Date().valueOf() })
        }

        return [output, ofiles]
    }

    /** Function that throws the exception received through the API */
    throwError(error: Record<string, any>, operation_id: string | undefined) {
        const message = error.message || 'Unknown error'
        if (error.name === 'UnauthorizedError') {
            throw new UnauthorizedError(message)
        } else if (error.name === 'InfoError') {
            throw new InfoError(message)
        } else if (error.name === 'NotFoundError') {
            throw new NotFoundError(message)
        } else if (error.name === 'InputError') {
            throw new InputError(message)
        } else {
            throw new Error(message)
        }
    }

    /** Simple login */
    // @ts-expect-error: CredentialsOut is not defined here
    async login({ email, password }: { email: string; password: string }): Promise<CredentialsOut> {
        const [credentials, _] = await this.execute('auth.login', { email, password })
        if (credentials.error) throw new UnauthorizedError(credentials.error)
        this.meta = { token: credentials.token, exam: null }
        return credentials
    }

    /** Simple logout */
    async logout(): Promise<void> {
        await this.execute('auth.logout', {})
        this.meta = null
    }

    /** Clear the contents of the cache */
    clearCache() {
        if (this.logCache) console.log('clear')
        this.cache = new Map()
    }

    /** Provide a new value to the cache */
    setCache(newCache: string) {
        const obj = JSON.parse(newCache)
        this.cache = new Map(Object.entries(obj))
        this.removeExpired()
    }

    /** Get current value of the cache */
    getCache(): string {
        this.removeExpired()
        const obj = Object.fromEntries(this.cache.entries())
        return JSON.stringify(obj)
    }

    /** Remove expired entries from cache */
    private removeExpired() {
        for (const [key, entry] of this.cache) {
            const { func } = JSON.parse(key)
            const ttl = this.clientTTLs.get(func)
            if (ttl !== undefined && entry.epoch + ttl * 1000 < new Date().getTime()) {
                this.cache.delete(key)
            }
        }
    }

    // MAIN_MODULE_HERE
}

// MODULES_HERE
