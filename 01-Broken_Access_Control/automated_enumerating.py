import csv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time

# ---- Configuration ----
## This is where you set the parameters for the enumeration. (This is only a template, you can change it as you like)
URL_PATTERN = "http://127.0.0.1:5000/api/items/{}"      # URL with placeholder (the placeholder is what is going to be changed (such as ID))
METHOD      = "GET"                                     # HTTP method (you can use GET, POST, PUT, DELETE, etc.)
START_ID    = 1                                         # first ID to try
END_ID      = 20                                        # last ID to try
CONCURRENCY = 10                                        # number of threads
HEADERS     = {                                         # any default headers in a `key: value` format
    # "Authorization": "Bearer YOUR_TOKEN_HERE",
    # "Accept": "application/json",
}
OUTPUT_CSV = "results.csv"                              # where to save results, null or empty string to disable saving
TIMEOUT    = 5.0                                        # request timeout (seconds)
REQUEST_INTERVAL = 0                                    # delay between each request (seconds)
VERBOSE    = False                                      # True → DEBUG logs, False → INFO
SAVE_RESPONSE_BODY = False                              # True → save response body to CSV, False → only status code
# ---- xxxxxxxxxxxxx ----



def make_session():
    """
    This method creates a requests session with the specified headers.

    :return: requests.Session object
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def probe(session, url):
    """
    This method sends a request to the specified URL and returns the status code and response body.

    :param session: requests.Session object
    :param url: URL to send the request to

    :return: tuple (status_code, response_body)
    """

    if REQUEST_INTERVAL > 0:
        time.sleep(REQUEST_INTERVAL)

    try:
        # Execute the request
        resp = session.request(METHOD, url, timeout=TIMEOUT)
        if SAVE_RESPONSE_BODY:
            # Sanitize the CSV fields if the body is to be saved
            body = resp.text
            body = body.replace('\r\n', '\\n').replace('\n', '\\n')
            return resp.status_code, body
        return resp.status_code, None
    except requests.RequestException as e:
        logging.debug(f"Error requesting {url}: {e}")
        return None, None


def worker(session, ident):
    """
    This method is the worker function for each thread. It sends a request to the specified URL and returns the status code and response body.

    :param session: requests.Session object
    :param ident: ID to be used in the URL

    :return: tuple (id, status_code, response_body)
    """

    url = URL_PATTERN.format(ident)
    status, body = probe(session, url)
    logging.info(f"{ident}: {status or 'ERR'} → {url}")
    return ident, status, body


def main():
    # Define logging for console output based on verbose setting
    level = logging.DEBUG if VERBOSE else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S"
    )

    session = make_session()
    ids = range(START_ID, END_ID + 1)
    results = []

    # Create a ThreadPoolExecutor to manage concurrent requests
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {pool.submit(worker, session, i): i for i in ids}
        for fut in as_completed(futures):
            ident, status, body = fut.result()
            results.append((ident, status, body))

    # Write results to CSV if OUTPUT_CSV is set
    if OUTPUT_CSV and OUTPUT_CSV.strip():
        with open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(
                f,
                quoting=csv.QUOTE_ALL
            )
            header = ["id", "status"]
            if SAVE_RESPONSE_BODY:
                header.append("body")
            writer.writerow(header)
            for ident, status, body in sorted(results):
                row = [ident, status]
                if SAVE_RESPONSE_BODY:
                    row.append(body)
                writer.writerow(row)

        logging.info(f"Done! Results saved to {OUTPUT_CSV}")
    else:
        logging.info("Done! No results saved.")

if __name__ == "__main__":
    main()
