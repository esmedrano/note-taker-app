class Singleton:
    _instance = None
    class_var = 300

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'value'):  # Only initialize once
            self.value = 42

# Usage
singleton1 = Singleton()
singleton2 = Singleton()

singleton1.value = 100
print(singleton2.value)  # Outputs: 100, since both refer to the same instance
