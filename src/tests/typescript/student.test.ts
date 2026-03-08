import { describe, expect, it, beforeAll } from 'bun:test'
import { JutgeApiClient, UnauthorizedError } from './jutge_api_client'
import type {
    Profile,
    AllKeys,
    Submission,
    Course,
    Dashboard,
    AllDistributions,
    BriefAward,
    Award,
    BriefList,
    NewProfile,
} from './jutge_api_client'

const USER_UID = '99df26a2d6b44b41ad3772f5525dce52'

// --- Auth tests ---

describe('auth', () => {
    it('login success', async () => {
        const jutge = new JutgeApiClient()
        const creds = await jutge.login({ email: 'user1@jutge.org', password: 'setzejutges' })
        expect(creds.token).toBeString()
        expect(creds.token.length).toBeGreaterThan(0)
        expect(creds.user_uid).toBe(USER_UID)
        expect(creds.error).toBe('')
    })

    it('login failure', async () => {
        const jutge = new JutgeApiClient()
        expect(jutge.login({ email: 'user1@jutge.org', password: 'wrongpassword' })).rejects.toThrow(UnauthorizedError)
    })

    it('login with username', async () => {
        const jutge = new JutgeApiClient()
        const creds = await jutge.auth.loginWithUsername({ username: 'user1', password: 'setzejutges' })
        expect(creds.token).toBeString()
        expect(creds.token.length).toBeGreaterThan(0)
        expect(creds.user_uid).toBe(USER_UID)
        expect(creds.error).toBe('')
    })

    it('logout', async () => {
        const jutge = new JutgeApiClient()
        await jutge.login({ email: 'user1@jutge.org', password: 'setzejutges' })
        const profile = await jutge.student.profile.get()
        expect(profile.user_uid).toBe(USER_UID)
        await jutge.logout()
        expect(jutge.student.profile.get()).rejects.toThrow(UnauthorizedError)
    })
})

// --- Student tests ---

describe('student', () => {
    let jutge: JutgeApiClient

    beforeAll(async () => {
        jutge = new JutgeApiClient()
        await jutge.login({ email: 'user1@jutge.org', password: 'setzejutges' })
    })

    // --- profile ---

    describe('profile', () => {
        it('get', async () => {
            const profile = await jutge.student.profile.get()
            expect(profile.user_uid).toBe(USER_UID)
            expect(profile.email).toBeString()
            expect(profile.name).toBe('User One')
        })

        it('get avatar', async () => {
            const [_, avatar] = await jutge.student.profile.getAvatar()
            expect(avatar).toBeObject()
            const pngSignature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]
            expect(avatar.data.slice(0, 8)).toEqual(new Uint8Array(pngSignature))
        })

        it('update and restore', async () => {
            const updatable = new JutgeApiClient()
            await updatable.login({ email: 'updatable@jutge.org', password: 'setzejutges' })
            const original = await updatable.student.profile.get()
            const newProfile: NewProfile = {
                name: 'Temp Name',
                birth_year: original.birth_year ?? 2000,
                nickname: original.nickname ?? '',
                webpage: original.webpage ?? '',
                affiliation: original.affiliation ?? '',
                description: original.description ?? '',
                country_id: original.country_id ?? 'AD',
                timezone_id: original.timezone_id,
            }
            await updatable.student.profile.update(newProfile)
            const updated = await updatable.student.profile.get()
            expect(updated.name).toBe('Temp Name')
            // Restore
            await updatable.student.profile.update({
                name: original.name,
                birth_year: original.birth_year ?? 2000,
                nickname: original.nickname ?? '',
                webpage: original.webpage ?? '',
                affiliation: original.affiliation ?? '',
                description: original.description ?? '',
                country_id: original.country_id ?? 'AD',
                timezone_id: original.timezone_id,
            })
            const restored = await updatable.student.profile.get()
            expect(restored.name).toBe(original.name)
        })
    })

    // --- keys ---

    describe('keys', () => {
        it('get', async () => {
            const keys = await jutge.student.keys.get()
            expect(keys.problems).toBeArray()
            expect(keys.enrolled_courses).toContain('C00001')
            expect(keys.available_courses).toContain('C00002')
            expect(keys.available_courses).toContain('C00003')
        })

        it('get problems', async () => {
            const problems = await jutge.student.keys.getProblems()
            expect(problems).toBeArray()
            expect(problems.length).toBeGreaterThan(0)
        })

        it('get enrolled courses', async () => {
            const courses = await jutge.student.keys.getEnrolledCourses()
            expect(courses).toBeArray()
            expect(courses).toContain('C00001')
        })

        it('get available courses', async () => {
            const courses = await jutge.student.keys.getAvailableCourses()
            expect(courses).toBeArray()
            expect(courses).toContain('C00002')
        })

        it('get lists', async () => {
            const lists = await jutge.student.keys.getLists()
            expect(lists).toBeArray()
        })
    })

    // --- statuses ---

    describe('statuses', () => {
        it('get all', async () => {
            const statuses = await jutge.student.statuses.getAll()
            expect(statuses).toBeObject()
            expect(statuses).toHaveProperty('P68688')
            const s = statuses['P68688']
            expect(s.nb_submissions).toBeInteger()
            expect(s.status).toBeString()
        })

        it('get for abstract problem', async () => {
            const status = await jutge.student.statuses.getForAbstractProblem('P68688')
            expect(status.problem_nm).toBe('P68688')
            expect(status.nb_submissions).toBeInteger()
            expect(status.status).toBeString()
        })

        it('get for problem', async () => {
            const status = await jutge.student.statuses.getForProblem('P68688_ca')
            expect(status.problem_id).toBe('P68688_ca')
            expect(status.problem_nm).toBe('P68688')
            expect(status.nb_submissions).toBeInteger()
            expect(status.status).toBeString()
        })
    })

    // --- submissions ---

    describe('submissions', () => {
        it('get all', async () => {
            const subs = await jutge.student.submissions.getAll()
            expect(subs).toBeArray()
            expect(subs.length).toBeGreaterThanOrEqual(5)
        })

        it('index for problem', async () => {
            const index = await jutge.student.submissions.indexForProblem('P68688_ca')
            expect(index).toBeObject()
            for (const [key, sub] of Object.entries(index)) {
                expect(key).toBeString()
                expect((sub as Submission).problem_id).toBe('P68688_ca')
            }
        })

        it('get', async () => {
            const sub = await jutge.student.submissions.get({ problem_id: 'P68688_ca', submission_id: 'S001' })
            expect(sub.problem_id).toBe('P68688_ca')
            expect(sub.submission_id).toBe('S001')
        })

        it('get code as b64', async () => {
            const code = await jutge.student.submissions.getCodeAsB64({ problem_id: 'P68688_ca', submission_id: 'S001' })
            expect(code).toBeString()
            expect(code.length).toBeGreaterThan(0)
        })

        it('get analysis', async () => {
            const analysis = await jutge.student.submissions.getAnalysis({ problem_id: 'P68688_ca', submission_id: 'S001' })
            expect(analysis).toBeArray()
        })
    })

    // --- courses ---

    describe('courses', () => {
        it('index enrolled', async () => {
            const courses = await jutge.student.courses.indexEnrolled()
            expect(courses).toBeObject()
            expect(courses).toHaveProperty('instructor1:FAKE_COURSE1')
        })

        it('index available', async () => {
            const courses = await jutge.student.courses.indexAvailable()
            expect(courses).toBeObject()
            const hasExpected = 'instructor1:FAKE_COURSE2' in courses || 'instructor1:FAKE_COURSE3' in courses
            expect(hasExpected).toBe(true)
        })

        it('get enrolled', async () => {
            const course = await jutge.student.courses.getEnrolled('instructor1:FAKE_COURSE1')
            expect(course.course_nm).toBe('FAKE_COURSE1')
        })

        it('get available', async () => {
            const course = await jutge.student.courses.getAvailable('instructor1:FAKE_COURSE2')
            expect(course.course_nm).toBe('FAKE_COURSE2')
        })

        it('enroll and unenroll', async () => {
            await jutge.student.courses.enroll('instructor1:FAKE_COURSE2')
            const enrolled = await jutge.student.courses.indexEnrolled()
            expect(enrolled).toHaveProperty('instructor1:FAKE_COURSE2')
            // Restore state
            await jutge.student.courses.unenroll('instructor1:FAKE_COURSE2')
            const after = await jutge.student.courses.indexEnrolled()
            expect(after).not.toHaveProperty('instructor1:FAKE_COURSE2')
        })
    })

    // --- dashboard ---

    describe('dashboard', () => {
        it('get dashboard', async () => {
            const dashboard = await jutge.student.dashboard.getDashboard()
            expect(dashboard).toBeObject()
            expect(dashboard).toHaveProperty('stats')
            expect(dashboard).toHaveProperty('heatmap')
            expect(dashboard).toHaveProperty('distributions')
        })

        it('get stats', async () => {
            const stats = await jutge.student.dashboard.getStats()
            expect(stats).toBeObject()
        })

        it('get level', async () => {
            const level = await jutge.student.dashboard.getLevel()
            expect(level).toBeString()
        })

        it('get absolute ranking', async () => {
            const ranking = await jutge.student.dashboard.getAbsoluteRanking()
            expect(ranking).toBeInteger()
            expect(ranking).toBeGreaterThan(0)
        })

        it('get heatmap calendar', async () => {
            const heatmap = await jutge.student.dashboard.getHeatmapCalendar()
            expect(heatmap).toBeArray()
        })

        it('get all distributions', async () => {
            const dists = await jutge.student.dashboard.getAllDistributions()
            expect(dists).toBeObject()
            expect(dists).toHaveProperty('verdicts')
            expect(dists).toHaveProperty('compilers')
            expect(dists).toHaveProperty('proglangs')
        })
    })

    // --- awards ---

    describe('awards', () => {
        it('get all', async () => {
            const awards = await jutge.student.awards.getAll()
            expect(awards).toBeObject()
            expect(awards).toHaveProperty('A00000001')
        })

        it('get', async () => {
            const award = await jutge.student.awards.get('A00000001')
            expect(award.award_id).toBe('A00000001')
            expect(award.title).toBe('First AC')
            expect(award.type).toBe('solved')
        })
    })

    // --- lists ---

    describe('lists', () => {
        it('get all', async () => {
            const lists = await jutge.student.lists.getAll()
            expect(lists).toBeObject()
            for (const [key, brief] of Object.entries(lists)) {
                expect(key).toBeString()
                expect((brief as BriefList).list_nm).toBeString()
            }
        })

        it('get', async () => {
            const allLists = await jutge.student.lists.getAll()
            const keys = Object.keys(allLists)
            expect(keys.length).toBeGreaterThan(0)
            const lst = await jutge.student.lists.get(keys[0])
            expect(lst).toBeObject()
        })
    })
})
