const HelloBlockchain = artifacts.require("HelloBlockchain");

contract("HelloBlockchain", (accounts) => {
  it("should emit RequestSent event on SendRequest", async () => {
    const instance = await HelloBlockchain.deployed();

    // Send a request
    const tx = await instance.SendRequest("Test Message", { from: accounts[0] });

    // Verify the event
    assert.equal(tx.logs.length, 1, "Expected one event");
    assert.equal(tx.logs[0].event, "RequestSent", "Expected RequestSent event");
    assert.equal(tx.logs[0].args.requestor, accounts[0], "Incorrect requestor");
    assert.equal(tx.logs[0].args.requestMessage, "Test Message", "Incorrect message");
    assert.equal(tx.logs[0].args.state.toString(), "0", "Incorrect state");
  });
});
