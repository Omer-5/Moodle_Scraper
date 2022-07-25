# Moodle_Scraper
Selenium based scraper that alerts of new content added to a moodle course through a telegram bot  

:exclamation: Intented for private usage- USE AT YOUR OWN RISK

:memo: The telegram bot send a link that requires the user to by logged-in by the instition

## Currently Working
- [x] Configureable course list to scan
- [x] Database to hold old content links
- [x] Telegram message of new content
- [x] Different action based on content type - Assigment, Quiz, URL, Resource

## Planned Features
- [ ] Monitor folder content and alerts on changes inside of it - currently only alerts of new folds
- [ ] Telegram error handling- specificly error 429 (too many requests)
- [ ] Resource type identifier (pdf, doc, ppt)

## Down the line
- [ ] OneNote integration-upload and organize content in OneNote notebooks
