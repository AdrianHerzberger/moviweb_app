from .user_storage import db, User
from .movie_storage import db, Movie
from .review_storage import db, Review
from .director_storage import db, Director
from .data_manager_interface import DataManagerInterface
from sqlalchemy.exc import SQLAlchemyError


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_all_users(self):
        return User.query.all()
    
    def get_all_directors(self):
        return Director.query.all()

    def get_all_movies(self):
        return Movie.query.all()

    def get_all_reviews(self):
        return Review.query.all()

    def add_user(self, first_name, last_name, birth_date):
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
        )
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, movie_title, release_date, directory, movie_rating, user_id):
        try:
            new_movie = Movie(
                movie_title=movie_title,
                release_date=release_date,
                directory=directory,
                movie_rating=movie_rating,
                user_id=user_id,
            )
            self.db.session.add(new_movie)
            self.db.session.commit()
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Error adding movie: {e}")

    def update_movie(
        self, movie_id, movie_title, release_date, directory, movie_rating, user_id
    ):
        update_movie = Movie.query.get(movie_id)
        if update_movie:
            update_movie.movie_title = movie_title
            update_movie.release_date = release_date
            update_movie.directory = directory
            update_movie.movie_rating = movie_rating
            update_movie.user_id = user_id
            try:
                self.db.session.commit()
            except SQLAlchemyError as e:
                self.db.session.rollback()
                print(f"Error updating movie: {e}")
                return None
            return update_movie
        return None

    def delete_movie(self, movie_id):
        delete_movie = Movie.query.get(movie_id)
        if delete_movie:
            try:
                self.db.session.delete(delete_movie)
                self.db.session.commit()
            except SQLAlchemyError as e:
                self.db.session.rollback()
                print(f"Error deleting movie: {e}")
                return False
        return True


    def get_movie_by_id(self, movie_id):
        return Movie.query.get(movie_id)

    def add_review(self, review_text, rating, user_id, movie_id):
        try:
            new_rating = Review(
                review_text=review_text,
                rating=rating,
                user_id=user_id,
                movie_id=movie_id,
            )
            self.db.session.add(new_rating)
            self.db.session.commit()
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Error adding movie: {e}")
            
    def add_director(self, director_name, birth_date, movie_id):
        try:
            new_director = Director(
                director_name=director_name,
                birth_date=birth_date,
                movie_id=movie_id
            )
            self.db.session.add(new_director)
            self.db.session.commit()
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Error adding movie: {e}")
