from bson.objectid import ObjectId


class Product:
    def __init__(self, name: str, price: float, unitsInStock: int, categoryId: str):
        self.Name = name
        self.Price = price
        self.UnitsInStock = unitsInStock
        self.CategoryId = ObjectId(categoryId) if categoryId else None
        
        # db.Products.insertOne({Name: "Chai", Price: 10, UnitsInStock: 100, CategoryId: '67aaf9be3961c0aac69240f5'})

    def __str__(self):  # ToString
        return f"{self.Name} {self.Price} {self.UnitsInStock} {self.CategoryId}"

    def to_dict(self):
        return {
            "Name": self.Name,
            "Price": self.Price,
            "UnitsInStock": self.UnitsInStock,
            "CategoryId": self.CategoryId,
        }


p = Product("Chai", 10, 100, 1)
print(p)
print(p.to_dict())
# var c = new Category("Beverages","test");
# Console.WriteLine(c.Name);
# Console.WriteLine(c.Description);
# Console.WriteLine($"{c.Name} {c.Description}");


# Console.WriteLine(c);  -> namespace + class name
# Console.WriteLine(c);  -> $"{c.Name} {c.Description}"   -> override ToString() -> $"{c.Name} {c.Description}"
