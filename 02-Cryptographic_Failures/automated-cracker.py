import itertools
import hashlib
import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---- Configuration ----
## This is where you set the parameters for the hash‑cracker. (This is only a template; change as you like)
TARGET_HASH         = "a9993e364706816aba3e25717850c26c9cd0d89d"   # Hash to crack
ALGORITHM           = "sha1"                                       # Hash algorithm (md5, sha1, sha256, etc.)
SALT                = ""                                           # Optional salt prepended to plaintext
MODE                = "brute"                                    # "rainbow", "dict", or "brute"
RAINBOW_TABLE       = "rainbow_table.txt"                          # File with plaintext:hash entries
WORDLIST            = "rockyou.txt"                                # Path to wordlist file (one word per line)
MAX_LEN             = 5                                            # Max length for brute‑force
CHARSET             = "abcdefghijklmnopqrstuvwxyz0123456789"       # Characters to include in brute‑force
CONCURRENCY         = 4                                            # Number of threads for dict/brute modes
VERBOSE             = False                                        # True for DEBUG logs, False for INFO
# ---- xxxxxxxxxxxxx ----


def get_hasher(name):
    try:
        return getattr(hashlib, name)
    except AttributeError:
        logging.error("Unsupported hash algorithm: %s", name)
        sys.exit(1)

def rainbow_lookup(hash_value, table_path):
    if not os.path.isfile(table_path):
        logging.error("Rainbow table not found: %s", table_path)
        return None
    with open(table_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if ':' not in line:
                continue
            pwd, h = line.split(':', 1)
            if h.lower() == hash_value.lower():
                return pwd
    return None

def chunk_list(seq, n):
    """Split seq into n roughly equal chunks."""
    k, m = divmod(len(seq), n)
    return [seq[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]

def _dict_worker(passwords, hash_value, hasher, salt):
    target = hash_value.lower()
    for pwd in passwords:
        test = salt + pwd
        digest = hasher(test.encode()).hexdigest().lower()
        if digest == target:
            return pwd
    return None

def dictionary_attack_concurrent(hash_value, wordlist_path, hasher, salt, threads):
    if not os.path.isfile(wordlist_path):
        logging.error("Wordlist not found: %s", wordlist_path)
        return None

    # Load and clean passwords (drop empty/commented lines)
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [
            line.strip() for line in f
            if line.strip() and not line.lstrip().startswith(('#', '//'))
        ]

    chunks = chunk_list(passwords, min(threads, len(passwords)))
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(_dict_worker, chunk, hash_value, hasher, salt): chunk
            for chunk in chunks
        }
        for fut in as_completed(futures):
            result = fut.result()
            if result:
                # cancel remaining tasks
                for other in futures:
                    other.cancel()
                logging.debug("Password found in chunk: %s", result)
                return result
    return None

def brute_chunk_attack(hash_value, max_len, charset_subset, full_charset, hasher, salt):
    target = hash_value.lower()
    # length 1
    for ch in charset_subset:
        test = salt + ch
        if hasher(test.encode()).hexdigest().lower() == target:
            return ch
    # lengths 2..max_len
    for length in range(2, max_len + 1):
        for first in charset_subset:
            for tail in itertools.product(full_charset, repeat=length-1):
                pwd = first + ''.join(tail)
                test = salt + pwd
                if hasher(test.encode()).hexdigest().lower() == target:
                    return pwd
    return None

def brute_force_concurrent(hash_value, max_len, charset, hasher, salt, threads):
    chars = list(charset)
    chunks = chunk_list(chars, min(threads, len(chars)))
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(brute_chunk_attack, hash_value, max_len, chunk, charset, hasher, salt): chunk
            for chunk in chunks
        }
        for fut in as_completed(futures):
            result = fut.result()
            if result:
                for other in futures:
                    other.cancel()
                logging.debug("Password found in brute-force chunk: %s", result)
                return result
    return None

def main():
    # configure logging
    level = logging.DEBUG if VERBOSE else logging.INFO
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)

    logging.info("Mode: %s", MODE)
    logging.info("Algorithm: %s", ALGORITHM.upper())
    if SALT:
        logging.info("Using salt: '%s'", SALT)

    hasher_fn = get_hasher(ALGORITHM)

    if MODE == "rainbow":
        result = rainbow_lookup(TARGET_HASH, RAINBOW_TABLE)
    elif MODE == "dict":
        result = dictionary_attack_concurrent(TARGET_HASH, WORDLIST, hasher_fn, SALT, CONCURRENCY)
    elif MODE == "brute":
        result = brute_force_concurrent(TARGET_HASH, MAX_LEN, CHARSET, hasher_fn, SALT, CONCURRENCY)
    else:
        logging.error("Unknown MODE: %s", MODE)
        sys.exit(1)

    if result:
        logging.info("Cracked! Plaintext = '%s'", result)
    else:
        logging.error("Failed to crack the hash with given settings.")

if __name__ == "__main__":
    main()