MAX_PAGE_SIZE = 50

class RouteException(Exception):
    name = "Route Exception"
    status_code = 400      

    def __init__(self, source=None, value=None, message=None, route=None, route_args=None, queries=None):
        super().__init__(source, value, message, route, route_args, queries)
        self.source = source
        self.value = value
        self._message = message
        self.route = route
        self.route_args = route_args if route_args else {}
        self.queries = queries if queries else {}

    @property 
    def message(self):
        if self._message is None:
            return self.defaultMessage()
        else:
            return self._message

    @classmethod
    def fromRequest(cls, request, source=None, value=None, message=None):
        return cls(source, value, message = message, route = request.path, route_args = request.view_args.copy(), queries = request.args.copy())

    def defaultMessage(self):
        outMessage = "Route Exception 400"
        if self.route:
            outMessage += "at route '%s'" % self.route
            if self.queries:
                outMessage += "with queries: %s" % self.reprQueries()
        return outMessage + "."

    def reprQueries(self):
        outQueries = ""
        if self.queries:
            for attr, val in self.queries.items():
                if isinstance(val, int):
                    outQueries += "'%s': %s, " % (attr, val)
                else:
                    outQueries += "'%s': '%s', " % (attr, val)
        return outQueries[:-2]
    
    def marshall(self): 
        return {"name": self.name, "status_code": self.status_code, "route": self.route, 
                "queries": self.queries, "route_args": self.route_args, "source": self.source, 
                "value": self.value, "message": self.message}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        outRepr = "%s: %s. Error at '%s' with value: %s." % (self.name, self.status_code, self.source, self. value)
        outRepr += " Inputted Route: %s." % self.route
        outRepr += " Inputted Queries: %s. " % self.reprQueries()
        return outRepr


class InvalidUserException(RouteException):
    name = "Invalid User Exception"
    status_code = 422

    def __init__(self, source=None, value=None, **kwargs):
        source = source if source is not None else "user"
        if value is None and kwargs.get('queries') is not None:
            value = kwargs.get('queries').get("user", None)
        super().__init__(source=source, value=value, **kwargs)

    def defaultMessage(self):
        outMessage = "User ID Error: "
        if self.value is None:
            outMessage += "User ID expected. Received None."
        elif self.queries.get("user") is not None and self.queries.get("user").isdigit():
            outMessage += "Invalid user ID given. Value: %s." % self.value
        else:
            outMessage += "Wrong type for user query given. Value: %s, Type: %s. Should only be given values of type Int." % (self.value, type(self.value))
        return outMessage

    def __str__(self):
        return super().__str__() + "Expected Error Message: '%s'" % self.message


class InvalidOrderException(RouteException):
    name = "Invalid Order Exception"
    status_code = 400

    def __init__(self, source=None, value=None, **kwargs):
        source = source if source is not None else "ordering"
        if value is None and kwargs.get('route_args') is not None:
            value = kwargs.get('route_args').get('ordering', None)
        super().__init__(source=source, value=value, **kwargs)

    def defaultMessage(self):
        outMessage = "Ordering Error: "
        outMessage += "Invalid ordering value given: '%s'. Only use accepted ordering types." % self.value
        return outMessage

    def __str__(self):
        return super().__str__() + "Expected Error Message: '%s'" % self.message

class InvalidFilterException(RouteException):
    name = "Invalid Filter Exception"
    status_code = 400

    def __init__(self, source=None, value=None, **kwargs):
        source = source if source is not None else "filter value id"
        value  = value  if value  is not None else "null"
        super().__init__(source=source, value=value, **kwargs)

    def defaultMessage(self):
        outMessage = "%s Error: " % self.source
        outMessage += "Invalid {source} value given: '{value}'. Please use a positive int.".format(
                      source=self.source, value=self.value)
        return outMessage

    def __str__(self):
        return super().__str__() + "Expected Error Message: '%s'" % self.message
        

class InvalidPageSizeException(RouteException):
    name = "Invalid Page Size Exception"
    status_code = 422

    def __init__(self, source=None, value=None, **kwargs):
        source = source if source is not None else "page_size"
        if value is None and kwargs.get('queries') is not None:
            value = kwargs.get('queries').get("page_size", None)
        super().__init__(source, value, **kwargs)

    def defaultMessage(self):
        outMessage = "Page Size Error: "
        if self.queries.get("page_size") is not None and self.queries.get("page_size").isdigit():
            if int(self.value) <= 0:
                outMessage += "Invalid page size %s is given. Page size can only be a positive number." % self.value
            elif int(self.value) > MAX_PAGE_SIZE:
                outMessage += "Invalid page size %s is given. Page size cannot be greater than %s." % (self.value, MAX_PAGE_SIZE)
        else:
            outMessage += "Wrong type for page size query given. Value: %s, Type: %s. Should only be given values of type Int." % (self.value, type(self.value))
        return outMessage

    def __str__(self):
        return super().__str__() + "Expected Error Message: '%s'" % self.message


class InvalidPageException(RouteException):
    name = "Invalid Page Exception"
    status_code = 400

    def __init__(self, source=None, value=None, **kwargs):
        source = source if source is not None else "page"
        if value is None and kwargs.get('route_args') is not None:
            value = kwargs.get('route_args').get('page', None)
        super().__init__(source, value, **kwargs)

    def defaultMessage(self):
        return "Invalid Page Error: page %s does not exist. Pages can only be greater than 0." % self.value

    def __str__(self):
        return super().__str__() + "Expected Error Message: '%s'" % self.message
