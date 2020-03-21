.. image:: logo.png


What for
----------
Demo project build with FastAPI


Features
----------
1) User Authentication & sign in
2) File/Assets upload to s3
3) Send OTP/Mail (MSG91 api integrated would require MSG91 api key)

Quickstart
----------

Run the following commands to  ``poetry``: ::

    git clone https://github.com/neerajshukla1911/fastapi-project
    cd fastapi-project
    poetry install

To run the web application in debug use::

    uvicorn app.main:app --reload

    or

    python3 start_server.py


Application will be available on ``localhost`` or ``127.0.0.1`` in your browser.

Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.


Project structure
-----------------

Files related to application are in the ``app`` directory:

::

    models  - pydantic models that used in crud or handlers
    crud    - CRUD for types from models (User, assets )
    db      - db specific utils
    core    - some general components (s3, msg_91, smtp)
    api     - handlers for routes
    main.py - FastAPI application instance, CORS configuration and api router including


Todo
----
1) Dockerize application
2) Add unit test
