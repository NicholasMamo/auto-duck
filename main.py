#!/usr/bin/env python
"""
CONFIGURATION

The configuration variables are defined globally, and then set in the :func:`config` function once all the fade functions have been defined.
This is only done to place the configuration at the top of the file.
"""

DURATION = None
DUCK = None
STEPS = None
FADE = None

def config():
    """
    Configure the auto-ducker.
    The function is defined here so that by the time it is called, the functions have all been defined.
    """

    # the number of milliseconds to spend fading
    global DURATION
    DURATION = 2000

    # the minimum volume to which to duck music applications
    global DUCK
    DUCK = 0.4

    # how detailed the auto-ducking; the higher the steps, the lower the performance but the more seamless the ducking
    global STEPS
    STEPS = 30

    # the fade function
    global FADE
    FADE = bezier


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
