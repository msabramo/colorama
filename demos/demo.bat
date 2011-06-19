@rem!/usr/bin/env bash

@rem Script to demonstrate features of colorama.

@rem This demo is also used to verify correctness visually, because we don't have automated tests.

@rem Implemented as a bash script which invokes python so that we can test the
@rem behaviour on exit, which resets default colors again.

python demo01.py

python demo02.py

python demo03.py

if exist demo04.out del demo04.out
python demo04.py 2> demo04.out
type demo04.out

python demo05.py

python demo06.py
