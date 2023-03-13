<h1 align="center" style="color:black"> Simil Photo <img src="/resources/graphics/logo.png" width="80" align="center"/>  </h1> 

I developed this project because I needed a way to easily detect and erase similar or duplicate images on my PC.\
This is a pure Python 🐍 application and it's ready to run on Windows without any additional software (it doesn't even need Python).

### Languages and tools
<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="PYTHON" alt="Python" width="40" height="40"/>&nbsp;
</div>

## Showcase

**These are the images that I'll be using.**\
<img src="https://user-images.githubusercontent.com/60658991/222874785-cc8fc6f6-a0e0-4a80-a6d4-ce22de80eb3f.png" width="400" align="center"/>
</br>
</br>
**I initialize the program and select the corresponding folder.**\
<img src="https://user-images.githubusercontent.com/60658991/222874879-b8276638-36a9-485a-a59e-e85f21edd21e.png" width="400" align="center"/>
</br>
</br>
**Using VGG16, the program has separated these images into 5 groups as expected.**\
<img src="https://user-images.githubusercontent.com/60658991/222874953-4c93ff46-9a71-4cfb-870a-472c1f8725bc.png" width="400" align="center"/>
<img src="https://user-images.githubusercontent.com/60658991/222874977-8d39f771-4db7-49c1-9432-fe765b5a6fe4.png" width="400" align="center"/>
<img src="https://user-images.githubusercontent.com/60658991/222874982-611bf538-a40b-458e-9ce9-371ea06709d7.png" width="400" align="center"/>
<img src="https://user-images.githubusercontent.com/60658991/222874987-9fe24516-b9da-4ca9-a3ed-c23dcdc10999.png" width="400" align="center"/>
<img src="https://user-images.githubusercontent.com/60658991/222874992-58fc446d-640a-48fa-9156-af31e131d6d3.png" width="400" align="center"/>
</br>
</br>
**Now I can navigate the groups, inspect the images, and detele them individually.**

## What I've learned
- MVP (Model View Presenter) pattern
- Using keras pre-trained models to extract features from images
- Load, resize and use images in Python with the PILLOW library
- Build a UI with Tkinter and style it using Ttk and Ttkthemes

### Some insight into development
- For my first approach to this problem, I tried to use LSH (Locality-sensitive hashing) to generate the buckets or groups of images. But figuring out how many buckets  were needed was not possible. That's when I realized that it would be better to just group the images with a clustering algorithm that didn't need the number of clusters as an input. (In this case, I used Affinity Propagation)
- When it was time to extract the features from the images, I created a "Color histogram" model. This method was very slow, as it iterated every pixel of the image. I didn't know exactly how to optimize it using Numpy, but I was sure it was possible. I ended up optimizing it with the help of AI.
- I was not completely happy with having only one method of extracting features, so I also investigated how to use Keras pre-trained models to have other options. I ended up using VGG16 and MobilenetV2 to give the user the option to choose between speed and precision.
- I investigated how to make a UI for my program and ended up using Tkinter, as the UI I needed was very simple, and other options like PyQT had a lot more unnecesary complexity for this particular case.
- The program has to do some intensive work when extracting features and clustering the images, so the UI was freezing for seconds or even minutes. I ended up using a thread for the heavy calculations to free the UI main thread. I also implemented a queue to send messages from the worker thread to the UI thread to give the user visual updates on how the process is going.

## How to use it
1) Unzip the files to a folder
2) Execute SimilPhoto.exe inside the folder
3) Use the configuration menu to set up the settings as you need

  #### The configuration menu
  - On **File Search** submenu, choose the destination folder and if you also want the subfolders to be searched. 
  You can also choose which types of files get detected with the checkboxes.
  - On **Feature Extraction** submenu, choose the feature extraction method to be used. Each one is briefly explained in the side textbox.
  Basically: 
    - vgg16 -> slow, reliable. 
    - mobilenet -> faster, less reliable. 
    - color histogram -> MUCH faster, different approach to detection, often less precise.

    Here you can also choose if your images features will be cached. This will create a file that stores the features which the program will use when available to make the calculations much faster.\
    If you don't want the program to use the cached features, you can select the *Force recalculate features* checkbox.
    
  - On "Clustering" submenu, change the damping and max iterations sliders if the clustering algorithm doesn't converge.

  - On the bottom part of the configuration menu, you'll find the run/cancel button, alongside two progress bars and a text that gives you information about the status of the run

4) Click the run button and wait a bit... ⏳
5) Navigate the groups tabs to inspect the details of each image and delete the one you want! Be careful, deletion is **forever**

### IMPORTANT TIPS (Read before using)

- If Windows tries to "protect" you from executing the program, this is probably because the executable is not signed. I'll look into this, but you can be sure that there is nothing fishy about it. Check the code!

- If you notice that the groups of images suddenly don't make much sense (especially when using vgg16), that could be because of an error in the cached features files. This does not occur under normal circumstances, but if you find yourself constantly deleting and adding files to the folder while the program caches features this might happen. ***To get rid of this simply check the 'Force recalculate features' checkbox, or even delete the cache file which is in the same directory (cached_features.csv)***

- If you find that you cannot open or delete images, this might be because the program does not have permissions to do so. ***Try to run the executable in administrator mode and give it another try***

- If you are planning to run the program in a folder with lots of images (+2000) you should keep an eye on RAM usage 👀. Especially if your PC doesn't have much RAM capacity. (Turns out that loading +2000 images, extracting their features, and clustering them uses a lot of memory, who could have thought)

- On the same note, if you're using the program in folders with large amounts of images, the clustering algorithm may not converge. You can change the parameters on the "Clustering" submenu to try to fix that. If the algorithm still doesn't converge try selecting a subfolder with less images.

- Be VERY careful when using Ctrl + Z on the folder after using the program to delete a file. I'm not sure if this is a Windows bug, but doing Ctrl + Z could end up with you **LOSING ALL THE FILES ON THE FODLER**. You could maybe try to restore them by doing Ctrl + Y but success is not assured.

## Upgrade ideas
- Show all error messages to the user in a popup so they can know when something goes wrong (And what went wrong)
- Make the tkinter implementation more scalable to other screen resolutions (It is currently optimized for 1920x1080)
- Have the possibility of changing the parameters of the Feature Extracting methods
- Give the option to search in a group of folders
- Give the option to select and delete groups of images instead of doing it individually

## Disclaimer
I advise you to be careful when using the program. After all, it can delete files from your PC that may not be recoverable.\
You should always have backups of your photos.
