import sys

with open(r'c:\Users\Woundex\Desktop\norest\BookManagement\seed_db.py', 'r', encoding='utf-8') as f:
    content = f.read()

seed_borrowed_and_rate = """

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
"""

content = content.replace('    print("Seeding complete!")', seed_borrowed_and_rate)

with open(r'c:\Users\Woundex\Desktop\norest\BookManagement\seed_db.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated seed_db.py with Borrowed and BooksRate')
