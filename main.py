import sys

from frame_generator import *
from kf_parser import *

def readLocalFile(path = "css/keyframes.css"):
    with open(path, 'r') as file:
        return file.read()

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


def build30FPSKeyframes(_duration):
    keyframes = {}

    print("[0] Reading and parsing keyframes.css...")
    _kfStr =    readLocalFile()
    _kf =       parseKeyframes(_kfStr)
    
    _kfName =   next(iter(_kf))
    _kfFramesIter = iter(_kf[_kfName])

    print("[1] Comparing frames...")
    _prevKf = next(_kfFramesIter, None)
    _currKf = next(_kfFramesIter, None)
    
    while _currKf is not None:
        comparedProps = compareProps(_kf[_kfName], _prevKf, _currKf)

        print(f"[i] {_prevKf}% -> {_currKf}%")
        if len(comparedProps) > 0:
            print(" > Generating frames...")
            keyframes.update(generateKeyframes(
                Duration(_duration), 
                comparedProps, 
                TimingRange(_prevKf, _currKf), 
                linear
            ))
        else:
            print(" > No transition.")

        _prevKf, _currKf = _currKf, next(_kfFramesIter, None)
    
    return {_kfName: keyframes}
    

if __name__ == '__main__':
    kf = build30FPSKeyframes(float(sys.argv[1]))

    print("[2] Saving new keyframes...")
    with open("css/30FPSkeyframes.css", "w") as file:
        file.write(
            buildKeyframes(
                kf
            )
        )
    print("[3] Done! See in 30FPSkeyframes.css")
