# CV Maker

## Description
Custom CV maker that takes in a detailed json file and outputs a pdf file with a formatted CV.

## How to Run

To run this project, you need to execute the `main.py` script. Make sure you have the necessary Python environment set up.

```sh
python main.py
```

You should have a `cv.json` file in the root directory with the structure of the example file. You can modify the file to fit your needs.

It needs to connect to Chromium to generate the pdf file, so make sure you have the necessary drivers installed.

Finally, the resulting pdf file will be in the root directory with the name `cv.pdf`.


## Future Work

- [ ] Refactor the code to make it more modular
- [ ] Implement LLM to be able to modify input json file 
- [ ] Allow LLM to modify styles for a user friendly way to interact with the model
- [ ] Add Visual input to the LLM to get a feedback of the modifications
- [ ] Add Web Interface