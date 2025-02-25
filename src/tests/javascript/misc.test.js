import { describe, expect, it } from 'bun:test'
import { jutge_api_client } from './jutge_api_client'

describe('testMisc', async () => {
    it('testGetTime', async () => {
        const jutge = jutge_api_client
        const time = await jutge.misc.getTime()
        expect(time).toBeObject()
        expect(time.full_time).toBeString()
        expect(time.int_timestamp).toBeInteger()
        expect(time.float_timestamp).toBeNumber()
        expect(time.time).toBeString()
        expect(time.date).toBeString()
    })

    it('testFortune', async () => {
        const jutge = jutge_api_client
        const fortune = await jutge.misc.getFortune()
        expect(fortune).toBeString()
    })
    it('testGetHomepageStats', async () => {
        const jutge = jutge_api_client
        const stats = await jutge.misc.getHomepageStats()
        expect(stats).toBeObject()
        expect(stats.users).toBeInteger()
        expect(stats.problems).toBeInteger()
        expect(stats.submissions).toBeInteger()
        expect(stats.exams).toBeInteger()
        expect(stats.contests).toBeInteger()
    })

    it('testGetLogo', async () => {
        const jutge = jutge_api_client
        const logo = await jutge.misc.getLogo()
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
