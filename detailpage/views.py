import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from .serializers import CommentCreateSerializer, CommentResponseSerializer

API_URL = "http://43.200.28.219:1313/movies/"

# 영화 상세 정보 + 코멘트
@api_view(['GET'])
def movie_detail(request, movie_id):
    res = requests.get(API_URL)
    if res.status_code != 200:
        return Response({"error": "영화 데이터를 가져오지 못했습니다."}, status=500)

    movies = res.json().get('movies', [])
    try:
        movie = movies[movie_id]  # 인덱스 기반 #0부터 시작 #수정 
    except IndexError:
        return Response({"error": "해당 영화가 존재하지 않습니다."}, status=404)

    comments = Comment.objects.filter(movie_id=movie_id).order_by('-created_at')
    serialized_comments = CommentResponseSerializer(comments, many=True).data

    # 외부 영화 데이터 + 코멘트 같이 반환
    movie['comments'] = serialized_comments
    return Response(movie)


# 코멘트 작성
@api_view(['POST'])
@permission_classes([IsAuthenticated]) #로그인 하지 않은 사람 #권한 제한 
def comment_create(request, movie_id):
    data = {
        "movie_id": movie_id,
        "user": request.user.id,
        "content": request.data.get("content")
    }
    serializer = CommentCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user, movie_id=movie_id)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

