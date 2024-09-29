def test_new_testcases(desktop_app):
    desktop_app.login()
    desktop_app.create_test()
    desktop_app.open_tests()
    desktop_app.check_test_created()
    desktop_app.delete_test()
    #desktop_app.close()