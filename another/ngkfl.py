"""
╔══════════════════════════════════════════════╗
║       WiFi Profile Viewer — Windows          ║
║  Shows YOUR saved network passwords via      ║
║  Windows netsh (no third-party deps needed)  ║
╚══════════════════════════════════════════════╝
"""

import subprocess
import re
import os
import sys
import json
import datetime

# ── Colour / style helpers ────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
ITALIC  = "\033[3m"

# Foreground colours
BLACK   = "\033[30m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"

# Background colours
BG_DARK  = "\033[48;5;234m"
BG_PANEL = "\033[48;5;236m"

def enable_ansi():
    """Enable ANSI codes on Windows 10+ terminals."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
        except Exception:
            pass

def c(text, *codes):
    return "".join(codes) + str(text) + RESET

def box_line(width=62):
    return c("─" * width, DIM, CYAN)

def header_box(title, subtitle="", width=62):
    pad = width - 2
    lines = [
        c("╔" + "═" * pad + "╗", CYAN, BOLD),
        c("║" + title.center(pad) + "║", CYAN, BOLD),
    ]
    if subtitle:
        lines.append(c("║" + c(subtitle.center(pad), DIM, WHITE) + c("║", CYAN, BOLD), CYAN, BOLD))
    lines.append(c("╚" + "═" * pad + "╝", CYAN, BOLD))
    return "\n".join(lines)

def section_header(label, icon="▸"):
    return f"\n{c(icon, CYAN, BOLD)} {c(label, YELLOW, BOLD)}\n{box_line()}"

def signal_bar(pct_str):
    """Convert '80%' → coloured bar ████░░░░"""
    try:
        pct = int(pct_str.replace("%", ""))
    except Exception:
        return c("N/A", DIM)
    filled = round(pct / 10)
    bar = "█" * filled + "░" * (10 - filled)
    colour = GREEN if pct >= 70 else YELLOW if pct >= 40 else RED
    return c(bar, colour) + c(f" {pct}%", colour, BOLD)

def lock_icon(auth):
    auth_l = auth.lower()
    if "open" in auth_l or auth_l in ("", "none"):
        return c("🔓 Open", YELLOW)
    elif "wpa3" in auth_l:
        return c("🔒 WPA3", GREEN, BOLD)
    elif "wpa2" in auth_l:
        return c("🔒 WPA2", GREEN)
    elif "wpa" in auth_l:
        return c("🔒 WPA", CYAN)
    elif "wep" in auth_l:
        return c("⚠  WEP", RED)
    else:
        return c(f"🔒 {auth}", WHITE)

# ── Core Windows netsh functions ──────────────────────────────────────────────

def run(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return out.decode("utf-8", errors="ignore")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8", errors="ignore")

def get_visible_networks():
    raw = run("netsh wlan show networks mode=Bssid")
    ssids   = re.findall(r"SSID\s+\d+\s*:\s*(.*)", raw)
    signals = re.findall(r"Signal\s*:\s*(\d+%)", raw)
    auths   = re.findall(r"Authentication\s*:\s*(.+)", raw)
    bssids  = re.findall(r"BSSID \d+\s*:\s*(.+)", raw)
    channels= re.findall(r"Channel\s*:\s*(\d+)", raw)

    nets = []
    for i, ssid in enumerate(ssids):
        ssid = ssid.strip() or "[Hidden Network]"
        nets.append({
            "ssid":    ssid,
            "signal":  signals[i]  if i < len(signals)  else "N/A",
            "auth":    auths[i].strip()   if i < len(auths)    else "Unknown",
            "bssid":   bssids[i].strip()  if i < len(bssids)   else "N/A",
            "channel": channels[i] if i < len(channels) else "N/A",
        })
    return nets

def get_stored_profiles():
    raw = run("netsh wlan show profiles")
    names = re.findall(r"All User Profile\s*:\s*(.+)", raw)
    profiles = {}
    for name in names:
        name = name.strip()
        detail = run(f'netsh wlan show profile name="{name}" key=clear')
        pw_match   = re.search(r"Key Content\s*:\s*(.+)", detail)
        auth_match = re.search(r"Authentication\s*:\s*(.+)", detail)
        profiles[name] = {
            "password": pw_match.group(1).strip()   if pw_match   else None,
            "auth":     auth_match.group(1).strip() if auth_match else "Unknown",
        }
    return profiles

def get_adapter_info():
    raw = run("netsh wlan show interfaces")
    info = {}
    for key, pattern in [
        ("name",    r"Name\s*:\s*(.+)"),
        ("state",   r"State\s*:\s*(.+)"),
        ("ssid",    r"SSID\s*:\s*(.+)"),
        ("bssid",   r"BSSID\s*:\s*(.+)"),
        ("signal",  r"Signal\s*:\s*(.+)"),
        ("rx",      r"Receive rate.*?:\s*(.+)"),
        ("tx",      r"Transmit rate.*?:\s*(.+)"),
        ("channel", r"Channel\s*:\s*(.+)"),
        ("radio",   r"Radio type\s*:\s*(.+)"),
    ]:
        m = re.search(pattern, raw, re.IGNORECASE)
        info[key] = m.group(1).strip() if m else "N/A"
    return info

# ── Display helpers ───────────────────────────────────────────────────────────

def print_adapter(info):
    print(section_header("ADAPTER STATUS", "📡"))
    rows = [
        ("Adapter",  info["name"]),
        ("State",    c(info["state"].upper(), GREEN if "connected" in info["state"].lower() else YELLOW, BOLD)),
        ("Connected SSID",  info["ssid"]),
        ("BSSID",    c(info["bssid"], DIM)),
        ("Signal",   signal_bar(info["signal"])),
        ("Channel",  info["channel"]),
        ("Radio",    info["radio"]),
        ("RX Rate",  c(info["rx"] + " Mbps", CYAN) if info["rx"] != "N/A" else "N/A"),
        ("TX Rate",  c(info["tx"] + " Mbps", CYAN) if info["tx"] != "N/A" else "N/A"),
    ]
    for label, val in rows:
        print(f"  {c(label + ':', DIM):<30} {val}")

def print_visible(nets, stored):
    print(section_header(f"VISIBLE NETWORKS  ({len(nets)} found)", "📶"))
    if not nets:
        print(c("  No networks detected. Check your Wi-Fi adapter.", RED))
        return

    for idx, net in enumerate(nets, 1):
        ssid = net["ssid"]
        pw_data = stored.get(ssid)
        has_pw  = pw_data and pw_data["password"]

        badge = c(" ✔ SAVED ", BG_PANEL, GREEN, BOLD) if pw_data else c(" ● NEW  ", BG_PANEL, YELLOW, BOLD)

        print(f"\n  {c(str(idx).zfill(2), DIM, CYAN)}  {c(ssid, WHITE, BOLD)}  {badge}")
        print(f"      {'Signal:':<12} {signal_bar(net['signal'])}")
        print(f"      {'Security:':<12} {lock_icon(net['auth'])}")
        print(f"      {'BSSID:':<12} {c(net['bssid'], DIM)}")
        print(f"      {'Channel:':<12} {c(net['channel'], DIM)}")

        if has_pw:
            pw = pw_data["password"]
            print(f"      {'Password:':<12} {c(pw, CYAN, BOLD)}")
        elif pw_data and not pw_data["password"]:
            print(f"      {'Password:':<12} {c('(none / open network)', DIM)}")
        else:
            print(f"      {'Password:':<12} {c('Not saved on this device', DIM)}")

    print(f"\n  {box_line(58)}")

def print_all_stored(stored, visible_ssids):
    not_visible = {k: v for k, v in stored.items() if k not in visible_ssids}
    print(section_header(f"ALL SAVED PROFILES  ({len(stored)} total)", "🗂 "))

    categories = {
        "Currently Visible":    {k: v for k, v in stored.items() if k in visible_ssids},
        "Saved (Not in Range)": not_visible,
    }

    for cat, items in categories.items():
        if not items:
            continue
        print(f"\n  {c('▪ ' + cat, MAGENTA, BOLD)}")
        for ssid, data in items.items():
            pw = data["password"]
            pw_display = c(pw, CYAN, BOLD) if pw else c("(open / no key)", DIM)
            print(f"    {c('◦', DIM)} {c(ssid, WHITE):<40} {pw_display}")
            print(f"       {c('Security:', DIM)} {lock_icon(data['auth'])}")

def export_results(visible, stored):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wifi_export_{ts}.json"

    data = {
        "exported_at": datetime.datetime.now().isoformat(),
        "visible_networks": [],
        "all_stored_profiles": [],
    }

    visible_ssids = {n["ssid"] for n in visible}

    for net in visible:
        ssid = net["ssid"]
        entry = {**net}
        if ssid in stored:
            entry["password"] = stored[ssid]["password"]
        else:
            entry["password"] = None
        data["visible_networks"].append(entry)

    for ssid, info in stored.items():
        data["all_stored_profiles"].append({
            "ssid": ssid,
            "password": info["password"],
            "auth": info["auth"],
            "currently_visible": ssid in visible_ssids,
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename

def export_txt(visible, stored):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wifi_export_{ts}.txt"
    lines = [
        "WiFi Profile Export",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "VISIBLE NETWORKS:",
    ]
    for net in visible:
        ssid = net["ssid"]
        pw = stored.get(ssid, {}).get("password") or "Not saved"
        lines.append(f"  SSID:     {ssid}")
        lines.append(f"  Password: {pw}")
        lines.append(f"  Signal:   {net['signal']}")
        lines.append(f"  Security: {net['auth']}")
        lines.append("-" * 40)
    lines += ["", "ALL STORED PROFILES:"]
    for ssid, data in stored.items():
        lines.append(f"  SSID:     {ssid}")
        lines.append(f"  Password: {data['password'] or '(none)'}")
        lines.append(f"  Security: {data['auth']}")
        lines.append("-" * 40)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filename

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    enable_ansi()
    os.system("cls" if os.name == "nt" else "clear")

    now = datetime.datetime.now().strftime("%A, %d %B %Y  %H:%M:%S")
    print(header_box(
        "  📶  WiFi Profile Viewer  ",
        now,
    ))

    # ── Adapter info ──
    print(c("\n  Gathering adapter info…", DIM))
    adapter = get_adapter_info()
    print_adapter(adapter)

    # ── Visible networks ──
    print(c("\n  Scanning visible networks…", DIM))
    visible = get_visible_networks()

    # ── Stored profiles ──
    print(c("  Reading saved profiles…", DIM))
    stored = get_stored_profiles()

    visible_ssids = {n["ssid"] for n in visible}

    # ── Print sections ──
    print_visible(visible, stored)
    print_all_stored(stored, visible_ssids)

    # ── Summary ──
    print(section_header("SUMMARY", "📊"))
    matched = sum(1 for n in visible if n["ssid"] in stored)
    print(f"  {c('Visible networks:', DIM):<30} {c(len(visible), CYAN, BOLD)}")
    print(f"  {c('Saved profiles:', DIM):<30} {c(len(stored), CYAN, BOLD)}")
    print(f"  {c('Visible + password known:', DIM):<30} {c(matched, GREEN, BOLD)}")
    print(f"  {c('Visible + not saved:', DIM):<30} {c(len(visible) - matched, YELLOW, BOLD)}")

    # ── Export prompt ──
    print(f"\n{box_line()}")
    print(c("  Export options:", BOLD))
    print(f"    {c('[1]', CYAN)} Save as JSON")
    print(f"    {c('[2]', CYAN)} Save as TXT")
    print(f"    {c('[3]', CYAN)} Both")
    print(f"    {c('[Enter]', DIM)} Skip")

    choice = input(f"\n  {c('Choose:', YELLOW, BOLD)} ").strip()
    if choice in ("1", "3"):
        fn = export_results(visible, stored)
        print(c(f"  ✔ JSON saved → {fn}", GREEN))
    if choice in ("2", "3"):
        fn = export_txt(visible, stored)
        print(c(f"  ✔ TXT  saved → {fn}", GREEN))

    print(f"\n{box_line()}")
    print(c("  Done. Press Enter to exit.", DIM))
    input()

if __name__ == "__main__":
    if sys.platform != "win32":
        print("⚠  This tool uses Windows netsh and only runs on Windows.")
        sys.exit(1)
    main()