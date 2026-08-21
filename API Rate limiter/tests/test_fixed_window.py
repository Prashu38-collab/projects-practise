from src.rate_limiter import FixedWindowRateLimiter

def test_allow_and_reject():
    limiter=FixedWindowRateLimiter(3,10)
    assert limiter.allow_request("A") == True
    assert limiter.allow_request("A") == True
    assert limiter.allow_request("A") == True
    assert limiter.allow_request("A") == False

def test_different_limits_clients():
    limiter=FixedWindowRateLimiter(3,10)
    assert limiter.allow_request("A")==True
    assert limiter.allow_request("A")==True
    assert limiter.allow_request("A")==True
    assert limiter.allow_request("A")==False
    assert limiter.allow_request("B")==True

def test_rejected_request_counter_no_change():
    limiter=FixedWindowRateLimiter(3,10)
    assert limiter.allow_request("A") == True
    assert limiter.allow_request("A") == True
    assert limiter.allow_request("A") == True
    assert limiter.allow_request("A")==False
    assert limiter.clients["A"]["request_count"]==3

def test_new_windows_request_accepted(mocker):
    limiter=FixedWindowRateLimiter(3,10)
    mocker.patch("src.rate_limiter.time.time",return_value=100)
    assert limiter.allow_request('A') is True
    assert limiter.allow_request('A') is True
    assert limiter.allow_request('A') is True
    assert limiter.allow_request('A') is False

    # Move clock to foward 10 second
    mocker.patch("src.rate_limiter.time.time", return_value=110)
    # new window= request should be allowed

    assert limiter.allow_request('A') is True
