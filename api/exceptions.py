class LibraryException(Exception):
    """Base class for all library-related exceptions."""
    def __init__(self, message: str):
        self.message = message

class BookNotFoundError(LibraryException):
    """Raised when a book is not found in the database."""
    def __init__(self, book_id: int):
        super().__init__(f"Libro con ID {book_id} no encontrado")

class UserNotFoundError(LibraryException):
    """Raised when a user is not found in the database."""
    def __init__(self, user_id: int):
        super().__init__(f"Usuario con ID {user_id} no encontrado")

class UserNotEligibleForLoanError(LibraryException):
    """Raised when a user cannot borrow a book (e.g., already has too many loans)."""
    pass

class BookAlreadyBorrowedError(LibraryException):
    """Raised when trying to borrow a book that is already out."""
    def __init__(self, book_id: int):
        super().__init__(f"El libro con ID {book_id} ya se encuentra prestado")
