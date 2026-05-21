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

    for frame_i in range(1, timing.getFrameLen() + 1):
        key = round( 
            timing.getFrom() + frame_i * duration.getFrameStep(), 
            TimingRange.ACCURACY
            )
        
        NEW_VAL = False
        frame = {}

        # Loop through props
        for prop_i in range(len(props)):
            prop = props[prop_i]
            frame[prop.getPropertyName()] = {
                "value": [],
                "mask": prop.getMask()
            }

            # Pointers
            p_fValue = frame[prop.getPropertyName()]["value"]
            p_prevFValue = frames[prevKey][prop.getPropertyName()]["value"]

            # Loop through values of prop
            for val_i in range(prop.getLen()):
                
                # If values are equal just save one of them
                if prop.compareValues(val_i):
                    p_fValue.append(prop.getFrom()[val_i])
                    continue

                val = round( 
                    prop.getFrom()[val_i] + prop.getDiff(val_i) * timingFunc(frame_i / timing.getFrameLen()), 
                    2 
                )

                # The judge of Worthy frame
                NEW_VAL = val != p_prevFValue[val_i]

                p_fValue.append(val)
            
        if NEW_VAL:
            closestKey = round(key - 1 / 10**TimingRange.ACCURACY, TimingRange.ACCURACY)
            frames[closestKey] = frames[prevKey]

            frames[key] = frame
            prevKey = key

    return frames

        



if __name__ == '__main__':
    Prop1 = KfProperty("opacity", "%s", [0.0], [1.0])
    Prop2 = KfProperty("position", "%spx, %spx, %spx", [0.0, 58.0, 0.0], [0.0, 100.0, 0.0])

    fr = generateKeyframes(
        duration = Duration(0.5), 
        props = [Prop1, Prop2],
        timing = TimingRange(0.0, 100.0), 
        timingFunc = linear
        )
   
    print(json.dumps(fr, indent=4))