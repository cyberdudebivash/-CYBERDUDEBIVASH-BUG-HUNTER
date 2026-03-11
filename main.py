import argparse
import asyncio
import time
from pathlib import Path

from recon_pipeline import ReconPipeline


BANNER = """
==============================================================
 CYBERDUDEBIVASH BUG HUNTER — AI Recon Platform
==============================================================
 Asset Discovery | Subdomain Recon | Tech Fingerprinting
==============================================================
"""


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--domain", required=True)
    parser.add_argument("-w", "--wordlist", required=True)
    parser.add_argument("-c", "--concurrency", type=int, default=100)

    return parser.parse_args()


def validate_inputs(domain, wordlist):

    if not domain:
        raise SystemExit("[ERROR] Domain required")

    if not Path(wordlist).exists():
        raise SystemExit(f"[ERROR] Wordlist not found: {wordlist}")


async def run_pipeline(args):

    pipeline = ReconPipeline(
        domain=args.domain,
        wordlist=args.wordlist,
        concurrency=args.concurrency
    )

    await pipeline.run()


def main():

    print(BANNER)

    args = parse_args()

    validate_inputs(args.domain, args.wordlist)

    start = time.time()

    try:

        asyncio.run(run_pipeline(args))

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted")

    except Exception as e:
        print(f"[FATAL] {e}")

    finally:

        duration = round(time.time() - start, 2)

        print(f"\nScan completed in {duration}s")


if __name__ == "__main__":
    main()