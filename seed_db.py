import sys
import os
sys.path.append('.')

from config.dbConfig import get_db, Base, engine
from domain.Books import Book
from domain.user import User
from domain.UserProfile import UserProfile
from domain.Borrowed import Borrowed
from domain.BooksRate import BooksRate
import service.auth.authHelper as AuthHelper

def seed_database():
    # Drop and recreate all tables for a fresh start
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)

    db = next(get_db())

    # Seed Books
    print("Seeding books...")
    books_data = [
        # Sci-Fi
        Book(title='Dune', author='Frank Herbert', category='Sci-Fi', image='', stock=5, description='A sci-fi classic', year=1965, language='English', pages=412, isbn='9780441172719'),
        Book(title='Neuromancer', author='William Gibson', category='Sci-Fi', image='', stock=3, description='Cyberpunk origin', year=1984, language='English', pages=271, isbn='9780441569595'),
        Book(title='Foundation', author='Isaac Asimov', category='Sci-Fi', image='', stock=4, description='Galactic Empire', year=1951, language='English', pages=255, isbn='9780553293357'),
        Book(title='Snow Crash', author='Neal Stephenson', category='Sci-Fi', image='', stock=2, description='Metaverse explorer', year=1992, language='English', pages=470, isbn='9780553380958'),
        Book(title='The Martian', author='Andy Weir', category='Sci-Fi', image='', stock=6, description='Stranded on Mars', year=2011, language='English', pages=369, isbn='9780553418026'),
        Book(title='Ender\'s Game', author='Orson Scott Card', category='Sci-Fi', image='', stock=7, description='Battle school', year=1985, language='English', pages=324, isbn='9780812550702'),
        Book(title='Brave New World', author='Aldous Huxley', category='Sci-Fi', image='', stock=4, description='Dystopian future', year=1932, language='English', pages=311, isbn='9780060850524'),
        Book(title='Fahrenheit 451', author='Ray Bradbury', category='Sci-Fi', image='', stock=5, description='Burning books', year=1953, language='English', pages=158, isbn='9781451673319'),
        Book(title='The Left Hand of Darkness', author='Ursula K. Le Guin', category='Sci-Fi', image='', stock=3, description='Alien culture', year=1969, language='English', pages=286, isbn='9780441478125'),
        Book(title='Hyperion', author='Dan Simmons', category='Sci-Fi', image='', stock=4, description='Pilgrimage to Hyperion', year=1989, language='English', pages=482, isbn='9780553283686'),

        # Fantasy
        Book(title='The Hobbit', author='J.R.R. Tolkien', category='Fantasy', image='', stock=5, description='An unexpected journey', year=1937, language='English', pages=310, isbn='9780547928227'),
        Book(title='A Game of Thrones', author='George R.R. Martin', category='Fantasy', image='', stock=4, description='Winter is coming', year=1996, language='English', pages=694, isbn='9780553573404'),
        Book(title='The Name of the Wind', author='Patrick Rothfuss', category='Fantasy', image='', stock=3, description='Kingkiller Chronicle', year=2007, language='English', pages=662, isbn='9780756404741'),
        Book(title='The Way of Kings', author='Brandon Sanderson', category='Fantasy', image='', stock=6, description='Stormlight Archive', year=2010, language='English', pages=1007, isbn='9780765326355'),
        Book(title='Mistborn', author='Brandon Sanderson', category='Fantasy', image='', stock=5, description='The Final Empire', year=2006, language='English', pages=541, isbn='9780765350381'),
        Book(title='American Gods', author='Neil Gaiman', category='Fantasy', image='', stock=3, description='Old gods vs new', year=2001, language='English', pages=465, isbn='9780060558123'),
        Book(title='Good Omens', author='Terry Pratchett', category='Fantasy', image='', stock=4, description='The end is nigh', year=1990, language='English', pages=432, isbn='9780060853983'),
        Book(title='The Color of Magic', author='Terry Pratchett', category='Fantasy', image='', stock=2, description='Discworld start', year=1983, language='English', pages=206, isbn='9780061020353'),
        Book(title='Harry Potter and the Sorcerer\'s Stone', author='J.K. Rowling', category='Fantasy', image='', stock=10, description='The boy who lived', year=1997, language='English', pages=309, isbn='9780439708180'),
        Book(title='The Lies of Locke Lamora', author='Scott Lynch', category='Fantasy', image='', stock=4, description='Gentleman Bastards', year=2006, language='English', pages=499, isbn='9780553588941'),

        # Programming
        Book(title='Clean Code', author='Robert C. Martin', category='Programming', image='', stock=4, description='Craftsmanship', year=2008, language='English', pages=464, isbn='9780132350884'),
        Book(title='The Pragmatic Programmer', author='David Thomas', category='Programming', image='', stock=5, description='Professionalism', year=1999, language='English', pages=352, isbn='9780135957059'),
        Book(title='Design Patterns', author='Erich Gamma', category='Programming', image='', stock=3, description='Reusable software', year=1994, language='English', pages=395, isbn='9780201633610'),
        Book(title='Refactoring', author='Martin Fowler', category='Programming', image='', stock=2, description='Improving design', year=1999, language='English', pages=464, isbn='9780201485677'),
        Book(title='Head First Design Patterns', author='Eric Freeman', category='Programming', image='', stock=4, description='Visual learning', year=2004, language='English', pages=638, isbn='9780596007126'),
        Book(title='Introduction to Algorithms', author='Thomas H. Cormen', category='Programming', image='', stock=3, description='Algorithm bible', year=1990, language='English', pages=1312, isbn='9780262033848'),
        Book(title='Structure and Interpretation of Computer Programs', author='Harold Abelson', category='Programming', image='', stock=2, description='Wizard book', year=1984, language='English', pages=657, isbn='9780262510875'),
        Book(title='Code Complete', author='Steve McConnell', category='Programming', image='', stock=4, description='Software construction', year=1993, language='English', pages=960, isbn='9780735619678'),
        Book(title='You Don\'t Know JS', author='Kyle Simpson', category='Programming', image='', stock=5, description='Deep JS', year=2014, language='English', pages=100, isbn='9781491904244'),
        Book(title='Fluent Python', author='Luciano Ramalho', category='Programming', image='', stock=6, description='Effective Python', year=2015, language='English', pages=792, isbn='9781491946008'),

        # Self-Help / Motivation
        Book(title='Atomic Habits', author='James Clear', category='Self-Help', image='', stock=6, description='Tiny changes', year=2018, language='English', pages=320, isbn='9780735211292'),
        Book(title='Deep Work', author='Cal Newport', category='Self-Help', image='', stock=4, description='Focused success', year=2016, language='English', pages=304, isbn='9781455586691'),
        Book(title='The 7 Habits of Highly Effective People', author='Stephen R. Covey', category='Self-Help', image='', stock=5, description='Personal change', year=1989, language='English', pages=381, isbn='9780743269513'),
        Book(title='Thinking, Fast and Slow', author='Daniel Kahneman', category='Self-Help', image='', stock=3, description='Two systems', year=2011, language='English', pages=499, isbn='9780374275631'),
        Book(title='Mindset', author='Carol S. Dweck', category='Self-Help', image='', stock=4, description='Growth mindset', year=2006, language='English', pages=320, isbn='9780345472328'),
        Book(title='Man\'s Search for Meaning', author='Viktor E. Frankl', category='Self-Help', image='', stock=5, description='Logo-therapy', year=1946, language='English', pages=165, isbn='9780807014295'),
        Book(title='The Power of Habit', author='Charles Duhigg', category='Self-Help', image='', stock=3, description='Why we do what we do', year=2012, language='English', pages=416, isbn='9781400069286'),
        Book(title='Outliers', author='Malcolm Gladwell', category='Self-Help', image='', stock=4, description='Story of success', year=2008, language='English', pages=304, isbn='9780316017923'),
        Book(title='Grit', author='Angela Duckworth', category='Self-Help', image='', stock=5, description='Passion and perseverance', year=2016, language='English', pages=352, isbn='9781501111105'),
        Book(title='Start with Why', author='Simon Sinek', category='Self-Help', image='', stock=6, description='Inspire action', year=2009, language='English', pages=256, isbn='9781591846444'),

        # General Fiction / Classics
        Book(title='To Kill a Mockingbird', author='Harper Lee', category='Classic', image='', stock=5, description='Racial injustice', year=1960, language='English', pages=281, isbn='9780061120084'),
        Book(title='1984', author='George Orwell', category='Classic', image='', stock=6, description='Big Brother', year=1949, language='English', pages=328, isbn='9780451524935'),
        Book(title='Pride and Prejudice', author='Jane Austen', category='Classic', image='', stock=3, description='Manners and marriage', year=1813, language='English', pages=279, isbn='9780141439518'),
        Book(title='The Great Gatsby', author='F. Scott Fitzgerald', category='Classic', image='', stock=4, description='American Dream', year=1925, language='English', pages=180, isbn='9780743273565'),
        Book(title='The Catcher in the Rye', author='J.D. Salinger', category='Classic', image='', stock=5, description='Teenage angst', year=1951, language='English', pages=214, isbn='9780316769174'),
        Book(title='Moby-Dick', author='Herman Melville', category='Classic', image='', stock=2, description='The whale', year=1851, language='English', pages=635, isbn='9780142437247'),
        Book(title='War and Peace', author='Leo Tolstoy', category='Classic', image='', stock=1, description='Napoleonic wars', year=1869, language='English', pages=1225, isbn='9780140447934'),
        Book(title='The Odyssey', author='Homer', category='Classic', image='', stock=3, description='Epic journey', year=-800, language='Greek', pages=448, isbn='9780140268867'),
        Book(title='Crime and Punishment', author='Fyodor Dostoevsky', category='Classic', image='', stock=2, description='Guilt and redemption', year=1866, language='Russian', pages=671, isbn='9780140449136'),
        Book(title='The Brothers Karamazov', author='Fyodor Dostoevsky', category='Classic', image='', stock=2, description='Faith and reason', year=1880, language='Russian', pages=796, isbn='9780374528379'),
        Book(title='Jane Eyre', author='Charlotte Brontë', category='Classic', image='', stock=3, description='Inner strength', year=1847, language='English', pages=532, isbn='9780141441146'),
        Book(title='Wuthering Heights', author='Emily Brontë', category='Classic', image='', stock=4, description='Obsessive love', year=1847, language='English', pages=416, isbn='9780141439556'),

        # Mystery / Thriller
        Book(title='The Girl with the Dragon Tattoo', author='Stieg Larsson', category='Mystery', image='', stock=8, description='Hacker investigates mystery', year=2005, language='Swedish', pages=590, isbn='9780307454546'),
        Book(title='Gone Girl', author='Gillian Flynn', category='Mystery', image='', stock=5, description='Marriage gone wrong', year=2012, language='English', pages=432, isbn='9780307588371'),
        Book(title='The Da Vinci Code', author='Dan Brown', category='Mystery', image='', stock=10, description='Symbologist on the run', year=2003, language='English', pages=454, isbn='9780307474278'),
        Book(title='And Then There Were None', author='Agatha Christie', category='Mystery', image='', stock=6, description='Ten strangers on an island', year=1939, language='English', pages=272, isbn='9780062073488'),
        Book(title='The Silent Patient', author='Alex Michaelides', category='Mystery', image='', stock=7, description='Woman refuses to speak', year=2019, language='English', pages=336, isbn='9781250301697'),
        Book(title='The Girl on the Train', author='Paula Hawkins', category='Mystery', image='', stock=4, description='Witness to a crime', year=2015, language='English', pages=336, isbn='9781594634024'),
        Book(title='Shutter Island', author='Dennis Lehane', category='Mystery', image='', stock=3, description='Asylum investigation', year=2003, language='English', pages=369, isbn='9780062068415'),
        Book(title='The Silence of the Lambs', author='Thomas Harris', category='Mystery', image='', stock=2, description='FBI meets Hannibal', year=1988, language='English', pages=367, isbn='9780312924584'),
        Book(title='Big Little Lies', author='Liane Moriarty', category='Mystery', image='', stock=5, description='Mothers and murder', year=2014, language='English', pages=460, isbn='9780399167065'),
        Book(title='Sharp Objects', author='Gillian Flynn', category='Mystery', image='', stock=3, description='Reporter returns home', year=2006, language='English', pages=254, isbn='9780307341556'),

        # Romance
        Book(title='The Notebook', author='Nicholas Sparks', category='Romance', image='', stock=6, description='Enduring love', year=1996, language='English', pages=214, isbn='9780446605236'),
        Book(title='Outlander', author='Diana Gabaldon', category='Romance', image='', stock=4, description='Time-traveling romance', year=1991, language='English', pages=850, isbn='9780440212560'),
        Book(title='Me Before You', author='Jojo Moyes', category='Romance', image='', stock=5, description='Tragic love story', year=2012, language='English', pages=369, isbn='9780670026609'),
        Book(title='The Fault in Our Stars', author='John Green', category='Romance', image='', stock=7, description='Star-crossed lovers', year=2012, language='English', pages=313, isbn='9780525478812'),
        Book(title='Twilight', author='Stephenie Meyer', category='Romance', image='', stock=10, description='Vampire romance', year=2005, language='English', pages=498, isbn='9780316015844'),
        Book(title='Fifty Shades of Grey', author='E.L. James', category='Romance', image='', stock=8, description='Passionate affair', year=2011, language='English', pages=514, isbn='9780345803481'),
        Book(title='The Time Traveler\'s Wife', author='Audrey Niffenegger', category='Romance', image='', stock=3, description='Love out of time', year=2003, language='English', pages=546, isbn='9780156029438'),
        Book(title='A Walk to Remember', author='Nicholas Sparks', category='Romance', image='', stock=4, description='Heartbreaking romance', year=1999, language='English', pages=240, isbn='9780446608958'),
        Book(title='It Ends with Us', author='Colleen Hoover', category='Romance', image='', stock=9, description='Emotional journey', year=2016, language='English', pages=384, isbn='9781501110368'),
        Book(title='The Hating Game', author='Sally Thorne', category='Romance', image='', stock=5, description='Enemies to lovers', year=2016, language='English', pages=384, isbn='9780062439598'),

        # Historical Fiction
        Book(title='The Book Thief', author='Markus Zusak', category='Historical', image='', stock=6, description='Death tells a story', year=2005, language='English', pages=552, isbn='9780375842207'),
        Book(title='All the Light We Cannot See', author='Anthony Doerr', category='Historical', image='', stock=4, description='WWII paths cross', year=2014, language='English', pages=531, isbn='9781476746586'),
        Book(title='The Kite Runner', author='Khaled Hosseini', category='Historical', image='', stock=5, description='Friendship in Afghanistan', year=2003, language='English', pages=371, isbn='9781594480003'),
        Book(title='The Help', author='Kathryn Stockett', category='Historical', image='', stock=7, description='Maids in Mississippi', year=2009, language='English', pages=451, isbn='9780399155345'),
        Book(title='The Nightingale', author='Kristin Hannah', category='Historical', image='', stock=5, description='Sisters in France', year=2015, language='English', pages=440, isbn='9780312577223'),
        Book(title='Memoirs of a Geisha', author='Arthur Golden', category='Historical', image='', stock=3, description='Life of a Geisha', year=1997, language='English', pages=448, isbn='9780679781585'),
        Book(title='The Boy in the Striped Pajamas', author='John Boyne', category='Historical', image='', stock=4, description='Innocence in WWII', year=2006, language='English', pages=216, isbn='9780385751537'),
        Book(title='The Pillars of the Earth', author='Ken Follett', category='Historical', image='', stock=6, description='Cathedral building', year=1989, language='English', pages=976, isbn='9780451166890'),
        Book(title='A Thousand Splendid Suns', author='Khaled Hosseini', category='Historical', image='', stock=5, description='Women in Kabul', year=2007, language='English', pages=384, isbn='9781594489501'),
        Book(title='The Alchemist', author='Paulo Coelho', category='Historical', image='', stock=8, description='Follow your dreams', year=1988, language='Portuguese', pages=163, isbn='9780061122415'),

        # Harry Potter Series
        Book(title='Harry Potter and the Chamber of Secrets', author='J.K. Rowling', category='Fantasy', image='', stock=8, description='The chamber is opened', year=1998, language='English', pages=341, isbn='9780439064873'),
        Book(title='Harry Potter and the Prisoner of Azkaban', author='J.K. Rowling', category='Fantasy', image='', stock=7, description='The dementors are coming', year=1999, language='English', pages=435, isbn='9780439136365'),
        Book(title='Harry Potter and the Goblet of Fire', author='J.K. Rowling', category='Fantasy', image='', stock=6, description='The Triwizard Tournament', year=2000, language='English', pages=734, isbn='9780439139601'),
        Book(title='Harry Potter and the Order of the Phoenix', author='J.K. Rowling', category='Fantasy', image='', stock=9, description='Dumbledore\'s Army', year=2003, language='English', pages=870, isbn='9780439358071'),
        Book(title='Harry Potter and the Half-Blood Prince', author='J.K. Rowling', category='Fantasy', image='', stock=8, description='The prince\'s tale', year=2005, language='English', pages=652, isbn='9780439785969'),
        Book(title='Harry Potter and the Deathly Hallows', author='J.K. Rowling', category='Fantasy', image='', stock=10, description='The final battle', year=2007, language='English', pages=759, isbn='9780545010221'),

        # Arabic Famous Novels
        Book(title='The Cairo Trilogy', author='Naguib Mahfouz', category='Historical', image='', stock=5, description='Life in Cairo', year=1956, language='Arabic', pages=1313, isbn='9780307310491'),
        Book(title='Season of Migration to the North', author='Tayeb Salih', category='Fiction', image='', stock=4, description='East meets West', year=1966, language='Arabic', pages=169, isbn='9781590173022'),
        Book(title='The Yacoubian Building', author='Alaa Al Aswany', category='Fiction', image='', stock=6, description='Modern Egyptian society', year=2002, language='Arabic', pages=273, isbn='9780060878132'),
        Book(title='Frankenstein in Baghdad', author='Ahmed Saadawi', category='Fantasy', image='', stock=3, description='A monster in war-torn Iraq', year=2013, language='Arabic', pages=281, isbn='9780143128793'),
        Book(title='Men in the Sun', author='Ghassan Kanafani', category='Fiction', image='', stock=5, description='Palestinian refugees', year=1962, language='Arabic', pages=120, isbn='9780894108570')
    ]

    for b in books_data:
        db.add(b)
    
    db.commit()
    print(f"Successfully added {len(books_data)} books.")

    # Seed Users
    print("Seeding users...")
    users_data = [
        {"full_name": "Admin Librarian", "email": "admin@library.com", "password": "password123", "role": "librarian"},
        {"full_name": "John Doe", "email": "john@example.com", "password": "password123", "role": "user"},
        {"full_name": "Jane Smith", "email": "jane@example.com", "password": "password123", "role": "user"},
        {"full_name": "Alice Johnson", "email": "alice@example.com", "password": "password123", "role": "user"},
    ]

    for u_info in users_data:
        hashed_password = AuthHelper.hash_password(u_info["password"])
        new_user = User(
            full_name=u_info["full_name"],
            email=u_info["email"],
            password=hashed_password,
            role=u_info["role"]
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create profile
        new_profile = UserProfile(user_id=new_user.id, bio=f"I am {new_user.full_name}")
        db.add(new_profile)
        db.commit()
        print(f"Added user: {new_user.email}")



    # Seed Borrowed Books
    print("Seeding borrowed books...")
    borrowed_data = [
        Borrowed(reader_id=2, librarian_id=1, book_id=1, borrow_date='2026-04-01', return_date='2026-04-15', state='Returned'),
        Borrowed(reader_id=2, librarian_id=1, book_id=2, borrow_date='2026-04-10', return_date='2026-04-24', state='Approved'),
        Borrowed(reader_id=3, librarian_id=1, book_id=10, borrow_date='2026-04-20', return_date='2026-05-04', state='Pending'),
        Borrowed(reader_id=4, librarian_id=1, book_id=20, borrow_date='2026-04-22', return_date='2026-05-06', state='Pending'),
        Borrowed(reader_id=2, librarian_id=1, book_id=83, borrow_date='2026-03-01', return_date='2026-03-15', state='Returned'),
        Borrowed(reader_id=3, librarian_id=1, book_id=84, borrow_date='2026-04-18', return_date='2026-05-02', state='Approved'),
    ]

    for b in borrowed_data:
        db.add(b)
    
    db.commit()
    print(f"Successfully added {len(borrowed_data)} borrowed records.")

    # Seed Book Rates
    print("Seeding book rates...")
    import random
    rate_data = []
    # Give random ratings to the first 50 books
    for book_id in range(1, 51):
        rate_data.append(BooksRate(book_id=book_id, user_id=random.choice([2, 3, 4]), rate=random.randint(3, 5), review="Great book!"))
    
    # Give high ratings to Harry Potter
    for book_id in range(83, 89):
        rate_data.append(BooksRate(book_id=book_id, user_id=2, rate=5, review="Magical!"))
        rate_data.append(BooksRate(book_id=book_id, user_id=3, rate=5, review="Love it!"))

    for r in rate_data:
        db.add(r)
        
    db.commit()
    print(f"Successfully added {len(rate_data)} rating records.")

    print("Seeding complete!")


if __name__ == "__main__":
    seed_database()
