#!/bin/bash
# Setup script for PoliceDetector on Termux

echo "-------------------------------------------------------"
echo " PoliceDetector Termux Setup Script"
echo "-------------------------------------------------------"

echo "[*] Updating packages..."
pkg update && pkg upgrade -y

echo "[*] Installing system dependencies..."
pkg install -y python termux-api mpv bluez-utils

echo "[*] Setting up permissions..."
echo "1. Install the 'Termux:API' app from F-Droid."
echo "2. Grant Location and Nearby Devices permissions to BOTH Termux and Termux:API in Android Settings."

echo ""
echo "[!] IMPORTANT: ROOT ACCESS REQUIRED"
echo "Due to Android's restrictions on Bluetooth scanning from Termux,"
echo "you MUST have a rooted device to run this utility effectively."
echo ""
echo "The script will use 'hcitool' via 'su' (root) to scan."
echo ""

echo "[*] Done. You can now run the detector with:"
echo "    su -c 'python police.py'"
echo "-------------------------------------------------------"
