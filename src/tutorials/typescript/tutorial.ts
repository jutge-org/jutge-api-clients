/**
 * This is a tutorial script that shows how to use the Jutge API client in TypeScript.
 *
 * In order to run this script you need to have the Jutge API client.
 * You can download it from https://api.jutge.org/api/clients/typescript
 *
 * Full reference documentation is available at https://api.jutge.org
 */

// Import the Jutge API client
import * as j from './jutge_api_client'

// Make a client
const jutge = new j.JutgeApiClient()

// Get a fortune cookie
console.log(await jutge.misc.getFortune())

// Get the current time in the server and print one of its attributes
const time = await jutge.misc.getTime()
console.log(time.full_time)
console.log()

// Get the homepage stats and print them
const stats = await jutge.misc.getHomepageStats()
console.log(`users: ${stats.users}, problems: ${stats.problems}, submissions: ${stats.submissions}`)
console.log()

// Get all compilers
const compilers = await jutge.tables.getCompilers()
// Filter C++ compilers amd print their name
for (const [compiler_id, compiler] of Object.entries(compilers)) {
    if (compiler.language === 'C++') {
        console.log(compiler.name)
    }
}
console.log()

// Get P68688 (Hello, world!) problem and print its title and author.
const problem = await jutge.problems.getProblem('P68688_en')
console.log(problem.title)
console.log(problem.abstract_problem.author)

// All previous functions where public, but in order to access
// other functions, we need to login. Please fill your email and
// password below.

const email = '...'
const password = '...'
await jutge.login({ email, password })

// Get user's name an uid in the profile.
const profile = await jutge.student.profile.get()
console.log(profile.name)
console.log(profile.user_uid)
console.log()

// All authenticated users are students and can use the student module.
// There are other modules for different roles, such as admin, instructor, etc.

// Get all problem statuses, filter those that are accepeted and print the first 8 in alphabetical order.
const statuses = await jutge.student.statuses.getAll()
const accepteds = []
for (const [problem_nm, status] of Object.entries(statuses)) {
    if (status.status == 'accepted') {
        accepteds.push(problem_nm)
    }
}
console.log(accepteds.sort().slice(0, 7))
console.log()

// Get the status of P68688
const status = await jutge.student.statuses.getForAbstractProblem('P68688')
console.log(status)
console.log()

// Logging out is not necessary, but it is advisable.
await jutge.logout()
console.log()

// See the full doc at https://api.jutge.org
