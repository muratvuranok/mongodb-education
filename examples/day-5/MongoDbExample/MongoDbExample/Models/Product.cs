using MongoDB.Bson.Serialization.Attributes;

namespace MongoDbExample.Models;

public class Product : IEntity
{
    public ObjectId Id { get; set; }
    public string Name { get; set; } = default!;
    public decimal Price { get; set; }
    public int UnitsInStock { get; set; }

    [BsonRepresentation(BsonType.ObjectId)]
    public string CategoryId { get; set; } = string.Empty;
}
