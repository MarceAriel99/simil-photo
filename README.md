<h1 align="center" style="color:black"> Simil Photo <img src="/resources/graphics/logo.png" width="80" align="center"/>  </h1> 



I developed this project because I needed a way to easily detect and erase similar images or duplicates I have in my PC.
This is a pure Python application and it's ready to run on Windows.

### Languages and tools
<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="PYTHON" alt="Python" width="40" height="40"/>&nbsp;
</div>

## What I've learned
- Implemented MVP (Model View Presenter) pattern
- How to use keras pre-trained models to extract features from images
...

### Some insight into development
- First approach (LSH)
- Keras pre-trained models
- Color histogram model
- Tkinter
- Threads
...

## How to use it
1) Unzip the files to a folder
2) Execute SimilPhoto.exe inside the folder

#### The configuration menu
- On **File Search** submenu choose the destination folder and if you also want the subfolders to be searched. 
You can also choose which types of files get detected with the checkboxes.
- On **Feature Extraction** submenu, choose the feature extraction method to be used. Each one is breafly explained in the side textbox.
Basically: 
  - vgg16 -> slow, reliable. 
  - mobilenet -> faster, less reliable. 
  - color histogram -> MUCH faster, different approach to detection, often less precise.

  Here you can also choose if your images features will be cached. This will create a file that stores the images features which the program will use when available to make the calculations much faster.\
  If you don't want the program to use the cached features you can select the *Force recalculate features* checkbox.
  
  
...

### IMPORTANT TIPS

- If Windows tries to "protect" you from executing the program, this is probably because the executable is not signed. I'll look into this, but you can be sure that there is nothing fishy about it. Check the code!

- If you notice the groups of images suddenly don't make much sense (especially when using vgg16) that could be because of an error in the cached features files. This does not occur under normal circumstances, but if you find yourself deleting and adding files constantly to the folder while the program caches features this might happen. ***To get rid of this simply check the 'Force recalculate features' checkbox, or even delete the cache file which is in the same directory (cached_features.csv)***

- If you find that you cannot open or delete images, this might be because the program does not have permissions to do so. ***Try to run the executable in administrator mode and give it another try***

## Upgrade ideas
...
