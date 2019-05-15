
from rest_framework import viewsets
from .models import ReportModel, ArticleModel
from .serializers import ReportSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .utils import user_object
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, DestroyAPIView
from ...apps.authentication.serializers import UserSerializer


class ReportView(viewsets.ModelViewSet):
    """
    The report View
    """

    queryset = ReportModel.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        post:
        The create report endpoint
        """

        try:
            report = ArticleModel.objects.filter(id=request.data['article'])[0]
        except:
            return Response(
                {"status": 404,
                 "error": "The article you are trying "
                 "to report does not exist."},
                status=404)

        if report.author == request.user:
            return Response(
                {"status": 403,
                 "error": "You cannot report your own article."},
                status=403)

        request.data['user'] = request.user.id
        if self.is_duplicate(request):
            return Response(
                {"status": 409,
                 "error": "You have already reported this "
                 "article with the same reason."},
                status=409)
        return self.create_report(request)

    def create_report(self, request):
        """
        Function for creating a report
        """
        request.data['reporter'] = request.user.id
        response = super().create(request)
        response.data['reported_article']['author'] = user_object(
            response.data['reported_article']['author'].id)
        return Response({"status": 201, "data": response.data}, status=201)

    def list(self, request):
        """
        get:
        The get reports endpoint
        """

        page_limit = request.GET.get('limit')

        if not page_limit or not page_limit.isdigit():
            page_limit = 9

        queryset = ReportModel.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = page_limit

        page = paginator.paginate_queryset(queryset, request)
        serializer = ReportSerializer(page, many=True,
                                      context={'request': request})
        dictionary = None
        data = []
        for report in serializer.data:  # pragma: no cover
            dictionary = dict(report)
            dictionary['reported_article']['author'] = user_object(
                dictionary['reported_article']['author'].id)
            data.append(dictionary)

        return paginator.get_paginated_response(data=data)

    def retrieve(self, request, pk=None):
        """
        get:
        The get one report endpoint
        """

        try:
            report = ReportModel.objects.filter(id=pk)[0]
        except:
            return Response({"status": 404,
                             "error": "Report with id {} "
                             "not found".format(pk)},
                            status=404)

        if request.user != report.user:
            return Response(
                {"status": 401,
                 "error": "You are not authorized to view this report"},
                status=401)

        serializer = ReportSerializer(report,
                                      context={'request': request})
        response = Response(serializer.data)
        response.data['reported_article']['author'] = user_object(
            response.data['reported_article']['author'].id)
        return Response({"status": 200,
                         "data": response.data},
                        status=200)

    def update(self, request, pk=None, *args, **kwargs):
        """
        put:
        The update report endpoint
        """

        try:
            report = ReportModel.objects.filter(id=pk)[0]
        except:
            return Response(
                {"status": 404,
                 "error": "Report with id {} not found".format(pk)},
                status=404)

        if self.is_duplicate(request):
            return Response(
                {"status": 409,
                 "error": "You have already reported this "
                 "article with the same reason."},
                status=409)

        serializer = ReportSerializer(report, context={'request': request})

        if request.user != report.user:
            return Response(
                {"status": 401,
                 "error": "You are not authorized to edit this report"},
                status=401)

        serializer = ReportSerializer(report,
                                      data=request.data,
                                      context={'request': request},
                                      partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data)
        response.data['reported_article']['author'] = user_object(
            response.data['reported_article']['author'].id)
        return Response({"status": 201,
                         "data": response.data},
                        status=201)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        delete:
        The delete report endpoint
        """
        try:
            report = ReportModel.objects.filter(id=pk)[0]

            if request.user != report.user:
                return Response({'status': 401, 'error': "You are not "
                                 "authorized to delete this report."},
                                status=401)

            self.perform_destroy(report)
            return Response({'status': 200,
                             'data': 'Report deleted successfully'},
                            status=200)
        except:
            return Response(
                {'status': 404,
                 'error': 'Report with id {} not found'.format(pk)},
                status=404)

    def is_duplicate(self, request):
        """
        Function for checking if a duplicate record exists
        """
        duplicate_records = ReportModel.objects.filter(
            user=request.user, reason=request.data['reason'].strip())

        if duplicate_records.exists():
            return True
        return False


class ReportList(ListAPIView):
    """
    This view is to be used to fetch all reports by the admin
    """

    permission_classes = [IsAdminUser]
    queryset = ReportModel.objects.all()
    serializer_class = ReportSerializer

    def list(self, request):
        """
        get:
        The get all reports endpoint
        """
        page_limit = request.GET.get('limit')

        if not page_limit or not page_limit.isdigit():
            page_limit = 9

        queryset = self.queryset
        paginator = PageNumberPagination()
        paginator.page_size = page_limit

        page = paginator.paginate_queryset(queryset, request)
        serializer = ReportSerializer(page, many=True,
                                      context={'request': request})

        dictionary = None
        data = []
        for report in serializer.data:  # pragma: no cover
            dictionary = dict(report)
            dictionary['reported_article']['author'] = user_object(
                dictionary['reported_article']['author'].id)
            data.append(dictionary)

        return paginator.get_paginated_response(data=data)


class DeleteView(DestroyAPIView):
    """
    This view is to be used to delete reports by the admin
    """

    permission_classes = [IsAdminUser]
    queryset = ReportModel.objects.all()
    serializer_class = ReportSerializer

    def destroy(self, request, id=None, *args, **kwargs):
        """
        delete:
        The delete report endpoint
        """
        try:
            report = ReportModel.objects.filter(id=id)[0]

            self.perform_destroy(report)
            return Response({'status': 200,
                             'data': 'Report deleted successfully'},
                            status=200)
        except:
            return Response(
                {'status': 404,
                 'error': 'Report with id {} not found'.format(id)},
                status=404)


class ArticleDeleteView(DestroyAPIView):
    """
    This view is to be used to delete articles by the admin
    """

    permission_classes = [IsAdminUser]
    queryset = ArticleModel.objects.all()
    serializer_class = ReportSerializer

    def destroy(self, request, slug=None, *args, **kwargs):
        """
        delete:
        The delete article endpoint
        """
        try:
            article = ArticleModel.objects.filter(slug=slug)[0]
            reports = ReportModel.objects.filter(article__slug=slug)

            self.perform_destroy(reports)
            self.perform_destroy(article)

            return Response({'status': 200,
                             'data': 'Article deleted successfully'},
                            status=200)
        except:
            return Response(
                {'status': 404,
                 'error': 'Article with id {} not found'.format(id)},
                status=404)
