import os
import sys

from frame_generator import *
from kf_parser import *

timingFuncDict = {
    "linear": linear,
    "easeIn": easeInSine,
    "easeOut": easeOutSine,
    "easeInOut": easeInOutSine,

    "ease-in": easeInSine,
    "ease-out": easeOutSine,
    "ease-in-out": easeInOutSine,
    
    "0": linear,
    "1": easeInSine,
    "2": easeOutSine,
    "3": easeInOutSine,
}

def readLocalFile(path = "css/keyframes.css"):
    with open(path, 'r') as file:
        return file.read()
    
def saveFile(data: str, style, path = "css/30FPSkeyframes.css"):
    with open("css/30FPSkeyframes.css", "w") as file:
        file.write(
            data.replace("  ", "").replace("\n", "") if style == "flat" else data
        )

def compareProps(kfs, kf1, kf2) -> list[KfProperty]:
    # [0] = MIN; [1] = MAX; by length
    MIN, MAX = sorted([kfs[kf1], kfs[kf2]], key=len)

    DIFF = []
    for i in list(MAX):
        if i not in MIN: continue

        if MAX[i]["value"] != MIN[i]["value"]:
            DIFF.append(
                KfProperty(
                    propName=i, 
                    mask=MIN[i]["mask"], 
                    fr=MIN[i]["value"], 
                    to=MAX[i]["value"]
                )
            )

    return DIFF


def build30FPSKeyframes(_duration, _timingFunction):
    keyframes = {}

    print("[0] Reading and parsing keyframes.css...\n")
    _kfStr =    readLocalFile()
    _kf =       parseKeyframes(_kfStr)
    
    _kfName =   next(iter(_kf))
    _kfFramesIter = iter(_kf[_kfName])

    print("[1] Comparing frames...")
    _prevKf = next(_kfFramesIter, None)
    _currKf = next(_kfFramesIter, None)
    print("===================================")
    while _currKf is not None:
        comparedProps = compareProps(_kf[_kfName], _prevKf, _currKf)

        print(f"[i] {_prevKf}% -> {_currKf}%")
        if len(comparedProps) > 0:
            print(" > Generating frames...")
            keyframes.update(generateKeyframes(
                Duration(_duration), 
                comparedProps, 
                TimingRange(_prevKf, _currKf), 
                timingFuncDict[_timingFunction]
            ))
        else:
            print(" > No transition.")

        _prevKf, _currKf = _currKf, next(_kfFramesIter, None)
    print("===================================")
    return {_kfName: keyframes}
    
def run():
    os.system('cls')
    if len(sys.argv) < 3:
        print("[!] Missing arguments.")
        return
    
    dur = 0
    tF = sys.argv[2]
    style = "normal"
    if len(sys.argv) >= 4:
        if sys.argv[3] in ["normal", "flat"]:
            style = sys.argv[3]
        else:
            print("[!] Problems with parsing style.\n\n\n")

    try:
        dur = float(sys.argv[1])
    except ValueError:
        print("[!] Problems with parsing duration.\n\n\n")
        return
    
    if tF not in timingFuncDict:
        print("[!] Wrong timing function.\n\n\n")
        return

    kf = build30FPSKeyframes(dur, tF)

    print("[2] Saving new keyframes...\n")

    saveFile(buildKeyframes(kf), style)

    print("[3] Done! See in 30FPSkeyframes.css\n\n\n")


if __name__ == '__main__':
    run()
