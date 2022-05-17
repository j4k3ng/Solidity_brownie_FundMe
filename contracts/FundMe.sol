//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.6.1;

//import chailnlink to use as oracle, we can do it with just import or copy the function directly from url
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

// interface AggregatorV3Interface {
//     function decimals() external view returns (uint8);

//     function description() external view returns (string memory);

//     function version() external view returns (uint256);

//     // getRoundData and latestRoundData should both raise "No data present"
//     // if they do not have data to report, instead of returning unset values
//     // which could be misinterpreted as actual reported values.
//     function getRoundData(uint80 _roundId)
//         external
//         view
//         returns (
//             uint80 roundId,
//             int256 answer,
//             uint256 startedAt,
//             uint256 updatedAt,
//             uint80 answeredInRound
//         );

//     function latestRoundData()
//         external
//         view
//         returns (
//             uint80 roundId,
//             int256 answer,
//             uint256 startedAt,
//             uint256 updatedAt,
//             uint80 answeredInRound
//         );
// }

contract FundMe {
    address public owner;
    AggregatorV3Interface public priceFeed;

    // in the constructor I define the priceFeed address where I get the chainlink ethusd price. I also define the owner by telling that is who deploy the contract
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    //create a map to store address and amount
    mapping(address => uint256) public addressToAmountFunded;

    function fund() public payable {
        //require at least 50 usd
        uint256 minimum = 50;
        //require(50/getConversionRate(msg.value)>= minimum, "you need at least 50 usd");
        //send money to the address associated with who send the money
        //which basically means send to myself a quantity equal to msg.value
        addressToAmountFunded[msg.sender] += msg.value;
    }

    function getVersion() public view returns (uint256) {
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(
        //     0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        // );
        return priceFeed.version();
    }

    function getDecimals() public view returns (uint256) {
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(
        //     0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        // );
        return 10**priceFeed.decimals();
    }

    function getPrice() public view returns (uint256) {
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(
        //     0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        // );
        (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return uint256(answer);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / getDecimals();
        return ethAmountInUsd;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        //send all the eth present in the contract to anyone who call this function
        //require(msg.sender == owner);
        payable(msg.sender).transfer(address(this).balance);
    }
}
