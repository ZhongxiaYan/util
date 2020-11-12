import React, { useState, useEffect, useRef } from "react"
import uPlot from "uplot"
import "/node_modules/uplot/dist/uPlot.min.css"

const opts = {
    title: "MyPlot",
    width: 800,
    height: 600,
    series: [
        {},
        {
            stroke: "red"
        }
    ]
}

let now = Math.floor(new Date() / 1e3)

const data = [[now, now + 60, now + 120, now + 180], [1, 2, 3, 4]]

export default function App(props) {
  const [data, setData] = useState(null);
  const plotRef = useRef()

  useEffect(() => {
    let ws = new WebSocket(`wss://${window.location.hostname}`)
    ws.onopen = () => {
      console.log('Connected to Websocket')
    }
    ws.addEventListener('message', ev => {
      let event = JSON.parse(ev.data)
      let data = event.data
      let series = data.series
      let iMax = data.iMax

      let y = series['outflow']
      let n_ii = Math.round(y.length / iMax)
      let x = y.map((v, i) => i * n_ii)
      setData([x, y])
      console.log([x, y])
      console.log('Plot')
      new uPlot(opts, [x, y], plotRef.current)
    })
  }, [props])

  return (
    <div>
      <div ref={plotRef} />
    </div>
  )
}