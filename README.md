### Pathfinder RPG Reference Document Scraper
This is a collection of python scripts that convert the content found on the Pathfinder RPG Reference Document to JSON for ease of parsing. Currently, the scripts are capable of creating JSON for the entirety of the Pathfinder RPG bestiaries, monster codex and NPC codex. Future support will include spell and feat descriptions, detailed class descriptions, items and more. 

Requires Python 3 and BeautifulSoup4. 

To run:

```
python scrape-monsters.py -b -m -n
```
