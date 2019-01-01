#!/usr/bin/env python3
import os
import logging
import subprocess
import tempfile

# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)

class AudioPlayer:
    '''Base class for WAV based audio players'''
    def __init__(self, device=None):
        '''Optional audio device handled by sub-classes.'''
        self.device = device

    def play_file(self, path: str):
        '''Plays a WAV file from a path'''
        pass

    def play_data(self, wav_data: bytes):
        '''Plays a WAV file from a buffer'''
        with tempfile.NamedTemporaryFile(suffix='.wav', mode='wb+') as wav_file:
            wav_file.write(wav_data)
            wav_file.seek(0)
            self.play_file(wav_file.name)

# -----------------------------------------------------------------------------
# APlay based audio player
# -----------------------------------------------------------------------------

class APlayAudioPlayer(AudioPlayer):
    '''Plays WAV files using aplay'''

    def play_file(self, path: str):
        if not os.path.exists(path):
            return

        aplay_cmd = ['aplay', '-q']

        if self.device is not None:
            aplay_cmd.extend(['-D', str(self.device)])

        # Play file
        aplay_cmd.append(path)

        logger.debug(aplay_cmd)
        subprocess.run(aplay_cmd)

    def play_data(self, wav_data: bytes):
        aplay_cmd = ['aplay', '-q']

        if self.device is not None:
            aplay_cmd.extend(['-D', str(self.device)])

        logger.debug(aplay_cmd)

        # Play data
        subprocess.run(aplay_cmd, input=wav_data)