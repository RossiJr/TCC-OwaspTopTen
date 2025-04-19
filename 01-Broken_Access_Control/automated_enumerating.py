import csv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time
import json

# ---- Configuration ----
## This is where you set the parameters for the enumeration. (This is only a template, you can change it as you like)
URL_PATTERN         = "http://127.0.0.1:5000/api/items/{}"      # URL with placeholder (the placeholder is what is going to be changed (such as ID))
METHOD              = "GET"                                     # HTTP method (you can use GET, POST, PUT, DELETE, etc.)
MODE                = "idor"                                    # "idor" or "traversal" or "files"
START_ID            = 1                                         # first ID to try
END_ID              = 20                                        # last ID to try
PAYLOAD_FILE        = "payloads.txt"                            # file with traversal payloads (one per line)
SERVER_FILES        = [                                         # list of server files to check (for files mode)
    "robots.txt",
    "sitemap.xml",
    "favicon.ico",
    "ads.txt",
    "humans.txt",
    "crossdomain.xml",
    ".env",
    ".git/config",
]
CONCURRENCY         = 10                                        # number of threads
HEADERS             = {                                         # any default headers in a `key: value` format
    # "Authorization": "Bearer YOUR_TOKEN_HERE",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
REQUEST_BODY        = '{{"identifier": "{}"}}'                  # Template for body, e.g. '{{"id": "{}"}}'
OUTPUT_CSV          = "results.csv"                             # where to save results, null or empty string to disable saving
TIMEOUT             = 5.0                                       # request timeout (seconds)
REQUEST_INTERVAL    = 0                                         # delay between each request (seconds)
VERBOSE             = False                                     # True → DEBUG logs, False → INFO
SAVE_RESPONSE_BODY  = False                                     # True → save response body to CSV, False → only status code
# ---- xxxxxxxxxxxxx ----



def make_session():
    """
    This method creates a requests session with the specified headers.

    :return: requests.Session object
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def probe(session, payload):
    """
    This method sends a request to the specified URL and returns the status code and response body.

    :param session: requests.Session object
    :param payload: payload to be used (e.g., ID or traversal payload)

    :return: tuple (status_code, response_body)
    """
    url = URL_PATTERN.format(payload)

    if REQUEST_INTERVAL > 0:
        time.sleep(REQUEST_INTERVAL)
    
    req_args = {"timeout": TIMEOUT}

    # Insert body if method supports it
    if METHOD.upper() in ("POST", "PUT", "PATCH") and REQUEST_BODY:
        # Use positional formatting to insert payload
        body = REQUEST_BODY.format(payload)
        try:
            req_args["json"] = json.loads(body)
        except json.JSONDecodeError:
            # Fallback to raw data if JSON parsing fails
            req_args["data"] = body
    
    try:
        resp = session.request(METHOD, url, **req_args)
        if SAVE_RESPONSE_BODY:
            # Sanitize the CSV fields if the body is to be saved
            body = resp.text.replace('\r\n', '\n').replace('\n', '\n')
            return resp.status_code, body
        return resp.status_code, None
    except requests.RequestException as e:
        logging.debug(f"Error requesting {url}: {e}")
        return None, None


def worker(session, payload):
    """
    This method is the worker function for each thread. It sends a request to the specified URL and returns the status code and response body.

    :param session: requests.Session object
    :param payload: payload to be used (e.g., ID or traversal payload)

    :return: tuple (payload, status_code, response_body)
    """

    status, body = probe(session, payload)
    logging.info(f"{payload}: {status or 'ERR'} -> {URL_PATTERN.format(payload)}")
    return payload, status, body


def main():
    # Define logging for console output based on verbose setting
    level = logging.DEBUG if VERBOSE else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S"
    )

    session = make_session()

    # Build payload list
    if MODE.lower() == "idor":
        payloads = [str(i) for i in range(START_ID, END_ID + 1)]
    elif MODE.lower() == "traversal":
        payloads = []
        try:
            with open(PAYLOAD_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    payloads.append(line)
        except IOError as e:
            logging.error(f"Failed reading payload file {PAYLOAD_FILE}: {e}")
            return
    elif MODE.lower() == "files":
        payloads = SERVER_FILES
    else:
        logging.error("MODE must be 'idor', 'traversal', or 'files'")
        return

    results = {}

    # Create a ThreadPoolExecutor to manage concurrent requests
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {pool.submit(worker, session, p): p for p in payloads}
        for future in as_completed(futures):
            payload, status, body = future.result()
            results[payload] = (status, body)
    
    # Write results to CSV if OUTPUT_CSV is set
    if OUTPUT_CSV and OUTPUT_CSV.strip():
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            header = ["payload", "status"]
            if SAVE_RESPONSE_BODY:
                header.append("body")
            writer.writerow(header)
            for p in payloads:
                status, body = results.get(p, (None, None))
                row = [p, status]
                if SAVE_RESPONSE_BODY:
                    row.append(body)
                writer.writerow(row)
        logging.info(f"Done! Results saved to {OUTPUT_CSV}")
    else:
        logging.info("Done! No CSV output.")

if __name__ == "__main__":
    main()
