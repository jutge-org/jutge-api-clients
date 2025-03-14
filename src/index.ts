import { Command } from "@commander-js/extra-typings"
import type { Language } from "./gen-client"
import { clients, generateClient } from "./gen-client"

const languages = Object.keys(clients)
    .map((c) => `'${c}'`)
    .join(", ")

const cmd = new Command("jutge-api-client")
    .description("Generate a client for the Jutge API")
    .option("-d, --destination <dir>", "The directory where the client will be generated", "client-out")
    .argument("<language>", `The language of the client to generate (${languages})`)
    .action(async (language: string, { destination }) => {
        await generateClient(language as Language, destination)
    })

cmd.parse()
