function toggle_audio
	set aud_card (pactl list cards short | grep -i "bluez" | awk '{print $1}' )
	set aud_prof (pactl list sinks short | grep -i "bluez" | awk '{print $2}'| awk -F. '{print $3}')

	if test "$aud_prof" = "a2dp_sink"
	pactl set-card-profile $aud_card headset_head_unit
	else
	pactl set-card-profile $aud_card a2dp_sink
	end 
end
