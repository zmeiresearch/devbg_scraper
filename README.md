# devbg_scraper
A rudimentary scraper for dev.bg to extract and dump company information in a CSV

# Why?
- Educational purposes
- Dev.bg provides no easy way to see recently-added companies

# Legality
As of time of writing, `robots.txt` contains:
```
User-agent: *
Disallow: /%D0%B8%D1%82-%D1%81%D1%8A%D0%B1%D0%B8%D1%82%D0%B8%D1%8F/action~*
```

meaning all content under `/companies/` should be safe to scrape.
