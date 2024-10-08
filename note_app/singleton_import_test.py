import singleton_test
from singleton_test import Singleton
import singleton_modify

single = singleton_test.Singleton()

print(single.value)
print(Singleton.class_var)
