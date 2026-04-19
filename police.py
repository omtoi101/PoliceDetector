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
'''
                                                                                                         
 *#####:         .##:*##                   @@@@@: @@@@@@=#@@@@@@#-@@@@@@  @@@@@:@@@@@@@= @@@@@@ -@@@@@   
 #######-        .##:###                   @@@@@- @@@@@@=#@@@@@@#-@@@@@@ .@@@@@:@@@@@@@= @@@@@@ -@@@@@   
 ###::###  -==:  .##:-=-   ===     ===     @%  %@ @@        @@   -@=     @@        @@   %@    @#-@-  @@  
 ###  ### ###### .##:###  #####- .#####:   @%  %@ @@        @@   -@=     @@        @@   %@    @#-@=  @@  
 #######*-##. ##:.##:### *## ### ##+ :##   @%  %@ @@@@%     @@   -@@@@.  @@        @@   %@    @#-@@@@@   
 ######* +##  ##*.##:### ###     #######.  @%  %@ @@@@*     @@   -@@@@   @@        @@   %@    @#-@@@@@.  
 ###     =##  ##*.##:### ### :** ##+  .:   @%  %@ @@        @@   -@=     @@        @@   %@    @#-@-  @@  
 ###      ###### .##:### -#####* =##*##*   @@--@# @@----.   @@   -@*---- *@----    @@   =@=--=@=-@-  @@  
 *##      .####. .##.*##  -###+   -###+    @@@@@: @@@@@@+   @@   -@@@@@@  @@@@@:   @@    @@@@@@ -@-  @@  
                                           =====. ======:   ==   .======  =====    =-    ====== .=.  ==  

"If He Was Going To Commit A Crime, Would He Have Invited The Number One Cop In Town? Now, Where Did I Put My Gun?
Oh Yeah, I Set It Down When I Got A Piece Of Cake!" - Clancy Wiggum 
'''
#################################################################################################################
# Open Sauce Software, tasty and free!
#################################################################################################################
import time, threading, logging, os, sys
from datetime import datetime

try:
    import simplepyble
except ImportError:
    simplepyble = None
#################################################################################################################
current_dateTime = datetime.now()
#################################################################################################################

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
 #######*-##. ##:.##:### *## ### ##+ :##   @%  %@ @@@@%     @@   -@@@@.  @@        @@   %@    @#-@@@@@   
 ######* +##  ##*.##:### ###     #######.  @%  %@ @@@@*     @@   -@@@@   @@        @@   %@    @#-@@@@@.  
 ###     =##  ##*.##:### ### :** ##+  .:   @%  %@ @@        @@   -@=     @@        @@   %@    @#-@-  @@  
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
#if __name__ == "__main__":
def GetBluetoothMacList():
    global count, police_detected

    found_addresses = []

    if simplepyble:
        try:
            adapters = simplepyble.Adapter.get_adapters()
            if len(adapters) == 0:
                print(" >>>> No Adapters Found...")
                return

            hci = int(0) # 0 for built in bt interface, 1 for USB bt interface (hci0, hci1)
            adapter = adapters[hci]
            print(f" >>>> Bluetooth adapter: {adapter.identifier()} [{adapter.address()}]")
            adapter.set_callback_on_scan_start(lambda: print(" >>>> Scan started.", datetime.now()))
            adapter.set_callback_on_scan_stop(lambda: print(" >>>> Scan complete.", datetime.now()))
            # adapter.set_callback_on_scan_found(lambda peripheral: print(f" > Found {peripheral.identifier()} [{peripheral.address()}]"))
            adapter.scan_for(5000) # Scan for 5 seconds
            peripherals = adapter.scan_get_results()
            found_addresses = [p.address().upper() for p in peripherals]
        except Exception as e:
            print(f" >>>> simplepyble scan failed: {e}")
    else:
        print(" >>>> simplepyble not found. Attempting fallback scan...")
        # Fallback for rooted Termux/Linux using hcitool
        try:
            import subprocess
            # Requires root on Termux
            cmd = "su -c 'hcitool lescan --passive --timeout=5' 2>/dev/null" if is_termux() else "sudo hcitool lescan --passive --timeout=5"
            output = subprocess.check_output(cmd, shell=True).decode()
            for line in output.split('\n'):
                parts = line.split()
                if len(parts) > 0:
                    found_addresses.append(parts[0].upper())
        except Exception as e:
            print(f" >>>> Fallback scan failed: {e}")
            print(" >>>> Please ensure simplepyble is installed or you have root access with hcitool available.")

    count = count + 1
    print(" >>>> Scan Count:", count)

    police_in_this_scan = []
    for addr in found_addresses:
        if "00:25:DF" in addr: # Axon / Taser International OUI
            police_in_this_scan.append(addr)

    if police_in_this_scan:
        police_detected = police_detected + len(police_in_this_scan)
        print(f" >>>>>>>>>> POLICE DETECTED: {len(police_in_this_scan)} device(s) found. Total: {police_detected}", datetime.now())

        with open("detections.log", "a") as detectionslog:
            for addr in police_in_this_scan:
                print(f" >>>>>>>>>> POLICE DETECTED: {police_detected} {datetime.now()} [{addr}]", file=detectionslog)

        # Alerting once per scan
        if is_termux():
            os.system("termux-notification --title 'POLICE DETECTED' --content 'Possible Police Raid Imminent' --priority high")
            os.system("termux-vibrate -d 1000")
            os.system("mpv POLICE.mp4 > /dev/null 2>&1 &")
        else:
            # Debian / Raspberry Pi
            # Check if mpv exists, otherwise try omxplayer
            if os.system("command -v mpv >/dev/null 2>&1") == 0:
                os.system("mpv POLICE.mp4 > /dev/null 2>&1 &")
            elif os.system("command -v omxplayer >/dev/null 2>&1") == 0:
                os.system("omxplayer POLICE.mp4 > /dev/null 2>&1 &")

        if police_detected >= 5:
            print(" >>>>>>>>>> POLICE OFFICERS DETECTED - POSSIBLE POLICE RAID IMMINENT")
            with open("detections.log", "a") as detectionslog:
                print(f" >>>>>>>>>> POLICE OFFICERS DETECTED - POSSIBLE POLICE RAID IMMINENT {datetime.now()}", file=detectionslog)
    else:
        print(" > No Police Detected ", datetime.now())
                    
def detect():
    global count, police_detected
    while True:
        try:
            logo()
            GetBluetoothMacList()
            time.sleep(2)
        except:
            pass

if __name__ == "__main__":
    count = 0
    x = threading.Thread(target=detect)
    x.start()
    # x.join()
