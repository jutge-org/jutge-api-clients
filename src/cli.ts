import { Command } from '@commander-js/extra-typings'
import type { Language } from './clients'
import { clients, generateClient } from './clients'

const languages = Object.keys(clients)
    .map((c) => `'${c}'`)
    .join(', ')

const cmd = new Command('jutge-api-client')
    .description('Generate a client for the Jutge API')
    .argument('<language>', `The language of the client to generate (${languages})`)
    .option('-d, --destination <dir>', 'The directory to output the client to', 'out')
    .action(async (language: string, { destination }) => {
        const filename = await generateClient(language as Language, destination)
        console.log(filename)
    })

cmd.parse()
