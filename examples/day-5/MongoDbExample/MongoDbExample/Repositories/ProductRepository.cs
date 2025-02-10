using Microsoft.Extensions.Options;
using MongoDB.Driver;
using MongoDbExample.Models;
using MongoDbExample.Settings;

namespace MongoDbExample.Repositories;

public class ProductRepository : Repository<Product>, IProductRepository
{
    public ProductRepository(IOptions<MongoDbSettings> settings, IMongoClient mongoClient)
        : base(settings, mongoClient) { }
}