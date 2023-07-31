#!/usr/bin/env python

import asyncio
import pulsectl_asyncio

"""
CONFIGURATION

The configuration variables are defined globally, and then set in the :func:`config` function once all the fade functions have been defined.
This is only done to place the configuration at the top of the file.
"""

DURATION = 2000 # how long to spend ducking (in milliseconds; minimum: 0)
DUCK = 0.4 # the minimum volume to which to duck music applications (minimum: 0; maximum: 1)
STEPS = 30 # how smooth the auto-ducking (minimum: 1)
FADE = lambda x: bezier(x) # the fade function used to duck and unduck music applications

"""
MAIN LOOP
"""

async def main():
    ducking = [ ] # the apps that have been or are being ducked

    # connect to the PulseAudio sound server
    async with pulsectl_asyncio.PulseAsync('volume-increaser') as pulse:
        while True:
            apps = list(await pulse.sink_input_list())

            # check whether any non-music application is playing audio
            playback = False
            for app in apps:
                media_name = app.proplist.get('media.name', '').lower()
                media_role = app.proplist.get('media.role', '').lower()
                application_name = app.proplist.get('application.name', '').lower()
                if ((media_name and media_name == 'playback' and (not media_role or media_role == 'speech-dispatcher-espeak-ng')) or 
                    (media_role and media_role != 'music') or
                    (application_name and application_name == 'firefox')):
                    playback = True

                if playback:
                    break

            # duck or unduck music applications if there is playback
            # ducked apps are added to a list so they are not ducked multiple times
            # and similarly for unducked applications
            for app in apps:
                if app.proplist.get('media.role', '').lower() == 'music':
                    app_name = f"{ app.index }_{ app.name }" # app name may not be unique
                    if playback and app_name not in ducking:
                        ducking.append(app_name)
                        asyncio.ensure_future(duck(pulse, app))

                    if not playback and app_name in ducking:
                        ducking.remove(app_name)
                        asyncio.ensure_future(unduck(pulse, app))

            await asyncio.sleep(1) # yield

async def duck(pulse, app):
    """
    Duck the given application.

    :param pulse: The asynchronous connection with the PulseAudio sound server.
    :type pulse: :class:`pulsectl_asyncio.pulsectl_async.PulseAsync`
    :param app: The sink input information for the app that will be duck.
    :type app: :class:`pulsectl.pulsectl.PulseSinkInputInfo`
    """

    volume = app.volume
    for i in range(STEPS):
        volume.value_flat = DUCK + (1 - DUCK) * (1 - FADE(i))
        await pulse.volume_set(app, volume)
        await asyncio.sleep(DURATION/1000/STEPS)

    volume.volume_flat = DUCK
    await pulse.volume_set(app, volume)

async def unduck(pulse, app):
    """
    Unduck the given application.

    :param pulse: The asynchronous connection with the PulseAudio sound server.
    :type pulse: :class:`pulsectl_asyncio.pulsectl_async.PulseAsync`
    :param app: The sink input information for the app that will be unduck.
    :type app: :class:`pulsectl.pulsectl.PulseSinkInputInfo`
    """

    volume = app.volume
    for i in range(STEPS):
        volume.value_flat = DUCK + (1 - DUCK) * (FADE(i))
        await pulse.volume_set(app, volume)
        await asyncio.sleep(DURATION/1000/STEPS)

    volume.volume_flat = 1
    await pulse.volume_set(app, volume)

"""
FADE FUNCTIONS
"""

def bezier(x):
    """
    Calculate the bezier coefficient.

    :param x: The parameter value of the bezier function.
    :type x: int

    :return: The bezier coefficient.
    :rtype: float
    """

    x = x / STEPS
    return x * x * (3.0 - 2.0 * x) # bezier

# run event loop until main_task finishes
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
