from . import login
import pytest
from freeshelf.models import Book

_login = login

@pytest.fixture
def login(user, client):
    _login(user, client)

@pytest.mark.usefixtures("login")
class TestBookClass:
    def test_creating_book(self, client, session):
        response = client.post('/book/new', data=dict(
            title="Test Book",
            url="http://example.org/book/"
        ), follow_redirects=True)

        assert "has been added" in str(response.data)

        book = Book.query.filter_by(url="http://example.org/book/").first()
        assert book is not None


    def test_editing_book(self, client, session):
        book = Book(title="Test Book", url="http://example.org/book/")
        session.add(book)
        session.commit()

        response = client.post('/book/' + str(book.id) + "/edit", data=dict(
            title="Test Book",
            authors="Test Author",
            url="http://example.org/book/"
        ), follow_redirects=True)

        assert "has been updated" in str(response.data)

        session.refresh(book)
        assert book.authors == "Test Author"

