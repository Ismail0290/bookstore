from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Book
import random

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        
        # Create sample books
        books_data = [
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'description': 'A classic novel about racial injustice in the American South.',
                'price': 12.99,
                'stock': random.randint(5, 50)
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'description': 'A dystopian novel set in a totalitarian society.',
                'price': 10.99,
                'stock': random.randint(5, 50)
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'description': 'A novel about the American Dream set in the Roaring Twenties.',
                'price': 9.99,
                'stock': random.randint(5, 50)
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'description': 'A romantic novel about societal expectations and marriage.',
                'price': 8.99,
                'stock': random.randint(5, 50)
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'description': 'A fantasy novel about a hobbit who goes on an adventure.',
                'price': 14.99,
                'stock': random.randint(5, 50)
            },
            {
                'title': 'Harry Potter and the Sorcerer\'s Stone',
                'author': 'J.K. Rowling',
                'description': 'The first book in the Harry Potter series.',
                'price': 15.99,
                'stock': random.randint(5, 50)
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'description': 'A novel about teenage alienation and identity.',
                'price': 11.99,
                'stock': random.randint(5, 50)
            },
            {
                'title': 'The Lord of the Rings',
                'author': 'J.R.R. Tolkien',
                'description': 'An epic fantasy trilogy about the quest to destroy the One Ring.',
                'price': 29.99,
                'stock': random.randint(5, 50)
            },
        ]
        
        for book_data in books_data:
            Book.objects.get_or_create(
                title=book_data['title'],
                defaults={
                    'author': book_data['author'],
                    'description': book_data['description'],
                    'price': book_data['price'],
                    'stock': book_data['stock']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Added {len(books_data)} sample books'))