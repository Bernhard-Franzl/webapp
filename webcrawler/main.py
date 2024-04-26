from webcrawler import Snail

snail = Snail()

# Get the course catalog
course_catalog = snail.get_detailed_course_catalogue()
#print(course_catalog)

room_dropdown = snail.search_html(course_catalog, "select", {"id": "room"})
print(room_dropdown)


