from django.shortcuts import render
from django.http import HttpResponse
import requests


# API에서 영화 데이터 가져오기
def fetch_movies_from_api():
    url = "http://43.200.28.219:1313/movies/"
    response = requests.get(url)
    movies_data = response.json().get('movies', [])
    return movies_data


# 외부 API 데이터를 DB에 초기 저장
def init_db(request):
    movies = fetch_movies_from_api()
    for item in movies:
        Movie.objects.create(
            title_kor=item['title_kor'],
            poster_url=item['poster_url']
        )
    return HttpResponse("DB 초기화 완료!")


'''
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Movie
'''
'''

def movie_list(request):
    query = request.GET.get('q', '')  # 검색어 기본값 빈 문자열
    page = request.GET.get('page', 1)  # 기본값 1페이지

    # 검색어 포함된 영화만 필터링
    movies = Movie.objects.filter(title_kor__icontains=query)

    # 페이지네이션 설정
    paginator = Paginator(movies, 12)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    data = [
        {
            "title_kor": movie.title_kor,
            "poster_url": movie.poster_url
        }
        for movie in page_obj
    ]

    # 페이지 정보 포함
    response = {
        "movies": data,
        "page_info": {
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
        },
        "query": query  # 현재 검색어도 응답에 포함
    }

    return JsonResponse(response)
    '''
from django.http import JsonResponse
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()

    data = [
        {
            "title_kor": movie.title_kor,
            "poster_url": movie.poster_url
        }
        for movie in movies
    ]

    response = {
        "movies": data
    }

    return JsonResponse(response)

