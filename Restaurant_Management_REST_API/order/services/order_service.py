from order.models import Order, OrderItem
from cart.models import Cart
from decimal import Decimal
from order.serializers import OrderSerializer
from datetime import datetime
from django.contrib.auth.models import User

class OrderService:
    def get_orders(self, user):
        if user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
        elif user.groups.filter(name='Delivery Crew').exists():
            orders = user.delivery_crew.all()
        else:
            orders = Order.objects.filter(customer=user)
        order_serialized = OrderSerializer(orders, many=True)
        return True, order_serialized.data
    
    def get_order(self, user, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=user)
            result = OrderSerializer(order).data
            return True, result
        except Order.DoesNotExist:
            result = {"message": "order_id is not valid"}
            return False, result
    
    def delete_order(self, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order_items = OrderItem.objects.filter(order=order)
            order_items.delete()
            order.delete()
            result = {"message": f"Order with id: {order_id} is deleted successfully"}
            return True, result
        except Order.DoesNotExist:
            result = {"message": "order_id is not valid"}
            return False, result
    
    def place_order(self, user):
        carts = Cart.objects.filter(user=user).select_related('menu_item')
        if carts.exists():
            total = Decimal('0')
            order = Order(customer=user, date=datetime.now().date(), total=total)
            order.save()
            for cart in carts:
                order_item = OrderItem(
                    order=order, quantity=cart.quantity, menu_item=cart.menu_item,
                    unit_price=cart.unit_price, price=cart.price
                )
                order_item.save()
                total += cart.price
            order.total = total
            order.save()
            carts.delete()
            result = OrderSerializer(order).data
        else:
            result = {
                "message" : "Cart is empty, Please add menu_items in cart to place order"
            }
        return True, result
    
    def update_order(self, user, order_id, json_data):
        status, delivery_crew = json_data.get('status'), json_data.get('delivery_crew')
        try:
            order = Order.objects.get(id=order_id)
            if delivery_crew and user.groups.filter(name='Manager').exists():
                if not isinstance(delivery_crew, str):
                    return False, {"message": "delivery_crew should be of type: str"}
                try:
                    delivery_crew = User.objects.get(username=delivery_crew)
                    if not delivery_crew.groups.filter(name='Delivery Crew').exists():
                        return False, {"message": "The input delivery_crew is not a delivery crew member"}
                    order.delivery_crew = delivery_crew
                    order.save()
                except User.DoesNotExist:
                    return False, {"message": "delivery_crew does not exist"}
            if status is not None:
                if not isinstance(status, bool):
                    return False, {'message': "status should be of type: boolean"}
                order.status = status
                order.save()
            return True, OrderSerializer(order).data
        except Order.DoesNotExist:
            result = {"message": "order_id is not valid"}
            return False, result




        
        