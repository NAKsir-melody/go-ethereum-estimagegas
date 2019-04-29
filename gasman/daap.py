import time
from web3 import Web3, HTTPProvider
from solc import compile_source

contract_source_code = '''
contract Greeter {
    string public greeting;

    function Greeter() {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
'''

rpc_url = "http://localhost:8080"
w3 = Web3(HTTPProvider(rpc_url))
w3.personal.unlockAccount(w3.eth.accounts[0], "admin", 0)
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol["<stdin>:Greeter"]
contract = w3.eth.contract(abi= contract_interface['abi'],
                           bytecode= contract_interface['bin'],
                           bytecode_runtime= contract_interface['bin-runtime'])


tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0]})

w3.miner.start(1)
time.sleep(3)

tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']
contract_instance = contract(contract_address)

print('Gas {}'.format(contract_instance.estimateGas({'from': w3.eth.accounts[0]}).setGreeting("TEST")))

print('Contract value: {}'.format(contract_instance.call().greet()))

contract_instance.transact({'from': w3.eth.accounts[0]}).setGreeting("TEST")

w3.miner.start(1)
time.sleep(3)
w3.miner.stop()
print('Contract value: {}'.format(contract_instance.call().greet()))

print('Gas {}'.format(contract_instance.estimateGas({'from': w3.eth.accounts[0]}).setGreeting("hello")))

print('Gas {}'.format(contract_instance.estimateGas2({'from': w3.eth.accounts[0]}).setGreeting("hello")))


w3.miner.stop()
