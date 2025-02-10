using MongoDbExample.Models;

namespace MongoDbExample.Repositories;

public interface IRepository<T> where T : IEntity
{
    Task<T> CreateAsync(T entity);
    Task<IEnumerable<T>> CreateAsync(IEnumerable<T> entites);
    Task<T> UpdateAsync(T entity);
    Task<T> GetByIdAsync(string id);
    Task<IEnumerable<T>> GetAllAsync();
    Task DeleteAsync(string id);
}
