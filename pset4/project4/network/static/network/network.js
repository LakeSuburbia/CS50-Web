document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#allposts').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#network').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));



    const likeLinks = document.querySelectorAll('.like-link');

    likeLinks.forEach(link => {
        link.onclick = (event) => {
            const post = event.target.parentElement;
            try {
                var like_author = document.querySelector('#username').innerHTML;
            } catch (TypeError) {
                alert("Please log in.");
                return false;
            }

            const data = {
                liker: like_author,
                liked: post.dataset.id,
            };

            fetch('/like', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
                .then(response => response.json())
                .then(data => {
                    event.target.innerHTML = data.likes;
                })
                .catch(error => console.error(error));
        };
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