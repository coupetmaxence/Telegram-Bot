# Telegram bitcoin bot

This Python powered bitcoin bot provides information such as account balance, account historic or even real-time exchange rates and bitcoin conversion to other currencies.

## About the project

### Libraries used

This project uses the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library and is based on one of the examples provided : the [echobot2.py](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot2.py) example.
It also uses the [emoji](https://pypi.python.org/pypi/emoji/) python package for emoji rendering in the messages and the [requests](http://docs.python-requests.org/en/master/) python package to make easier http requests.

### Webservices used

This project mainly uses two webservices : [blockcypher](https://www.blockcypher.com/dev/bitcoin/) and [blockchain.info](https://blockchain.info/api/exchange_rates_api) to get all the informations about bitcoins.

## Getting strated

### Prerequisites

You need to have [python](https://www.python.org/downloads/) installed on your computer (version 3.4 or higher).

### Installing

In order to use the python-telegram-bot library and the emoji and requests python packages you need to run thoses pip command line in your windows command line shell.
```
pip install python-telegram-bot
pip install emoji
pip install requests
```
If you are getting in trouble with thoses lines it is probably because your PATH environment variable does not contain your Python directory. Check this [link](http://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7) to solve the issue.

### Creating the bot

You now need to create your bot by exchanging with [BotFather](https://core.telegram.org/bots#6-botfather) on Telegram.
The last step is to replace the value of TOKEN at the line 15 of the Python script by your own token value returned by the BotFather.

Congratulation, your bitcoin Telegram bot is Ready !

<b>Note :</b> Be aware that you need the script to be run on a computer for the bot to work.

## Features

<img src="../master/screenshot/bot.png" height="400">
<div class=Row>
<div class="col-md-6 col-lg-6">
                                    <img src="../master/screenshot/bot.png" alt="bot" height="500" class="img-rounded" />
                                    <p>/balance and /ticker command</p>
                                </div>
<div class="col-md-6 col-lg-6">
                                    <img src="../master/screenshot/bot_conversion.png" alt="bot" height="500" class="img-rounded" />
                                    <p>/convert command</p>
                                </div>
<div class="col-md-6 col-lg-6">
                                    <img src="../master/screenshot/bot_conversion_keyboard.png" alt="bot" height="500" class="img-rounded" />
                                    <p>conversion specific keyboard</p>
                                </div>
<div class="col-md-6 col-lg-6">
                                    <img src="../master/screenshot/bot_historic.png" alt="bot" height="500" class="img-rounded" />
                                    <p>/historic command</p>
                                </div>
</div>
