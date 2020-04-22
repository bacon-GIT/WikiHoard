import re
import urllib3

a = "\"Hello, world\""
char = "\", "
b = re.sub('[^A-Za-z0-9]+', '', a)
print(b)