using Microsoft.AspNetCore.Mvc;
using MongoDbExample.Repositories;

namespace MongoDbExample.Controllers;

[Route("api/[controller]")]
[ApiController]
public class CategoriesController(ICategoryRepository categoryRepository)
    : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> Create(CreateCategoryDto entity)
    {

        if (entity.Name == null)
        {
            return BadRequest();
        }

        var category = new Category
        {
            Name = entity.Name,
            Description = entity.Description
        };

        await categoryRepository.CreateAsync(category);
        return Ok(category);
    }

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var categories = await categoryRepository.GetAllAsync();
        return Ok(categories);
    }



    [HttpGet("products")]
    public async Task<IActionResult> GetAllWithProducts()
    {
        var categories = await categoryRepository.GetAllCategoriesWithProductsAsync();
        return Ok(categories);
    }


    [HttpGet("{id}")]
    public async Task<IActionResult> Get(string id)
    {
        var categories = await categoryRepository.GetByIdAsync(id);
        return Ok(categories);
    }
}
