# Full-Stack File Management System

A full-stack file management system developed using React, Flask, PostgreSQL, and LocalStack. 

see demo here fmsdemo.hnd1.zeabur.app

This system allows users to upload, retrieve, and manage files with a user-friendly interface. The backend is containerized using Docker Compose, ensuring consistent deployment across the frontend, backend, database, and simulated S3 services.

## Features

- **File Upload**: Users can upload files through a web interface.
- **File Download**: Users can download files.
- **Metadata Storage**: File metadata (such as name and type) is stored in a PostgreSQL database.
- **Simulated S3**: LocalStack is used to simulate AWS S3 for testing and development.
- **RESTful APIs**: APIs built using Flask for handling file operations.

## Technologies Used

- **Frontend**: React
- **Backend**: Flask
- **Database**: PostgreSQL
- **File Storage**: LocalStack (simulated AWS S3)
- **Containerization**: Docker Compose

## Quick Start

To set up and run the application locally:

1. Clone the repository:
    ```bash
    git clone git@github.com:YUNHAN-LU/FileManageSystem.git
    cd FileManageSystem
    ```

2. Build and start the Docker containers using Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. Once the containers are running, you can access the following:

    - **Frontend**: Open your browser and navigate to `http://localhost:3000`
    - **Backend API**: The Flask backend will be accessible at `http://localhost:1234`
    - **PostgreSQL Database**: The PostgreSQL database is accessible via `localhost:5432` (use the `postgres` user and password `mysecretpassword`).
    - **Simulated S3 (LocalStack)**: LocalStack will be running at `http://localhost:4566`.


