/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable no-inner-declarations */

var jutge_api_client = {
    //

    // default value for the Jutge API URL
    JUTGE_API_URL: 'https://api.jutge.org/api',

    // global variable to store the meta information
    meta: undefined,

    // exceptions

    UnauthorizedError: class extends Error {
        name = 'UnauthorizedError'
        constructor(message = 'Unauthorized') {
            super(message)
        }
    },

    InfoError: class extends Error {
        name = 'InfoError'
        constructor(message) {
            super(message)
        }
    },

    NotFoundError: class extends Error {
        name = 'NotFoundError'
        constructor(message) {
            super(message)
        }
    },

    InputError: class extends Error {
        name = 'InputError'
        constructor(message) {
            super(message)
        }
    },

    ProtocolError: class extends Error {
        name = 'ProtocolError'
        constructor(message) {
            super(message)
        }
    },

    /** Function that sends a request to the API and returns the response **/

    execute: async function (func, input, ifiles = []) {
        // prepare form
        const iform = new FormData()
        const idata = { func, input, meta: jutge_api_client.meta }
        iform.append('data', JSON.stringify(idata))
        for (const index in ifiles) iform.append(`file_${index}`, ifiles[index])

        // send request
        const response = await fetch(jutge_api_client.JUTGE_API_URL, {
            method: 'POST',
            body: iform,
        })

        // process response
        const contentType = response.headers.get('content-type')?.split(';')[0].toLowerCase()
        if (contentType !== 'multipart/form-data') {
            throw new jutge_api_client.ProtocolError('The content type is not multipart/form-data')
        }

        const oform = await response.formData()
        const odata = oform.get('data')
        const { output, error, duration, operation_id, time } = JSON.parse(odata)

        if (error) {
            jutge_api_client.throwError(error, operation_id)
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

        return [output, ofiles]
    },

    throwError: function (error, operation_id) {
        const message = error.message || 'Unknown error'
        if (error.name === 'UnauthorizedError') {
            throw new jutge_api_client.UnauthorizedError(message)
        } else if (error.name === 'InfoError') {
            throw new jutge_api_client.InfoError(message)
        } else if (error.name === 'NotFoundError') {
            throw new jutge_api_client.NotFoundError(message)
        } else if (error.name === 'InputError') {
            throw new jutge_api_client.InputError(message)
        } else {
            throw new Error(message)
        }
    },
}
