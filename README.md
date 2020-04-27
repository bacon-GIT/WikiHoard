# Wikihoard
## Life Manual Generator

![Tutorial](/images/tut.gif)

### Windows Build
Unzip the repository and run the executable in the dist/ folder

### Anyone else
The only external package used is ```wikipediaapi``` so to run this script yourself, all you'll need is to

```sudo apt install wikipediaapi```


Current Features:
- Text Download
- Download all referenced other pages
- Download Disambiguations
- .Zip compression
- Every language available on wikipedia, the list of language codes at the beginning of the program is just a suggestion list

Coming:
- More f strings
- Flask webapp version for server deployments
- Eventually integration with ArgParse, and hopefully apt. I'd like to turn this into a very usable package

### Known Bugs
#### Currently, there is an issue with some of the pages downloading blank. This has something to do with special characters being in filenames, working on that!

#### Some non-UTF-8 or possibly non-Unicode characters cause the program to crash. This is absolutely the case with several ja / Japanese pages. I'm looking into exception handling that will ensure that data is still stored somehow.

