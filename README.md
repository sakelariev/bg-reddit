<div id="top"></div>

<!-- ABOUT THE PROJECT -->
## About the project

[![Bulgarian Reddit N-gram viewer][assets/screenshot.png]](assets/screenshot.png?raw=true)

I wanted to go through the whole process of building a similar tool to Google Ngram Viewer, so I decided to build this small app, that visualises the trends in uni- and bigrams in the main Bulgarian subreddit - r/bulgaria. I downloaded all the data from 2016 to May 2022 using [subreddit-comments-dl](https://github.com/pistocop/subreddit-comments-dl).


### Built With

This project was built in Python, almost entirely using Pandas and Plotly Dash.

* [Pandas](https://pandas.pydata.org)
* [Plotly Dash](https://plotly.com/dash/)


<!-- GETTING STARTED -->
### Installation
In order to be able to run this app locally you need to install the requirements first.


1. Clone the repo
   ```sh
   git clone https://github.com/sakelariev/bg-reddit.git
   ```
2. Create a new environment (conda or virtualenv)
    ```sh
    conda create -n bg-reddit
    ```
3. Activate new environment
    ```sh
    conda activate bg-reddit
    ```
3. Install all packages from requirements.txt
   ```sh
   pip install -r requirements.txt
   ```
4. Run the app
   ```sh
   python application.py
   ```
5. Access the app
    ```sh
    Open this link in your browser - http://127.0.0.1:8050/
    ```

<!-- USAGE EXAMPLES -->
## Usage
Check the examples for ideas on how to use the tool.


<!-- LICENSE -->
## License
Distributed under the CC BY-SA 4.0 License. You are free to:

Share — copy and redistribute the material in any medium or format

Adapt — remix, transform, and build upon the material
for any purpose, even commercially.

All you need to do is give appropriate credit.

<!-- CONTACT -->
## Contact

Ivaylo Sakelariev - [@sakelariev](https://twitter.com/sakelariev)

Live App Link: [http://reddit.ivaylo.xyz](http://reddit.ivaylo.xyz)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Plotly Dash](https://plotly.com/dash/)
* [Pandas](https://pandas.pydata.org)
* [subreddit-comments-dl](https://github.com/pistocop/subreddit-comments-dl)
* [PRAW](https://praw.readthedocs.io/en/stable/)


<p align="right">(<a href="#top">back to top</a>)</p>
