# A sketch for the future QualiPipe monitor.

## Environment Setup

To set up the Conda environment for this project, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Run the following command to create the Conda environment:

    ```bash
    conda env create -f environment.yml
    ```

4. Activate the environment using:

    ```bash
    conda activate flask-ctapipe-env
    ```

Now, the Conda environment is set up with all the required packages, including ctapipe.
## Used technologies:
- html to display the outputs
- javascript in some places, to render some elements dynamically
- python, because it's easy
- flask to connect back and frontends
- yaml for plot specifications
- plotly for plotting,
because its easy to embed in html
(although I didn't try it with matplotlib),
it is interactive and 
it looks cool.

## Already some questions:
- I'm not sure if it will be possible to continue with plotly,
at least the camera view won't be straightforward, I think.
- The user plotting is cool, but it is so limited:
for example, masking is only very trivial.
No possibility to combine variables.
And I don't see how it would be possible to do!