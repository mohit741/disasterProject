/**
 * Created by mohit on 19-01-2019.
 */
var i = 0;
var images = [];
var time = 3000;

//images list

images[0] = GLOBAL_PATH + "/main1.jpg";
images[1] = GLOBAL_PATH + "/main2.jpg";
images[2] = GLOBAL_PATH + "/main3.jpg";
images[3] = GLOBAL_PATH + "/main10.jpg";
images[4] = GLOBAL_PATH + "/main5.jpg";
images[5] = GLOBAL_PATH + "/main11.jpg";

//change image
function changeImg() {
    document.slide.src = images[i];

    if (i < images.length - 1)
        i++;
    else
        i = 0;
    setTimeout("changeImg()", time);
}
changeImg();