using MongoDB.Driver;
using MongoDbExample.Repositories;
using MongoDbExample.Settings;

namespace MongoDbExample;

public static class ApiDependencyInjection
{
    public static IServiceCollection AddApiDependency(this IServiceCollection services, IConfiguration configuration)
    {

        services.Configure<MongoDbSettings>(configuration.GetSection("MongoDbSettings"));
        var mongoSettings = configuration.GetSection("MongoDbSettings").Get<MongoDbSettings>();
        var mongoClient = new MongoClient(mongoSettings.ConnectionStringLocal);
        services.AddSingleton<IMongoClient>(mongoClient);


        services.AddTransient(typeof(IRepository<>), typeof(Repository<>));
        services.AddTransient<ICategoryRepository, CategoryRepository>();
        services.AddTransient<IProductRepository, ProductRepository>();


        return services;
    }
}
