namespace MongoDbExample.Settings;

public class MongoDbSettings
{
    public string ConnectionStringLocal { get; set; } = default!;
    public string ConnectionStringCloud { get; set; } = default!;
    public string DatabaseName { get; set; } = default!;
}
