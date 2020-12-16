# leetfind

**Using software engineering to find practice problems I need to practice to land a job as a software engineer.**

I use LeetCode to practice problems. After practicing a bunch of Dijkstra problems, I wanted to move to practicing other types of problems. However, there wasn't an easy way to find the different types of problems. In the discussions tab, people often post methods used to solve a problem. Webscraping + some way to easily interface = problem solved!

Built this in the quickest way so that I can search for these types of things locally. It may not have the best heuristic, but eh it works!

Note: I built this simply for a faster way for me to search for relevant problems rather than googling, etc. Nothing clean about this code!

## Setup:
This was built using `Python 3.9`

#### Virtual Environment:
`python3 -m venv <env_path>`

Enter the virtual environment: `source <env_path>/bin/activate`
Then: `pip install -r requirements.txt`

#### Run Script:
Once the dependencies are installed, run the scraper once:
`python3 run_scraper.py`

This will produce a text file called `leetfind.txt` that the server will use to search against. I didn't build in a way to configure where this file lives, so just place the file in the root (where `requirements.txt` is, if it's not already there).

#### Ripgrep:
This uses [ripgrep](https://github.com/BurntSushi/ripgrep) under the hood, so make sure that is installed. On a Mac: `brew install ripgrep` would get the job done. Installation processes for other OS's are in the link above.

#### React:
```
cd client
yarn install
```

## Running:
This was made to just run locally.
To start the server: `./start_server`
To start the client: `yarn start`
Then go to `localhost:3000` to start searching!
