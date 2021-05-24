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
    
    
    if (user == 'myProfile')
    {
        document.querySelector('#new-post').style.display = 'block';
        fetch(`/get_currentuser`)
        .then (response => response.json())
        .then(data => {
            console.log(data.userid)
            console.log(data.username)
            header = document.createElement('h2')
            header.textContent = data.username;
            document.querySelector('#username').appendChild(header)
            fetch(`/get_followcount/${data.userid}`)
            .then(response => response.json())
            .then(data => {
                
                console.log(data[0].followers)
                console.log(data[0].following)

                followers = document.createElement('b')
                followers.textContent = data[0].followers

                following = document.createElement('b')
                following.textContent = data[0].following
                
                document.querySelector('#followcount').appendChild(following)
                document.querySelector('#followercount').appendChild(followers)
            })
        })
    }
    else{
        document.querySelector('#new-post').style.display = 'none';
        fetch(`/get_followcount/${user}`)
        .then(response => json(response))
        .then(followers => {
            document.querySelector('followers').appendChild(followers)
        })
        .then(following => {
            document.querySelector('following').appendChild(following)
        })
    }
    
  }

  function load_posts(posts) {
    // Show compose view and hide other views
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#posts-view').style.display = 'block';
    
    if (posts == 'allposts')
    {
        document.querySelector('#new-post').style.display = 'block';
    }
    else{
        document.querySelector('#new-post').style.display = 'none';
    }
  }