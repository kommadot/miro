import os
interfaces="source-directory /etc/network/interfaces.d\n"
interfaces+="auto wlan0\n"
interfaces+="allow-hotplug wlan0\n"
interfaces+="iface wlan0 inet manual\n"

def set_wifi(ssid,password):
	os.system("wpa_passphrase '%s' '%s' > %s.conf" % (ssid,password,ssid))
	os.system("sudo mv %s.conf /etc/wpa_supplicant" % ssid)
	inter=interfaces+"wpa-conf /etc/wpa_supplicant/"+ssid+".conf\n"
	os.system("sudo echo '%s' > /etc/network/interfaces" % inter )


set_wifi("BrownBread","brownbread1")
