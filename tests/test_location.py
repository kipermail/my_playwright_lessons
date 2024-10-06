def test_location_ok(mobile_app_auth):
    location = mobile_app_auth.get_location()
    assert location == "48.0:2.4"