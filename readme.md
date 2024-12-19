# 🚀 Full-Stack File Management System

A dynamic full-stack file management system developed using React, Flask, PostgreSQL, and LocalStack. 

🌐 Check out the [demo here](https://fmsdemo.hnd1.zeabur.app) 🎉

This system empowers users to upload, retrieve, and manage files with an intuitive interface. The backend is containerized using Docker Compose, ensuring seamless deployment across the frontend, backend, database, and simulated S3 services.

## ✨ Features

- 📤 **File Upload**: Effortlessly upload files through a user-friendly interface.
- 📥 **File Download**: Conveniently download files whenever needed.
- 🗂️ **Metadata Storage**: Store file metadata (such as name and type) in a PostgreSQL database.
- ☁️ **Simulated S3**: Utilize LocalStack to simulate AWS S3 for testing and development.
- 🔗 **RESTful APIs**: Robust APIs built using Flask for handling file operations.

## 🛠️ Technologies Used

- 🎨 **Frontend**: React
- ⚙️ **Backend**: Flask
- 🗄️ **Database**: PostgreSQL
- 🗃️ **File Storage**: LocalStack (simulated AWS S3)
- 🐳 **Containerization**: Docker Compose

## 🚀 Quick Start

To set up and run the application locally:

1. 🏗️ Clone the repository:
    ```bash
    git clone git@github.com:YUNHAN-LU/FileManageSystem.git
    cd FileManageSystem
    ```

2. 🔧 Build and start the Docker containers using Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. 🌐 Once the containers are running, you can access the following:

    - 🖥️ **Frontend**: Open your browser and navigate to `http://localhost:3000?itemId=0`
    - 🛠️ **Backend API**: The Flask backend will be accessible at `http://localhost:1234`
    - 🗄️ **PostgreSQL Database**: Accessible via `localhost:5432` (use the `postgres` user and password `mysecretpassword`).
    - ☁️ **Simulated S3 (LocalStack)**: Running at `http://localhost:4566`

