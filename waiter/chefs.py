from waiter import Chef

class LaxRecipeChef(Chef):
    def __init__(self, domain, recipe):
        self.recipe = recipe
        self.domain = domain
        self.method = 'GET'

    def cook_data(self, stack, params):
        uri = ''.join(stack)
        endpoint, format = uri.rsplit('.', 1)
        if endpoint in self.recipe:
            self.method = self.recipe[endpoint]
        return super(LaxRecipeChef, self).cook_data([self.domain,'/']+stack, params)

    @classmethod
    def string_recipe_to_dict(cls, string):
        lines = string.strip().split('\n')
        output = {}
        for line in lines:
            endpoint, method = line.split('-', 1)
            output[endpoint.strip()] = method.strip()
        return output
