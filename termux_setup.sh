#!/bin/bash
# Setup script for PoliceDetector on Termux

echo "-------------------------------------------------------"
echo " PoliceDetector Termux Setup Script"
echo "-------------------------------------------------------"

echo "[*] Updating packages..."
pkg update && pkg upgrade -y

echo "[*] Installing system dependencies..."
pkg install -y python python-pip clang cmake ninja termux-api mpv

# Optional: if root is available, hcitool can be useful
pkg install -y bluez-utils

echo "[*] Installing Python libraries..."
pip install simplepyble || echo "Warning: simplepyble failed to install. Fallback scanning will be used."

echo "[*] Setting up permissions..."
echo "Please make sure you have:"
echo "1. Installed the 'Termux:API' app from F-Droid."
echo "2. Granted Location and Nearby Devices permissions to both Termux and Termux:API."
echo "3. If NOT rooted: Bluetooth scanning may be restricted by Android."
echo "4. If rooted: The script will use 'hcitool' via 'su' as a fallback."

echo "[*] Done. You can now run the detector with:"
echo "    python police.py"
echo "-------------------------------------------------------"
