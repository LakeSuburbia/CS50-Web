document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#allposts').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#network').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));

    document.querySelectorAll('#likebutton').forEach(like => {
        like.onclick = function() {
          like(like.dataset.id);
        }      
      });
    // By default, load the inbox
    load_posts('allposts');
});


function load_posts(postquery) {
    // Show compose view and hide other views
    document.querySelector('#posts-view').style.display = 'block';

    query = ""
    
    if (postquery == 'allposts')
    {
        document.querySelector('#new-post').style.display = 'block';
    }
    else{
        document.querySelector('#new-post').style.display = 'none';
        query+="/"+postquery;
    }


  }

  function like(postid) {
    
    fetch('/like', {
        method: 'POST',
        body: postid
      })
      .then(response => response.json())
      .then(result => {

        //Display the updated total like count
        document.querySelector(`#likes${id}`).innerHTML = result.likes;
        
        //Display updated like without page load, use views after page load
        if (result.is_liked === true) {
          document.querySelector(`#likebutton${id}`).innerHTML = "like"
        } else {
          document.querySelector(`#likebutton${id}`).innerHTML = "unlike"
        }

    });
};