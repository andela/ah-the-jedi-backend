class Data:
    """
    This class 'TestData' contains data
    used for testing
    """

    def __init__(self):

        self.user_data = {
            "user": {
                "email": "testuser@email.com",
                "username": "Alpha",
                "password": "Admin12345"
            }
        }

        self.missing_user_data = {
            "user": {
                "username": "Alpha",
                "password": "Admin12345"
            }
        }

        self.login_data = {
            "user": {
                "email": 'testuser@email.com',
                "password": 'Admin12345'
            }
        }

        self.update_data = {
            "user": {
                "username": "newMan"
            }
        }

        self.username, self.password = (
            self.user_data["user"]["email"],
            self.user_data["user"]["password"]
        )
