import React, { Component } from 'react';

class Current extends Component {
    render() {
        const column_names = this.props.state.graph.column_names
        const list_of_columns = this.props.state.graph.list_of_columns

        const last_index_row = column_names.map((name, index) => {
            const last_index = list_of_columns[index][list_of_columns[index].length - 1];
            return <td key={name}>{last_index}</td>;
        });

        const column_names_row = column_names.map(name => <th key={name}>{name}</th>);

        return (
            <table>
                <thead>
                    <tr>
                        {column_names_row}
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        {last_index_row}
                    </tr>
                </tbody>
            </table>
        );
    }
}

export default Current;
