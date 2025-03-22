
## Description

This project is a RESTful API for the social network Yatube, which allows users to create posts, comment on them, subscribe to other users, and view their subscription feed. The API is developed in accordance with the documentation available at `http://127.0.0.1:8000/redoc/`. The documentation serves as the technical specification for implementing the functionality.


## Install

Clone the repository to your computer:

```bash
git clone https://github.com/ваш-username/      
api_final_yatube.git
cd api_final_yatube
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Apply the migrations:
```bash
python manage.py migrate
```

Start the server:
```bash
python manage.py runserver
```
## API

#### Key Features of the API:
- Create, edit, and delete posts.
- Add and delete comments on posts.
- Subscribe to and unsubscribe from other users.
- View the subscription feed.
- User authentication using JWT tokens.
- The API provides access to data only for authorized users, except for some endpoints that are publicly readable.

### Available endpoints:

| Method | Endpoint     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `GET` `POST`      | `/api/v1/posts/` | Retrieve a list of all posts or create a new post. |
| `GET` `PUT` `PATCH` `DEL`    | `/api/v1/posts/{id}/` | Retrieve, update, partially update, or delete a specific post by its ID. |
| `GET` `POST`| `/api/v1/posts/{post_id}/comments/` | Retrieve a list of comments for a post or create a new comment. |
| `GET` `PUT` `PATCH` `DEL`| `/api/v1/posts/{post_id}/comments/{id}` | Retrieve, update, partially update, or delete a specific comment by its ID. |
| `GET` | `/api/v1/groups/` | Retrieve a list of all groups. |
| `GET` | `/api/v1/groups/{id}` | Retrieve information about a specific group by its ID. |
| `GET` `POST` | `/api/v1/follow/` | Retrieve a list of user subscriptions or create a new subscription. |
| `POST` | `/api/v1/jwt/create/` | Obtain a JWT token for authentication. |
| `POST` | `/api/v1/jwt/refresh/` | Refresh a JWT token. |
| `POST` | `/api/v1/jwt/verify/` | Verify the validity of a JWT token. |


## Examples

```http
  GET /api/v1/posts/
```

```http
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `limit` | `integer` | Number of publications per page |
| `offset` | `integer` | The number of the page after which to start the output |

---

```http
  GET /api/v1/posts/{id}/
```

```http
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer` | publication ID |


## Running Tests

### Preparing the Django Project

The file `API_for_yatube.postman_collection.json` contains a Postman collection—a set of pre-prepared requests to test the API functionality.

To prepare the Django project for running the collection:

1. Ensure that the virtual environment is set up and activated, and that the project dependencies are installed.
2. Navigate to the *postman_collection* directory and run the `bash set_up_data.sh` script to create the necessary database objects for the collection to work.  
   **Note:** The script will clear the existing database before proceeding.

```bash
bash set_up_data.sh
```
3. Navigate to the directory containing the `manage.py` file and start the test server.

### Using Postman

1. Launch Postman.
2. In the top-left corner, click `File` -> `Import`.
3. In the pop-up window, you will be prompted to either drag and drop the collection file or select it via the file manager.  
   Upload the `API_for_yatube.postman_collection.json` file to Postman.
4. After completing the previous steps, the imported collection will appear in the `Collections` tab on the left side of the Postman window.  
   Hover over the collection, click the three dots next to its name, and select `Run collection` from the dropdown menu.  
   A list of requests in the collection will appear in the center of the screen, and a settings menu will appear on the right.
5. In the right-hand menu, enable the `Persist responses for a session` option—this will allow you to view the API responses after running the collection.
6. Click the `Run <collection name>` button.
7. The results of the collection run and tests will be displayed in the center of the screen. You can filter failed tests by switching to the `Failed` tab.  
   To view the details of a specific request and its response, click on the test.

**Before running the collection again, make sure to re-run the bash script—it will clear the database and recreate the necessary fixtures.**
