# Install script

# Creating program folder and config file
cloner_dir=~/.cloner

# Check if the directory already exists
if [ ! -d "$cloner_dir" ]; then
    mkdir -p "$cloner_dir"
    echo "# Config file for the cloner program" > "$cloner_dir/config.txt"
    echo "# Edit your preferences here" >> "$cloner_dir/config.txt"
    tail -n +4 config.txt.sample >> "$cloner_dir/config.txt"
    echo "Created program folder."
fi

# Putting a desktop entry in the autostart folder making the program start on boot up
mkdir ~/.config/autostart
echo "[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=false
Exec=/usr/bin/python /home/pi/cloner/src/main.py
Name=Cloner" > ~/.config/autostart/cloner.desktop
echo "Set program auto start on bootup."


# Installing requirements
pip install -r requirements.txt