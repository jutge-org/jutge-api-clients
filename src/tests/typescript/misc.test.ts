import { afterAll, describe, expect, it } from 'bun:test'
import { JutgeApiClient } from './jutge_api_client'

describe('x-forwarded-host header', () => {
    const savedDomain = process.env.JUTGE_DOMAIN

    afterAll(() => {
        if (savedDomain !== undefined) {
            process.env.JUTGE_DOMAIN = savedDomain
        } else {
            delete process.env.JUTGE_DOMAIN
        }
    })

    it('should include x-forwarded-host when JUTGE_DOMAIN is set', () => {
        process.env.JUTGE_DOMAIN = 'test.jutge.org'
        const client = new JutgeApiClient()
        expect(client.headers['x-forwarded-host']).toBe('test.jutge.org')
    })

    it('should not include x-forwarded-host when JUTGE_DOMAIN is not set', () => {
        delete process.env.JUTGE_DOMAIN
        const client = new JutgeApiClient()
        expect(client.headers['x-forwarded-host']).toBeUndefined()
    })
})

describe('testMisc', async () => {
    it('testGetTime', async () => {
        const jutge = new JutgeApiClient()
        const time = await jutge.misc.getTime(null)
        expect(time).toBeObject()
        expect(time.full_time).toBeString()
        expect(time.int_timestamp).toBeInteger()
        expect(time.float_timestamp).toBeNumber()
        expect(time.time).toBeString()
        expect(time.date).toBeString()
    })

    it('testFortune', async () => {
        const jutge = new JutgeApiClient()
        const fortune = await jutge.misc.getFortune(null)
        expect(fortune).toBeString()
    })
    it('testGetHomepageStats', async () => {
        const jutge = new JutgeApiClient()
        const stats = await jutge.misc.getHomepageStats(null)
        expect(stats).toBeObject()
        expect(stats.users).toBeInteger()
        expect(stats.problems).toBeInteger()
        expect(stats.submissions).toBeInteger()
        expect(stats.exams).toBeInteger()
        expect(stats.contests).toBeInteger()
    })

    it('testGetLogo', async () => {
        const jutge = new JutgeApiClient()
        const [_, logo] = await jutge.misc.getLogo(null)
        expect(logo).toBeObject()
        expect(logo.name).toBeString()
        expect(logo.type).toBeString()
        // TODO ??? expect(logo.data).toBeBinary()
        expect(logo.name).toBe('jutge.png')
        expect(logo.type).toBe('image/png')
        const pngSignature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]
        expect(logo.data.slice(0, 8)).toEqual(new Uint8Array(pngSignature))
    })
})
