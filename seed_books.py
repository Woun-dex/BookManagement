import sys
sys.path.append('.')

from config.dbConfig import get_db
from domain.Books import Book

db = next(get_db())

books_data = [
    # Sci-Fi
    Book(title='Dune', author='Frank Herbert', category='Sci-Fi', cover_image='', stock=5),
    Book(title='Neuromancer', author='William Gibson', category='Sci-Fi', cover_image='', stock=3),
    Book(title='Foundation', author='Isaac Asimov', category='Sci-Fi', cover_image='', stock=4),
    Book(title='Snow Crash', author='Neal Stephenson', category='Sci-Fi', cover_image='', stock=2),
    Book(title='The Martian', author='Andy Weir', category='Sci-Fi', cover_image='', stock=6),
    Book(title='Ender\'s Game', author='Orson Scott Card', category='Sci-Fi', cover_image='', stock=7),
    Book(title='Brave New World', author='Aldous Huxley', category='Sci-Fi', cover_image='', stock=4),
    Book(title='Fahrenheit 451', author='Ray Bradbury', category='Sci-Fi', cover_image='', stock=5),
    Book(title='The Left Hand of Darkness', author='Ursula K. Le Guin', category='Sci-Fi', cover_image='', stock=3),
    Book(title='Hyperion', author='Dan Simmons', category='Sci-Fi', cover_image='', stock=4),

    # Fantasy
    Book(title='The Hobbit', author='J.R.R. Tolkien', category='Fantasy', cover_image='', stock=5),
    Book(title='A Game of Thrones', author='George R.R. Martin', category='Fantasy', cover_image='', stock=4),
    Book(title='The Name of the Wind', author='Patrick Rothfuss', category='Fantasy', cover_image='', stock=3),
    Book(title='The Way of Kings', author='Brandon Sanderson', category='Fantasy', cover_image='', stock=6),
    Book(title='Mistborn', author='Brandon Sanderson', category='Fantasy', cover_image='', stock=5),
    Book(title='American Gods', author='Neil Gaiman', category='Fantasy', cover_image='', stock=3),
    Book(title='Good Omens', author='Terry Pratchett', category='Fantasy', cover_image='', stock=4),
    Book(title='The Color of Magic', author='Terry Pratchett', category='Fantasy', cover_image='', stock=2),
    Book(title='Harry Potter and the Sorcerer\'s Stone', author='J.K. Rowling', category='Fantasy', cover_image='', stock=10),
    Book(title='The Lies of Locke Lamora', author='Scott Lynch', category='Fantasy', cover_image='', stock=4),

    # Programming
    Book(title='Clean Code', author='Robert C. Martin', category='Programming', cover_image='', stock=4),
    Book(title='The Pragmatic Programmer', author='David Thomas', category='Programming', cover_image='', stock=5),
    Book(title='Design Patterns', author='Erich Gamma', category='Programming', cover_image='', stock=3),
    Book(title='Refactoring', author='Martin Fowler', category='Programming', cover_image='', stock=2),
    Book(title='Head First Design Patterns', author='Eric Freeman', category='Programming', cover_image='', stock=4),
    Book(title='Introduction to Algorithms', author='Thomas H. Cormen', category='Programming', cover_image='', stock=3),
    Book(title='Structure and Interpretation of Computer Programs', author='Harold Abelson', category='Programming', cover_image='', stock=2),
    Book(title='Code Complete', author='Steve McConnell', category='Programming', cover_image='', stock=4),
    Book(title='You Don\'t Know JS', author='Kyle Simpson', category='Programming', cover_image='', stock=5),
    Book(title='Fluent Python', author='Luciano Ramalho', category='Programming', cover_image='', stock=6),

    # Self-Help / Motivation
    Book(title='Atomic Habits', author='James Clear', category='Self-Help', cover_image='', stock=6),
    Book(title='Deep Work', author='Cal Newport', category='Self-Help', cover_image='', stock=4),
    Book(title='The 7 Habits of Highly Effective People', author='Stephen R. Covey', category='Self-Help', cover_image='', stock=5),
    Book(title='Thinking, Fast and Slow', author='Daniel Kahneman', category='Self-Help', cover_image='', stock=3),
    Book(title='Mindset', author='Carol S. Dweck', category='Self-Help', cover_image='', stock=4),
    Book(title='Man\'s Search for Meaning', author='Viktor E. Frankl', category='Self-Help', cover_image='', stock=5),
    Book(title='The Power of Habit', author='Charles Duhigg', category='Self-Help', cover_image='', stock=3),
    Book(title='Outliers', author='Malcolm Gladwell', category='Self-Help', cover_image='', stock=4),
    Book(title='Grit', author='Angela Duckworth', category='Self-Help', cover_image='', stock=5),
    Book(title='Start with Why', author='Simon Sinek', category='Self-Help', cover_image='', stock=6),

    # General Fiction / Classics
    Book(title='To Kill a Mockingbird', author='Harper Lee', category='Classic', cover_image='', stock=5),
    Book(title='1984', author='George Orwell', category='Classic', cover_image='', stock=6),
    Book(title='Pride and Prejudice', author='Jane Austen', category='Classic', cover_image='', stock=3),
    Book(title='The Great Gatsby', author='F. Scott Fitzgerald', category='Classic', cover_image='', stock=4),
    Book(title='The Catcher in the Rye', author='J.D. Salinger', category='Classic', cover_image='', stock=5),
    Book(title='Moby-Dick', author='Herman Melville', category='Classic', cover_image='', stock=2),
    Book(title='War and Peace', author='Leo Tolstoy', category='Classic', cover_image='', stock=1),
    Book(title='The Odyssey', author='Homer', category='Classic', cover_image='', stock=3),
    Book(title='Crime and Punishment', author='Fyodor Dostoevsky', category='Classic', cover_image='', stock=2),
    Book(title='The Brothers Karamazov', author='Fyodor Dostoevsky', category='Classic', cover_image='', stock=2),
    Book(title='Jane Eyre', author='Charlotte Brontë', category='Classic', cover_image='', stock=3),
    Book(title='Wuthering Heights', author='Emily Brontë', category='Classic', cover_image='', stock=4)
]

for b in books_data:
    db.add(b)

db.commit()
print(f'Successfully added {len(books_data)} new books to the database!')
