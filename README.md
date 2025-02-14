# Blockpad Testnet Autoreferral
Blockpad Testnet autoreferral using gmail imap and proxies
- Another script, [Blockpad Automate](https://github.com/im-hanzou/blockpad-automate)
## Tools and components required
1. Blockpad Account, Register here: [https://testnet.blockpad.fun/register](https://testnet.blockpad.fun/register?ref=V779JC)
2. Blockpad Account Referral code, ex: `TZSXOS`
3. Gmail IMAP Accounts, Tutorial how to get your imap credentials, here: [YouTube](https://www.youtube.com/watch?v=pgoLc7TuHi8&ab_channel=TheKingofOnlineTools)
4. VPS or RDP (OPTIONAL)
### Buy Proxies
- Free Proxies Static Residental: 
1. [WebShare](https://www.webshare.io/?referral_code=p7k7whpdu2jg)
2. [ProxyScrape](https://proxyscrape.com/?ref=odk1mmj)
3. [MonoSans](https://github.com/monosans/proxy-list)
- Paid Premium Static Residental:
1. [922proxy](https://www.922proxy.com/register?inviter_code=d03d4fed)
2. [Proxy-Cheap](https://app.proxy-cheap.com/r/JysUiH)
3. [Infatica](https://dashboard.infatica.io/aff.php?aff=544)
## Installation
- Install Python For Windows: [Python](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)
- For Unix:
```bash
apt install python3 python3-pip git -y
```
- For Termux:
```bash
pkg install python python-pip git -y
```
- Download script [Manually](https://github.com/im-hanzou/blockpad-autoref/archive/refs/heads/main.zip) or use git:
```bash
git clone https://github.com/im-hanzou/blockpad-autoref
```
### Requirements installation
- Make sure you already in bot folder:
```bash
cd blockpad-autoref
```
#### Windows and Termux:
```bash
pip install -r requirements.txt
```
#### Unix:
```bash
pip3 install -r requirements.txt
```
## Run the Bot
- Insert your IMAP credentials to .env, example:
```bash
EMAIL_ADDRESS = "youremail@gmail.com"
PASSWORD = "xxxx xxxx xxxx xxxx"
```
- Replace the proxies ```proxies.txt``` to your own proxies, with the format example is like:
```bash
http://127.0.0.1:8080
http://user:pass@127.0.0.1:8080
```
>Only http proxies supported for now
- Windows and Termux:
```bash
python main.py
```
- Unix:
```bash
python3 main.py
```
- Then insert your Referral Code, ex: `TZSXOS`
# Notes
- Run this bot, use my referral code if you don't have one.
- You can just run this bot at your own risk, I'm not responsible for any loss or damage caused by this bot.
- This bot is for educational purposes only.
