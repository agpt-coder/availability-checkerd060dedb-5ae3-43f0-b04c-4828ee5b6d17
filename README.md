---
date: 2024-04-18T09:33:59.722269
author: AutoGPT <info@agpt.co>
---

# Availability Checker

To develop a function returning the real-time availability of professionals, updating based on current activity or schedule, the requirements and findings are as follows:

1. The target professionals span technology, healthcare, and emergency services sectors, necessitating a system that's flexible yet robust enough to handle diverse and dynamic scheduling needs.

2. Integration with existing scheduling or booking systems is essential to ensure seamless operation and maintain user experience. This requirement highlights the need for a compatible and adaptable backend structure that can interface with various external systems.

3. Upon a professional's availability status change, the system should notify relevant users and update the database accordingly. This dual-action ensures both real-time awareness for users and accurate record-keeping.

4. Implementing real-time updates will involve using WebSockets for bi-directional communication, leveraging FastAPI's support for asynchronous tasks and WebSockets. Employing background tasks for operations that should not interrupt the main flow is also advised.

5. Managing and storing professional schedules in PostgreSQL will require designing an efficient database schema with appropriate data types and indexing. Incorporating range types and PostgreSQL's robust date and time functions will support dynamic scheduling and querying.

6. Prisma ORM with FastAPI can streamline real-time data management through its efficient database access and manipulation, integrated with FastAPI's capabilities for WebSocket communication for pushing updates to clients.

To achieve this, our tech stack will include Python, FastAPI, PostgreSQL, and Prisma ORM. Best practices highlighted involve using WebSockets for real-time communication, ensuring data integrity with transactional operations in PostgreSQL, and leveraging Prisma for seamless database interactions coupled with FastAPI's async capabilities for an efficient, responsive application.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Availability Checker'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
