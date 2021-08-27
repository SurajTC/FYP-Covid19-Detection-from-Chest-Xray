# <img alingn="left" alt="icon" width="32px" src="https://img.icons8.com/cotton/64/000000/coronavirus--v3.png"/> Covid-19 Detection form Chest X-Ray using Machine Learning

:snowflake: View the static version of the _**app** [here](https://surajtc.github.io/FYP-Covid19-Detection-from-Chest-Xray/)_ :snowflake:

## Description

This is a Computer Aided Detection (CAD) tool for iterative Covid-19 detection,
along with the adequate description of its forming techniques which includes feature selection,
extraction and classification of neuro images to support the clinicians for early and more accurate
diagnosis. This takes a chest X-Ray Image as input and outputs a prediction among two classes:

* Normal/COVID-19 negative and 
* COVID-19 positive 

using the novel Deep Neural Network based model.

## Objectives

* To design and develop a Covid-19 detection system which can help in quick and accurate results.
* To establish an early screening model to distinguish Covid-19 infected and healthy cases.
* To overcome the problem of lack of specialized physicians in remote villages.
* To build a real time application useful for doctors, patients and the rest of the world.

## Using this Project

**1.Cloning the Repository :octocat:**
```
git clone https://github.com/SurajTC/FYP-Covid19-Detection-from-Chest-Xray.git
```
```
cd FYP-Covid19-Detection-from-Chest-Xray
```
**2.Installing Dependencies :wrench:**

Using Anaconda :

```
conda env create --name myenv --file=environment.yml

conda activate myenv
```

Using Pip :
```
python -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt
```
**3.Starting the Flask server :large_blue_circle:**

```
python app.py
```
Then follow the instructions on the console to run the webapp.

## Attribution

Illustrations : <a href="https://storyset.com/people">Storyset</a> - People illustrations by Storyset
Iconset : <a href="https://remixicon.com">Remix Icon</a> - Open source icon library
Live Statistics : <a href="https://www.worldometers.info">Worldometer</a> - Real time world statistics

