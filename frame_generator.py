'''
 This script creates 30 FPS
 keyframes for CSGO Panorama
'''

from collections import OrderedDict, defaultdict
from typing import Callable
import math
import json

from classes import *

linear = lambda x: x
easeInSine = lambda x: 1 - math.cos((x * math.pi) / 2);
easeOutSine = lambda x: math.sin((x * math.pi) / 2);
easeInOutSine = lambda x: -(math.cos(math.pi * x) - 1) / 2;

def generateKeyframes(
        duration: Duration, 
        props: list[KfProperty], 
        timing: TimingRange, 
        timingFunc = linear
        ) -> dict:
    
    timing.fixRange(duration)

    prevKey = timing.getFrom()

    frames = defaultdict(dict)
    for prop in props:
        frames[prevKey].update(prop.buildFrame(prop.getFrom()))

    for frame in range(1, timing.getFrameLen() + 1):
        key = round( 
            timing.getFrom() + frame * duration.getFrameStep(), 
            TimingRange.ACCURACY
            )
        
        # Loop through props
        for prop_i in range(len(props)):
            prop = props[prop_i]
            frameValues = []

            NEW_VAL = False
            # Loop through values of prop
            for val_i in range(prop.getLen()):

                if prop.compareValues(val_i):
                    frameValues.append(prop.getFrom()[val_i])
                    continue
                else:
                    NEW_VAL = True

                val = round( 
                    prop.getFrom()[val_i] + prop.getDiff(val_i) * timingFunc(frame/timing.getFrameLen()), 
                    2 
                )

                if val == frames[prevKey][prop.getPropertyName()]["value"][val_i]:
                    NEW_VAL = False
                    continue

                frameValues.append(val)
            
            if NEW_VAL:
                closeKey = round(key - 1 / 10**TimingRange.ACCURACY, TimingRange.ACCURACY)
                frames[closeKey] = frames[prevKey]

                frames[key].update(prop.buildFrame(frameValues))
        prevKey = key

    return frames

        



if __name__ == '__main__':
    Prop1 = KfProperty("opacity", "%s", [0.0], [1.0])
    Prop2 = KfProperty("position", "%spx, %spx, %spx", [0.0, 58.0, 0.0], [0.0, 100.0, 0.0])

    fr = generateKeyframes(
        duration = Duration(2.9), 
        props = [Prop1, Prop2],
        timing = TimingRange(0.0, 8.0), 
        timingFunc = linear
        )
   
    print(json.dumps(fr, indent=4))