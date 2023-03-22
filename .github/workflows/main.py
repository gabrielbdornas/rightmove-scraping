name: scraping_rightmove

# on:
#   schedule:
#     - cron: '0 11 23 * *' # set in UTC timezone - https://crontab.guru - 11 UTC = 8 SP
on: [repository_dispatch]

jobs:
  scraping-rightmove:
    name: Scraping Rightmove
    runs-on: ubuntu-latest    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        # with: # Only if private repos
        #   token: ${{ secrets.GH_TOKEN }}
      - name: Install packages
        run: pip install -r requirements.txt
      - name: Scraping Rightmove
        run: python main.py
      - name: Commit
        uses: stefanzweifel/git-auto-commit-action@v4