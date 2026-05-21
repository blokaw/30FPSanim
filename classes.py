'''
 TODO:
 [+] Duration class
 [+] TimingRange class
 [+] ValueRange class
 [+] KfProperty class
'''

class Duration:
    FPS = 30
    def __init__(self, seconds):
        self._seconds = seconds
        self._frames = seconds * self.FPS

        self._frameStep = 100 / self._frames

    def getSeconds(self) -> float:  return self._seconds
    def getFrames(self) -> float:   return self._frames
    def getFrameStep(self) -> float:return self._frameStep

class TimingRange:
    ACCURACY = 2
    def __init__(self, fr: float, to: float):
        self._fr = fr
        self._to = to
        self._frameFr = 0
        self._frameTo = 0

    def getFrom(self) -> float:     return self._fr
    def getTo(self) -> float:       return self._to
    def getFrameLen(self) -> float: return self._frameTo - self._frameFr
    def getRangeObj(self) -> object:
        timRange = object()
        timRange.fr = self._fr
        timRange.to = self._to

        return timRange

    def fixRange(self, dur: Duration) -> None:
        frames = dur.getFrames()
        self._frameFr = round( frames * self._fr / 100 )
        self._fr = round( self._frameFr / frames * 100 , self.ACCURACY )

        self._frameTo = round( dur.getFrames() * self._to / 100 )
        self._to = round( self._frameTo / frames * 100 , self.ACCURACY )

class ValueRange:
    def __init__(self, fr: list[float], to: list[float]):
        self._fr = fr
        self._to = to

    def getFrom(self) -> list[float]:   return self._fr
    def getTo(self) -> list[float]:     return self._to
    def getRangeObj(self) -> object:
        valRange = object()
        valRange.fr = self._fr
        valRange.to = self._to

        return valRange
    
    def getDiff(self, ind: int) -> float:
        return self._to[ind] - self._fr[ind]
    
    def compareValues(self, ind: int) -> bool:
        return self._fr[ind] == self._to[ind]
    
    def getLen(self) -> int:
        return len(self._fr)
    
class KfProperty(ValueRange):
    def __init__(self, propName: str, mask: str, fr: list[float], to: list[float]):
        self._propName = propName
        self._mask = mask
        super().__init__(fr, to)

    def getPropertyName(self) -> str:   return self._propName
    def getMask(self) -> str:           return self._mask
    def buildFrame(self, val: list[float]) -> dict:
        return {
            self._propName: {
                "value": val,
                "mask": self._mask
            }
        }
