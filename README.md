# SerpentTests
A simple python module for testing simple serpent contracts, written in **Python 3.6** (bleeding edge! :)

The plan is to use this to test some more basic Serpent contracts
I'm writing and then once I've finished those, to use them to add functionality. So expect interesting updates
in the future!

See [tests/test_fibs](tests/test_fibs.py) for an example.

### Installation
Installing this module requires cloning the repositories for serpent and pyethereum, and manually installing those.
Copy paste the following code snippets into a bash terminal to install all the parts (I recommend using a virtual env!)

1. `git clone https://github.com/ethereum/serpent.git && cd serpent && python setup.py install && cd ..`
2. `git clone https://github.com/ethereum/pyethereum.git && cd pyethereum && python setup.py install && cd ..`
3. `git clone https://github.com/SerpentChris/SerpentTests.git && cd SerpentTests && python setup.py install && cd ..`
