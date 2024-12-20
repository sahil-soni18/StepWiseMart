
# **StepWiseMart - E-commerce with AR Shoe Try-On**

StepWiseMart is an e-commerce platform that allows users to shop for shoes with a unique augmented reality (AR) feature, letting them try on shoes virtually using their camera. The platform also includes all essential e-commerce features such as product sorting, categories, and a checkout system.

This project is built using the following tech stack:
- **Frontend**: ReactJS with Tailwind CSS (via Vite)
- **Backend**: FastAPI with Uvicorn
- **Database**: PostgreSQL

## **Table of Contents**
- [Prerequisites](#prerequisites)
- [Backend Setup](#backend-setup)
  - [FastAPI with Uvicorn](#fastapi-with-uvicorn)
  - [Database Setup](#database-setup)
- [Frontend Setup](#frontend-setup)
  - [Vite with ReactJS and Tailwind CSS](#vite-with-reactjs-and-tailwind-css)
- [Running the Project](#running-the-project)
- [Contributing](#contributing)

## **Prerequisites**
Before running this project, ensure you have the following installed:
- Python 3.7+
- Node.js (with npm)
- PostgreSQL (or use a cloud database)

## **Backend Setup**

### **1. FastAPI with Uvicorn**
To set up the FastAPI backend:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/StepWiseMart.git
   cd StepWiseMart
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt`, run:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2
   ```

   You can add any additional dependencies as your project grows.

4. **Set up your PostgreSQL database**:
   - Create a PostgreSQL database (e.g., `stepwisemart`).
   - Update the database URL in your project’s configuration (for example, in `config.py` or `.env`):
     ```bash
     DATABASE_URL="postgresql://user:password@localhost:5432/stepwisemart"
     ```

5. **Run the backend**:
   - Start Uvicorn to run FastAPI:
     ```bash
     uvicorn app.main:app --reload
     ```
   - This will start the FastAPI server at `http://127.0.0.1:8000`.

### **Database Setup**
1. **Migrate the database** (using Alembic or a similar tool):
   If you have SQLAlchemy models, run migrations:
   ```bash
   alembic upgrade head
   ```

   If you don't have migrations, you can manually create tables in PostgreSQL using the `Base.metadata.create_all()` command in your FastAPI code.

---

## **Frontend Setup**

### **2. Vite with ReactJS and Tailwind CSS**
To set up the frontend with Vite, ReactJS, and Tailwind CSS:

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   First, ensure you have Node.js installed. Then, run the following:
   ```bash
   npm install
   ```

3. **Configure Tailwind CSS**:
   If Tailwind isn't set up yet, you can follow these steps:
   - Install Tailwind and its dependencies:
     ```bash
     npm install tailwindcss postcss autoprefixer
     npx tailwindcss init
     ```
   - Add the following configuration to `tailwind.config.js`:
     ```js
     module.exports = {
       content: [
         "./index.html",
         "./src/**/*.{js,ts,jsx,tsx}",
       ],
       theme: {
         extend: {},
       },
       plugins: [],
     }
     ```
   - Add the Tailwind directives to your main `index.css` file:
     ```css
     @tailwind base;
     @tailwind components;
     @tailwind utilities;
     ```

4. **Run the frontend**:
   Start the Vite development server:
   ```bash
   npm run dev
   ```
   - This will run the frontend at `http://localhost:3000`.

---

## **Running the Project**

1. **Start the backend** (FastAPI with Uvicorn):
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Start the frontend** (Vite):
   ```bash
   npm run dev
   ```

   With both the backend and frontend running, you can now visit `http://localhost:3000` to view the app and test the features.

---

## **Contributing**
We welcome contributions to improve the project! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## **License**
This project is licensed under the MIT License.
