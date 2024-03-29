# DASHMED LIBRARY RESTAPI SERVICE

## **Note:**
Before running the project, follow these steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/OxOv3rH4uL/Dashmed-API
   ```
2. **Move to the Repository Folder and Install Dependencies and Setup the Configuration**:
   ```bash
   cd Dashmed-API
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver   
   ```
3. **Running the RESTAPI**:
   
   Open the browser and visit the following link to enjoy the RESTAPI Service.
   ```bash
    http://127.0.0.1:8000/
    ```
4. **Docker Configuration**:
    This is for Docker Setup. Enter the command step by step.

    ```bash
    docker build -t dashmed-api .
    docker run -p 8000:8000
    ```

    You can now enjoy the RESTAPI Service by visiting the link
    ```bash
    http://0.0.0.0:8000/

5.  **For Running the Tests**:
    
    You need to clone this repository and follow the above setup except Docker Setup to run the Tests.

    ```bash
    python manage.py test libraryapi
    python manage.py test users
    ```

## **Introduction:**

Dashmed Library API uses Django for Backend Services. It handles data related to Library.

```bash
1. Title - Mandatory
2. Author - Mandatory
3. Publication Date - Optional
4. ISBN - Mandatory
5. Description - Optional
```

## **Features:**
1) Token-Based Authentication
2) Pagination of Datas
3) Fully Tested API

## **Endpoints**:
1) The First Step is to create user:
   - `/user/register` (POST):
    - User details such as name,email and password is provided. 

    ```bash
    http://127.0.0.1:8000/user/register
    {
        "name":"Test",
        "email":"test@gmail.com",
        "password":"pass123"
    }
    ```

    **Output:**
    ```bash
    {
        "message": "User Registered Successfully!"
    }
    ```

2) `/user/login` (POST):
    - Now we need to login so that JWT Token is created for authentication purpose.

    ```bash
    http://127.0.0.1:8000/user/login

    {
        "email":"test@gmail.com",
        "password":"pass123"
    }
    ```
    **Output:**
    ```bash
    {
        "message": "Login Successful!"
    }
    ```

3) **ADDING BOOKS:** 
    - `/api/books/` (POST):
     - First it verifies whether user has logged in or not and then it allows the user to add books.
     *Note: ISBN Format is XXX-XXX-XXXX*

    ```bash
    http://127.0.0.1:8000/api/books/

    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publication_date": "1960-07-11",
        "isbn": "978-006-1120",
        "description": "A gripping, heart-wrenching, and wholly remarkable tale of coming-of-age in a South poisoned by virulent prejudice."

    }
    ```

    **Output:**
    ```bash
    {
        "message": "Book Added Successfully!"
    }
    ```

4) **READ ALL BOOKS**:
    - `/api/books/` (GET):
    - Lists all the available books

    ```bash
    http://127.0.0.1:8000/api/books/
    ```

    **Output:**
    ```bash
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
            "title": "To Kill a Mockingbird",
            "isbn": "978-006-1120",
            "author": "Harper Lee",
            "publication_date": "1960-07-11",
            "description": "A gripping, heart-wrenching, and wholly remarkable tale of coming-of-age in a South poisoned by virulent prejudice."
            }
        ]
    }
    ```

5) **READ A BOOK BY THEIR ISBN**
    - `/api/books/<ISBN>/` (GET):
     - Retrieve the details of the specific book
    
    ```bash
    http://127.0.0.1:8000/api/books/978-006-1120/
    ```
    **Output**:
    ```bash
    {
        "title": "To Kill a Mockingbird",
        "isbn": "978-006-1120",
        "author": "Harper Lee",
        "publication_date": "1960-07-11",
        "description": "A gripping, heart-wrenching, and wholly remarkable tale of coming-of-age in a South poisoned by virulent prejudice."
    }
    ```

6) **UPDATE BOOK BY THEIR ISBN**
    - `/api/books/<ISBN>` (PUT):
        Updates the Book by giving all the details including optional ones as it is a complete update.

    ```bash
    http://127.0.0.1:8000/api/books/978-006-1120/

    {
        "title": "To Kill a Mockingbird Updated",
        "isbn": "978-006-1120",
        "author": "Harper Lee",
        "publication_date": "1960-07-11",
        "description": "A gripping, heart-wrenching, and wholly remarkable tale of coming-of-age in a South poisoned by virulent prejudice."
    }

    ```
    **Output:**
    ```bash
    {
        "message": "Updated Successfully!",
        "data": {
            "title": "To Kill a Mockingbird Updated",
            "isbn": "978-006-1120",
            "author": "Harper Lee",
            "publication_date": "1960-07-11",
            "description": "A gripping, heart-wrenching, and wholly remarkable tale of coming-of-age in a South poisoned by virulent prejudice."
        }
    }
    ```

7. **DELETE BOOK BY THEIR ISBN**
    - `api/books/<ISBN>` (DELETE):
     - Deletes the Book.
    
    ```bash
    http://127.0.0.1:8000/api/books/978-006-1120/
    ```
    **Output:**
    ```bash
    {
        "message": "Book deleted successfully"
    }
    ```
    You can verify it by retrieving all the books or by their ISBN

8. **LOGOUT**
    `/user/logout` (GET):
     - User is Logged Out.
    
    ```bash
    http://127.0.0.1:8000/user/logout
    ```

    **Output:**
    ```bash
    {
        "message": "Logout Successfull!"
    }
    ```

## **Testing:**
All the unit tests are writtened and tested perfectly and you can simply run those tests by:

```bash
python manage.py test library
python manage.py test users
```
 **LIBRARY API TESTS**
 - `register_and_login_user_01` - Login and Register Functionality Testing
 - `test_add_book_02` - Adding a Book
 - `test_get_books_03` - Getting all the Books
 - `test_get_single_book_04` - Getting Single Book by their ISBN
 - `test_update_book_05` - Updates the Book
 - `test_delete_book_06` - Deletes the Book
 - `test_invalid_endpoint_07` - Invalid Endpoint Testing
 
 *FAILURE CASES*
 - `test_not_authenticated_01` - When user not authenticated.
 - `test_add_book_same_isbn_04` - When a user attempts to add a book with an ISBN that is already stored in the database.
 - `test_add_book_invalid_data_05` - When a user tries to add a book with invalid datas.
 - `test_get_notfound_book_06` - When user tries to retrieve a book that is not present.
 - `test_update_incomplete_detail_07` - When user tries to update with incomplete datas.
 - `test_update_notfound_book_08` - When user tries to update a book that is not present.
 - `test_delete_notfound_book_09` - When user tries to delete a book that is not present.

 **USER TESTS**
 - `test_create_user` - User Registration
 - `test_login_user` - User Login
 - `test_invalid_endpoint` - Invalid Endpoint

 *FAILURE CASES*
 - `test_failure_create_user_01` - Creating a user whose data is invalid.
 - `test_failure_login_user_02` - When user tries to Login without Registering.
 - `test_failure_user_email_exists_03` - When user tries to register whose email already exists.

## **Conclusion:**
This project was really fun to work with!















