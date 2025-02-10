class Category:
    def __init__(self, name, description):
        self.Name = name
        self.Description = description

    def __str__(self):
        return f"{self.Name} {self.Description}"

    def to_dict(self):
        return {"Name": self.Name, "Description": self.Description}


# record Category(string Name, string Description);
