LIQUIDATE_EVENT ={
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "collateralAsset",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "debtAsset",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "user",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "debtToCover",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "liquidatedCollateralAmount",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "liquidator",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "bool",
          "name": "receiveAToken",
          "type": "bool"
        }
      ],
      "name": "LiquidationCall",
      "type": "event"
    }