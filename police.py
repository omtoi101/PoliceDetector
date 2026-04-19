#coding:utf-8
#################################################################################################################
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################################################################
# Utility to detect Victoria Police officers within bluetooth signal range via their body worn camera.
#################################################################################################################
import time, threading, logging, os, sys, subprocess
from datetime import datetime

try:
    import simplepyble
except ImportError:
    simplepyble = None

def is_termux():
    return 'TERMUX_VERSION' in os.environ

def logo():
    print(
            '''
#################################################################################################################
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################################################################
# Utility to detect Police officers within bluetooth signal range via their body worn camera.
#################################################################################################################

                                                                                                         
 *#####:         .##:*##                   @@@@@: @@@@@@=#@@@@@@#-@@@@@@  @@@@@:@@@@@@@= @@@@@@ -@@@@@   
 #######-        .##:###                   @@@@@- @@@@@@=#@@@@@@#-@@@@@@ .@@@@@:@@@@@@@= @@@@@@ -@@@@@   
 ###::###  -==:  .##:-=-   ===     ===     @%  %@ @@        @@   -@=     @@        @@   %@    @#-@-  @@  
 ###  ### ###### .##:###  #####- .#####:   @%  %@ @@        @@   -@=     @@        @@   %@    @#-@=  @@  
 #######*-##. ##:.##:### *## ### ##+ :##   @%  %@ @@@@%     @@   -@@@@.  @@        @@   @%    @#-@@@@@
 ######* +##  ##*.##:### ###     #######.  @%  %@ @@@@*     @@   -@@@@   @@        @@   @%    @#-@@@@@.
 ###     =##  ##*.##:### ### :** ##+  .:   @%  %@ @@        @@   -@=     @@        @@   @%    @#-@-  @@
 ###      ###### .##:### -#####* =##*##*   @@--@# @@----.   @@   -@*---- *@----    @@   =@=--=@=-@-  @@  
 *##      .####. .##.*##  -###+   -###+    @@@@@: @@@@@@+   @@   -@@@@@@  @@@@@:   @@    @@@@@@ -@-  @@  
                                           =====. ======:   ==   .======  =====    =-    ====== .=.  ==  

"If He Was Going To Commit A Crime, Would He Have Invited The Number One Cop In Town? Now, Where Did I Put My Gun?
Oh Yeah, I Set It Down When I Got A Piece Of Cake!" - Clancy Wiggum

#################################################################################################################
# Open Sauce Software, tasty and free!
#################################################################################################################
                                            '''
        )

police_detected = 0

def GetBluetoothMacList():
    global count, police_detected
    found_addresses = []

    # On Termux, prioritize hcitool (requires root) because simplepyble often fails to build/run
    if is_termux():
        try:
            # Passive scan for 5 seconds
            cmd = "su -c 'hcitool lescan --passive --timeout=5' 2>/dev/null"
            output = subprocess.check_output(cmd, shell=True).decode()
            for line in output.split('\n'):
                parts = line.split()
                if len(parts) > 0:
                    found_addresses.append(parts[0].upper())
        except Exception as e:
            print(f" >>>> Termux fallback scan failed (Is your device rooted?): {e}")
            if simplepyble:
                print(" >>>> Attempting simplepyble as a secondary option...")

    # If not on Termux, or if Termux scan failed and simplepyble is available
    if not found_addresses and simplepyble:
        try:
            adapters = simplepyble.Adapter.get_adapters()
            if len(adapters) > 0:
                adapter = adapters[0]
                print(f" >>>> Using adapter: {adapter.identifier()} [{adapter.address()}]")
                adapter.scan_for(5000)
                peripherals = adapter.scan_get_results()
                found_addresses = [p.address().upper() for p in peripherals]
        except Exception as e:
            print(f" >>>> simplepyble scan failed: {e}")

    if not found_addresses and not is_termux():
         print(" >>>> No devices found. Check your Bluetooth adapter and permissions.")

    count = count + 1
    print(f" >>>> Scan Count: {count} ({datetime.now()})")

    police_in_this_scan = []
    # Deduplicate addresses from the current scan
    for addr in set(found_addresses):
        if "00:25:DF" in addr: # Axon / Taser International OUI
            police_in_this_scan.append(addr)

    if police_in_this_scan:
        police_detected = police_detected + len(police_in_this_scan)
        print(f" >>>>>>>>>> POLICE DETECTED: {len(police_in_this_scan)} device(s) found. Total: {police_detected}")

        try:
            with open("detections.log", "a") as detectionslog:
                for addr in police_in_this_scan:
                    print(f" >>>>>>>>>> POLICE DETECTED: {police_detected} {datetime.now()} [{addr}]", file=detectionslog)
        except:
            pass

        # Alerting
        if is_termux():
            os.system("termux-notification --title 'POLICE DETECTED' --content 'Possible Police Raid Imminent' --priority high > /dev/null 2>&1")
            os.system("termux-vibrate -d 1000 > /dev/null 2>&1")

        # Audio/Video Alert
        if os.system("command -v mpv >/dev/null 2>&1") == 0:
            os.system("mpv POLICE.mp4 > /dev/null 2>&1 &")
        elif os.system("command -v omxplayer >/dev/null 2>&1") == 0:
            os.system("omxplayer POLICE.mp4 > /dev/null 2>&1 &")

        if police_detected >= 5:
            print(" >>>>>>>>>> POSSIBLE POLICE RAID IMMINENT")
    else:
        print(" > No Police Detected")
                    
def detect():
    global count, police_detected
    while True:
        try:
            logo()
            GetBluetoothMacList()
            time.sleep(2)
        except Exception as e:
            print(f"Error in detect loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    count = 0
    detect()
