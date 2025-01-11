// Import the SimpleStorage contract artifact
const SimpleStorage = artifacts.require("SimpleStorage");

module.exports = function (deployer) {
  // Deploy the SimpleStorage contract
  deployer.deploy(SimpleStorage, 42);
};
