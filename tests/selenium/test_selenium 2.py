import pytest
from virtual_user import Build_user

'''
This Python class selects a virtual user at random and navigates them through the site.

The routes that each virtual user tests:
- User #1: registers and traverses through all the routes within Main Page.
'''


@pytest.mark.selenium_test
class VirtualUser:

    def __init__(self):
        self.testing = Build_user()

    def run(self):
        print("Virtual user has been activated... Running user:\n")
        self.testing.user1_execute()
        self.testing.close()


if __name__ == "__main__":
    user = VirtualUser()
    user.run()
