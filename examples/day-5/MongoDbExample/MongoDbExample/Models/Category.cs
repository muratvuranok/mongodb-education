namespace MongoDbExample.Models;
public class Category : IEntity
{
    public ObjectId Id { get; set; }
    public string Name { get; set; } = default!;
    public string? Description { get; set; }
}
