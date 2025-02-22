import fs from 'fs/promises'

/**
 * Executes a function with a temporary directory path and cleans up the directory afterwards.
 *
 * @param fn - The function to be executed with the temporary directory path.
 * @returns A promise that resolves to the result of the function.
 */
export async function withTmpDir<T>(
    fn: (tmp: string) => Promise<T>,
    options: { remove: boolean } = { remove: true },
): Promise<T> {
    const dir = await fs.mkdtemp('/tmp/jutge-tmp-')
    try {
        return await fn(dir)
    } finally {
        if (options.remove) await fs.rmdir(dir, { recursive: true })
    }
}
