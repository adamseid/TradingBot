import React, { Component } from 'react'
import { updateState } from '../modules/TradingBot'
import Graph from './trading_bot/Graph'
import Current from './trading_bot/Current'
import Navigator from './trading_bot/Navigator'
import Timeframe from './trading_bot/Timeframe'


const default_state = {
    graph: {
        column_names: [],
        list_of_columns: [[]],
    },
    navigator: {
        location: [],
        selection_list: []
    }
}

export default class TradingBot extends Component {
    ws = new WebSocket('ws://localhost:8000/ws/' + 'trading-bot' + '/')

    constructor(props) {
        super(props)
        this.state = default_state
    }

    componentDidMount() {
        this.ws.onopen = () => {
            console.log('connected');

        }

        this.ws.onmessage = (e) => {
            const data_obj = JSON.parse(e.data)
            let state = updateState(data_obj, this.state, default_state)
            this.setState(state)
        }
    }


    render() {
        return (
            <div>
                <div>TradingBot</div>
                <div>{this.state.graph.column_names}</div>
                <div>
                    <Navigator
                        state={this.state}
                        ws={this.ws}
                    />
                </div>

                <div>
                    <Current
                        state={this.state}
                    />
                </div>

                <div>
                    <Timeframe
                        state={this.state}
                        ws={this.ws}
                    />
                </div>

                <div>
                    <Graph
                        state={this.state}

                    />
                </div>



            </div>

        )
    }
}
