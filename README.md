# Automatic Assistant

usage:`main.py [-h] -name PROFILE_NAME -task TASK_DESCRIPTION`

examples of usage are in ```scripts``` directory.
The hardest task i succesfully managed to run through it is:
```
from data/test.csv select the website which was visited the most. Then find out what the website is about. Send what it is about to piotrpiekos@gmail.com
```


## Installation 
```
pip install -r requirements.txt
```

Make sure that environmental variable `OPENAI_API_KEY` the contains key to openai api.

Create a profile by editing the `data/profiles` and adding similar one to `piotr`. In order to use email features it is necessary to put app specific password from gmail (mail assumes its host is gmail)
** (This is of course just a hack for the demo version, no one with the right mind would store passwords like that) **

run scripts from the main project directory for example:
```python main.py -n piotr -t "enter https://aigrant.com and find out who can apply for the grant. Save the result to the file \"result.txt\""```



## Code
Primitives that can be called by the model are in `src/actions/`

Main loop together with Planner, Summarizer and ActionSelector classes are in `src/main_loop.py`

## Assumptions / Limitations


The code is a very basic demonstration version of the assistant and operates on several assumptions and simplifications. For example:
### Scraping
- Web scraping is shallow - it doesn't search through the links inside
- Doesn't handle session and related concepts
- assumes that the text from the website will fit the context length. I even "cheated" and checked how autogpt deals that and from my understanding, they just split it into chunks, so i decided it's not worth implementing in the demo.
### Crashing and other limitations
- there is no validation of the results returned by the language models, so currently the assistant crashes often. Adding verifier and allowing the model to redo the step or refine the task should help a lot there
- No refinement of the plan after some steps, so it's hard to make dynamics plan and handle situations like "visit all website from the file".
- another way to deal with it is to have recursive calls of the main function, that is also not implemented to limit complexity.
### Other important extensions
Of course apart from fixing issues above, extending the list of primitives or llms there are other also important things that would help a lot. The most important are:
- few-shotting some models - adding examples in the prompt in selected models would definitely drastically help with their performance
- interaction with user - as a primitive in `src/actions` one can implement asking user for specification
- verification at the end and at interim steps

