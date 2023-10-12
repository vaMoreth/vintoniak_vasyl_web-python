import cgi

print("Content-type: text/html\n")

form = cgi.FieldStorage()

name = form.getvalue("name")
gender = form.getvalue("gender")
favorite_food = form.getlist("food")
favorite_city = form.getvalue("city")

print("<html>")
print("<head>")
print("<title>Results</title>")
print("</head>")
print("<body>")
print("<h1>Results:</h1>")
print(f"<p>Name: {name}</p>")
print(f"<p>Gender: {gender} </p>")
print("<p>Favorite Ukrainian Food: " + ", ".join(favorite_food) + "</p>")
print(f"<p>Favorite Ukrainian City: {favorite_city} </p>")
print("</body>")
print("</html>")