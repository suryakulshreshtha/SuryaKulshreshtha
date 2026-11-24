#!/usr/bin/env python3
"""
gold_rate.py — Live gold rate calculator for India (INR), with international
comparison for any other currency.

================================================================================
OVERVIEW
================================================================================
This script fetches the live international gold price and converts it into a
realistic Indian retail-equivalent rate — in Indian Rupees, using Indian
weight units (gram / 10 gram / tola / kg) and Indian karat purities
(24K / 22K / 18K), formatted with the Indian numbering system (lakh/crore
grouping, e.g. ₹1,27,593.00) — alongside the raw international wholesale
price for transparency and comparison.

Zero REQUIRED third-party dependencies: uses only the Python standard
library (urllib, json, ssl, datetime, zoneinfo-free fixed IST offset).
Nothing to pip install just to run this. `certifi` is used automatically
as an OPTIONAL fallback if already installed (see SETUP below).

================================================================================
DATA SOURCES (both free, no API key required, neither Chinese-operated)
================================================================================
  1. Gold spot/futures price in USD per troy ounce
     -> Yahoo Finance's public chart JSON endpoint:
        https://query1.finance.yahoo.com/v8/finance/chart/GC=F
        Ticker "GC=F" = COMEX gold futures (nearest contract), the standard
        live proxy for international gold spot price. Yahoo Finance is a
        U.S. (Yahoo/Apollo Global Management) service. The response includes
        the exchange's own "regularMarketTime" tick timestamp, which this
        script reports separately from the time the script itself ran.

  2. USD -> INR (or any other currency) exchange rate
     -> Frankfurter API: https://api.frankfurter.app/latest
        An open-source European project that republishes the official
        European Central Bank (ECB) daily reference rate. NOTE: the ECB
        publishes this rate once per business day (around 16:00 CET), so
        it is NOT a live tick — it can lag the live gold price by up to
        ~1 business day. The script reports the rate's own "date" field so
        you always know exactly which day's FX rate was used.

================================================================================
HOW THE INDIA-LANDED PRICE IS CALCULATED
================================================================================
"International (raw wholesale)" price = spot_usd_per_oz * fx_rate / 31.1034768
This is what a bullion dealer would pay on the international market, with
NO Indian taxes applied. It is NOT what you'll see quoted by an Indian
jeweller or bullion association.

"India-landed (retail-equivalent)" price layers on the two taxes that are
unavoidably embedded in every gram of gold sold in India, since India
imports nearly all the gold it consumes:

  1. Customs duty on imported gold:
       - Basic Customs Duty (BCD):      10%
       - Agriculture Infrastructure and Development Cess (AIDC): 5%
       - TOTAL EFFECTIVE CUSTOMS DUTY:  15%
     This rate took effect 13 May 2026 (Finance Ministry/CBIC customs
     notifications 15-18/2026-Customs), raised from the prior ~6% rate
     (5% BCD + 1% AIDC) that had been in place since the Union Budget
     2024-25 cut. Gold import duty has changed several times in recent
     years (cuts in 2021 and 2024, hikes in 2022 and 2026), so this is a
     policy-sensitive number — see VERIFICATION below.

  2. GST on the value of the gold itself: 3% (1.5% CGST + 1.5% SGST, or
     3% IGST on import). This has been stable at 3% since GST's
     introduction and was explicitly left unchanged in the GST 2.0 rate
     revision of 22 September 2025.
     (NOT included here: a separate 5% GST that applies only to jewellery
     MAKING CHARGES, which this script does not model since it computes
     a bare-metal rate, not a finished-jewellery invoice.)

  Combined landed-cost multiplier = (1 + duty%) × (1 + gst%)
                                   = 1.15 × 1.03 = 1.1845  (≈ +18.45%)

  This 18.45% uplift over the raw international price is what trade
  analysts (e.g. GTRI) cite as the effective import-tax load on gold
  entering India today. It approximates the wholesale/bullion-association
  rate. An actual jewellery showroom price will typically run a further
  5-15% above this for dealer margin and making charges, which is why an
  optional --local-premium-percent knob is provided (default 0%, since
  that margin varies by city, jeweller, and whether it's bar/coin vs
  ornament gold — set it yourself if you want to calibrate to a specific
  local source).

VERIFICATION / LAST CHECKED: 2026-11-24
  The 15% customs duty and 3% GST figures above were checked against
  multiple independent news/finance sources on 2026-11-24 (duty hike
  effective 13 May 2026; GST rate confirmed stable post 22 Sept 2025
  GST 2.0 revision). Indian gold import duty in particular has been
  revised multiple times within 2026 alone — DO NOT treat the defaults
  below as permanently correct. Before relying on this for an actual
  transaction, re-verify current rates at:
    - Customs duty: https://www.cbic.gov.in (official CBIC notifications)
    - GST on gold:  https://cbic-gst.gov.in (GST Council rate schedule)
  and update INDIA_CUSTOMS_DUTY_PERCENT / INDIA_GST_PERCENT below, or pass
  --duty-percent / --gst-percent on the command line to override without
  editing the file.

================================================================================
UNITS EXPLAINED
================================================================================
  ounce   = 1 troy ounce = 31.1034768 grams (the international standard
            unit gold is quoted in on exchanges like COMEX/LBMA)
  gram    = 1 gram
  10gram  = 10 grams (the most common retail quoting unit in India)
  tola    = 11.6638038 grams (a traditional South Asian unit; 1 tola =
            3/8 troy ounce exactly, still widely used in India/Pakistan)
  kg      = 1000 grams

KARAT PURITY (India commonly transacts in all three):
  24K = 999/1000 fine  (99.9% pure gold)  -> multiplier 0.999
  22K = 916/1000 fine  (91.6% pure gold)  -> multiplier 0.916  (standard
        for Indian jewellery/hallmarking, labelled "916 KDM/hallmark")
  18K = 750/1000 fine  (75.0% pure gold)  -> multiplier 0.750

================================================================================
INDIAN CURRENCY FORMATTING
================================================================================
Amounts in INR are printed using the Indian numbering system (lakh/crore
digit grouping — groups of 2 digits after the first group of 3 from the
right), e.g. 12700000 is shown as ₹1,27,00,000.00, not ₹12,700,000.00.
This is implemented locally (format_indian_number()) rather than relying
on the system locale module, so it works identically on any machine
regardless of installed locales.

================================================================================
SETUP
================================================================================
No installation is required to run this script — just `python3 gold_rate.py`.

If you get an SSL error like:
    [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
    unable to get local issuer certificate

...it means your Python interpreter can't find a trusted root-CA bundle to
verify the HTTPS connection (common on macOS, especially inside a
virtualenv/venv or a python.org-installed Python). Fix it with ONE of:

  1. (Recommended, one-time) Install the optional `certifi` package, which
     ships an up-to-date CA bundle. This script auto-detects and uses it
     if present:
         pip install certifi
     (in PyCharm: open the Terminal tab at the bottom, make sure your
     project's .venv is active — the prompt shows "(.venv)" — run the
     command above, then re-run this script)

  2. (macOS, python.org installer only — not needed for Homebrew or
     PyCharm-managed Python) Run the certificate-install script that ships
     with your Python.app, e.g.:
         "/Applications/Python 3.13/Install Certificates.command"
     (quote the path in your shell since it contains a space)

  3. (Alternative) Upgrade pip and reinstall certifi:
         pip install --upgrade pip certifi

This script needs no dependencies at all once your system/Python already
trusts standard public root CAs (most Linux, Windows, and many macOS
setups do by default) — `certifi` above is only a fallback for the
environments where that trust store isn't reachable.

================================================================================
USAGE
================================================================================
    python3 gold_rate.py
        Full India report: international + India-landed rates, for 24K/22K/18K,
        across gram/10gram/tola/kg, in INR with Indian digit grouping.

    python3 gold_rate.py --unit gram --karat 22
        Just the headline summary for 22K gold, per gram, in INR.

    python3 gold_rate.py --currency USD
        International-only report in US Dollars (no Indian duty/GST layer
        is applied for non-INR currencies).

    python3 gold_rate.py --duty-percent 15 --gst-percent 3 --local-premium-percent 5
        Override the India duty/GST assumptions, and add a 5% local
        dealer/making-charge premium on top, to calibrate against a
        specific jeweller's quoted rate.

    python3 gold_rate.py --no-india-charges
        Show only the raw international price in INR (no duty/GST), useful
        for comparing against the "international spot" figure financial
        news sites quote.

================================================================================
DISCLAIMER
================================================================================
This tool is for informational/educational purposes only. It is NOT
financial or investment advice, and the computed "India-landed" figure is
an approximation (it does not include jeweller margin, making charges, or
GST on making charges). Always verify against an authorized jeweller, bank,
or bullion dealer, and official government sources, before any transaction.
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

# ------------------------------------------------------------------------------
# SSL setup: verify certificates even on systems (common on macOS) where Python
# can't find the OS root-CA store. If the optional `certifi` package is
# installed, use its bundle; otherwise fall back to Python's own default.
# ------------------------------------------------------------------------------
try:
    import certifi
    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = ssl.create_default_context()

# ------------------------------------------------------------------------------
# Physical-unit constants
# ------------------------------------------------------------------------------
GRAMS_PER_TROY_OUNCE = 31.1034768  # exact, internationally standard

UNITS_IN_GRAMS = {
    "ounce": GRAMS_PER_TROY_OUNCE,   # troy ounce (international exchange standard)
    "gram": 1.0,
    "10gram": 10.0,                  # most common Indian retail quoting unit
    "tola": 11.6638038,              # traditional South Asian unit (3/8 troy oz)
    "kg": 1000.0,
}

# Preferred display order for the full India report
INDIA_REPORT_UNITS = ["gram", "10gram", "tola", "kg"]

# Karat purity -> fineness fraction (how much of the metal is actually gold)
KARAT_PURITY = {
    24: 0.999,   # 999/1000 fine — bars, coins, investment-grade
    22: 0.916,   # 916/1000 fine — standard Indian jewellery/hallmark gold
    18: 0.750,   # 750/1000 fine — lighter, more durable jewellery alloy
}
INDIA_REPORT_KARATS = [24, 22, 18]

# A few well-known currency -> common-unit presets, just for friendlier defaults
CURRENCY_DEFAULT_UNIT = {
    "INR": "10gram",
    "PKR": "tola",
    "USD": "ounce",
    "AED": "gram",
    "SAR": "gram",
}

# ------------------------------------------------------------------------------
# India-specific tax assumptions — SEE "VERIFICATION / LAST CHECKED" IN THE
# MODULE DOCSTRING ABOVE. These change periodically; override via CLI flags
# (--duty-percent / --gst-percent) rather than editing this file if you just
# need a one-off recalculation with different numbers.
# ------------------------------------------------------------------------------
INDIA_BASIC_CUSTOMS_DUTY_PERCENT = 10.0   # BCD, effective since 13 May 2026
INDIA_AIDC_PERCENT = 5.0                  # Agri Infra & Dev Cess, since 13 May 2026
INDIA_CUSTOMS_DUTY_PERCENT = INDIA_BASIC_CUSTOMS_DUTY_PERCENT + INDIA_AIDC_PERCENT  # 15.0
INDIA_GST_PERCENT = 3.0                   # on bare gold value, stable since GST 2.0 (22 Sep 2025)
INDIA_RATES_LAST_VERIFIED = "2026-11-24"

IST = timezone(timedelta(hours=5, minutes=30), name="IST")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


# ==============================================================================
# HTTP helper
# ==============================================================================
def _http_get_json(url: str, params: dict | None = None) -> dict:
    """Minimal standard-library HTTP GET that returns parsed JSON."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10, context=_SSL_CONTEXT) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} requesting {url}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        hint = ""
        if "CERTIFICATE_VERIFY_FAILED" in str(exc.reason):
            hint = (
                " (SSL certificate verification failed — run 'pip install certifi' "
                "and try again; on macOS with python.org Python you may also need to "
                "run its 'Install Certificates.command')"
            )
        raise RuntimeError(f"Network error requesting {url}: {exc.reason}{hint}") from exc
    return json.loads(raw)


# ==============================================================================
# Data fetch
# ==============================================================================
def get_gold_price_usd_per_ounce() -> tuple[float, datetime | None]:
    """Fetch the latest gold price in USD per troy ounce from Yahoo Finance's
    chart API, along with the exchange's own tick timestamp for that price
    (None if the API didn't provide one, in which case the caller should
    treat the script's own run time as the best available timestamp)."""
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
    payload = _http_get_json(url, {"interval": "1m", "range": "1d"})

    try:
        result = payload["chart"]["result"][0]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected response shape from Yahoo Finance: {payload}") from exc

    meta = result.get("meta", {})
    price = meta.get("regularMarketPrice")
    market_time_epoch = meta.get("regularMarketTime")

    if price is None:
        # Fall back to the last non-null close in the intraday series, and its
        # matching timestamp, if the live tick field isn't present (e.g. market
        # closed and Yahoo omitted regularMarketPrice).
        quote = result.get("indicators", {}).get("quote", [{}])[0]
        closes = quote.get("close", [])
        timestamps = result.get("timestamp", [])
        for close, ts in zip(reversed(closes), reversed(timestamps)):
            if close is not None:
                price = close
                market_time_epoch = market_time_epoch or ts
                break
        if price is None:
            raise RuntimeError("Could not find a usable gold price in Yahoo Finance response.")

    market_time = (
        datetime.fromtimestamp(market_time_epoch, tz=timezone.utc)
        if market_time_epoch is not None
        else None
    )
    return float(price), market_time


def get_usd_to_currency_rate(currency: str) -> tuple[float, str | None]:
    """Fetch the latest USD -> `currency` exchange rate from the Frankfurter
    API (ECB reference rates), along with the date that rate was published
    for (Frankfurter's own "date" field)."""
    if currency.upper() == "USD":
        return 1.0, None
    payload = _http_get_json("https://api.frankfurter.app/latest", {"from": "USD", "to": currency.upper()})
    rate = payload.get("rates", {}).get(currency.upper())
    if rate is None:
        raise ValueError(
            f"Currency '{currency}' not found/supported by the exchange-rate API. "
            f"Try a standard 3-letter ISO code, e.g. INR, PKR, AED, GBP, EUR."
        )
    return float(rate), payload.get("date")


# ==============================================================================
# Formatting helpers
# ==============================================================================
def format_indian_number(value: float, decimals: int = 2) -> str:
    """Format a number using the Indian numbering system (lakh/crore digit
    grouping): the last 3 digits form one group, then every 2 digits moving
    left form a group, e.g. 12345678.9 -> '1,23,45,678.90'."""
    negative = value < 0
    value = abs(value)
    s = f"{value:.{decimals}f}"
    int_str, _, frac_str = s.partition(".")

    if len(int_str) <= 3:
        grouped = int_str
    else:
        last3 = int_str[-3:]
        rest = int_str[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        grouped = ",".join(parts) + "," + last3

    result = grouped + (f".{frac_str}" if decimals > 0 else "")
    return ("-" if negative else "") + result


def format_money(value: float, currency: str, decimals: int = 2) -> str:
    """Format a monetary amount, using Indian digit grouping + the ₹ symbol
    for INR, and plain Western grouping + the ISO code for everything else."""
    if currency.upper() == "INR":
        return f"₹{format_indian_number(value, decimals)}"
    return f"{value:,.{decimals}f} {currency.upper()}"


def fmt_dt(dt: datetime | None, tz: timezone, label: str) -> str:
    if dt is None:
        return f"{label}: unavailable"
    local = dt.astimezone(tz)
    return f"{label}: {local.strftime('%Y-%m-%d %H:%M:%S %Z')}"


# ==============================================================================
# Price calculations
# ==============================================================================
def international_price_per_gram(usd_per_ounce: float, fx_rate: float) -> float:
    """Raw international wholesale price per gram of pure (24K/999) gold, in
    the target currency, with NO Indian (or any other country's) import
    duty or taxes applied."""
    return (usd_per_ounce * fx_rate) / GRAMS_PER_TROY_OUNCE


def india_landed_price_per_gram(
    international_per_gram: float,
    duty_percent: float,
    gst_percent: float,
    local_premium_percent: float = 0.0,
) -> float:
    """India retail-equivalent price per gram of pure (24K/999) gold: the
    international price with customs duty, GST, and an optional extra local
    premium layered on top (see module docstring for the formula and its
    sources)."""
    multiplier = (1 + duty_percent / 100) * (1 + gst_percent / 100) * (1 + local_premium_percent / 100)
    return international_per_gram * multiplier


def price_for_karat_and_unit(price_per_gram_24k: float, karat: int, unit: str) -> float:
    purity = KARAT_PURITY[karat]
    grams_in_unit = UNITS_IN_GRAMS[unit]
    return price_per_gram_24k * purity * grams_in_unit


# ==============================================================================
# Report assembly
# ==============================================================================
def build_report(
    currency: str,
    unit: str,
    karat: int,
    duty_percent: float,
    gst_percent: float,
    local_premium_percent: float,
    apply_india_charges: bool,
) -> dict:
    run_time_utc = datetime.now(timezone.utc)

    usd_per_ounce, market_time_utc = get_gold_price_usd_per_ounce()
    fx_rate, fx_date = get_usd_to_currency_rate(currency)

    intl_per_gram_24k = international_price_per_gram(usd_per_ounce, fx_rate)

    india_per_gram_24k = None
    if apply_india_charges and currency.upper() == "INR":
        india_per_gram_24k = india_landed_price_per_gram(
            intl_per_gram_24k, duty_percent, gst_percent, local_premium_percent
        )

    return {
        "run_time_utc": run_time_utc,
        "market_time_utc": market_time_utc,
        "fx_date": fx_date,
        "currency": currency.upper(),
        "unit": unit,
        "karat": karat,
        "usd_per_ounce": usd_per_ounce,
        "fx_rate": fx_rate,
        "intl_per_gram_24k": intl_per_gram_24k,
        "india_per_gram_24k": india_per_gram_24k,
        "duty_percent": duty_percent,
        "gst_percent": gst_percent,
        "local_premium_percent": local_premium_percent,
    }


def print_timestamps(report: dict) -> None:
    print(fmt_dt(report["run_time_utc"], timezone.utc, "Script run (data retrieved) - UTC"))
    print(fmt_dt(report["run_time_utc"], IST, "Script run (data retrieved) - IST"))
    print(fmt_dt(report["market_time_utc"], timezone.utc, "Gold price exchange tick - UTC"))
    print(fmt_dt(report["market_time_utc"], IST, "Gold price exchange tick - IST"))
    fx_date = report["fx_date"] or ("n/a (USD requested)" if report["currency"] == "USD" else "unavailable")
    print(f"FX reference rate date (ECB/Frankfurter): {fx_date}")


def print_headline(report: dict) -> None:
    currency = report["currency"]
    unit = report["unit"]
    karat = report["karat"]

    print("=" * 72)
    print(f"GOLD RATE — {karat}K, per {unit}, in {currency}")
    print("=" * 72)
    print_timestamps(report)
    print("-" * 72)
    print(f"Spot price            : {report['usd_per_ounce']:,.2f} USD / troy ounce")
    if currency != "USD":
        print(f"USD -> {currency} rate      : {report['fx_rate']:.4f}")
    print("-" * 72)

    intl_value = price_for_karat_and_unit(report["intl_per_gram_24k"], karat, unit)
    print(f"International (raw, no duty/GST): {format_money(intl_value, currency)}")

    if report["india_per_gram_24k"] is not None:
        india_value = price_for_karat_and_unit(report["india_per_gram_24k"], karat, unit)
        print(
            f"India-landed (+{report['duty_percent']:g}% duty, +{report['gst_percent']:g}% GST"
            + (f", +{report['local_premium_percent']:g}% local premium" if report["local_premium_percent"] else "")
            + f"): {format_money(india_value, currency)}"
        )


def print_full_india_table(report: dict) -> None:
    # Column widths are sized generously (kg-unit values reach into crores,
    # e.g. "1,48,39,482.05" = 14 chars) and cells are always joined with an
    # explicit separator, so columns never run together regardless of how
    # wide an individual formatted number gets.
    UNIT_COL_WIDTH = 7
    VALUE_COL_WIDTH = 16
    SEP = "  "

    def cell(text: str, width: int = VALUE_COL_WIDTH) -> str:
        return f"{text:>{width}}"

    print()
    print("=" * 100)
    print("FULL INDIA REPORT — all karats x all units (INR)")
    print("=" * 100)

    header_cells = [f"{'Unit':<{UNIT_COL_WIDTH}}"]
    for k in INDIA_REPORT_KARATS:
        header_cells.append(cell(f"{k}K intl"))
        header_cells.append(cell(f"{k}K India"))
    print(SEP.join(header_cells))

    for unit in INDIA_REPORT_UNITS:
        row_cells = [f"{unit:<{UNIT_COL_WIDTH}}"]
        for karat in INDIA_REPORT_KARATS:
            intl_value = price_for_karat_and_unit(report["intl_per_gram_24k"], karat, unit)
            row_cells.append(cell(format_indian_number(intl_value)))
            if report["india_per_gram_24k"] is not None:
                india_value = price_for_karat_and_unit(report["india_per_gram_24k"], karat, unit)
                row_cells.append(cell(format_indian_number(india_value)))
            else:
                row_cells.append(cell("n/a"))
        print(SEP.join(row_cells))
    print("-" * 100)
    print(
        f"India-landed multiplier applied: duty {report['duty_percent']:g}% x "
        f"GST {report['gst_percent']:g}%"
        + (f" x local premium {report['local_premium_percent']:g}%" if report["local_premium_percent"] else "")
        + f" (see module docstring; assumptions last verified {INDIA_RATES_LAST_VERIFIED})"
    )
    print(
        "Note: India-landed figures approximate the wholesale/bullion-association rate. "
        "A jewellery showroom price will typically run further above this for dealer "
        "margin and making charges (not modelled here)."
    )


# ==============================================================================
# CLI
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Find the current gold rate, with an India-specific duty+GST landed-cost breakdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--currency", default="INR", help="3-letter ISO currency code, e.g. INR, USD, PKR, AED (default: INR)")
    parser.add_argument(
        "--unit",
        choices=list(UNITS_IN_GRAMS.keys()),
        default=None,
        help="Weight unit for the headline summary (default: sensible preset for the chosen currency, else 'gram')",
    )
    parser.add_argument("--karat", type=int, choices=sorted(KARAT_PURITY.keys()), default=24, help="Gold purity for the headline summary (default: 24)")
    parser.add_argument("--duty-percent", type=float, default=INDIA_CUSTOMS_DUTY_PERCENT, help=f"India customs duty %% to apply (BCD+AIDC; default: {INDIA_CUSTOMS_DUTY_PERCENT:g}, last verified {INDIA_RATES_LAST_VERIFIED})")
    parser.add_argument("--gst-percent", type=float, default=INDIA_GST_PERCENT, help=f"India GST %% on gold value to apply (default: {INDIA_GST_PERCENT:g}, last verified {INDIA_RATES_LAST_VERIFIED})")
    parser.add_argument("--local-premium-percent", type=float, default=0.0, help="Extra local dealer/market premium %% on top of duty+GST (default: 0)")
    parser.add_argument("--no-india-charges", action="store_true", help="Disable the India duty/GST layer; show only the raw international price")
    parser.add_argument("--no-full-table", action="store_true", help="Suppress the full karat x unit table (headline summary only)")
    args = parser.parse_args()

    currency = args.currency.upper()
    unit = args.unit or CURRENCY_DEFAULT_UNIT.get(currency, "gram")
    apply_india_charges = not args.no_india_charges

    try:
        report = build_report(
            currency=currency,
            unit=unit,
            karat=args.karat,
            duty_percent=args.duty_percent,
            gst_percent=args.gst_percent,
            local_premium_percent=args.local_premium_percent,
            apply_india_charges=apply_india_charges,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print_headline(report)

    if currency == "INR" and apply_india_charges and not args.no_full_table:
        print_full_india_table(report)

    print()
    print(
        "Disclaimer: informational/educational use only, not financial advice. "
        "India-landed figures are an approximation (no jeweller margin/making "
        "charges modelled). Verify with an authorized source before any transaction."
    )


if __name__ == "__main__":
    main()
