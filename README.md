# E-commerce Project - Django/Python TCM

![E-commerce Banner](/ecommerce/static/images/Captura.JPG) 

## 📖 Project Overview

The E-commerce Project is a comprehensive online shopping platform developed from scratch using Django and Python. This project aims to provide a seamless shopping experience, showcasing a wide range of products with robust backend functionalities. The site provides a full shopping experience, including user registration, shopping cart, payment processing with the Mercado Pago API, and much more. The design and frontend elements were collaboratively developed, ensuring an engaging user interface.

## 🛠️ Technologies Used

- **Django**: The main framework for building the web application, providing a powerful backend structure.
- **Python**: The programming language utilized for implementing business logic and server-side operations.
- **HTML/CSS**: Core technologies for structuring and styling the web pages.
- **JavaScript**: For dynamic content and enhancing user interactions.
- **PostgreSQL/MySQL/SQLite**: The database management system used for storing product, user, and transaction data.
- **Mercado Pago API**: Integrated for secure payment processing.
- **Bootstrap**: CSS framework for responsive design and layout.

## 🔍 Key Features

- **User Authentication**: Users can register, log in, and manage their profiles securely.
- **Product Management**: Admin panel for adding, editing, and deleting products, including image uploads and stock management.
- **Shopping Cart**: Users can add products to their cart, modify quantities, and proceed to checkout seamlessly.
- **Order Processing**: Integration with the Mercado Pago API for handling payments, ensuring a secure transaction process.
- **Responsive Design**: The site is fully responsive, providing an optimal viewing experience across various devices.

## ⚙️ Techniques and Practices

- **MVC Architecture**: Utilized Django's Model-View-Controller (MVC) architecture to separate concerns and organize code efficiently.
- **RESTful API Design**: Developed a RESTful API for managing product data and user interactions.
- **Unit Testing**: Implemented unit tests to ensure the reliability and stability of core functionalities.
- **Version Control**: Used Git for version control, enabling collaborative development and efficient tracking of changes.


### Detailed Breakdown

![Site_estruture](/ecommerce/static/images/site_extrutur.JPG)

1. **Project Directory (`ecommerce/`)**:
   - This is the main directory containing the project settings and configurations. It houses the `settings.py` file, which defines database connections, middleware, and installed apps, ensuring a modular and scalable architecture.

2. **Store Application (`store/`)**:
   - The core application of the project, dedicated to managing products and transactions. Key files include:
     - **`models.py`**: Defines the data models that map to the database schema, encapsulating product attributes and relationships.
     - **`views.py`**: Contains the view functions that process incoming requests, interact with the models, and render templates for user interaction.
     - **`urls.py`**: Manages URL routing for the store app, directing requests to the appropriate view functions.

3. **Templates and Static Files**:
   - **`templates/`**: Contains HTML files that define the user interface for the application. The use of templates promotes code reusability and separation of concerns, adhering to the MVC pattern.
   - **`static/`**: A dedicated folder for static files such as CSS, JavaScript, and images, ensuring they are served efficiently.

4. **Migrations**:
   - The `migrations/` directory tracks changes to the models, allowing for version control of the database schema. This ensures smooth updates and modifications to the database structure over time.


5. **Utilities and APIs**:
   - **`api_mercadopago.py`**: Integrates with the Mercado Pago payment API, facilitating secure transactions and enhancing the user experience.
   - **`util.py`**: Contains helper functions that can be reused across different parts of the application, promoting DRY (Don't Repeat Yourself) principles.

### Conclusion

This organized structure not only enhances the maintainability of the project but also follows best practices in Django development. Each component has a clear purpose, promoting collaboration and ease of understanding for new developers joining the project.
