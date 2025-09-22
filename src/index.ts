import { Command } from '@commander-js/extra-typings'
import type { Language } from './clients'
import { clients, generateClient } from './clients'

export const JUTGE_API_URL = process.env.JUTGE_API_URL || 'https://api.jutge.org/api'

const allLanguages = Object.keys(clients).join(', ')

const cmd = new Command('jutge-api-client')
    .description('Generate a client for the Jutge API')
    .argument('[languages...]', `The programming languages to generate (${allLanguages}), empty for all`)
    .option('-o, --output <dir>', 'Output folder', 'out')
    .option('-h, --host <host>', 'The host that stores the API directory', JUTGE_API_URL)
    .action(async (languages, { output, host }) => {
        if (languages.length === 0) {
            languages = Object.keys(clients)
        }
        for (const language of languages) {
            const filename = await generateClient(host + "/dir", language as Language, output)
            console.log(`Writting ${language} client to`, filename)
        }
    })

cmd.parse()
