import requests
import random
import time
import csv
from faker import Faker

fake = Faker()
REF_LINK = "https://app.flow3.tech/sale-nodes?ref=QAZbu9555"
API_REGISTER = "https://api.flow3.tech/api/auth/local/register"

def get_random_email():
    username = fake.user_name() + str(random.randint(1000,9999))
    return username, f"{username}@1secmail.com"

def load_proxies():
    with open("proxy.txt", "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def simpan_data(email, password, status):
    with open("akun.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([email, password, status])
    with open("akun.txt", "a") as f:
        f.write(f"{email} | {password} | {status}\n")

def create_session(proxy):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    })
    if proxy:
        session.proxies = {
            "http": proxy,
            "https": proxy
        }
    return session

def buat_akun(proxy=None):
    session = create_session(proxy)
    username, email = get_random_email()
    password = fake.password()

    try:
        res = session.get("https://app.flow3.tech/sale-nodes")
        if res.status_code != 200:
            print(f"[!] Gagal buka halaman utama ({res.status_code})")
            return False

        payload = {
            "email": email,
            "username": username,
            "password": password
        }

        resp = session.post(API_REGISTER, json=payload)
        if resp.status_code == 200:
            print(f"[+] Berhasil: {email}")
            simpan_data(email, password, "Sukses")
        else:
            print(f"[-] Gagal ({resp.status_code}): {email}")
            simpan_data(email, password, f"Gagal ({resp.status_code})")
        return True

    except Exception as e:
        print(f"[!] Error: {e}")
        simpan_data(email, password, "Error")
        return False

def main():
    jumlah = 50
    proxies = load_proxies()
    for i in range(jumlah):
        print(f"\n[+] Membuat akun ke-{i+1}")
        proxy = random.choice(proxies) if proxies else None
        buat_akun(proxy)
        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    main()
