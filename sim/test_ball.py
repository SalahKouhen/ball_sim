# Unit tests to be run on ball.py

import pytest

def test_play():
    from ball import Ball

    test_ball = Ball(1)
    test_ball.play(0.1)
    assert test_ball.pos - -0.049 < 0.01;

test_play()