
//  Product details 
var mainImg = document.getElementById("main_img");
var img1 = document.getElementsByClassName("cimg1")
var img2 = document.getElementsByClassName("cimg2")
var img3 = document.getElementsByClassName("cimg3")
var img4 = document.getElementsByClassName("cimg4")

img1[0].onmouseover = () => {
    mainImg.src = img1[0].src
}
img2[0].onmouseover = () => {
    mainImg.src = img2[0].src
}
img3[0].onmouseover = () => {
    mainImg.src = img3[0].src
}
img4[0].onmouseover = () => {
    mainImg.src = img4[0].src
}
