# 30FPSanim

Python script for generating keyframes for CSGO Panorama in 30FPS

## Tutorial

### Pretty simple to use:

+ Put your keyframes in css/keyframes.css
  
+ Open terminal and do `python main.py <animation-duration> <animation-timing-function> <normal | flat>`
  
+ See in css/30FPSkeyframes.css

### Timing functions:

> [!IMPORTANT]
> Since it turns animation into snappy frames you have to choose timing function to generate them, because CSS's animation-timing-function won't work

+ linear = 0 | linear
  
+ ease-in = 1 | easeIn | ease-in
  
+ ease-out = 2 | easeOut | ease-out
  
+ ease-in-out = 3 | easeInOut | ease-in-out
