import singleton_test
from singleton_test import Singleton

single = singleton_test.Singleton()

single.value = 200

Singleton.class_var = 500
