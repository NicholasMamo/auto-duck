# PulseAudio auto-ducker

A simple script that ducks the volume of music applications when it detects audio playback.

## Description

The auto-ducker is a simple script to duck the volume of music applications during playback.
To detect music applications, the script looks for applications running on the PulseAudio sound server with the media role set to _music_.
The script considers any other application running on the PulseAudio sound server as playback and ducks the volume of music applications.

The auto-ducker has been tested and works with Spotify and [Amberol](https://gitlab.gnome.org/World/amberol).
The script runs asynchronously every second to minimize resource use.

## Getting Started

### Dependencies

The script uses [mhthies/pulsectl-asyncio](mhthies/pulsectl-asyncio), and so it only works on systems that use the PulseAudio sound server.

* PulseAudio sound server

### Installing

- Clone the repository and create a virtual environment: `python -m venv venv`
- Activate the virtual environment (`source venv/bin/activate`) and install the requirements: `pip install -r requirements.txt`

### Executing program

The script can be run in two ways: manually, as a script, or automatically on start-up, as a server.
You can run the script manually when needed by following the next steps:

- Navigate to the script location and activate the virtual environment (`source venv/bin/activate`)
- Run the script using `./main.py`
- When ready, close the script using `CTRL+C`

Alternatively, you can run the script as a service on boot.
Running the script as a service requires a slightly more complex setup:

- Create a service in `/etc/systemd/system/auto-ducker.service` by copying the template from `auto-ducker.service`
- Fill in the following variables in the template:
	- `USERID`: your user ID; you can find it using `printenv | grep XDG_RUNTIME_DIR`
	- `USER`: your username; you can find it using `echo ${USER}`
	- `GROUP`: your user's group, normally the same as your user name
	- `/PATH/TO`: the path to this repository
- Test the service using `sudo systemctl start autho-ducker.service`
- Enable the service to start on boot using `sudo systemctl enable auto-ducker.service`.

## Help

### Configuration

The script configuration is at the beginning of the `main.py` script.
You can configure the following variables:

- `DURATION`: how long to spend ducking volume (in milliseconds; default: 2 seconds; minimum: 0)
- `DUCK`: the minimum volume to which to duck the volume ofmusic applications (default: 0.4; minimum: 0; maximum: 1)
- `STEPS`: how smooth the auto-ducking (default: 30); larger values lower performance but make ducking and unducking smoother (minimum: 1)
- `FADE`: the fade function used to duck and unduck the volume of music applications (default: `bezier`); see the end of the script for fade functions

### Debug

You can debug the main script by running it manually, as described above, and observing errors in the output.

When running the auto-ducker as a service, the errors are written to the journal.
You can view the journal entries for the auto-ducker service using: `sudo journalctl -u auto-ducker.service -f`.

Remember that whenever you edit the service configuration, you need to reload the service configuration (`sudo systemctl daemon-reload`) and restart the service (`sudo systemctl restart auto-ducker.service`).

### FAQ

- Why doesn't YouTube duck or unduck?
  The auto-ducker only ducks the volume of music applications, not browser tabs.
If you are listening to YouTube on Google Chrome or Firefox, the auto-ducker will see a browser with audio playback, not a music player.
The auto-ducker has been tested and works with Spotify and [Amberol](https://gitlab.gnome.org/World/amberol).

- Why is there a delay until music applications are unducked?
  The auto-ducker only detects that playback has stopped when the application releases the PulseAudio sound server.
Google Chrome, for example, signals that playback has stopped when no tab has played audio for 15 seconds.

## Authors

- [Nicholas Mamo](https://github.com/NicholasMamo/)

## Version History

- 0.1
	- Initial release

## License

This project is licensed under the MIT License.
See the LICENSE.md file for details.

## Acknowledgments

* [README.md template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc) from [DomPizzie](https://gist.github.com/DomPizzie)
* [mhthies/pulsectl-asyncio](mhthies/pulsectl-asyncio) for the asynchronous PulseAudio API