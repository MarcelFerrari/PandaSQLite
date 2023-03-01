# --- Useful decorators --- #
def log_query(func):
    def wrapper(self, *args, **kwargs):
        if self.verbose:
            print(f"Executed: {args[0]}") 
        return func(self, *args, **kwargs)
    return wrapper

def commit_on_complete(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        # Auto-commit changes
        if self.auto_commit:
            self.commit()
        return result
    return wrapper

def check_exists_condition(func):
    def wrapper(self, *args, **kwargs):
        if kwargs["if_exists"] not in ['fail', 'replace', 'append']:
            print(f"Executed: {args[0]}") 
        return func(self, *args, **kwargs)
    return wrapper