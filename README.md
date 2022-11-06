# Treeleaf Computer Vision Internship Task

## Task Description:

● From the given image below complete the following given task:

- Task 1: Assign the number (1 to 4) below the image of the rectangle with respect to its
  length inside the rectangle. The shorter the line lower the number (No need to reorder the
  image of the rectangle, only give numbering)

- Task 2: Align(make the rectangle image straight) all the given images of the rectangle.

> Both of the tasks are different, please do them separately.

Make 2 python files with the names rectangle_numbering.py and rectangle_alignment.py. Place your Task
1 and Task 2 code there.

**Note**: Push your task code to GitHub(public) and share the link in the mail.

<img src="https://user-images.githubusercontent.com/46085301/200157696-936a24d0-92cc-4ac8-a403-759be1da612c.png" height="300" alt="image"/>

## Setup

```shell
  # install required packages
  $ pip install -r requirements.txt

  # generate numbered image
  $ python rectangle_numbering.py

  # generate aligned image
  $ python rectangle_alignment.py

```

## My approach for the task:

### 1. For assigning the number.

l needed to find the coordinates of the rectangles & lines so as to find the line length and number them accordingly.
So for that, I went through the following steps:

- I cropped and resized the image.
  > ![image](https://user-images.githubusercontent.com/46085301/200164065-e3dd97a3-1ba8-49bf-a0f6-9ae31880dc1b.png)
- Then found out the bounding boxes around all the rectangles using OpenCV findContours and boundingRect method.
  > ![image](https://user-images.githubusercontent.com/46085301/200164105-c3b66f2e-caa0-4bc6-9019-9211dcd42883.png)
- And also calculated all the corners of the rectangles and lines from the image using OpenCV goodFeaturesToTrack method.
  > ![image](https://user-images.githubusercontent.com/46085301/200164077-902746fd-e7c0-4bcd-bea2-3158157de503.png)
- Then, I looped over the rectangles (from the 2nd point) and for each rectangle calculated its centre and filtered the two closest points from centres from the coordinates of all the corners(from the 3rd point)
  > ![image](https://user-images.githubusercontent.com/46085301/200164135-873d585b-8b5e-4531-94f9-f91fccd2b703.png)
- Because the two closest points are the points of the lines.
  > ![image](https://user-images.githubusercontent.com/46085301/200164309-0bf8611c-04fd-4db1-8463-766caf872058.png)
- Finally, compared all the line lengths and numbered on the image using OpenCV accordingly and saved the image.
  > ![image](https://user-images.githubusercontent.com/46085301/200164175-7b591769-f562-441e-bef1-d01bd36d3b9f.png)

### 2. For aligning all the rectangles.

l needed to find the coordinates of the rectangles & angles of alignment so as to rotate and align them accordingly.
So for that, I went through the following steps:

- I cropped and resized the image.
  > ![image](https://user-images.githubusercontent.com/46085301/200164065-e3dd97a3-1ba8-49bf-a0f6-9ae31880dc1b.png)
- Then found out the contours for rectangles using OpenCV findContours method.
- Looped over each contour of the rectangle and calculated the angle of alignment using the OpenCV minAreaRect method
  > ![image](https://user-images.githubusercontent.com/46085301/200164514-73e33654-1b22-45f6-9ce5-82089c1eb358.png)
- Then rotated the image using OpenCV warpAffine method
- But the whole image was rotated so, for that I created a copy of the original image and also calculated the bounding box for each rectangle
  > ![image](https://user-images.githubusercontent.com/46085301/200164569-27387b57-901f-4275-a94a-d98798d8bd22.png)
- Then replaced only the bounding box part from the rotated image on to the copied image for each contour
- And then finally the image was ready and saved using OpenCV
  > ![image](https://user-images.githubusercontent.com/46085301/200164631-fc0e8a7b-f59a-4bda-ae99-6634b4bf3c80.png)
