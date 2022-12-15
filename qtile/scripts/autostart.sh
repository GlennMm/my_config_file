#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

#Set your native resolution IF it does not exist in xrandr
#More info in the script
# run $HOME/.config/qtile/scripts/set-screen-resolution-in-virtualbox.sh
#run $HOME/.config/qtile/scripts/set-pywal.sh
#Find out your monitor name with xrandr or arandr (save and you get this line)
#xrandr --output VGA-1 --primary --mode 1360x768 --pos 0x0 --rotate normal
#xrandr --output DP2 --primary --mode 1920x1080 --rate 60.00 --output LVDS1 --off &
#xrandr --output LVDS1 --mode 1366x768 --output DP3 --mode 1920x1080 --right-of LVDS1
#xrandr --output HDMI2 --mode 1920x1080 --pos 1920x0 --rotate normal --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output VIRTUAL1 --off
#autorandr horizontal

#change your keyboard if you need it
#setxkbmap -layout be
MONITORS=$(xrandr -q | grep " connected" | wc -l)

if [ $MONITORS = "2" ]; then
  run $HOME/.config/qtile/scripts/screen.sh
# │ xrandr --output eDP1 --primary --mode 1366x768 --scale 1.5 --pos 2112x0 --rotate normal --output HDMI1 --mode 1920x1080 --pos 0x0 --rate 59 --scale 1.1 --rotate normal --output VIRTUAL1 --off 
else [ $MONITORS = "1" ];
  xrandr --output eDP1 --mode 1366x768 --scale 1.5 --rotate normal
fi

keybLayout=$(setxkbmap -v | awk -F "+" '/symbols/ {print $2}')

if [ $keybLayout = "be" ]; then
  cp $HOME/.config/qtile/config-azerty.
  py $HOME/.config/qtile/config.py
fi

#autostart ArcoLinux Welcome App
# run dex $HOME/.config/autostart/arcolinux-welcome-app.desktop &

#Some ways to set your wallpaper besides variety or nitrogen
# feh --bg-fill /usr/share/backgrounds/arcolinux/arco-wallpaper.jpg &
#start the conky to learn the shortcuts
#  (conky -c $HOME/.config/qtile/scripts/system-overview) &

#start sxhkd to replace Qtile native key-bindings
run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &


#starting utility applications at boot time
#run variety &
run nm-applet &
run pamac-tray &
run xfce4-power-manager &
numlockx on &
blueberry-tray &
picom --config $HOME/.config/qtile/scripts/picom.conf &
/usr/lib/xfce-polkit/xfce-polkit &
# /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &

#starting user applications at boot time

run volumeicon &
run wal -R &
#run discord &
#nitrogen --restore &
#run caffeine -a &
#run vivaldi-stable &
#run firefox &
#run thunar &
#run dropbox &
#run insync start &
#run spotify &
#run atom &
run emacs --daemon &
# run nitrogen --restore &
# run telegram-desktop &

