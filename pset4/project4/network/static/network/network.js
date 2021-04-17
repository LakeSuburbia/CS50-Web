document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#allposts').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#network').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));
    document.querySelector('#profile').addEventListener('click', () => load_profile('myProfile'));
  
    // By default, load the inbox
    load_posts('allposts');
  });

  function load_profile(user) {
    // Show compose view and hide other views
    document.querySelector('#profile-view').style.display = 'block';
    document.querySelector('#posts-view').style.display = 'block';
    fetch(`/get_followcount/${user.id}`)
        .then(response => json(response))
        .then(followers => {
            document.querySelector('followers').appendChild(followers)
        })
        .then(following => {
            document.querySelector('following').appendChild(following)
        })
    
    if (user == 'myProfile')
    {
        document.querySelector('#new-post').style.display = 'block';
        fetch(`/get_currentuser`)
        .then(response => json(response))
        .then(username => {
            header = document.createElement('h2')
            header.textContent = "test";
            document.querySelector('#username').appendChild(bold)
        })
    }
    else{
        document.querySelector('#new-post').style.display = 'none';
    }
  }

  function load_posts(posts) {
    // Show compose view and hide other views
    if (posts == 'allposts')
    {
        document.querySelector('#new-post').style.display = 'block';
    }
    else{
        document.querySelector('#new-post').style.display = 'none';
    }
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#posts-view').style.display = 'block';
  }