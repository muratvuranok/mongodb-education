namespace MongoDbExample.Repositories;

public class CategoryRepository : Repository<Category>, ICategoryRepository
{
    public CategoryRepository(IOptions<MongoDbSettings> settings, IMongoClient mongoClient)
        : base(settings, mongoClient) { }

    public async Task<IEnumerable<CategoryWithProductsDto>> GetAllCategoriesWithProductsAsync()
    {
        var pipeline = new[] {

            new BsonDocument ("$lookup",
                new BsonDocument
                {
                    {"from", "Products" },
                    {"localField", "_id" },
                    {"foreignField", "CategoryId" },
                    {"as", "Products" },
                }),
            new BsonDocument("$project",
            new BsonDocument
                {
                    {"_id",  1 },
                    {"Name",  1 },
                    {"Description",  1 },
                    {"Products._id",  1 },
                    {"Products.Name",  1 }
                }
            )
        };

        return await _collection.Aggregate<CategoryWithProductsDto>(pipeline).ToListAsync();
    }
}



/*
 
    db.Categories.Aggregate([
        {   $lookup: {
                from: "Products",
                localField: "_id",
                foreignField: "CategoryId",
                as: "Products"
            }
        }
    ]);
 
 */