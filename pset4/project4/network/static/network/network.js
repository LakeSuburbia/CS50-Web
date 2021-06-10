document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#allposts').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#network').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));
    
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

  