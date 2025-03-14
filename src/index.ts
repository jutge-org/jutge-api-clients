import { Command } from "@commander-js/extra-typings"
import type { Language } from "./gen-client"
import { generateClient } from "./gen-client"

const cmd = new Command("jutge-api-client")
    .description("Generate a client for the Jutge API")
    .option("-d, --destination <dir>", "The directory where the client will be generated", ".")
    .argument("<language>", "The language of the client to generate")
    .action(async (language: string, { destination }) => {
        await generateClient(language as Language, destination)
    })

cmd.parse()
