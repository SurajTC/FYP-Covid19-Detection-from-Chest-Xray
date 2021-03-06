<h1 align="center">
  <img alingn="left" alt="icon" width="32px" src="https://img.icons8.com/cotton/64/000000/coronavirus--v3.png"/>
  Covid-19 Detection form Chest X-Ray using Machine Learning
</h1>

:snowflake: View the static version of the _**app** [here](https://surajtc.github.io/FYP-Covid19-Detection-from-Chest-Xray/)_ :snowflake:

## Index

* [Description](#Description)
* [Objectives](#Objectives)
* [Usage](#Usage)

---

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

## Usage

**1.Clone this Repository**
```shell
git clone https://github.com/SurajTC/FYP-Covid19-Detection-from-Chest-Xray.git;
cd FYP-Covid19-Detection-from-Chest-Xray
```
**2.Satisfy Dependencies**

Using Anaconda :

```shell
conda env create --name myenv --file=environment.yml

conda activate myenv
```

Using Pip :
```shell
python -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt
```
**3.Start the Flask server**

```shell
python app.py
```
Further follow the instructions on the console to use the webapp.

## Attribution

Illustrations   : <a href="https://storyset.com/people">Storyset</a> - People illustrations by Storyset
<br/>
Iconset         : <a href="https://remixicon.com">Remix Icon</a> - Open source icon library
<br/>
Live Statistics : <a href="https://www.worldometers.info">Worldometer</a> - Real time world statistics

