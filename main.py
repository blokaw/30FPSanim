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

import sys
import os

def get_exe_dir():
    """Возвращает папку, где находится запущенный .exe файл"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def readLocalFile(path="css/keyframes.css"):
    base_dir = get_exe_dir()
    full_path = os.path.join(base_dir, path)
    
    with open(full_path, 'r', encoding='utf-8') as file:
        return file.read()

def saveFile(data: list[str], style, path="css/30FPSkeyframes.css"):
    base_dir = get_exe_dir()
    full_path = os.path.join(base_dir, path)
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, "w", encoding='utf-8') as file:
        file.write(
            "\n".join(x.replace("  ", "").replace("\n", "") for x in data) if style == "flat" else data
        )

def compareProps(kfs, kf1, kf2) -> list[KfProperty]:
    # [0] = MIN; [1] = MAX; by length
    MIN, MAX = sorted([kfs[kf1], kfs[kf2]], key=len)

    DIFF = []
    NEW_VAL = False
    for i in list(MAX):
        if i not in MIN: continue
        DIFF.append(
            KfProperty(
                propName=i, 
                mask=MIN[i]["mask"], 
                fr=MIN[i]["value"], 
                to=MAX[i]["value"]
            )
        )
        if MAX[i]["value"] != MIN[i]["value"]:
            NEW_VAL = True
            

    return DIFF if NEW_VAL else []


def build30FPSKeyframes(kf, _duration, _timingFunction):
    keyframes = {}
    
    kfFramesIter = iter(kf)

    prevKf = next(kfFramesIter, None)
    currKf = next(kfFramesIter, None)
    print("===================================")
    while currKf is not None:
        comparedProps = compareProps(kf, prevKf, currKf)

        print(f"[i] {prevKf}% -> {currKf}%")
        if len(comparedProps) > 0:
            print(" > Generating frames...")
            keyframes.update(generateKeyframes(
                Duration(_duration), 
                comparedProps, 
                TimingRange(prevKf, currKf), 
                timingFuncDict[_timingFunction]
            ))
        else:
            print(" > No transition.")

        prevKf, currKf = currKf, next(kfFramesIter, None)
    print("===================================")
    return keyframes
    
def run():
    os.system('cls')

    print("[0] Reading and parsing keyframes.css...\n")
    kfStr =    readLocalFile()
    kf =       parseKeyframes(kfStr)

    print(f"[i] Animations found > {len(kf)}\n")

    cfg = parseAnimationConfig(kfStr)

    data = []

    for name in cfg:
        print(f"[1] Comparing frames for {name}...")

        new_kf = {name: build30FPSKeyframes(kf[name], cfg[name]["duration"], cfg[name]["timingFunction"])}

        print("[2] Saving new keyframes...\n")

        data.append(buildKeyframes(new_kf))
    
    if data == []:
        print("[i] Nothing was saved. Add animations and run the script again.")
    else:
        saveFile(data, cfg[name]["style"])

        print("[3] Done! See in 30FPSkeyframes.css\n\n\n")

    if getattr(sys, 'frozen', False):
        input("Press Enter...")


if __name__ == '__main__':
    run()
