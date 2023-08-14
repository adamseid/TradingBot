export const updateGraph = (data, state, default_state) => {
    console.log('modules -> UpdateState.updateGraph(): STARTED')

    console.log(data)

    const message = data.message
    const column_names = data.column_names
    const list_of_columns = data.list_of_columns



    state.graph.column_names = column_names
    state.graph.list_of_columns = list_of_columns


    console.log('modules -> UpdateState.updateGraph(): STARTED')
    return state
}



export const updateSelectionMenu = (data, state, default_state) => {
    console.log('modules -> UpdateState.updateSelectionMenu(): STARTED')
    console.log(data)
    state.navigator.location = data['location']
    state.navigator.selection_list = data['selection_list']
    console.log('modules -> UpdateState.updateSelectionMenu(): FINISHED')
    return state
}