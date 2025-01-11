# blockchain-for-42
trascendence, blockhain, solidity, ethereum
<h2>Useful links</h2>
<h3>1. Storing Data on Ethereum Blockchain With Python</h3>
<p>Link: https://medium.com/geekculture/storing-data-on-ethereum-blockchain-with-python-c76e6d91383f . Since only two options for tests of blockchain exist, could be useful to test ganashe (not in-browser) and understand how to check data on blockchain. Not suitable for the project, because it's solutions that doesn;t require to code anything on solidity.</p>
<h3>2. Basic info about Ethereum blockchain</h3>
<p>Link: https://www.geeksforgeeks.org/how-to-store-data-on-ethereum-blockchain/</p>
<h3>3. What type of data to actually store on blockchain</h4>
<p>Link: https://stackoverflow.com/questions/50781062/storing-users-data-on-ethereum-blockchain. Only hash or all the info??? </p>
<h3>4. Blockchain deployment as 4th service in docker apart from frontend, backend, db???</h3>
<p>Link: https://www.abastos.dev/projects/transcendence/</p>
<h4>5. Running ganachee</h4>
<p>./ganache-2.7.1-linux-x86_64.AppImage </p>
<h4>6. Building solidity project using truffle for vscode</h4>
<p>Link: https://archive.trufflesuite.com/blog/build-on-web3-with-truffle-vs-code-extension/</p>
<h2>12.11.24</h2>
<h4>7. Deploy Solidity Smart Contracts with Ganache</h4>
<p>Link: https://www.youtube.com/watch?v=UnNPv6zEbwc&t=171s/p>
<p>Folder: truffle_smart_contract_1, truffle develop -> migrate -> CANT DEPLOY ToDo.sol . Maybe problems with migration .js file?</p>
<h4>8. How to use ganache gui with truffle !</h4>
<p>Link: https://www.youtube.com/watch?v=aRJA1r1Gwu0</p>
<h4>9.Website to check ethereum raw transactions</h4>
<p>Link: https://rawtxdecode.in/</p>
<h4>Commands to create smart contract + create new solidity project</h4>
<ol>
  <li>npx truffle test</li>
  <li>npx truffle init</li>
</ol>
<h4>10. Examples of blockchain implementation in other 42 transcendence projects</h4>
<p>Link: https://github.com/DGross245/42-ft_transcendence/tree/master/contracts</p>
<h2>Tasks for 19.11.24</h2>
<p>Instead of only creation of the contract on blockchain, test contract call, events, retrieve the stored data on blockchain</p>
<p>Test interaction in different ganache workspaces</p>
<h3>Current folder</h3>
<h4>Compilation</h4>
<p>truffle compile</p>
<h4>Deployment</h4>
<p>truffle migrate</p>
<h4>Contract interaction</h4>
<p>1.truffle console</p>
<p>2.in terminal use tests from store.js to call the function in the contract</p>
<p>3.if needed to call the function at the specified address use:</p>
<p>const HelloBlockchain = await artifacts.require("HelloBlockchain"); <br>
const instance = await HelloBlockchain.at("0xYourContractAddressHere");
</p>
<p>4. To create new contract and call the function at the same time use <truffle test></p>
<h3>22.11.24</h3>
<h4>1. Getting Started with smart contract: https://blog.arashtad.com/blockchain/ethereum/smart-contracts-using-solidity/</h4>
<h4>2. Deploying Smart Contract using Python web3 tools: https://medium.com/@arashtad/how-to-deploy-a-smart-contract-using-python-web3-tools-a-full-coverage-59e6c2ad3f9f</h4>
<h4>3. Should I retrieve data from the Blockchain in python code and display it on webpage to keep track of the scores?? https://stackoverflow.com/questions/59160115/how-can-i-get-the-data-stored-in-blockchain-and-then-display-on-webpage</h4>
<h4>Stopped on web3_simple_storage. Next time try to retreive data from a certain block!</h4>
<h2>Tasks for 24.11.24</h2>
  <ol>
    <li>Compile current python project</li>
    <li>Ask Misha about data storage</li>
    <li>Add and test web3, solcx on the current project</li>
  </ol>
<h2>Tasks for 26.11.24</h2>
<ol>
  <li>Learn about events/modifiers</li>
  <li>Learn solidity syntax, how to work with different data types</li>
  <li>Difference between contract calls?</li>
  <li>Test restreiving data from python file and using smart contracts putting it on blockchain</li>
  <li>Better research usage of migrations, tests</li>
  <li>Run truffle and ganache on linux with similar to school working environment = OR create docker and put the program inside</li>
  <li>Test other frameworks and local development environments</li>
  <li>Test the function to retrieve the data from the blockchain: https://www.quora.com/How-can-I-store-data-on-the-blockchain-with-a-smart-contract</li>
  <li><b>EVENTS!!!</b>: https://medium.com/coinmonks/solidity-events-explained-82dc9104bc62#:~:text=In%20Solidity%2C%20events%20are%20a,it%20transparent%20and%20easily%20accessible.</li>
  <li><b>MODIFIERS</b>: https://www.freecodecamp.org/news/what-are-solidity-modifiers/</li>
</ol>
<h2>24.11.24</h2>
<p>1. Django and Web3: https://medium.com/@adabur/how-to-build-a-decentralized-authentication-system-with-django-and-web3-287e9c6c5301</p>
<p>2. To start docker on mac: 
  <ul>
  <li>colima start</li>
<li>docker ps -a </li>
  </ul></p>
<p>3. To acces psql on mac from docker:
<ul>
  <li>docker-compose up -d</li>
  <li>docker exec -it postgres-db bash</li>
  <li>psql -U django_admin -d django</li>
</ul></p>
<h2>Tasks for the future:</h2>
<ol>
  <li><b>Idea:</b> connecting user wallet from the start like here https://github.com/DGross245/42-ft_transcendence</li>
</ol>
