from typing import List, Dict, Optional
from datetime import datetime, date
from library_app.models import Book, Loan, User

def binary_search_book_by_id(books: List[Book], book_id: int) -> Optional[Book]:
    """Binary search to find a book by ID in a sorted list of books.
    
    Args:
        books: List of Book objects, sorted by book_id.
        book_id: ID of the book to find.
    Returns:
        Book object if found, else None.
    Time Complexity: O(log n)
    """
    left, right = 0, len(books) - 1
    while left <= right:
        mid = (left + right) // 2
        if books[mid].id == book_id:
            return books[mid]
        elif books[mid].id < book_id:
            left = mid + 1
        else:
            right = mid - 1
    return None

def merge_sort_loans_by_due_date(loans: List[Loan]) -> List[Loan]:
    """Merge sort loans by due date.
    
    Args:
        loans: List of Loan objects.
    Returns:
        Sorted list of Loan objects by due_date (ascending).
    Time Complexity: O(n log n)
    """
    if len(loans) <= 1:
        return loans
    mid = len(loans) // 2
    left = merge_sort_loans_by_due_date(loans[:mid])
    right = merge_sort_loans_by_due_date(loans[mid:])
    return merge(left, right, key=lambda x: x.due_date)

def merge(left: List[Loan], right: List[Loan], key) -> List[Loan]:
    """Helper function for merge sort."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def filter_overdue_loans(loans: List[Loan], current_date: date) -> List[Loan]:
    """Filter loans that are overdue based on current date.
    
    Args:
        loans: List of Loan objects.
        current_date: Date to check against due_date.
    Returns:
        List of overdue Loan objects.
    Time Complexity: O(n)
    """
    return [loan for loan in loans if loan.due_date < current_date and not loan.return_date]

def quick_sort_books_by_title(books: List[Book]) -> List[Book]:
    """Quick sort books by title.
    
    Args:
        books: List of Book objects.
    Returns:
        Sorted list of Book objects by title (ascending).
    Time Complexity: O(n log n) average
    """
    if len(books) <= 1:
        return books
    pivot = books[len(books) // 2].title
    left = [b for b in books if b.title < pivot]
    middle = [b for b in books if b.title == pivot]
    right = [b for b in books if b.title > pivot]
    return quick_sort_books_by_title(left) + middle + quick_sort_books_by_title(right)

def find_top_borrowers(loans: List[Loan], limit: int = 5) -> List[Dict]:
    """Find top N users by number of loans.
    
    Args:
        loans: List of Loan objects.
        limit: Number of top borrowers to return.
    Returns:
        List of dicts with user_id and loan_count.
    Time Complexity: O(n)
    """
    from collections import Counter
    user_counts = Counter(loan.user_id for loan in loans)
    return [{"user_id": user_id, "loan_count": count} for user_id, count in user_counts.most_common(limit)]

def recommend_books_by_category(user: User, books: List[Book]) -> List[Book]:
    """Recommend books based on user’s past loan categories.
    
    Args:
        user: User object.
        books: List of Book objects.
    Returns:
        List of recommended Book objects.
    Time Complexity: O(n)
    """
    user_loans = Loan.objects.filter(user=user).select_related('book')
    categories = {loan.book.category for loan in user_loans}
    return [book for book in books if book.category in categories][:5]

def linear_search_book_by_title(books: List[Book], title: str) -> Optional[Book]:
    """Linear search for a book by title (case-insensitive).
    
    Args:
        books: List of Book objects.
        title: Title to search for.
    Returns:
        Book object if found, else None.
    Time Complexity: O(n)
    """
    title = title.lower()
    for book in books:
        if book.title.lower() == title:
            return book
    return None

def calculate_fine(loan: Loan, daily_fine: float = 1.0) -> float:
    """Calculate fine for an overdue loan.
    
    Args:
        loan: Loan object.
        daily_fine: Fine per day overdue.
    Returns:
        Total fine amount.
    Time Complexity: O(1)
    """
    if loan.return_date or loan.due_date >= date.today():
        return 0.0
    days_overdue = (date.today() - loan.due_date).days
    return days_overdue * daily_fine

def group_loans_by_category(loans: List[Loan]) -> Dict[str, List[Loan]]:
    """Group loans by book category.
    
    Args:
        loans: List of Loan objects.
    Returns:
        Dict mapping category to list of loans.
    Time Complexity: O(n)
    """
    result = {}
    for loan in loans:
        category = loan.book.category
        if category not in result:
            result[category] = []
        result[category].append(loan)
    return result

def find_available_books(books: List[Book], loans: List[Loan]) -> List[Book]:
    """Find books that are currently available (not loaned).
    
    Args:
        books: List of Book objects.
        loans: List of active Loan objects.
    Returns:
        List of available Book objects.
    Time Complexity: O(n)
    """
    loaned_book_ids = {loan.book_id for loan in loans if not loan.return_date}
    return [book for book in books if book.id not_d in loaned_book_ids]
