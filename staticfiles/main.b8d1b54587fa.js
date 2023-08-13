function showcomment(){
    var my_disply = document.getElementById('comment').style.display;
        if(my_disply == "block")
              document.getElementById('comment').style.display = "none";
        else
              document.getElementById('comment').style.display = "block";
}

function showReply(id) {
      var replySection = document.getElementById(id);
      if (replySection.style.display === "none") {
          replySection.style.display = "block";
      } else {
          replySection.style.display = "none";
      }
  }


  
function bigImg(x) {
    x.classList.add('edit_forum_girl');
}

function a(x) {
    x.classList.remove('edit_forum_girl');
}
  

  