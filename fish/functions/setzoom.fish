function setzoom
	gsettings set org.gnome.desktop.interface text-scaling-factor "$argv[1]"
end
