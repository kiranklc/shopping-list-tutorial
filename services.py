from models import ShoppingModel


class ShoppingService:
    def __init__(self):
        self.model = ShoppingModel()

    def create(self,name,quantity,user_id):
        return self.model.create(name,quantity,user_id)

    def update(self, items, uid):
        return self.model.update(items, uid)

    def delete(self, item_id, uid):
        return self.model.delete(item_id, uid)

    def list(self,uid):
        return self.model.list_items(uid)



