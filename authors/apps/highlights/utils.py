from rest_framework.response import Response
from rest_framework import status


types_or_locations = ["title", "description", "body"]


class HighlightUtils:
    def validate_location(self, location):
        if not location:
            return Response({
                "error": "Location field is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        elif location not in map(str.lower, types_or_locations):
            return Response({
                "error": "Location can only be title, description or body"
            }, status=status.HTTP_400_BAD_REQUEST)
