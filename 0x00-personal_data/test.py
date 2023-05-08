import re
message = "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;"
field = 'email'
sep = ';'
re.sub(field + '=.*?' + sep, field + '=' + 'XXX;', message)
print(message.split(';')[:-1])
