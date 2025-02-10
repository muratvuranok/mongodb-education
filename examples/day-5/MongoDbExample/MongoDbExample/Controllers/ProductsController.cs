using Microsoft.AspNetCore.Mvc;
using MongoDbExample.Dtos;
using MongoDbExample.Models;
using MongoDbExample.Repositories;

namespace MongoDbExample.Controllers;

[Route("api/[controller]")]
[ApiController]
public class ProductsController(IProductRepository productRepository) : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> Create(CreateProductDto entity)
    {
        if (entity.Name == null)
        {
            return BadRequest();
        }

        var product = new Product
        {
            Name = entity.Name,
            Price = entity.Price,
            UnitsInStock = entity.UnitsInStock,
            CategoryId = entity.CategoryId
        };

        await productRepository.CreateAsync(product);

        return Ok(product);
    }
}
