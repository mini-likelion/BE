from rest_framework import serializers
from .models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']  # 작성 시는 content만 


class CommentResponseSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'nickname', 'content', 'created_at'] #id - x 

# class ActorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Actor
#         fields = ['name', 'character', 'image_url']

# #영화 세부 정보 조회 시 코멘트도 함께 
# class MovieDetailSerializer(serializers.ModelSerializer): 
#     comments = CommentResponseSerializer(many=True, read_only=True)
#     actors = ActorSerializer(many=True,read_only=True)

#     #필드 - 화면에 나타나는 순서 상관 x (프론트엔터에서 조정 가능 )
#     class Meta:
#         model = Movie
#         fields = [
#             'audience_score', 'critic_score', 'netizen_score',  # 평점
#             'genre', 'showtime', 'rating', 'release_date', 'plot',  # 영화 정보
#             'actors',  # 인물정보
#             'comments',  # 한줄평
#             'title_kor', 'title_eng', 'poster_url', 'director_name'  # 필요 시 추가
#         ]


