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
                "email": "anotheruser@gmail.com",
                "username": "NewUser",
                "password": "admin1211"
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

        self.login_data2 = {
            "user": {
                "email": 'anotheruser@gmail.com',
                "password": 'admin1211'
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

        self.article_data1 = {
            'title': 'First test data',
            'description': 'This is the first test data',
            'body': 'This is the first body'
        }

        self.article_control_data = {
            'title': 'Second test data',
            'description': 'This is the second test data',
            'body': 'This is the second body'
        }

        self.article_missing_data = {
            'title': 'Second test data',
            'body': 'This is the second test data'
        }

        self.social_login_data = {
            "provider": "facebook",
            "access_token": "EAAF0xkrzTnQBZCNDEBHIhwEB8AgYptZCeuqobAZC7Nq7IiZC3tUx15BvptU0Cj1SZBX0s"
        }

        self.twitter_login_data = {
            "provider": "twitter",
            "access_token": "4756399233-iOILAWjwYoZ2yaehdI3BPn7drvXAa3yvMz63pAm",
            "access_token_secret": "iYPNrBm7OlbyIrGLtcWi5iOwHJdlNJFQx338SLDsEXyu5"
        }

        self.invalid_provider = {
            "provider": "github",
            "access_token": "absnabshajhakjsajhbajhbajbajbnkwshiwhoijqlwjmslkam.L,PQWSWJDQWJH"
        }

        self.invalid_token = {
            "provider": "facebook",
            "access_token": "12233890900-0-0-0--0--00-0-djjkjknsknjsknkjsn"
        }
        self.comment_data = {
            "comment": "I like this article"
        }

        self.rating_data = {
            "rating": "5"
        }
        self.highlight_data = {
            "highlight": "the first",
            "comment": "this is a sample comment for highlight",
            "location": "body"
        }
        self.in_existent_highlight_data = {
            "highlight": "this is so inexistent data, unique",
            "comment": "this is a sample comment for highlight",
            "location": "body"
        }
