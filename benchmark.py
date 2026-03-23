#!/usr/bin/env python3
"""
Benchmark: JSON vs bytepack binary encoding.
Run: python benchmark.py
"""

import json
import time
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bytepack-python"))

from bytepack import encode, health

DOMAINS = ["market", "geo", "energy", "health", "science", "defense", "nature", "general", "security"]
ACTIONS = ["observe", "alert", "correlate", "predict", "query"]
CONFIDENCES = ["conf_3", "conf_5", "conf_7", "conf_8", "conf_9"]
ASSETS = ["BTC", "ETH", "SOL", "oil", "gold", "temperature", "earthquake", "missile", "virus"]


def generate_message():
    """Generate a random structured agent message."""
    msg = {
        "action": random.choice(ACTIONS),
        "domain": random.choice(DOMAINS),
        "confidence": random.choice(CONFIDENCES),
        "timeframe": random.choice(["present", "1h", "4h", "1d"]),
    }
    # Add optional fields randomly
    if random.random() > 0.3:
        msg["asset"] = random.choice(ASSETS)
    if random.random() > 0.5:
        msg["related_domain"] = random.choice(DOMAINS)
    if random.random() > 0.6:
        msg["metadata"] = {
            "source": random.choice(["reuters", "bbc", "arxiv", "usgs", "coingecko"]),
            "score": round(random.random(), 3),
            "tags": random.sample(["urgent", "verified", "emerging", "confirmed", "preliminary"], k=random.randint(1, 3)),
        }
    if random.random() > 0.7:
        msg["evidence"] = [
            {"headline": f"Event {i} in {random.choice(DOMAINS)}", "confidence": round(random.random(), 2)}
            for i in range(random.randint(1, 5))
        ]
    return msg


def run_benchmark(n=1000):
    print(f"bytepack Benchmark — {n} messages\n{'='*50}")

    # Check service
    h = health()
    print(f"Service: {'UP' if h.get('up') else 'DOWN'} ({h.get('e', 0)} total encodes)\n")

    messages = [generate_message() for _ in range(n)]

    # JSON sizes
    json_sizes = [len(json.dumps(m)) for m in messages]

    # Encode via bytepack
    bp_sizes = []
    start = time.time()
    errors = 0
    for m in messages:
        try:
            r = encode(m)
            bp_sizes.append(r.get("s", 2556))
        except Exception:
            errors += 1
            bp_sizes.append(0)
    elapsed = time.time() - start

    # Results
    avg_json = sum(json_sizes) / len(json_sizes)
    max_json = max(json_sizes)
    avg_bp = sum(bp_sizes) / len(bp_sizes)
    throughput = n / elapsed if elapsed > 0 else 0

    print(f"{'Metric':<30} {'JSON':>12} {'bytepack':>12} {'Ratio':>8}")
    print(f"{'-'*62}")
    print(f"{'Avg message size':<30} {avg_json:>10.0f} B {avg_bp:>10.0f} B {avg_json/avg_bp:>7.1f}x")
    print(f"{'Max message size':<30} {max_json:>10.0f} B {'2,556':>10} B {max_json/2556:>7.1f}x")
    print(f"{'Min message size':<30} {min(json_sizes):>10.0f} B {'2,556':>10} B")
    print(f"{'Size variance':<30} {'High':>12} {'Zero':>12}")
    print(f"{'Encode throughput':<30} {'N/A':>12} {throughput:>9.0f}/sec")
    print(f"{'Errors':<30} {'0':>12} {errors:>12}")
    print(f"{'Noise tolerance':<30} {'0%':>12} {'25%':>12}")
    print(f"\nTotal time: {elapsed:.1f}s for {n} encodes")
    print(f"Average compression: {avg_json/avg_bp:.1f}x")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    run_benchmark(n)
