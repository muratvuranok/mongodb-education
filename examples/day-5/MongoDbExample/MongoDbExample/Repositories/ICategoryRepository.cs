using MongoDbExample.Dtos;
using MongoDbExample.Models;

namespace MongoDbExample.Repositories;

public interface ICategoryRepository : IRepository<Category>
{
    Task<IEnumerable<CategoryWithProductsDto>> GetAllCategoriesWithProductsAsync();
}
