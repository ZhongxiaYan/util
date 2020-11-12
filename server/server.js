// Args
const args = require('minimist')(process.argv.slice(2))
const port = args.port
const exp = args.exp

// Libraries
const path = require('path')
const fs = require('fs')
const readline = require('readline')
const express = require('express')
const app = express()
const expressWs = require('express-ws')(app)

app.use((req, res, next) => {
    res.setHeader('Content-Security-Policy', "connect-src 'self' ws: wss:;")
    return next()
})

loadData = async exp_path => {
    let series = {}
    let iMax = 0
    let files = fs.readdirSync(exp_path).filter(
        file => file.endsWith('.log') && file.startsWith('202')
    )
    for (const file of files) {
        let log_path = path.join(exp_path, file)
        console.log(file)
        let fileStream = readline.createInterface({ input: fs.createReadStream(log_path) })

        for await (const line of fileStream) {
            if (line.includes(' | ')) {
                let kvs = line.split(' | ').map(kv => kv.split(' '))
                kvs.filter(([k, v]) => !['', 'i', 'ii'].includes(k)).forEach(([k, v]) => {
                    (series[k] || (series[k] = [])).push(parseFloat(v))
                })
                let [k, i] = kvs[0]
                if (k == 'i') {
                    iMax = Math.max(iMax, parseInt(i))
                }
            }
        }
    }
    // console.log(Object.entries(data).map(([k, v]) => { console.log(k, v.length) }))
    return { series, iMax }
}

app.ws('/', async (ws, req) => {
    ws.send(JSON.stringify({
        event: 'connected',
        data: await loadData(exp)
    }))
    ws.on('message', msg => {
        console.log(msg)
    })
})

app.use(express.static(path.join(__dirname, 'client/dist')))

app.listen(port, () => {
    console.log(`Running server on port ${port}`)
})