from django.core.management.base import BaseCommand
from movies.models import Movie, Actor
import requests
from datetime import datetime

class Command(BaseCommand):
    help = '영화 데이터를 외부 API에서 불러와 DB에 저장합니다'

    def handle(self, *args, **kwargs):
        url = "http://43.200.28.219:1313/movies/"
        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            movies_data = res.json().get('movies', [])

            for m in movies_data:
                if Movie.objects.filter(title_kor=m.get('title_kor')).exists():
                    continue

                release_date = None
                if m.get('release_date'):
                    try:
                        release_date = datetime.strptime(m['release_date'], '%Y-%m-%d').date()
                    except ValueError:
                        pass

                movie = Movie.objects.create(
                    title_kor=m.get('title_kor'),
                    title_eng=m.get('title_eng'),
                    poster_url=m.get('poster_url'),
                    genre=m.get('genre'),
                    showtime=int(m.get('showtime', 0)),
                    release_date=release_date,
                    plot=m.get('plot'),
                    audience_score=m.get('rating'),
                    director_name=m.get('director_name'),
                    director_image_url=m.get('director_image_url'),
                )

                for actor in m.get('actors') or []:
                    Actor.objects.create(
                        movie=movie,
                        name=actor.get('name'),
                        character=actor.get('character'),
                        image_url=actor.get('image_url'),
                    )

            self.stdout.write(self.style.SUCCESS("✅ 영화 데이터 저장 완료"))

        except Exception as e:
            self.stderr.write(f"🚨 에러 발생: {str(e)}")
