import pyglet
import Settings

# Play audio clip ('storing')
def storing():
    alarm = pyglet.resource.media(Settings.audio_clip)
    alarm.play()

