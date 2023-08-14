import { updateGraph, updateSelectionMenu } from './update_state/UpdateState'


export const updateState = (data, state, default_state) => {
    console.log('modules -> TradingBot.updateState(): STARTED')



    if (data.message === 'connect') {
        console.log('connect')

    }

    if (data.message === 'send-data') {
        console.log('send-data')
        state = updateGraph(data, state, default_state)

    }

    if (data.message === 'selection-menu') {
        console.log('selection-menu')
        updateSelectionMenu(data, state, default_state)

    }



    console.log('modules -> TradingBot.updateState(): FINISHED')
    return state
}