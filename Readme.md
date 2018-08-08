This is a minimal example of how to get numpy working under Android with p4a and python 3.6.

Suppose you have a directory called 'Android' under $HOME where your Android SDK and NDK as well as the crystax NDK lives. You can build the APK with:

```
export ANDROIDSDK="$HOME/Android"
export ANDROIDNDK="$HOME/Android/crystax-ndk-10.3.2"
export ANDROIDAPI="19"
export ANDROIDNDKVER="10.3.2"
```
```
p4a apk --private `pwd` --package=de.plapadoo.p4anumpy --name "p4a numpy" --bootstrap=sdl2 --version 0.1 --local_recipes=`pwd`/recipes --requirements=python3crystax==3.6,numpy,pysdl2
```

Installing and running the app should give the following logcat output:

```
08-08 19:27:00.771 27599 27618 I python  : sys.version is 3.6.0 (default, Feb 12 2017, 21:45:03)
08-08 19:27:02.439 27599 27618 I python  : numpy seems to work:
08-08 19:27:02.440 27599 27618 I python  :  [[ 0  1  2  3  4]
08-08 19:27:02.440 27599 27618 I python  :  [ 5  6  7  8  9]
08-08 19:27:02.440 27599 27618 I python  :  [10 11 12 13 14]]

```
