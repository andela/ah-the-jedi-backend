errors = {
    "profile_missing": {"errors": "profile with this username does not exist",
                        "status": 404},
    "bad_image": {"errors": "Ensure that the file is an image",
                  "status": 400},
    "follow_exists": {"errors": "You already follow this user",
                      "status": 403},
    "unfollow_failed": {"errors": "You do not follow this user",
                        "status": 400},
    "self_follow": {"errors": "You cannot follow yourself",
                    "status": 403},


}
