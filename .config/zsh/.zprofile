[ "$(tty)" = "/dev/tty1" ] && exec /home/juftuf/.local/bin/startdwl
[ "$(tty)" = "/dev/tty2" ] && exec startx
[ "$(tty)" = "/dev/tty3" ] && exec /home/juftuf/.local/bin/starthyprland
