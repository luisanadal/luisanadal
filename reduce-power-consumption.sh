#/bin/bash
# Turn off USB/LAN
echo '1-1' |tee /sys/bus/usb/drivers/usb/unbind

# Turn on USB/LAN (default)
#echo '1-1' |tee /sys/bus/usb/drivers/usb/bind


# Turn off HDMI output
tvservice -o

# Turn on HDMI output (default)
#tvservice -p

# apt install cpufrequtils

# Powersave
for i in 0 1 2 3; do cpufreq-set -c $i -g powersave; done
# 600000 700000 800000 900000 1000000 1100000 1200000 1300000 1400000
for i in 0 1 2 3; do cpufreq-set -c $i -u 1200000; done

# Ondemand (default)
#for i in 0 1 2 3; do cpufreq-set -c $i -g ondemand; done
#for i in 0 1 2 3; do cpufreq-set -c $i -u 1400000; done

for i in 0 1 2 3
do
  echo CPU${i}: $(cat "/sys/devices/system/cpu/cpu${i}/cpufreq/scaling_governor") \
                $(cat "/sys/devices/system/cpu/cpu${i}/cpufreq/scaling_cur_freq") 
done
