import cgi

while(1):
  id = cgi.FieldStorage()
  if id.value != []:
   print id.value
   break 
