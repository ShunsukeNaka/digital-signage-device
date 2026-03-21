#!/bin/bash

FLAG="/home/tns0/service/datas/hdmi_mode"

# 初期値（無ければON）
[ -f "$FLAG" ] || echo 0 > "$FLAG"

while true; do
  mode=$(cat "$FLAG")

  if [ "$mode" = "1" ]; then
    echo 1 > /sys/class/graphics/fb0/blank
  else
    echo 0 > /sys/class/graphics/fb0/blank
  fi

  sleep 1
done

