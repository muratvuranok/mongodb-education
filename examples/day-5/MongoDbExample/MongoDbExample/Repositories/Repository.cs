using Humanizer;
using Microsoft.Extensions.Options;
using MongoDB.Driver;
using MongoDbExample.Models;
using MongoDbExample.Settings;

namespace MongoDbExample.Repositories;

public class Repository<T>
    : IRepository<T> where T : IEntity
{
    public IMongoCollection<T> _collection;
    public Repository(IOptions<MongoDbSettings> settings, IMongoClient mongoClient)
    {
        var database = mongoClient.GetDatabase(settings.Value.DatabaseName);
        //_collection = database.GetCollection<T>(typeof(T).Name.Pluralize().Camelize());  // Category -> categories
        _collection = database.GetCollection<T>(typeof(T).Name.Pluralize());  // Category -> Categories
    }

    public async Task<T> CreateAsync(T entity)
    {
        await _collection.InsertOneAsync(entity);
        return entity;
    }


    public async Task<IEnumerable<T>> CreateAsync(IEnumerable<T> entities)
    {
        await _collection.InsertManyAsync(entities);
        return entities;
    }

    public async Task DeleteAsync(string id) => await _collection.DeleteOneAsync(x => x.Id == ObjectId.Parse(id));
    public async Task<IEnumerable<T>> GetAllAsync() => await _collection.Find(x => true).ToListAsync();
    public async Task<T> GetByIdAsync(string id) => await _collection.Find(x => x.Id == ObjectId.Parse(id)).FirstOrDefaultAsync();
    public async Task<T> UpdateAsync(T entity) => await _collection.FindOneAndReplaceAsync(x => x.Id == entity.Id, entity);
}
