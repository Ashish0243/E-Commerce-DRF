# ShopFlow API - E-commerce REST API

A comprehensive e-commerce REST API built with Django REST Framework that provides complete functionality for managing products, categories, shopping carts, orders, and user ratings.

## 🚀 Features

- **User Management**: Custom user model with email-based authentication
- **Product Management**: CRUD operations for products with categories
- **Shopping Cart**: Add, update, and manage cart items
- **Order Processing**: Complete order workflow with status tracking
- **Rating System**: Product rating and review functionality
- **Authentication**: JWT-based authentication with registration/login
- **Admin Interface**: Django admin for backend management
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Async Tasks**: Celery integration for background tasks (email notifications)
- **Filtering & Search**: Advanced filtering and search capabilities
- **Pagination**: Built-in pagination for large datasets

## 🛠️ Tech Stack

- **Backend**: Django 5.2.1, Django REST Framework
- **Database**: SQLite (default), easily configurable for PostgreSQL/MySQL
- **Authentication**: JWT (Simple JWT), Django Allauth
- **Task Queue**: Celery with Redis
- **Documentation**: DRF Spectacular (OpenAPI/Swagger)
- **Image Handling**: Pillow for image uploads
- **Email**: SMTP email backend
- **Monitoring**: Django Silk for performance monitoring

## 📋 Prerequisites

- Python 3.8+
- Redis (for Celery)
- Virtual environment (recommended)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shopflow-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load Sample Data** (Optional)
   ```bash
   python manage.py popluate_db
   ```

8. **Start Redis Server** (for Celery)
   ```bash
   redis-server
   ```

9. **Start Celery Worker** (in separate terminal)
   ```bash
   celery -A E_COM worker --loglevel=info
   ```

10. **Run Development Server**
    ```bash
    python manage.py runserver
    ```

## 📚 API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

## 🔐 Authentication

The API uses JWT authentication. To access protected endpoints:

1. **Register a new user**:
   ```
   POST /dj-rest-auth/registration/
   ```

2. **Login**:
   ```
   POST /dj-rest-auth/login/
   ```

3. **Get JWT Token**:
   ```
   POST /api/token/
   ```

4. **Include token in requests**:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

## 📡 API Endpoints

### Authentication
- `POST /dj-rest-auth/registration/` - User registration
- `POST /dj-rest-auth/login/` - User login
- `POST /dj-rest-auth/logout/` - User logout
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Products
- `GET /product/` - List all products (with filtering, search, pagination)
- `POST /product/` - Create new product (Admin only)
- `GET /product/{id}/` - Get product details
- `PUT /product/{id}/` - Update product (Admin only)
- `DELETE /product/{id}/` - Delete product (Admin only)

### Categories
- `GET /category/` - List all categories (Admin only)
- `POST /category/` - Create new category (Admin only)
- `GET /category/{id}/` - Get category details (Admin only)
- `PUT /category/{id}/` - Update category (Admin only)
- `DELETE /category/{id}/` - Delete category (Admin only)

### Cart
- `GET /cart/` - List all carts
- `POST /cart/` - Create new cart
- `GET /cart/{id}/` - Get cart details
- `PUT /cart/{id}/` - Update cart (add/remove items)
- `DELETE /cart/{id}/` - Delete cart

### Orders
- `GET /order/` - List orders (filtered by user)
- `GET /order/{id}/` - Get order details
- `PUT /order/{id}/` - Update order status (Admin only)
- `DELETE /order/{id}/` - Cancel order (Admin only)

### Ratings
- `GET /rating/` - List all ratings
- `POST /rating/` - Create new rating (Authenticated users)
- `GET /rating/{id}/` - Get rating details
- `PUT /rating/{id}/` - Update rating
- `DELETE /rating/{id}/` - Delete rating

## 🔍 Filtering & Search

### Products
- **Filter by price**: `?price=100` or `?price__gte=50&price__lte=200`
- **Filter by category**: `?category_slug=electronics`
- **Filter by stock**: `?stock__gt=0`
- **Search**: `?search=laptop`
- **Ordering**: `?ordering=price` or `?ordering=-price`
- **In-stock only**: Automatically filters in-stock products

### Orders
- **Filter by status**: `?status=Confirmed`
- **Filter by date**: `?created_at__date=2024-01-01`
- **Filter by date range**: `?created_at__gte=2024-01-01&created_at__lte=2024-12-31`

## 🛒 Shopping Cart Workflow

1. **Create Cart**: User creates a new cart with products
2. **Add Items**: Add products to cart with quantities
3. **Update Cart**: Modify quantities or remove items
4. **Checkout**: Set `checked_out=true` to process the cart
5. **Order Creation**: System automatically creates order from cart
6. **Stock Update**: Product stock is automatically reduced
7. **Email Notification**: User receives order confirmation email

## 📧 Email Notifications

The system automatically sends email notifications for:
- Order confirmations
- Account registration (console backend in development)

Configure SMTP settings in `.env` for production email delivery.

## 🔒 Permissions

- **Public**: Product listing, product details
- **Authenticated**: Cart operations, order creation, ratings
- **Admin**: Product/category management, order management

## 🗄️ Database Models

### User
- Custom user model with email as username
- Fields: username, email, phone_number, first_name, last_name

### Product
- Fields: name, description, price, stock, image, category
- Relationships: belongs to category, has many ratings

### Category
- Fields: category_name, slug, description, image
- Auto-generates slug from category name

### Cart
- Fields: user, date_added, checked_out
- Relationships: belongs to user, has many cart items

### Order
- Fields: order_id (UUID), user, status, created_at
- Status choices: Pending, Confirmed, Cancelled
- Relationships: belongs to user, has many order items

### Rating
- Fields: user, product, rating (1-5), review, created_at
- Relationships: belongs to user and product

## 🚀 Production Deployment

1. **Environment Variables**:
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=your-database-url
   REDIS_URL=your-redis-url
   ```

2. **Database**: Configure PostgreSQL or MySQL
3. **Static Files**: Configure static file serving
4. **Media Files**: Configure media file storage (AWS S3, etc.)
5. **Celery**: Deploy with proper process management
6. **Security**: Enable HTTPS, configure security headers

## 📊 Performance Monitoring

Access Django Silk profiler at `/silk/` for:
- Request/response analysis
- Database query optimization
- Performance bottleneck identification


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the API documentation for endpoint details
- Review the Django and DRF documentation

## 🔄 Changelog

### v1.0.0
- Initial release with core e-commerce functionality
- JWT authentication
- Product and category management
- Shopping cart and order processing
- Rating system
- Email notifications
- API documentation
