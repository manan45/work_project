class UserOutputAdapter():

    def parse(self, user):
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "company_name": user.company_name,
            "city": user.city,
            "state": user.state,
            "zip": user.zip,
            "email": user.email,
            "web": user.web,
            "age": user.age
        }