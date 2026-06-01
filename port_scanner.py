#!/usr/bin/env python3
"""
Intermediate-level Python Port Scanner
Educational project for portfolio use only.
Scan only systems you own or have explicit permission to test.
"""

import socket
import threading
import time
from datetime import datetime
from colorama import init, Fore, Style
import sys

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Global variables
open_ports = []
lock = threading.Lock()
total_scanned = 0

def print_banner():
    """Display a professional banner"""
    print(Fore.CYAN + Style.BRIGHT + """
    ===============================================
           PYTHON PORT SCANNER (Educational)
    ===============================================
    """ + Style.RESET_ALL)

def resolve_target(target):
    """Resolve domain name to IP if needed"""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(Fore.RED + f"[-] Error: Could not resolve hostname '{target}'")
        sys.exit(1)

def scan_port(target_ip, port):
    """Scan a single port"""
    global total_scanned
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1.0)  # 1 second timeout
            result = sock.connect_ex((target_ip, port))
            
            with lock:
                total_scanned += 1
                if result == 0:
                    open_ports.append(port)
                    print(Fore.GREEN + f"[+] Port {port} is OPEN")
                else:
                    # Optional: Show closed ports (uncomment for verbose mode)
                    # print(Fore.YELLOW + f"[-] Port {port} is CLOSED")
                    pass
    except socket.timeout:
        with lock:
            total_scanned += 1
    except Exception as e:
        with lock:
            total_scanned += 1
            print(Fore.RED + f"[-] Error scanning port {port}: {e}")

def scan_range(target_ip, start_port, end_port, threads=100):
    """Scan a range of ports using multithreading"""
    global open_ports, total_scanned
    open_ports = []
    total_scanned = 0
    
    print(Fore.BLUE + f"[*] Starting scan on {target_ip} from port {start_port} to {end_port}")
    print(Fore.BLUE + f"[*] Using {threads} threads...\n")
    
    start_time = time.time()
    
    # Create threads
    thread_list = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target_ip, port))
        thread_list.append(thread)
        thread.start()
        
        # Limit concurrent threads
        if len(thread_list) >= threads:
            for t in thread_list:
                t.join()
            thread_list = []
    
    # Join any remaining threads
    for t in thread_list:
        t.join()
    
    end_time = time.time()
    duration = end_time - start_time
    
    return duration

def print_summary(target, start_port, end_port, duration):
    """Print professional scan summary"""
    total_ports = end_port - start_port + 1
    
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*60)
    print(" " * 20 + "SCAN SUMMARY")
    print("="*60 + Style.RESET_ALL)
    
    print(Fore.WHITE + f"Target          : {target}")
    print(Fore.WHITE + f"Port Range      : {start_port}-{end_port}")
    print(Fore.WHITE + f"Total Ports     : {total_ports}")
    print(Fore.WHITE + f"Ports Scanned   : {total_scanned}")
    print(Fore.GREEN + f"Open Ports      : {len(open_ports)}")
    print(Fore.WHITE + f"Duration        : {duration:.2f} seconds")
    
    if open_ports:
        print(Fore.GREEN + "\nOpen Ports:")
        for port in sorted(open_ports):
            service = socket.getservbyport(port) if port < 1024 else "unknown"
            print(Fore.GREEN + f"   • Port {port:<6} ({service})")
    else:
        print(Fore.YELLOW + "\nNo open ports found in the scanned range.")
    
    print(Fore.CYAN + "\n⚠️  Remember: Use this tool ethically and legally!")

def main():
    """Main function with user input"""
    print_banner()
    
    try:
        # Get target
        target = input(Fore.WHITE + "Enter target IP or domain: ").strip()
        if not target:
            print(Fore.RED + "[-] Target cannot be empty!")
            return
        
        target_ip = resolve_target(target)
        print(Fore.GREEN + f"[+] Target resolved to: {target_ip}")
        
        # Get port range
        port_range = input(Fore.WHITE + "Enter port range (e.g., 1-1000): ").strip()
        try:
            start_port, end_port = map(int, port_range.split('-'))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError
        except:
            print(Fore.RED + "[-] Invalid port range! Using default 1-500")
            start_port, end_port = 1, 500
        
        # Start scan
        duration = scan_range(target_ip, start_port, end_port, threads=150)
        
        # Show summary
        print_summary(target, start_port, end_port, duration)
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Scan interrupted by user.")
    except Exception as e:
        print(Fore.RED + f"\n[-] Unexpected error: {e}")

if __name__ == "__main__":
    main()