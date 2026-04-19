![image](https://user-images.githubusercontent.com/57064943/163714778-8598c24a-6ae2-49f6-ba4c-42de94dfa025.png)


<p align="right">


	
</p>
<img align="left" src="https://github.com/PoliceDetector/PoliceDetector/assets/145007532/d1cb1037-6032-45e5-928c-ea322142507b" height="50%" width="50%"/>

<br>
<br>
<br>


      
<p align="left"> 
<sup>
<a href="https://facebook.com/PoliceProximity">
Utility to detect police officers equipped with Axon brand Body Worn Cameras and Tasers using Bluetooth Low Energy.
	</a></sup><br />
	
</p>

## Running on Termux (Android)

To run this on an Android device using Termux, follow these steps:

1. **Install Termux** from [F-Droid](https://f-droid.org/en/packages/com.termux/).
2. **Install Termux:API** app from [F-Droid](https://f-droid.org/en/packages/com.termux.api/).
3. **Grant Permissions**: In Android settings, grant "Location" and "Nearby Devices" permissions to both Termux and Termux:API.
4. **Open Termux** and run the setup script:
   ```bash
   pkg install git
   git clone https://github.com/PoliceDetector/PoliceDetector
   cd PoliceDetector
   chmod +x termux_setup.sh
   ./termux_setup.sh
   ```
5. **Run the detector (with root)**:
   ```bash
   su -c 'python police.py'
   ```

*Note: **Root access is required** for reliable Bluetooth scanning on Android via Termux. The script uses `hcitool` through the `su` command to access the phone's built-in Bluetooth hardware.*
