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
    document.querySelector('#profile-view').style.display = 'none';
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

    fetch(`/posts${query}`)
      .then(response => response.json())
      .then(posts => {
        // Only for debugging purposes 
        console.log(posts);

        for (let post of posts) {
          
            const row = document.createElement('div')
            row.setAttribute("class", "col post");

            // create a div for the mail preview itself
            
            row.innerHTML += "<a href=''> <h3>" + post.poster + "</h3></a> <p>"
            + post.body + "</p> <p class='timestamp'>" 
            + post.timestamp + " | "+post.likes+" LIKES </p> ";

            // Bring the row to the DOM
            document.querySelector('#posts-view').appendChild(row);
        }
      });



  }