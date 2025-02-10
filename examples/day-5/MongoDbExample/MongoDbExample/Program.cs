using MongoDbExample;

var builder = WebApplication.CreateBuilder(args);


builder.Services.AddControllers();
builder.Services.AddOpenApi();


builder.Services
    // .AddApplicationServices
    // .AddInfrastructureServices
    .AddApiDependency(builder.Configuration);












var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseAuthorization();

app.MapControllers();

app.Run();
