import requests
import names
import random
import string
from fake_useragent import UserAgent
import imaplib
import email
import re
import os
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from dotenv import load_dotenv
import time
import email.utils
from twocaptcha import TwoCaptcha

init()

def print_banner():
    banner = f"""{Fore.CYAN}
╔══════════════════════════════════════════════╗
║           Blockpad Testnet Autoref           ║
║     Github: https://github.com/im-hanzou     ║
╚══════════════════════════════════════════════╝
    {Style.RESET_ALL}"""
    print(banner)

class Logger:
    account_number = 0
    
    @staticmethod
    def log(message, color=Fore.WHITE):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.WHITE}[{Style.DIM} {timestamp} {Style.RESET_ALL}{Fore.WHITE}] [{Fore.YELLOW}#{Logger.account_number}{Fore.WHITE}] {color}{message}{Style.RESET_ALL}")

class ProxyManager:
    def __init__(self, proxy_file="proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies = self.load_proxies()
        self.current_proxy = None
    
    def load_proxies(self):
        try:
            with open(self.proxy_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            Logger.log(f"Proxy file {self.proxy_file} not found!", Fore.RED)
            return []
    
    def get_random_proxy(self):
        if not self.proxies:
            return None
        self.current_proxy = random.choice(self.proxies)
        return {
            'http': f'{self.current_proxy}',
            'https': f'{self.current_proxy}'
        }

class CaptchaSolver:
    def __init__(self, api_key):
        self.solver = TwoCaptcha(api_key)
        self.site_key = "6LeLFdcqAAAAANR5eO7sNEKMmWGYhrBIjwxRpjnY"
        self.url = "https://testnet.blockpad.fun"

    def solve_captcha(self):
        try:
            Logger.log("Solving reCAPTCHA...", Fore.YELLOW)
            result = self.solver.recaptcha(
                sitekey=self.site_key,
                url=self.url
            )
            Logger.log("reCAPTCHA solved successfully!", Fore.GREEN)
            return result['code']
        except Exception as e:
            Logger.log(f"Error solving captcha: {e}", Fore.RED)
            return None

class GmailIMAP:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.imap_server = "imap.gmail.com"
        
    def get_verification_code(self, specific_email, max_retries=15, retry_delay=5):
        imap = imaplib.IMAP4_SSL(self.imap_server)
        try:
            imap.login(self.email_address, self.password)
        except Exception as e:
            Logger.log(f"IMAP login failed: {e}", Fore.RED)
            return None
        
        for attempt in range(max_retries):
            try:
                imap.select("INBOX")
                
                search_criteria = [
                    f'TO "{specific_email}"',
                    'SUBJECT "Verify Your Email - Blockpad Testnet"'
                ]
                
                _, messages = imap.search(None, ' '.join(search_criteria))
                
                if messages[0]:
                    email_ids = messages[0].split()
                    latest_email_id = email_ids[-1] 
                    _, msg = imap.fetch(latest_email_id, "(RFC822)")
                    email_body = msg[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            if part.get_content_type() == "text/html":
                                html_content = part.get_payload(decode=True).decode()
                                pattern = r'<h2 style="color: #1a73e8; margin: 0; font-family: monospace;">([A-Z0-9]+)</h2>'
                                match = re.search(pattern, html_content)
                                if match:
                                    verification_code = match.group(1)
                                    imap.close()
                                    imap.logout()
                                    return verification_code
                
                Logger.log(f"Attempt {attempt + 1}: Verification email not found, waiting {retry_delay} seconds...", Fore.YELLOW)
                time.sleep(retry_delay)
                
            except Exception as e:
                Logger.log(f"Error reading email (attempt {attempt + 1}): {e}", Fore.RED)
                time.sleep(retry_delay)
                
        imap.close()
        imap.logout()
        return None

def generate_username():
    first_name = names.get_first_name().lower()
    last_name = names.get_last_name().lower()
    random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    return f"{first_name}{last_name}{random_numbers}"

def generate_password():
    letters = ''.join(random.choices(string.ascii_lowercase, k=7))
    numbers = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    return letters.capitalize() + '@' + numbers

def generate_email_suffix():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_lowercase, k=4))
    return f"{timestamp}{random_str}"

def save_account(username, password, email, token):
    with open('accounts.txt', 'a') as f:
        f.write(f"Username: {username}\nEmail: {email}\nPassword: {password}\nToken: {token}\n\n")

def get_headers():
    ua = UserAgent()
    user_agent = ua.chrome
    return {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://testnet.blockpad.fun',
        'Referer': 'https://testnet.blockpad.fun/',
        'User-Agent': user_agent,
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

def try_verify_email(headers, verification_code, email, proxy, gmail_handler):
    MAX_VERIFY_ATTEMPTS = 5
    
    for attempt in range(MAX_VERIFY_ATTEMPTS):
        try:
            verify_response = requests.post(
                'https://api3.blockpad.fun/api/auth/verify-email',
                headers=headers,
                json={"verificationCode": verification_code},
                proxies=proxy,
            )
            
            verify_json = verify_response.json()
            if verify_json.get('success') == True:
                return verify_json.get('token')
            else:
                if attempt < MAX_VERIFY_ATTEMPTS - 1:
                    Logger.log(f"Verification attempt {attempt + 1} failed, getting new code...", Fore.YELLOW)
                    new_code = gmail_handler.get_verification_code(specific_email=email)
                    if new_code and new_code != verification_code:
                        verification_code = new_code
                        Logger.log(f"Got new verification code: {verification_code}", Fore.GREEN)
                    else:
                        time.sleep(5)
                else:
                    Logger.log("All verification attempts failed", Fore.RED)
                    
        except Exception as e:
            if attempt < MAX_VERIFY_ATTEMPTS - 1:
                Logger.log(f"Error during verification attempt {attempt + 1}: {e}, retrying...", Fore.YELLOW)
                time.sleep(5)
            else:
                Logger.log(f"All verification attempts failed with error: {e}", Fore.RED)
    return None

def register_account(referral_code, gmail_handler, proxy_manager, captcha_solver):
    proxy = proxy_manager.get_random_proxy()
    headers = get_headers()
    
    username = generate_username()
    password = generate_password()
    email_suffix = generate_email_suffix()
    base_email = EMAIL_ADDRESS.split('@')[0]
    email = f"{base_email}+{email_suffix}@gmail.com"
    
    captcha_token = captcha_solver.solve_captcha()
    if not captcha_token:
        Logger.log("Failed to solve captcha", Fore.RED)
        return None
    
    register_data = {
        "username": username,
        "email": email,
        "password": password,
        "referralCode": referral_code,
        "recaptchaToken": captcha_token
    }
    
    try:
        response = requests.post(
            'https://api3.blockpad.fun/api/auth/register',
            headers=headers,
            json=register_data,
            proxies=proxy,
        )
        
        response_json = response.json()
        
        if response_json.get('success') == True:
            Logger.log(f"Registration successful for {username}", Fore.GREEN)
        else:
            error_message = response_json.get('message', 'Unknown error')
            Logger.log(f"Registration failed: {error_message}", Fore.RED)
            return None
            
    except Exception as e:
        Logger.log(f"Error during registration: {e}", Fore.RED)
        Logger.log("Will still check for verification code...", Fore.YELLOW)
    
    Logger.log("Waiting for verification code...", Fore.YELLOW)
    verification_code = gmail_handler.get_verification_code(specific_email=email)
    
    if verification_code:
        Logger.log(f"Verification code received: {verification_code}", Fore.GREEN)
        
        token = try_verify_email(headers, verification_code, email, proxy, gmail_handler)
        
        if token:
            Logger.log(f"Email verification successful for {username}", Fore.GREEN)
            save_account(username, password, email, token)
            Logger.log("Registration successful! Account Details:", Fore.GREEN)
            Logger.log(f"Email: {email}", Fore.MAGENTA)
            Logger.log(f"Password: {password}", Fore.MAGENTA)
            Logger.log(f"Username: {username}", Fore.MAGENTA)
            Logger.log(f"Token: {token}\n", Fore.MAGENTA)
            return username, password, email, token
        else:
            Logger.log("Verification failed", Fore.RED)
    else:
        Logger.log("Failed to get verification code", Fore.RED)
    
    return None

def main():
    load_dotenv()
    print_banner()
    
    global EMAIL_ADDRESS
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    PASSWORD = os.getenv("PASSWORD")
    CAPTCHA_KEY = os.getenv("2CAPTCHA_KEY")
    
    if not all([EMAIL_ADDRESS, PASSWORD, CAPTCHA_KEY]):
        Logger.log("Please set EMAIL_ADDRESS, PASSWORD, and 2CAPTCHA_KEY in .env file", Fore.RED)
        return
    
    gmail_handler = GmailIMAP(EMAIL_ADDRESS, PASSWORD)
    proxy_manager = ProxyManager()
    captcha_solver = CaptchaSolver(CAPTCHA_KEY)
    
    if not proxy_manager.proxies:
        Logger.log("No proxies found in proxies.txt", Fore.RED)
        return
    
    referral_code = input(f"{Fore.YELLOW}Enter referral code: {Style.RESET_ALL}")
    print("\n")
    
    while True:
        try:
            Logger.account_number += 1
            Logger.log("Processing new account", Fore.CYAN)
            result = register_account(referral_code, gmail_handler, proxy_manager, captcha_solver)
            
            if result:
                username, password, email, token = result
            else:
                Logger.log("Registration failed", Fore.RED)
            
        except KeyboardInterrupt:
            Logger.log("Script stopped by user", Fore.YELLOW)
            break
        except Exception as e:
            Logger.log(f"Unexpected error: {e}", Fore.RED)

if __name__ == "__main__":
    main()
