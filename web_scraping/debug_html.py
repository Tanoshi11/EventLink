from bs4 import BeautifulSoup

# Read the saved HTML file
with open("eventbrite_debug.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find event titles
titles = soup.find_all("h3")

# Print found titles
if titles:
    print("\n🎟 EVENTS FOUND IN HTML:")
    for title in titles:
        print("- ", title.text.strip())
else:
    print("⚠️ No events found in the saved HTML.")