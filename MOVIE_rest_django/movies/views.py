from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, viewsets
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import *
from .service import get_client_ip, MovieFilter, PaginationMovies


# class MovieListView(APIView):
#     """Вывод списка фильмов"""
#     def get(self, request):
#         # movies = Movie.objects.filter(draft=False).annotate(
#         #     rating_user=models.Case(
#         #         models.When(ratings__ip=get_client_ip(request), then=True),
#         #         default=False,
#         #         output_field=models.BooleanField()
#         #     ),
#         # )
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count(
#                 "ratings",
#                 filter=models.Q(ratings__ip=get_client_ip(request))
#             )
#         ).annotate(
#             middle_star=models.Sum(models.F("ratings__star")) / models.Count(models.F("ratings"))
#         )
#         serializer = MovieListSerializer(movies, many=True)
#         return Response(serializer.data)

class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count(
                "ratings",
                filter=models.Q(ratings__ip=get_client_ip(self.request))
            )
        ).annotate(
            middle_star=models.Sum(models.F("ratings__star")) / models.Count(models.F("ratings"))
        )
        return movies

# class MovieDetailView(APIView):
#     def get(self, request, pk):
#         movie = Movie.objects.get(id=pk, draft=False)
#         serializer = MovieDetailSerializer(movie)
#         return Response(serializer.data)


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


# class ReviewCreateView(APIView):
#     """Добавление отзыва к фильму"""
#
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму через APIView"""
    serializer_class = ReviewCreateSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму ModelViewSet"""
    serializer_class = ReviewCreateSerializer

# class AddStarRatingView(APIView):
#     """Добавление рейтинга фильму"""
#
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)

class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorListView(generics.ListAPIView):
    """Вывод списка актеров и режиссеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод актера или режиссера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer




