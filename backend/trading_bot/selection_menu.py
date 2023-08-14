selection_menu = {

    'raw': {
        'meta': {
            'type': 'folder',
        },
        'BTCUSDT': {
            'meta': {
                'type': 'file',
            },
            'column-keys': ['time', 'price', 'volume']
        }
    },

    'analysis': {
        'meta': {
            'type': 'folder',
        },
        'momentum': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'dprice', 'volume', 'momentum', 'momentumStdev']
            },
        },
        'price-derivatives': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'dprice', 'dpriceStdev']
            },
        },
        'price-derivatives-dynamic': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'dprice', 'deltaT', 'rValue']
            },
        }
    },


    'simulation': {
        'meta': {
            'type': 'folder',
        },
        's-2023-3-21': {
            'meta': {
                'type': 'file',
            },
        },
        's-2023-4-20': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'state', 'balanceCash', 'balanceAsset', 'value']
            },
        },
        's-2023-5-30': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'state', 'value', 'balanceCash', 'balanceAsset']
            },
        },
        's-2023-7-6': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'state', 'value', 'balanceShort', 'balanceLong']
            },
        },
        's-2023-7-26': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'state', 'value']
            },
        },
        's-2023-7-29': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'state', 'value']
            },
        },
        's-2023-7-30': {
            'meta': {
                'type': 'file',
                'column-keys': ['time', 'price', 'state', 'value', 'prev_trade_unix', 'profit', 'profit_percent',]
            },
        }
    },

}
