import React, { Component } from 'react';

export default class ButtonList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            buttons: ['15m', '1h', '4h', '1d']
        }
    }

    send(timeframe) {
        console.log(timeframe);
        this.props.ws.send(
            JSON.stringify({
                message_1: 'timeframe',
                data: {
                    timeframe: timeframe
                }

            })
        )
    }

    render() {
        return (
            <div>
                {this.state.buttons.map(button => (
                    <button key={button} onClick={() => this.send(button)}>{button}</button>
                ))}
            </div>
        );
    }
}