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

        self.user_data2 = {
            "user": {
                "email": "testuser2@email.com",
                "username": "Alpha2",
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

        self.profile_data = {
            "bio": "I love swimming",
            "first_name": "Madison",
            "last_name": "Jade"
        }

        self.article_data = {
            'title': 'First test data',
            'description': 'This is the first test data',
            'body': 'This is the first body'
        }
