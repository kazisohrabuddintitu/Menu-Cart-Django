# Restaurant_API_Project

## Description
This project is a REST API project built with Django REST Framework. It provides endpoints for various functionalities related to user registration, token generation, menu item management, user group management, cart management, and order management. The project supports different user roles, including customers, managers, and delivery crew, with different permissions and access levels.

## Installation
1. Clone the repository:
<pre>
git clone https://github.com/your-username/your-repository.git
</pre>

2. Change into the project directory:
<pre>
cd your-repository
</pre>

3. Install the dependencies:
<pre>
pip install -r requirements.txt
</pre>

4. Configure the project by providing the necessary environment variables (if any).
5. Run the migrations:
<pre>
python manage.py migrate
</pre>

6. Start the development server:
<pre>
python manage.py runserver
</pre>


## User registration and token generation endpoints 
For user registration and token generation. It provides the following functionalities:

- User registration: **/api/users** (POST) - Creates a new user with name, email, and password.
- Get current user: **/api/users/users/me/** (GET) - Displays only the current user.
- Token generation: **/token/login/** (POST) - Generates access tokens that can be used in other API calls in this project.

### Example request for User Registration
<pre>
POST /api/users/
Content-Type: application/json

{
  "username": "john.doe@example.com",
  "password": "password123"
}
</pre>

### Example request for Get current user
<pre>
GET /api/users/users/me/
Authorization: Bearer <user-token>
</pre>

### Example request for Token generation
<pre>
POST /token/login/
Content-Type: application/json

{
  "username": "john.doe",
  "password": "password123"
}
</pre>


## Menu items endpoints
Endpoints for managing menu items. It supports various operations based on user roles. The following endpoints and functionalities are available:

### List Menu Items
- Endpoint: **/api/menu-items**
- Role: Customer, Manager, Delivery Crew
- Method: GET
- Purpose: Lists all menu items. Returns a 200 - Ok HTTP status code.

### Create Menu Item (Manager Only) - User with other role would get 403 - Unauthorized HTTP status code.
- Endpoint: **/api/menu-items**
- Role: Manager
- Method: POST
- Purpose: Creates a new menu item and returns 201 - Created HTTP status code.

### Get Single Menu Item
- Endpoint: **/api/menu-items/{menuItem}**
- Role: Customer, Delivery Crew, Manager
- Method: GET
- Purpose: Lists a single menu item.

### Update Single Menu Item (Manager Only) - User with other role would get 403 - Unauthorized HTTP status code.
- Endpoint: **/api/menu-items/{menuItem}**
- Role: Manager
- Methods: PUT, PATCH
- Purpose: Updates a single menu item.

### Delete Menu Item (Manager Only) - User with other role would get 403 - Unauthorized HTTP status code.
- Endpoint: **/api/menu-items/{menuItem}**
- Role: Manager
- Method: DELETE
- Purpose: Deletes a menu item.

## User Group Management Endpoints
Endpoints for managing user groups. It includes functionalities for managing managers and delivery crew. The following endpoints and functionalities are available:

### Get Managers
- Endpoint: **/api/groups/manager/users**
- Role: Manager
- Method: GET
- Purpose: Returns all managers.

### Assign Manager
- Endpoint: **/api/groups/manager/users**
- Role: Manager
- Method: POST
- Purpose: Assigns the user in the payload to the manager group and returns 201 - Created.

### Remove Manager
- Endpoint: **/api/groups/manager/users/{userId}**
- Role: Manager
- Method: DELETE
- Purpose: Removes this particular user from the manager group. Returns 200 - Success if everything is okay. If the user is not found, returns 404 - Not found.

### Get Delivery Crew
- Endpoint: **/api/groups/delivery-crew/users**
- Role: Manager
- Method: GET
- Purpose: Returns all delivery crew.

### Assign Delivery Crew
- Endpoint: **/api/groups/delivery-crew/users**
- Role: Manager
- Method: POST
- Purpose: Assigns the user in the payload to the delivery crew group and returns 201 - Created.

### Remove Delivery Crew
- Endpoint: **/api/groups/delivery-crew/users/{userId}**
- Role: Manager
- Method: DELETE
- Purpose: Removes this user from the delivery crew group. Returns 200 - Success if everything is okay. If the user is not found, returns 404 - Not found.

## Cart Management Endpoints
Endpoints for managing a cart. It allows customers to add menu items to their cart, view the current items in the cart, and delete all items from the cart. The following endpoints and functionalities are available:

### Get Cart Items
- Endpoint: **/api/cart/menu-items**
- Role: Customer
- Method: GET
- Purpose: Returns the current items in the cart for the authenticated user token.

### Add to Cart
- Endpoint: **/api/cart/menu-items**
- Role: Customer
- Method: POST
- Purpose: Adds the menu item to the cart and sets the authenticated user as the user ID for these cart items.

### Empty Cart
- Endpoint: **/api/cart/menu-items**
- Role: Customer
- Method: DELETE
- Purpose: Deletes all menu items created by the current user token, effectively emptying the cart.

## Order Management Endpoints
Endpoints for managing orders. It allows customers, managers, and delivery crew to perform various operations related to orders. The following endpoints and functionalities are available:

### Get User Orders
- Endpoint: **/api/orders**
- Role: Customer
- Method: GET
- Purpose: Returns all orders with order items created by the current user.

### Create Order
- Endpoint: **/api/orders**
- Role: Customer
- Method: POST
- Purpose: Creates a new order item for the current user. It retrieves the current cart items from the cart endpoints and adds those items to the order items table. Then it deletes all items from the cart for this user.

### Get Order Items
- Endpoint: **/api/orders/{orderId}**
- Role: Customer
- Method: GET
- Purpose: Returns all items for the specified order ID. If the order ID doesn't belong to the current user, it displays an appropriate HTTP error status code.

### Get All Orders
- Endpoint: **/api/orders**
- Role: Manager
- Method: GET
- Purpose: Returns all orders with order items for all users.

### Update Order
- Endpoint: **/api/orders/{orderId}**
- Role: Customer
- Method: PATCH
- Purpose: Updates the specified order. A manager can use this endpoint to set a delivery crew for this order and update the order status to indicate if it is out for delivery or has been delivered.

### Delete Order
- Endpoint: **/api/orders/{orderId}**
- Role: Manager
- Method: DELETE
- Purpose: Deletes the specified order.

### Get Orders Assigned to Delivery Crew
- Endpoint: **/api/orders**
- Role: Delivery crew
- Method: GET
- Purpose: Returns all orders with order items assigned to the delivery crew.

### Update Order Status (Delivery Crew)
- Endpoint: **/api/orders/{orderId}**
- Role: Delivery crew
- Method: PATCH
- Purpose: Updates the order status to indicate if it is out for delivery or has been delivered. The delivery crew can only update the order status and cannot modify anything else in the order.


     
