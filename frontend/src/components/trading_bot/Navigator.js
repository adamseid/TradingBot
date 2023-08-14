import React, { Component } from 'react'

export default class Navigator extends Component {

    constructor(props) {
        super(props);

        this.state = {
          position: "No Position",
          btc_balance: 0,
          btc_amount: 0,
          usdt_balance: 0,
          usdt_amount: 0,
        };
    }


  home = () => {
    this.props.ws.send(
      JSON.stringify({
        message_1: "navigator",
        message_2: "home",
      })
    );
  };

  goBack = () => {
    console.log("goBack");
    this.props.ws.send(
      JSON.stringify({
        message_1: "navigator",
        message_2: "go-back",
        data: {
          location: this.props.state.navigator.location,
        },
      })
    );
  };

  select = (button_name) => {
    console.log("select");
    console.log(button_name);
    this.props.ws.send(
      JSON.stringify({
        message_1: "navigator",
        message_2: "select",
        data: {
          location: this.props.state.navigator.location,
          selection: button_name,
        },
      })
    );
  };

  futurePosition = (position) => {
    console.log("futurePosition");
    console.log(position);
    this.props.ws.send(
      JSON.stringify({
        message_1: "future_contract",
        message_2: position,
        data: {
          position: position,
        },
      })
    );

    this.props.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if ("account_info" in data){
          console.log(data["account_info"]);
          this.setState({
            btc_balance:
              Math.round(data["account_info"][0]["dollar_value"] * 100) / 100,
          });
          this.setState({
            btc_amount: data["account_info"][0]["amount"],
          });
          this.setState({
            usdt_balance: Math.round(data["account_info"][1]["dollar_value"] * 100) / 100,
          });
          this.setState({
            usdt_amount: data["account_info"][1]["amount"],
          });
        }else if ("Position" in data) {
          console.log(data["Position"]);
          this.setState({ position: data["Position"] });
        } 
    };
  };

  render() {
    return (
      <div>
        <div className="navigation_bar_flex_container">
          <div>
            <div>Navigator</div>
            <button onClick={this.home}>Home</button>
            <button onClick={this.goBack}>Go Back</button>
          </div>
          <div>
            <div className="position_flex_container">
              <div>Position: </div>
              <div className="position_types">
                <span>{this.state.position}</span>
              </div>
            </div>
            <div className="position_flex_container">
              <div>BTC Amount / Balance: </div>
              <div className="position_types">
                <span>
                  {this.state.btc_amount} / ${this.state.btc_balance}
                </span>
              </div>
            </div>
            <div className="position_flex_container">
              <div>USDT Amount / Balance: </div>
              <div className="position_types">
                <span>
                  {this.state.usdt_amount} / ${this.state.usdt_balance}
                </span>
              </div>
            </div>
            <div>
              <div>
                <button onClick={() => this.futurePosition("Long")}>
                  Go Long
                </button>
                <button onClick={() => this.futurePosition("Short")}>
                  Go Short
                </button>
              </div>
              <div>
                <button onClick={() => this.futurePosition("CloseLong")}>
                  Close Long
                </button>
                <button onClick={() => this.futurePosition("CloseShort")}>
                  Close Short
                </button>
              </div>
              <div>
                <button onClick={() => this.futurePosition("GetCryptoData")}>
                  Get Crypto Data
                </button>
              </div>
            </div>
          </div>
        </div>
        <div>
          {/* {this.props.state.navigator.selection_list.map((buttonName) => (
            <button key={buttonName} onClick={() => this.select(buttonName)}>
              {buttonName}
            </button>
          ))} */}
        </div>
      </div>
    );
  }
}
