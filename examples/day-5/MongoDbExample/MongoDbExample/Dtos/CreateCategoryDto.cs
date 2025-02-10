using MongoDB.Bson.Serialization.Attributes;

namespace MongoDbExample.Dtos;



public class CreateCategoryDto
{
    public string Name { get; set; } = default!;
    public string? Description { get; set; }
}


public class CategoryWithProductsDto
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = default!;
    public string Name { get; set; } = default!;
    public string? Description { get; set; }
    public List<ProductDto> Products { get; set; } = new();
}

public class ProductDto
{

    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = default!;
    public string Name { get; set; } = default!;
    public decimal Price { get; set; }
    public int UnitsInStock { get; set; }

    [BsonRepresentation(BsonType.ObjectId)]
    public string CategoryId { get; set; } = default!;
}





public class CreateProductDto
{
    public string Name { get; set; } = default!;
    public decimal Price { get; set; }
    public int UnitsInStock { get; set; }
    public string CategoryId { get; set; } = default!;
}