from django.db import models
from django.contrib.postgres.fields import URLValidator


# Sample request data
# {
#   "profile": {
#     "username": "jake",
#     "bio": "I work at statefarm",
#     "image": "image-link",
#     "following": false, -for observer
#     "email": "this@gmail.com",
# bookmarked articles
# favorite articles
# user_articles
# }

# ACCEPTANCE CRITERIA
# As a User
# I want to get my profile created once I register to the application.
# I want my profile to display my bio, image/avatar and any other fields that "we" the dev team deem necessary. Let's get creative!
# I want to be able to View other users profiles, Edit my profile but I should NOT be able to edit another user's profile.

# Acceptance Criteria
# Scenario:
# Given a User registers to be a member of Authors Haven.

# Registration is done.
# User Profile is created.
# A timestamp is associated with the profile.

# Register listener


class UserProfile(models.Model):
    """
    The User Profile Model
    """

    username = models.CharField(max_length=30)
    bio = models.TextField(max_length=250)
    image = models.UrlField(validators=[URLValidator])
    following = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ""
