#!/bin/bash

value=$(acpi -b)


state=$(echo $value | awk '/0:/ {print$3}')
percentage=$(echo $value | awk '/0:/ {print$4}')
estimate_time=$(echo $value | awk '/0:/ {print$5,$6,$7}')
icon=""
percent_val=$(echo $percentage | sed 's/[^0-9]*//g' )

if [[ $percent_val -gt 80 ]]; then
  icon="  "
elif [[ $percent_val -lt 80 ]] && [[ $percent_val -gt 75 ]]; then
  icon="  "
elif [[ $percent_val -lt 56 ]] && [[ $percent_val -gt 45 ]]; then
  icon="  "
elif [[ $percent_val -lt 46 ]] && [[ $percent_val -gt 30 ]]; then
  icon="  "
elif [[ $percent_val -lt 15 ]] && [[ $percent_val -gt 0 ]]; then
  icon="  "
fi

if [[ "$state" == "Charging," ]]; then 
echo "   $state $percent_val% $estimate_time"
else
echo "$icon   $state $percent_val% $estimate_time"
fi


