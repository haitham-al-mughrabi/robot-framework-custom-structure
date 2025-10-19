#!/bin/bash

echo "🛑 Stopping VNC services..."

# Find and kill VNC processes
for proc in Xvfb x11vnc websockify; do
    pids=$(ps aux | grep $proc | grep -v grep | awk '{print $2}')
    if [ -n "$pids" ]; then
        echo "Killing $proc processes: $pids"
        echo $pids | xargs kill
    fi
done

echo "✅ VNC services stopped"